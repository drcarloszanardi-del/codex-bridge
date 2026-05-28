---
job_id: 20260528T060305-telegram-direct-local-guards-followup-review-v1
worker: personal-xh
status: completed
completed_at: 2026-05-28T06:09:01-03:00
front: TELEGRAM
no_external_actions: true
no_secrets: true
---

# Resultado - Telegram Direct local guards followup review v1

## summary

Revision declarativa de cierre sobre los guards locales agregados despues de
`20260528T054245-telegram-direct-context-isolation-parity-audit-v1`.

Con la evidencia declarada, los dos guards nuevos cubren los P0 inmediatos del
frente Telegram Directo:

- **Paridad Directo/Desktop:** cubierto en contrato si el test nuevo exige el
  mismo `quality_contract_id` o checks equivalentes para evidencia, buffer,
  no-secrets, no raw diff y result trace.
- **No mezcla REELS/CLINICA por `active_route`:** cubierto para el caso critico
  declarado: pedido directo explicito REELS con `active_route=CLINICA` previo
  debe terminar en `route=REELS`, no `CLINICA`.

Lo que aun no queda cerrado por esos dos guards es el P0 clinico: una correccion
simple desde Directo no debe modificar un protocolo equivocado si falta
`target_document_id` o identidad de seccion. Recomiendo una unica proxima accion:
**agregar solo el fixture clinico `clinical_edit_requires_target_document_identity`**.

## coverage_table

| Fuente | Estado | Uso |
| --- | --- | --- |
| `jobs/20260528T060305-telegram-direct-local-guards-followup-review-v1.md` | Revisada | Workorder y evidencia declarada del orquestador. |
| `results/20260528T054245-telegram-direct-context-isolation-parity-audit-v1.result.md` | Revisada | Riesgos P0/P1 y fixtures pendientes. |
| `/Users/jarvis/.openclaw/workspace/tests/telegram/test_desktop_handoff_guardrail.py` | Ausente en esta Mac | No se ejecuto test real; se toma evidencia declarada. |
| `/Users/jarvis/.openclaw/workspace/tests/telegram/test_media_buffer_policy.py` | Ausente en esta Mac | No se ejecuto test real; se toma evidencia declarada. |
| `/Users/jarvis/.openclaw/workspace/scripts/codex_telegram_direct.py` | Ausente en esta Mac | No se inspecciono codigo operativo. |
| `/Users/jarvis/.openclaw/workspace/scripts/codex_desktop_telegram_handoff.py` | Ausente en esta Mac | No se inspecciono consumer Desktop real. |

## evidencia_verificada

- El job nuevo existe en el bridge y pide una revision declarativa.
- En esta Mac no existen las rutas `/Users/jarvis/.openclaw/workspace/...`, por
  lo que no se pudo verificar el diff, ejecutar tests reales ni leer snapshots.
- El resultado previo `20260528T054245` dejo tres P0 principales pendientes de
  aislamiento: material/reel, claim visual con evidencia y target clinico.

## inferencias

- Infiero que el guard de paridad baja el riesgo de calidad distinta entre
  Directo y Desktop, siempre que no sea un test superficial de campos y realmente
  compruebe gates operativos.
- Infiero que el nuevo caso REELS vs `active_route=CLINICA` cubre el P0 mas
  probable de contaminacion entre frentes para material de reel.
- Infiero que el P0 clinico queda fuera: no es una colision de route por REELS,
  sino una identidad de documento/seccion antes de editar.

## risks_p0_p1_p2

| Pri | Riesgo residual | Estado tras guards | Proxima accion |
| --- | --- | --- | --- |
| P0 | Directo tiene contrato menor que Desktop. | Cubierto por guard declarado si verifica gates reales, no solo flags. | Mantener en observacion. |
| P0 | REELS hereda `active_route=CLINICA`. | Cubierto por `test_media_buffer_policy.py` declarado. | Mantener test como bloqueo de release. |
| P0 | Correccion clinica toca documento equivocado. | No cubierto por los dos guards declarados. | Agregar fixture clinico con `target_document_id`. |
| P1 | Claim visual sin evidencia declarada. | Parcialmente cubierto si paridad incluye evidence-first; no confirmado. | Dejar como siguiente hardening si aparece incidente visual. |
| P1 | Consumer legacy usa `latest_turn` para pending/seen. | Cubierto por auditorias previas y guardrail test si sigue activo. | Mantener guard estatico. |
| P2 | Latencia o falsos positivos por buffer conservador. | No es bloqueo de cierre. | Observar con contralor local. |

## decision

```yaml
decision: add_only_clinical_target_document_fixture
close_observation_now: false
human_intervention_required: false
guards_accepted:
  direct_desktop_parity_contract: true
  direct_reels_does_not_inherit_clinica_active_route: true
remaining_p0:
  clinical_edit_requires_target_document_identity: true
visual_evidence_fixture_required_now: false
```

## fixture_minimo_recomendado

`clinical_edit_requires_target_document_identity`

```text
Entrada:
  - history/scope reciente con dos documentos clinicos distintos
  - mensaje Directo: "cambia esa parte de hemostasia" o "corregi la frase"
  - sin target_document_id explicito

Esperado:
  - no se modifica ningun documento
  - route = CLINICA o UNKNOWN_REVIEW segun contrato local
  - action = needs_target_document_identity
  - result/health explica que falta target_document_id/seccion
  - no se toma el ultimo protocolo por memoria global ni active_route
```

Este fixture debe fallar si cualquier consumer aplica una correccion clinica
contra el documento "mas reciente" sin identidad explicita.

## recommendation

Agregar solo el fixture clinico de `target_document_id` antes de cerrar la
observacion. No pediria intervencion humana ahora. El fixture visual de evidence
es importante, pero puede quedar como P1/hardening inmediato posterior si el
guard de paridad ya valida evidence-first y no-invencion.

## confidence

Media-alta para aceptar los dos guards declarados como cierre de los P0
inmediatos de paridad y mezcla REELS/CLINICA. Media para certificar el estado
real porque los tests y scripts viven en `/Users/jarvis/.openclaw/workspace`,
que no existe en esta Mac.

## attempted_routes

- Se hizo `git pull --rebase origin main`.
- Se ejecuto `./scripts/personal_xh_check.sh` y se detecto el job asignado.
- Se reviso el workorder actual.
- Se reviso `results/20260528T054245-telegram-direct-context-isolation-parity-audit-v1.result.md`.
- Se intento listar `test_desktop_handoff_guardrail.py` y
  `test_media_buffer_policy.py` bajo `/Users/jarvis/.openclaw/workspace`, pero
  no existen en esta Mac.
- No se uso Telegram real, Gmail, Drive, Calendar, iCloud, Photos, adjuntos
  reales ni servicios externos.

## risks_limits

- Resultado declarativo; no certifica codigo real ni salida de tests reales.
- No se leyeron snapshots, adjuntos ni datos clinicos reales.
- La decision final queda en Codex orquestador.

## evidence_paths

- `jobs/20260528T060305-telegram-direct-local-guards-followup-review-v1.md`
- `results/20260528T060305-telegram-direct-local-guards-followup-review-v1.result.md`
- `results/20260528T054245-telegram-direct-context-isolation-parity-audit-v1.result.md`
- `/Users/jarvis/.openclaw/workspace/tests/telegram/test_desktop_handoff_guardrail.py`
- `/Users/jarvis/.openclaw/workspace/tests/telegram/test_media_buffer_policy.py`
- `/Users/jarvis/.openclaw/workspace/scripts/codex_telegram_direct.py`
- `/Users/jarvis/.openclaw/workspace/scripts/codex_desktop_telegram_handoff.py`
