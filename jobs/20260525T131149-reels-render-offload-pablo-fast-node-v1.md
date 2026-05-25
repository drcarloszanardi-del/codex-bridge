---
id: 20260525T131149-reels-render-offload-pablo-fast-node-v1
assignee: personal-xh
model: gpt-5.5-xh
created_at: 2026-05-25T13:11:49-03:00
front: REELS
no_external_actions: true
no_secrets: true
status: pending
---

# Workorder: usar la Mac de Pablo como nodo rápido de reels CMP

## 10 inicial - dirección del orquestador

- Objetivo: diseñar e implementar, hasta donde sea posible desde la Mac personal, un flujo controlado para que Pablo haga las partes pesadas de reels CMP: búsqueda/selección de assets autorizados, previsualizaciones, renders de prueba, QA visual y propuestas de mejora.
- Motivo: el Doctor confirmó que Pablo vive en una Mac mucho más potente y debe aprovecharse activamente, sin que el orquestador principal pierda control.
- Frente: REELS
- Contexto mínimo:
  - `context/fronts/reels_cmp.md`
  - `results/20260525T122941-reels-dia-patria-assets-and-timeline.result.md`
  - `results/20260525T124546-reels-cmp-next-editorial-options.result.md`
  - `jobs/20260525T130220-reels-assets-library-curation-protocol.md`
- Restricción crítica: no acceder a Photos.app completa ni copiar material personal al bridge. Solo usar carpetas autorizadas explícitamente por el Doctor, por ejemplo `~/CodexAssets/Reels/`, y reportar paths/manifest, no subir fotos privadas.
- Identidad visual: CMP sobrio/profesional; contacto correcto visible `2364384321`, IG `@drcarloszanardi`, web `www.centromedicopellegrini.com.ar`.
- Publicación: prohibida. Solo preparar artefactos, QA y recomendaciones.

## 80 delegado - trabajo del agente

Producir:
- `render_offload_contract`: qué archivos recibe Pablo, qué devuelve, límites y validaciones.
- `asset_manifest_contract`: manifest mínimo para fotos/videos autorizados, con campos de privacidad/licencia/uso.
- `pablo_fast_node_runbook`: pasos concretos para que Pablo renderice/QA sin intervención del Doctor.
- `queue_protocol`: nombres de carpetas/jobs/results y cómo avisar disponibilidad al orquestador.
- `qa_visual_checklist`: solapamiento de texto, datos de contacto, estética CMP, duración, audio, pacientes/datos.
- `first_reel_daily_pipeline`: cómo preparar un reel diario con Pablo trabajando siempre que esté idle.
- Si puede crear scripts en su copia local del bridge sin tocar datos personales, proponer nombres y contenido exacto; si no, devolver parche sugerido.

Separar evidencia, inferencia y opinión. No reportar “no se puede” sin alternativas.

## 10 final - retorno al orquestador

Incluir `summary honesto`, `coverage_table`, `risks / limits`, `recommendation`, `confidence`, `evidence_paths`.
Validar contra `scripts/validate_result_contract.py`.
