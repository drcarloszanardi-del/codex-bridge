---
id: 20260526T155816-radares-root-cause-no-error-report-v1
job_id: 20260526T155816-radares-root-cause-no-error-report-v1
created_at: 2026-05-26T15:58:16-03:00
created_by: codex-orchestrator
assignee: personal-xh
front: RADARES
model: gpt-5.5
reasoning_effort: xhigh
status: queued
no_external_actions: true
no_secrets: true
---

# RADARES root-cause: no volver a informar error como informe

## Contexto

El Doctor volvio a marcar que INM-001 e INV-001 entregaron reportes centrados en error/pagina no hallada/no pude. Eso esta prohibido por politica durable.

En la Mac de trabajo ya existen gates locales:

- `scripts/inmobiliaria/send_inm_radar_report.js`
- `scripts/inversiones/send_inv_neuro_instrument_report.js`
- `scripts/qa/run_radar_regression_gates.sh`
- `tests/radares/test_empty_technical_failure_gate.js`
- `tests/radares/test_radar_report_contract.js`

La suite local pasa, pero el problema reaparece en operacion. Necesito una auditoria XH de causa raiz, no otro resumen.

## Tarea

1. Revisar resultados recientes, logs y contratos disponibles en el bridge y, si estan en contexto, los snippets/reportes que muestren contaminacion.
2. Determinar como un mensaje de error sigue llegando al topic pese al gate:
   - wrapper cron que manda fallo tecnico,
   - `--force`,
   - ruta legacy,
   - reporter incorrecto,
   - artifact viejo/crudo,
   - topic/router que mezcla resumen tecnico,
   - o automation prompt que aun permite aviso de falla.
3. Proponer cambios concretos de bajo riesgo para que:
   - `no pude`, `pagina no hallada`, DNS/WAF/captcha/HTTP error no sean informe final;
   - si el scan falla, se genere `needs_retry/fallback_pending` local, no reporte publico;
   - si hay que avisar, que sea solo bloqueo operativo breve con proxima accion, no informe de oportunidades;
   - INM-001 siempre intente fuentes alternativas/casas/PH reales antes de publicar;
   - INV-001 nunca recomiende implantes sin trazabilidad ANMAT/importador/lote.
4. Entregar una lista priorizada P0/P1 con fixtures faltantes y parche sugerido.

## Restricciones

- No usar Telegram, Gmail, Drive, Calendar ni navegador autenticado.
- No tocar ObraCash ni datos sensibles.
- No hacer compras ni contactar fuentes.
- Devolver resultado en `results/<job_id>.result.md`.

## Formato esperado

- `verdict`: integrar ahora / ajustar antes / no integrar.
- `root_cause_hypothesis`: 3-6 bullets.
- `patch_plan`: archivos y cambios exactos.
- `fixtures_to_add`: nombres y criterio.
- `risk`: regresiones posibles.
- `next_action`: unica accion recomendada para el orquestador.
