---
job_id: 20260528T062330-telegram-direct-visual-evidence-guard-review-v1
worker: personal-xh
status: completed
completed_at: 2026-05-28T06:28:39-03:00
front: TELEGRAM
no_external_actions: true
no_secrets: true
---

# Resultado - Telegram Direct visual evidence guard review v1

## summary

Revision declarativa del guard visual agregado para el ultimo riesgo residual
marcado: claims visuales en REELS desde Telegram Directo sin evidencia declarada.

Con la evidencia declarada, el guard **cierra el riesgo visual residual
inmediato**: `direct_visual_claim_requires_declared_media_evidence(...)` y la
linea `Guard visual P0` en `build_telegram_task_brief(...)` obligan a no afirmar
elementos visuales del montaje si no estan respaldados por adjuntos, `media_id`,
frame, OCR o transcripcion. La suite declarada sube a 12 tests OK en
`test_desktop_handoff_guardrail.py`, con media buffer y postfix regression aun
verdes.

Recomendacion unica: **cerrar Telegram Directo -> Desktop en observacion**. No
pediria otro fixture concreto ahora ni intervencion humana.

## coverage_table

| Fuente | Estado | Uso |
| --- | --- | --- |
| `jobs/20260528T062330-telegram-direct-visual-evidence-guard-review-v1.md` | Revisada | Workorder y evidencia declarada del orquestador. |
| `results/20260528T061305-telegram-direct-clinical-target-identity-guard-review-v1.result.md` | Revisada | Cierre del P0 clinico y recomendacion de fixture visual. |
| `results/20260528T060305-telegram-direct-local-guards-followup-review-v1.result.md` | Revisada | Estado de guards de paridad y no mezcla REELS/CLINICA. |
| `results/20260528T054245-telegram-direct-context-isolation-parity-audit-v1.result.md` | Revisada | Riesgos originales de paridad, contexto, clinico y evidencia visual. |
| `/Users/jarvis/.openclaw/workspace/scripts/codex_telegram_direct.py` | Ausente en esta Mac | No se inspecciono codigo real; se usa evidencia declarada. |
| `/Users/jarvis/.openclaw/workspace/tests/telegram/test_desktop_handoff_guardrail.py` | Ausente en esta Mac | No se ejecuto test real; se usa evidencia declarada. |
| `/Users/jarvis/.openclaw/workspace/tests/telegram/test_media_buffer_policy.py` | Ausente en esta Mac | No se ejecuto test real; se usa evidencia declarada. |
| `/Users/jarvis/.openclaw/workspace/tests/telegram/test_postfix_regression_fixtures.py` | Ausente en esta Mac | No se ejecuto test real; se usa evidencia declarada. |

## evidencia_verificada

- El job nuevo existe en el bridge y declara el guard visual, el test sintetico
  y los checks locales del orquestador.
- En esta Mac no existen las rutas `/Users/jarvis/.openclaw/workspace/...`, por
  lo que no pude validar el diff ni ejecutar las suites reales.
- En el bridge consta que los P0 previos de paridad, REELS/CLINICA y target
  clinico ya fueron revisados declarativamente.

## inferencias

- Infiero que el guard visual cubre el P0 si se aplica antes de construir copy,
  brief o respuesta final de REELS y si todo claim visual relevante exige
  `evidence_id`.
- Infiero que el caso sintetico "no menciones microscopio si no esta en el
  montaje" es el fixture correcto para bloquear no-invencion visual en Directo.
- Infiero que ya no queda un P0 declarado sin guard especifico en el ciclo
  Telegram Directo -> Desktop; queda observacion operacional.

## risks_p0_p1_p2

| Pri | Riesgo residual | Estado | Accion |
| --- | --- | --- | --- |
| P0 | Claim visual inventado sin evidencia. | Cubierto por guard/test declarado. | Mantener como bloqueo de release. |
| P0 | Correccion clinica toca documento equivocado. | Cubierto por guard clinico declarado. | Mantener test. |
| P0 | REELS hereda `active_route=CLINICA`. | Cubierto por media buffer policy declarado. | Mantener test. |
| P0 | Directo usa contrato menor que Desktop. | Cubierto por guard de paridad declarado. | Mantener test. |
| P1 | Implementacion real no coincide con evidencia declarada. | No verificable en esta Mac. | Observacion local del orquestador y suites en CI/local. |
| P1 | Evidence visual existe pero es ambiguo. | Puede requerir criterio humano si el montaje no permite confirmar el claim. | Marcar "no verificado" o pedir revision. |
| P2 | Guard visual bloquea copy descriptivo generico. | Falso positivo aceptable frente a no-invencion. | Afinar allowlist en observacion. |

## decision

```yaml
visual_evidence_p0_closed: true
human_intervention_required: false
additional_fixture_required_now: false
single_next_action: close_telegram_direct_in_observation
observation_conditions:
  - keep_direct_desktop_parity_guard
  - keep_reels_does_not_inherit_clinica_guard
  - keep_clinical_target_document_identity_guard
  - keep_visual_claim_requires_declared_media_evidence_guard
  - keep_latest_turn_display_debug_only
```

## recommendation

Cerrar Telegram Directo -> Desktop en observacion. Reabrir solo si aparece una
senal concreta: claim visual sin `evidence_id`, edicion clinica sin
`target_document_id`, herencia de `active_route` entre frentes, o consumer que
use `latest_turn` para pending/seen.

## confidence

Media-alta para cerrar en observacion porque el ultimo P0 residual ya tiene guard
declarado y las suites relevantes siguen verdes segun el orquestador. Media para
certificar implementacion real, porque los scripts/tests viven en
`/Users/jarvis/.openclaw/workspace`, ausente en esta Mac.

## attempted_routes

- Se hizo `git pull --rebase origin main`.
- Se ejecuto `./scripts/personal_xh_check.sh` y se detecto el job asignado.
- Se reviso el workorder actual.
- Se revisaron resultados previos `20260528T061305`, `20260528T060305` y
  `20260528T054245`.
- Se intento listar scripts/tests bajo `/Users/jarvis/.openclaw/workspace`, pero
  no existen en esta Mac.
- No se uso Telegram real, Gmail, Drive, Calendar, iCloud, Photos, adjuntos
  reales ni servicios externos.

## risks_limits

- Resultado declarativo; no certifica codigo real ni salida de tests reales.
- No se leyeron snapshots, adjuntos, multimedia ni datos clinicos reales.
- La decision final queda en Codex orquestador.

## evidence_paths

- `jobs/20260528T062330-telegram-direct-visual-evidence-guard-review-v1.md`
- `results/20260528T062330-telegram-direct-visual-evidence-guard-review-v1.result.md`
- `results/20260528T061305-telegram-direct-clinical-target-identity-guard-review-v1.result.md`
- `results/20260528T060305-telegram-direct-local-guards-followup-review-v1.result.md`
- `results/20260528T054245-telegram-direct-context-isolation-parity-audit-v1.result.md`
- `/Users/jarvis/.openclaw/workspace/scripts/codex_telegram_direct.py`
- `/Users/jarvis/.openclaw/workspace/tests/telegram/test_desktop_handoff_guardrail.py`
- `/Users/jarvis/.openclaw/workspace/tests/telegram/test_media_buffer_policy.py`
- `/Users/jarvis/.openclaw/workspace/tests/telegram/test_postfix_regression_fixtures.py`
