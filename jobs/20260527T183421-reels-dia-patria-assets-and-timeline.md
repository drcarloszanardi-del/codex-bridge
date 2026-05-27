---
id: 20260527T183421-reels-dia-patria-assets-and-timeline
assignee: personal-xh
model: gpt-5.5-xh
created_at: 2026-05-27T18:34:21-03:00
front: REELS
no_external_actions: true
no_secrets: true
status: pending
---

# Workorder: Reel Dia de la Patria: timeline tecnico y pedido de assets

## 10 inicial - direccion del orquestador

- Objetivo: Convertir el concepto del reel Dia de la Patria en timeline tecnico editable, lista minima de assets, variantes de montaje y criterios de QA frame a frame.
- Frente: REELS
- Contexto minimo:
  - `context/fronts/reels_cmp.md`
  - `results/20260525T120325-reel-dia-patria-cmp-premium-v1.result.md`
- Herramientas permitidas: leer archivos locales del bridge, analizar, sintetizar y proponer implementacion.
- Herramientas prohibidas: acciones externas, compras, mails, Telegram, secretos, credenciales, datos sensibles no sanitizados.
- Criterio de terminado: resultado accionable, con evidencia, riesgo, decision sugerida y siguiente paso implementable por Codex principal.

## 80 delegado - trabajo del agente

Pablo debe producir estas secciones:

  - `timeline_40s`
  - `minimal_asset_pack`
  - `editing_notes`
  - `qa_frame_checklist`
  - `doctor_asset_request`

Tambien debe separar evidencia, inferencia y opinion; y no cerrar con bloqueo sin rutas alternativas, limite exacto y proxima accion.

## 10 final - retorno al orquestador

El resultado debe incluir:

- `summary honesto`
- `coverage_table` o `source_counts`
  - `timeline_40s`
  - `minimal_asset_pack`
  - `editing_notes`
  - `qa_frame_checklist`
  - `doctor_asset_request`
- `risks / limits`
- `recommendation`
- `confidence`
- `evidence_paths`

Validar contra `scripts/validate_result_contract.py` antes de marcarlo completado.
