---
job_id: 20260525T111227-telegram-contralor-action-event-handle-error
worker: personal-xh
status: completed
completed_at: 2026-05-25T11:20:19-03:00
front: CODEX-OPS
---

# Result

## summary

Diagnostico P1: `codex_guard_channel_gate.js` timeout al evaluar un texto largo/multilinea de Telegram que incluia un mensaje tecnico y un diff. Causa probable: el gate recibe payload grande por argumento `--text`, con saltos, comillas y diff; tarda mas de 30s o queda en parsing/ruteo costoso.

## findings con evidencia

- Finding: `event_handle_error`.
- Error: comando Node `codex_guard_channel_gate.js --channel telegram_message --text ...` excedio 30 segundos.
- El texto contenia un mensaje tecnico de falla y un diff multilinea.
- El evento no trae `message_id`, `chat_id` ni `route`, lo que dificulta idempotencia y reproduccion.

## diagnostico

El gate de canal esta siendo usado sobre un payload que no parece un mensaje normal del Doctor, sino una salida tecnica/diff destinada a Telegram. Hay dos fallos acoplados:

1. Transporte: pasar texto largo por argv (`--text`) es fragil para multilinea, comillas y diffs.
2. Politica: un mensaje de error tecnico con diff no deberia llegar crudo a canal Telegram; debe resumirse antes del gate.

## archivos/rutas probables en work-mac

```text
/Users/jarvis/.openclaw/workspace/scripts/codex_guard_channel_gate.js
scripts/codex_guard_channel_gate.js
scripts/codex_telegram_direct*
telegram_bridge/ack_policy.py
telegram_bridge/errors.py
telegram_bridge/observability.py
```

Paquete minimo:

```text
codex_guard_channel_gate.js
caller que invoca el gate para Telegram
log completo del evento 2026-05-23T23:00:52-0300
config de timeout
fixture del texto que produjo timeout, redacted si hace falta
```

## parche propuesto

### 1. Cambiar transporte de `--text` a stdin o archivo temporal

```bash
node codex_guard_channel_gate.js --channel telegram_message --text-file "$TMP_PAYLOAD"
```

o:

```bash
printf '%s' "$payload" | node codex_guard_channel_gate.js --channel telegram_message --stdin
```

### 2. Agregar limite y preclasificacion

```javascript
const MAX_TELEGRAM_GATE_CHARS = 6000;
if (text.length > MAX_TELEGRAM_GATE_CHARS) {
  return {
    ok: false,
    action: "summarize_before_send",
    reason: "payload_too_long_for_channel_gate"
  };
}
```

### 3. Resumir errores tecnicos antes de Telegram

No enviar diffs crudos. Convertir a:

```text
No pude completar desde Telegram.
Causa tecnica: fallo al aplicar/validar cambio.
Job/log: <local_ref>
```

El diff queda en archivo/log local, no en mensaje Telegram.

### 4. Timeout con fallback seguro

Si el gate excede 5-10s:

```text
do_not_send
create action item
store payload path
```

No reintentar indefinidamente ni mandar el texto sin gate.

## prueba sintetica

```javascript
it("does not timeout on multiline diff payload", async () => {
  const payload = makeLongTechnicalDiffPayload();
  const result = await runGate({ channel: "telegram_message", stdin: payload, timeoutMs: 5000 });
  expect(result.ok).toBe(false);
  expect(result.action).toBe("summarize_before_send");
  expect(result.reason).toBe("payload_too_long_for_channel_gate");
});

it("does not pass raw technical diff to telegram", async () => {
  const event = technicalFailureWithDiff();
  const outgoing = buildTelegramErrorMessage(event);
  expect(outgoing.text).not.toContain("@@ -");
  expect(outgoing.text).not.toContain("AUDIO = ROOT");
  expect(outgoing.local_ref).toBeTruthy();
});
```

## riesgo

- Si el gate se saltea por timeout, se puede filtrar texto tecnico o datos no destinados a Telegram.
- Si se bloquea todo error largo, el Doctor no recibe estado.
- Si se guarda payload sin redaccion, puede quedar material sensible en logs.

Mitigacion: `summarize_before_send`, local ref, secret scan sobre payload, y retencion corta para logs.

## recommendation

Prioridad de integracion:

1. Cambiar gate a stdin/text-file.
2. Agregar limite de longitud y deteccion de diff.
3. Resumir errores tecnicos antes del canal.
4. Registrar `message_id/chat_id/route` aun cuando falle el handler.

## confidence

High. El error contiene suficiente evidencia: timeout del gate con payload largo/multilinea pasado por `--text`.

## evidence_paths

- `jobs/20260525T111227-telegram-contralor-action-event-handle-error.md`
- `results/20260525T084316-telegram-codex-direct-router-observability-mvp-v2.result.md`
