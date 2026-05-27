---
id: 20260527T005221-ai-tools-pilot-prioritization
assignee: personal-xh
model: gpt-5.5-xh
created_at: 2026-05-27T00:52:21-03:00
front: CODEX-OPS
no_external_actions: true
no_secrets: true
status: pending
---

# Workorder: Herramientas IA: priorizar pilotos antes de membresias

## 10 inicial - direccion del orquestador

- Objetivo: Tomar la matriz de herramientas IA y priorizar 3 pilotos reales con criterio de impacto, privacidad, costo y esfuerzo para el ecosistema Zanardi.
- Frente: CODEX-OPS
- Contexto minimo:
  - `results/20260525T122119-ai-tools-apps-skills-models-deep-v1.result.md`
  - `context/youtube_content_packs/20260525-martell-maxmaxdata/`
- Herramientas permitidas: leer archivos locales del bridge, analizar, sintetizar y proponer implementacion.
- Herramientas prohibidas: acciones externas, compras, mails, Telegram, secretos, credenciales, datos sensibles no sanitizados.
- Criterio de terminado: resultado accionable, con evidencia, riesgo, decision sugerida y siguiente paso implementable por Codex principal.

## 80 delegado - trabajo del agente

Pablo debe producir estas secciones:

  - `pilot_priority`
  - `cost_privacy_matrix`
  - `success_metrics`
  - `do_not_buy_yet`
  - `next_actions`

Tambien debe separar evidencia, inferencia y opinion; y no cerrar con bloqueo sin rutas alternativas, limite exacto y proxima accion.

## 10 final - retorno al orquestador

El resultado debe incluir:

- `summary honesto`
- `coverage_table` o `source_counts`
  - `pilot_priority`
  - `cost_privacy_matrix`
  - `success_metrics`
  - `do_not_buy_yet`
  - `next_actions`
- `risks / limits`
- `recommendation`
- `confidence`
- `evidence_paths`

Validar contra `scripts/validate_result_contract.py` antes de marcarlo completado.
