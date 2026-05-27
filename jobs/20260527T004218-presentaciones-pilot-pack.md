---
id: 20260527T004218-presentaciones-pilot-pack
assignee: personal-xh
model: gpt-5.5-xh
created_at: 2026-05-27T00:42:18-03:00
front: PRESENTACIONES
no_external_actions: true
no_secrets: true
status: pending
---

# Workorder: Presentaciones IA: pack piloto operativo

## 10 inicial - direccion del orquestador

- Objetivo: Definir un pack piloto para una presentacion medica premium: brief, estructura de carpetas, criterios de fuente, visual direction, PPTX editable y QA.
- Frente: PRESENTACIONES
- Contexto minimo:
  - `context/fronts/presentaciones.md`
  - `results/20260525T122120-presentaciones-ai-pilot-premium-v1.result.md`
  - `results/20260525T112543-youtubers-auditoria-profunda-con-pack-obligatorio-v2.result.md`
- Herramientas permitidas: leer archivos locales del bridge, analizar, sintetizar y proponer implementacion.
- Herramientas prohibidas: acciones externas, compras, mails, Telegram, secretos, credenciales, datos sensibles no sanitizados.
- Criterio de terminado: resultado accionable, con evidencia, riesgo, decision sugerida y siguiente paso implementable por Codex principal.

## 80 delegado - trabajo del agente

Pablo debe producir estas secciones:

  - `pilot_pack`
  - `brief_template`
  - `folder_structure`
  - `qa_checklist`
  - `membership_trigger`

Tambien debe separar evidencia, inferencia y opinion; y no cerrar con bloqueo sin rutas alternativas, limite exacto y proxima accion.

## 10 final - retorno al orquestador

El resultado debe incluir:

- `summary honesto`
- `coverage_table` o `source_counts`
  - `pilot_pack`
  - `brief_template`
  - `folder_structure`
  - `qa_checklist`
  - `membership_trigger`
- `risks / limits`
- `recommendation`
- `confidence`
- `evidence_paths`

Validar contra `scripts/validate_result_contract.py` antes de marcarlo completado.
