---
id: 20260528T132759-tesis-protocolo-datos-y-material-audiovisual
assignee: personal-xh
model: gpt-5.5-xh
created_at: 2026-05-28T13:27:59-03:00
front: TESIS
no_external_actions: true
no_secrets: true
status: pending
---

# Workorder: Tesis: protocolo de datos y uso de material audiovisual

## 10 inicial - direccion del orquestador

- Objetivo: Proponer mejoras metodologicas accionables para recoleccion de datos y uso de videos/material quirurgico como insumo contextual, sin modificar el borrador base.
- Frente: TESIS
- Contexto minimo:
  - `results/20260525T021049-tesis-research-ops-protocol-v1.result.md`
  - `context/fronts/presentaciones.md`
- Herramientas permitidas: leer archivos locales del bridge, analizar, sintetizar y proponer implementacion.
- Herramientas prohibidas: acciones externas, compras, mails, Telegram, secretos, credenciales, datos sensibles no sanitizados.
- Criterio de terminado: resultado accionable, con evidencia, riesgo, decision sugerida y siguiente paso implementable por Codex principal.

## 80 delegado - trabajo del agente

Pablo debe producir estas secciones:

  - `data_collection_protocol_improvements`
  - `video_to_variable_mapping`
  - `ethics_privacy_limits`
  - `draft_change_candidates`
  - `questions_for_doctor`

Tambien debe separar evidencia, inferencia y opinion; y no cerrar con bloqueo sin rutas alternativas, limite exacto y proxima accion.

## 10 final - retorno al orquestador

El resultado debe incluir:

- `summary honesto`
- `coverage_table` o `source_counts`
  - `data_collection_protocol_improvements`
  - `video_to_variable_mapping`
  - `ethics_privacy_limits`
  - `draft_change_candidates`
  - `questions_for_doctor`
- `risks / limits`
- `recommendation`
- `confidence`
- `evidence_paths`

Validar contra `scripts/validate_result_contract.py` antes de marcarlo completado.
