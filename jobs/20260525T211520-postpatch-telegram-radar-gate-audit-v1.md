---
id: 20260525T211520-postpatch-telegram-radar-gate-audit-v1
created_at: 2026-05-25T21:15:20-03:00
created_by: orchestrator
assignee: personal-xh
front: CODEX-OPS
model: gpt-5.5-xh
reasoning_effort: xhigh
status: queued
no_external_actions: true
no_secrets: true
---

# Workorder: auditoria post-patch Telegram + radares anti informe vacio

## Contexto

El Doctor marco dos fallas operativas:

- REELS/voz y trabajos de reel se estaban mezclando con canal directo o topic incorrecto.
- Inmobiliaria e inversiones/instrumental volvieron a mandar respuestas tipo "error", "pagina no hallada" o "no pude", cuando eso ya estaba definido como no aceptable.

El orquestador aplico un parche local en la Mac de trabajo:

- `scripts/codex_telegram_direct.py`: agrego keywords de voz/locucion/voiceover/graves/lata de robot para que pedidos de edicion de voz vinculados a reel se enruten a `REELS`; el fixture "edicion de voz argentina ... graves ... lata de robot" ahora resuelve a `chat_id=-1003701553547`, `thread_id=6`, `reason=direct_deliverable_topic`.
- `scripts/inmobiliaria/send_inm_radar_report.js`: si todos los items son fallas tecnicas y no hay oportunidades vigentes dentro del radio, devuelve `sent:false` con `reason=blocked_empty_technical_failure_report` y no envia Telegram.
- `scripts/inversiones/send_inv_neuro_instrument_report.js`: si `queries_checked=0` y hay errores tecnicos, devuelve `sent:false`, `reason=blocked_empty_technical_failure_report`, `rule=anti_informe_vacio`.

Validaciones locales ya hechas por el orquestador:

- `python3 -m py_compile scripts/codex_telegram_direct.py`: OK.
- `node --check` en ambos scripts de radar: OK.
- Fixtures artificiales de inmobiliaria/inversiones error-only: `sent:false`, `blocked_empty_technical_failure_report`.
- Ultimo radar inmobiliario real no se bloquea: genera texto con 12 oportunidades vigentes dentro del radio y 127 candidatos vigentes.
- Codex Directo reiniciado y healthcheck `ok:true`, bot `Codexzanardibot`, grupo accesible, launchd running.

## Objetivo

Hacer segunda pasada XH sobre el diseno del parche y proponer una suite de regresion concreta para que no vuelva a ocurrir.

No tiene acceso a los archivos exactos de la Mac de trabajo salvo lo resumido aca y los resultados previos del bridge. No debe inventar que vio el patch real. Debe auditar la logica, detectar riesgos residuales y proponer tests/fixtures accionables para el orquestador.

## Fuentes locales permitidas

- `results/20260525T164232-telegram-topic-routing-regression-suite-v1.result.md`
- `results/20260525T164233-radares-anti-informe-vacio-operational-gate-v1.result.md`
- `results/20260525T120001-radares-anti-informe-vacio-v1.result.md`
- `results/20260525T124108-telegram-quality-scorecard.result.md`
- `context/fronts/telegram.md` si existe
- `context/fronts/radares.md` si existe
- `protocol.md`

No leer tokens, secretos, credenciales, Drive, iCloud, Photos ni contenido ObraCash.

## Entregable esperado

Crear `results/20260525T211520-postpatch-telegram-radar-gate-audit-v1.result.md` con:

- `summary`
- `what_seems_fixed`
- `residual_risks`
- `regression_tests` con comandos/fixtures sugeridos
- `radar_gate_tests`
- `telegram_routing_tests`
- `implementation_cautions`
- `recommendation`
- `confidence`
- `evidence_paths`

## Reglas

- No enviar Telegram ni mensajes externos.
- No tocar repos fuera del bridge.
- No imprimir secretos.
- No responder "no pude" como salida final; si falta evidencia, separar inferencia de verificacion.
- Priorizar hallazgos accionables, no teoria larga.
