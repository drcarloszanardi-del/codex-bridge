## Summary

Verdict: **nuevo patch minimo de tests, despues cerrar en observacion**. Con el contexto reportado por el orquestador, el guard final y la matriz tecnica ya cubren el bug principal. Lo que falta no es sumar heuristicas de radar sino probar que no existe una ruta lateral de entrega: wrapper/cron, replay de artifact viejo, `force`, o publicador directo.

Desde este bridge no estan presentes los archivos reales `scripts/radares/radar_delivery_guard.js`, `scripts/inmobiliaria/send_inm_radar_report.js`, `scripts/inversiones/send_inv_neuro_instrument_report.js` ni `scripts/qa/run_radar_regression_gates.sh`; por eso no certifico codigo linea a linea. La segunda mirada util es convertir los riesgos residuales en 4 tests chicos, deterministas y fail-closed.

## Findings

1. **P1: publicador directo residual.** Aunque los senders llamen `guardDelivery`, puede quedar algun helper que llame al cliente Telegram/topic directamente. Test bajo riesgo: escanear los scripts RADARES/INM/INV permitiendo envio externo solo desde un wrapper allowlisted. Criterio: si un archivo fuera del allowlist contiene `sendMessage`, `telegram`, `topic_id`, `chat_id`, `bot.send`, `postTopic` o equivalente, el test falla.

2. **P1: wrapper/cron formatea un `sent:false` como informe.** La raiz anterior era post-reporter: estado bloqueado convertido en texto para el Doctor. Test bajo riesgo: monkeypatch del sender/reporter para devolver `{sent:false, can_publish:false, reason:"blocked_empty_technical_failure_report"}` y assertion de wrapper: no llama a publisher, genera artifact local y devuelve `blocked_operational` o `fallback_pending`.

3. **P1: replay de artifact viejo sin guard vigente.** Si existe `report.md` heredado sin `delivery_guard.json`, el sistema debe bloquear o revalidar. Test bajo riesgo: fixture con artifact legacy que contiene "pagina no hallada"/"ENOTFOUND"; replay debe retornar `can_publish:false`, `sent:false`, `reason:"missing_or_failed_delivery_guard"` y escribir nuevo `delivery_guard.json`.

4. **P1: `force=true` conserva payload publicable.** Force puede ser local-only pero igual dejar armado `topic_id` o `telegram_payload`. Test bajo riesgo: con `force=true`, assert `sent:false`, `destination:"local_artifact_only"`, `can_publish:false`, y ausencia total de `topic_id`, `chat_id`, `telegram_payload`, `message_id`.

5. **P2: suite OK sin evidencia versionada.** El job reporta `bash scripts/qa/run_radar_regression_gates.sh` OK. Conviene guardar en artifact local el log o al menos el hash/summary de la suite para cerrar observacion sin depender de memoria operacional.

## Recommendation

Aplicar un **patch minimo de regresion**, no mas logica de negocio:

- Agregar 4 tests: `R_DIRECT_PUBLISHER_ALLOWLIST`, `R_CRON_SENT_FALSE_NOT_FORMATTED`, `R_LEGACY_ARTIFACT_REPLAY_REQUIRES_GUARD`, `R_FORCE_LOCAL_ONLY_STRIPS_TOPIC_PAYLOAD`.
- Conectar esos tests a `scripts/qa/run_radar_regression_gates.sh`.
- Si pasan junto con la matriz tecnica WAF/captcha/HTTP 403/ENOTFOUND/ECONNRESET/no encontre/sin resultados por error, cerrar en observacion.
- Si cualquiera falla, no publicar radares finales; guardar artifact local y crear job de patch especifico.

## Confidence

Media-alta para la recomendacion de tests. Media para el estado concreto del parche porque los archivos fuente reales no estan versionados en este checkout del bridge.

## Evidence_Paths

- `jobs/20260526T174756-radar-delivery-guard-residual-bypass-audit-v2.md`
- `claims/20260526T174756-radar-delivery-guard-residual-bypass-audit-v2.json`
- `results/20260526T164745-radares-delivery-guard-post-integration-review-v1.result.md`
- `results/20260526T155816-radares-root-cause-no-error-report-v1.result.md`
- `results/20260525T211520-postpatch-telegram-radar-gate-audit-v1.result.md`
- `results/20260525T214513-telegram-radar-regression-fixtures-v1.result.md`
- `scripts/`

## Coverage_Table

| Area | Evidencia | Resultado |
| --- | --- | --- |
| Guard final | Job v2 y resultado post-integracion previo | Direccion correcta; riesgo residual esta en rutas laterales. |
| Publicador directo | `results/20260526T164745-radares-delivery-guard-post-integration-review-v1.result.md` | Sigue siendo el test mas importante antes de cerrar. |
| Cron/wrapper | `results/20260526T155816-radares-root-cause-no-error-report-v1.result.md` | Debe probarse con reporter `sent:false`. |
| Replay artifact viejo | Plan previo exige `delivery_guard.json` por corrida | Falta test de legacy artifact si no fue agregado. |
| Force local-only | Job reporta bloqueo, pero no payload stripping | Requiere fixture dedicado. |
| Codigo real | `scripts/` del bridge no contiene subdirs de radares/qa | No hay revision linea-a-linea desde este checkout. |

## Riesgos

- Cerrar en "resuelto" con suite verde pero sin probar publicador directo.
- Mantener un cron que recibe `sent:false` y construye texto humano igual.
- Reutilizar artifacts viejos sin `delivery_guard.json` vigente.
- Permitir `force` como local-only pero dejando payload publicable en memoria/log/artifact.
- Seguir agregando patrones tecnicos y olvidar el choke point de entrega.

## Fixtures_Concretos

### R_DIRECT_PUBLISHER_ALLOWLIST

Entrada: scan de archivos `scripts/**/*radar*`, `scripts/**/*inm*`, `scripts/**/*inv*`.

Esperado: solo archivos allowlisted pueden importar o llamar publishers externos. Cualquier referencia directa a `telegram`, `topic_id`, `chat_id`, `sendMessage`, `postTopic`, `bot.send` fuera del wrapper aprobado falla.

### R_CRON_SENT_FALSE_NOT_FORMATTED

Entrada: mock de reporter con:

```json
{"sent": false, "can_publish": false, "reason": "blocked_empty_technical_failure_report", "report_text": "pagina no hallada"}
```

Esperado: wrapper no llama publisher, retorna `sent:false`, crea artifact local y conserva `audience:"orchestrator_only"`.

### R_LEGACY_ARTIFACT_REPLAY_REQUIRES_GUARD

Entrada: artifact viejo con `report.md` pero sin `delivery_guard.json`, texto con `ENOTFOUND`.

Esperado: replay bloqueado o revalidado; nunca `sent:true`; se escribe `delivery_guard.json` con `can_publish:false`.

### R_FORCE_LOCAL_ONLY_STRIPS_TOPIC_PAYLOAD

Entrada: `force=true` y reporte bloqueado por patron tecnico.

Esperado: `sent:false`, `can_publish:false`, `destination:"local_artifact_only"` y ausencia de `topic_id`, `chat_id`, `telegram_payload`, `message_id`.

## Attempted_Routes

- Sincronice el bridge con `git pull --rebase`.
- Verifique job pendiente con `./scripts/personal_xh_check.sh`.
- Reclame el job con `scripts/bridgectl.py`.
- Revise el job v2, el resultado post-integracion previo y la causa raiz previa.
- Busque referencias a guard, wrappers, artifacts y publishers dentro de `jobs/`, `results/`, `scripts/`, `context/`, `docs/` y `protocol.md`.
- No use Telegram, Gmail, Drive, Calendar ni acciones externas.

