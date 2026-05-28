---
id: 20260528T064336-reels-cmp-premium-visual-evidence-gate-review-v1
created_at: 2026-05-28T06:43:36-03:00
created_by: orchestrator
assignee: personal-xh
front: REELS
model: gpt-5.5-xh
reasoning_effort: xhigh
status: queued
no_external_actions: true
no_secrets: true
---

# reels-cmp-premium-visual-evidence-gate-review-v1

## Objetivo

Pablo, hacer una revision declarativa y de bajo riesgo del gate premium para reels CMP, tomando como criterio operativo los incidentes recientes:

- No aceptar previews silenciosos.
- No aceptar piezas sin evidencia visual suficiente.
- No afirmar elementos visuales no presentes en el montaje o material fuente.
- No mezclar materiales de reels distintos.
- Verificar topic y `message_id` antes de llamar entregado a cualquier envio.

## Alcance permitido

Solo auditoria/propuesta de guardrails y fixtures:

- No enviar Telegram ni publicar nada.
- No tocar Drive, iCloud, Photos, Gmail ni adjuntos reales.
- No abrir bibliotecas completas ni material multimedia privado.
- No modificar archivos operativos.
- Usar contexto declarativo del bridge y, si existen en tu Mac, resultados previos relacionados con REELS/Telegram.

## Entregable esperado

1. Proponer un checklist premium minimo para REELS CMP que bloquee:
   - `preview_silencioso`;
   - `visual_claim_without_evidence`;
   - `wrong_material_set`;
   - `missing_delivery_receipt_message_id`.
2. Clasificar riesgos P0/P1/P2.
3. Proponer 3 a 5 fixtures sinteticos, sin usar material real.
4. Recomendar si conviene implementar un guard local simple o dejarlo como checklist manual en observacion.

## Reglas

- Mantener lenguaje formal y operativo.
- Separar evidencia verificada de inferencias.
- No imprimir secretos, rutas de adjuntos reales ni datos personales.
- La decision final queda en Codex orquestador.
