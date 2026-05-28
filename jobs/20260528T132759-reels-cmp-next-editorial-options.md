---
id: 20260528T132759-reels-cmp-next-editorial-options
assignee: personal-xh
model: gpt-5.5-xh
created_at: 2026-05-28T13:27:59-03:00
front: REELS
no_external_actions: true
no_secrets: true
status: pending
---

# Workorder: Reels CMP: proximas piezas premium y material requerido

## 10 inicial - direccion del orquestador

- Objetivo: Proponer 3 ideas de reels CMP de alto valor y bajo riesgo para el Dr. Zanardi, con guion corto, asset pack minimo, QA de datos y criterio de publicacion.
- Frente: REELS
- Contexto minimo:
  - `context/fronts/reels_cmp.md`
  - `results/20260525T122941-reels-dia-patria-assets-and-timeline.result.md`
  - `results/20260525T021049-reels-cmp-premium-pipeline-qa-v1.result.md`
- Herramientas permitidas: leer archivos locales del bridge, analizar, sintetizar y proponer implementacion.
- Herramientas prohibidas: acciones externas, compras, mails, Telegram, secretos, credenciales, datos sensibles no sanitizados.
- Criterio de terminado: resultado accionable, con evidencia, riesgo, decision sugerida y siguiente paso implementable por Codex principal.

## 80 delegado - trabajo del agente

Pablo debe producir estas secciones:

  - `editorial_options`
  - `asset_requests`
  - `risk_filter`
  - `recommended_next_reel`
  - `telegram_topic_report`

Tambien debe separar evidencia, inferencia y opinion; y no cerrar con bloqueo sin rutas alternativas, limite exacto y proxima accion.

## 10 final - retorno al orquestador

El resultado debe incluir:

- `summary honesto`
- `coverage_table` o `source_counts`
  - `editorial_options`
  - `asset_requests`
  - `risk_filter`
  - `recommended_next_reel`
  - `telegram_topic_report`
- `risks / limits`
- `recommendation`
- `confidence`
- `evidence_paths`

Validar contra `scripts/validate_result_contract.py` antes de marcarlo completado.
