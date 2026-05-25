---
id: 20260525T130220-reels-assets-library-curation-protocol
assignee: personal-xh
model: gpt-5.5-xh
created_at: 2026-05-25T13:02:20-03:00
front: REELS
no_external_actions: true
no_secrets: true
status: pending
---

# Workorder: protocolo de biblioteca de fotos para reels CMP

## 10 inicial - direccion del orquestador

- Objetivo: definir un protocolo seguro para usar una carpeta curada de fotos/videos del Doctor en reels CMP sin abrir toda la biblioteca personal de Photos.app.
- Frente: REELS
- Contexto minimo:
  - `context/fronts/reels_cmp.md`
  - `results/20260525T124546-reels-cmp-next-editorial-options.result.md`
- Supuesto operativo: el Doctor puede crear en la Mac personal una carpeta autorizada tipo `~/CodexAssets/Reels/` con material usable. No pedir acceso indiscriminado a Photos.app.
- Herramientas permitidas: analizar, proponer estructura, manifest, reglas de descarte y QA.
- Herramientas prohibidas: copiar fotos reales al bridge, acceder a Photos.app, pedir secretos, publicar, Telegram o acciones externas.

## 80 delegado - trabajo del agente

Producir:
- `folder_structure`
- `asset_manifest_schema`
- `privacy_filter`
- `selection_workflow`
- `doctor_instructions_minimal`
- `how_to_report_assets_to_orchestrator`

Separar evidencia, inferencia y opinion.

## 10 final - retorno al orquestador

Incluir `summary honesto`, `coverage_table`, `risks / limits`, `recommendation`, `confidence`, `evidence_paths`.
Validar contra `scripts/validate_result_contract.py`.
