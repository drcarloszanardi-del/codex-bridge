# P2 route guard contexto

## Objetivo

Evitar rutas no canonicas y drift entre `app/app.js`, `app/product.html` y wrappers Jarvis.

## Propuesta

- Declarar `app/product.html` + `scripts/jarvis/clinical_document_handoff.js` como ruta canonica.
- Marcar `app/app.js` como demo o retirarlo del flujo de envio si conserva generadores rapidos.
- Agregar gate que falle si una ruta alternativa genera documentos sin pasar por redaction shield.
- Registrar en QA la ruta exacta usada por cada documento: `route_id`, `version`, `gate_version`.

## Evidencia de riesgo

El snapshot conserva generadores rapidos en `app/app.js` con tecnica interlaminar fija para microdiscectomia lumbar; `app/product.html` ya contiene gates mas especificos.
