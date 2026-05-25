# Frente Clinica / medico-legal

Actualizado: 2026-05-25.

## Estado canonico

- App canonica: `/Users/jarvis/.openclaw/workspace/clinica/app-clinica-medicolegal`.
- Todo consentimiento, historia clinica y parte quirurgico debe pasar por ruta canonica, manifiesto valido y QA medico-legal.
- Las correcciones del Doctor deben convertirse en reglas, fixtures o gates, no quedar solo en chat.

## Proximo foco

- Convertir correcciones lumbares/extraforaminal/fijacion en fixtures.
- Separar busqueda de corpus, cola de revision y gate activo.
- Rechazar salidas con diagnosticos inventados, indicaciones agregadas o secuencias quirurgicas incompatibles.

## Regla de seguridad

No modificar plantillas clinicas sin leer baseline/ruta canonica y sin test focal.
