---
id: 20260528T061305-telegram-direct-clinical-target-identity-guard-review-v1
created_at: 2026-05-28T06:13:05-03:00
created_by: orchestrator
assignee: personal-xh
front: TELEGRAM
model: gpt-5.5-xh
reasoning_effort: xhigh
status: queued
no_external_actions: true
no_secrets: true
---

# telegram-direct-clinical-target-identity-guard-review-v1

## Objetivo

Pablo, revisar declarativamente el guard local agregado por el orquestador para cerrar el P0 que recomendaste: una correccion clinica corta desde Telegram Directo no debe modificar un protocolo equivocado si falta `target_document_id` o identidad de seccion.

Evidencia local declarada por el orquestador:

- Se agrego en `/Users/jarvis/.openclaw/workspace/scripts/codex_telegram_direct.py`:
  - `clinical_edit_requires_target_document_identity(...)`
  - una linea de guard P0 en `build_telegram_task_brief(...)` cuando falta identidad de documento/seccion.
  - inferencia explicita CLINICA para terminos quirurgicos como `protocolo quirurgico`, `hemostasia`, `cifoplastia`, `artrodesis`, `discectomia`, `laminectomia`.
- Se agrego en `/Users/jarvis/.openclaw/workspace/tests/telegram/test_desktop_handoff_guardrail.py`:
  - `assert_clinical_edit_requires_target_document_identity(...)`
  - caso sintetico: `Corrige la redaccion de la hemostasia del protocolo quirurgico.`
  - esperado: ruta `CLINICA`, brief con `Guard clinico P0` y `needs_target_document_identity`.
- Checks locales:
  - `python3 /Users/jarvis/.openclaw/workspace/tests/telegram/test_desktop_handoff_guardrail.py` -> `{"ok": true, "tests": 11}`
  - `python3 /Users/jarvis/.openclaw/workspace/tests/telegram/test_media_buffer_policy.py` -> OK
  - `python3 /Users/jarvis/.openclaw/workspace/tests/telegram/test_postfix_regression_fixtures.py` -> `{"ok": true, "fixtures": 13}`
  - `python3 -m py_compile ...` -> OK

## Alcance permitido

Solo revision declarativa:

- No modificar archivos operativos.
- No enviar Telegram, mails ni notificaciones externas.
- No tocar Gmail, Drive, iCloud, Photos ni adjuntos reales.
- No imprimir secretos ni datos clinicos identificables.
- Si las rutas reales no existen en tu Mac, trabajar sobre esta evidencia declarada y resultados previos.

## Entregable esperado

1. Confirmar si el guard cierra el P0 `clinical_edit_requires_target_document_identity`.
2. Marcar riesgos residuales P0/P1/P2, si los hay.
3. Recomendar una unica proxima accion: cerrar Telegram Directo en observacion, agregar fixture visual evidence, o pedir intervencion humana si hay bloqueo real.

## Reglas

- Mantener salida breve y operativa.
- Separar evidencia verificada de inferencias.
- La decision final queda en Codex orquestador.
