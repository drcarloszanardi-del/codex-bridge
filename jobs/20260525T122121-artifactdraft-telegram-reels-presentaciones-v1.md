---
id: 20260525T122121-artifactdraft-telegram-reels-presentaciones-v1
assignee: personal-xh
model: gpt-5.5-xh
created_at: 2026-05-25T12:21:21-03:00
no_external_actions: true
no_secrets: true
status: pending
---

# Workorder: ArtifactDraft para separar conversacion, razonamiento, artefacto y entrega

## 10 inicial - direccion del orquestador

- Objetivo: especificar una implementacion concreta de `ArtifactDraft` para Telegram Directo, Reels/CMP y Presentaciones.
- Frente: CODEX-OPS / Telegram / Reels / Presentaciones.
- Contexto minimo:
  - `context/fronts/telegram.md`
  - `context/fronts/reels_cmp.md`
  - `context/fronts/presentaciones.md`
  - `results/20260525T112543-youtubers-auditoria-profunda-con-pack-obligatorio-v2.result.md`
- Problema:
  - El Doctor manda una orden o varios archivos.
  - El sistema no debe mezclar chat, razonamiento, borrador, asset plan y entrega final.
  - Necesitamos guardar drafts reutilizables antes de enviar/publicar.
- Herramientas permitidas: proponer schema/paths/scripts; no tocar app real ni ejecutar envios.
- Herramientas prohibidas: enviar Telegram, publicar, acciones externas.
- Criterio de terminado: especificacion implementable con paths, JSON schema, comandos y criterios de QA.

## 80 delegado - trabajo del agente

Pablo debe producir:

- `artifact_schema`
- `folder_layout`
- `telegram_flow`
- `reels_flow`
- `presentations_flow`
- `qa_contract`
- `implementation_steps`

## 10 final - retorno al orquestador

El resultado debe incluir:

- `summary honesto`
- `coverage_table`
- `artifact_schema`
- `folder_layout`
- `telegram_flow`
- `reels_flow`
- `presentations_flow`
- `qa_contract`
- `implementation_steps`
- `risks / limits`
- `recommendation`
- `confidence`
- `evidence_paths`

Validar contra `scripts/validate_result_contract.py`.
