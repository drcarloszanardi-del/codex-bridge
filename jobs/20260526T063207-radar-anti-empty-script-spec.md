---
id: 20260526T063207-radar-anti-empty-script-spec
assignee: personal-xh
model: gpt-5.5-xh
created_at: 2026-05-26T06:32:07-03:00
front: INVERSIONES
no_external_actions: true
no_secrets: true
status: pending
---

# Workorder: Implementacion gate anti informe vacio para radares

## 10 inicial - direccion del orquestador

- Objetivo: Convertir el contrato anti informe vacio de radares en una especificacion de script/gate aplicable a inmobiliaria e instrumental, con thresholds, JSON schema y mensajes de bloqueo.
- Frente: INVERSIONES
- Contexto minimo:
  - `context/fronts/radares.md`
  - `results/20260525T120001-radares-anti-informe-vacio-v1.result.md`
  - `decisions/radar_scorecards_v1.md`
- Herramientas permitidas: leer archivos locales del bridge, analizar, sintetizar y proponer implementacion.
- Herramientas prohibidas: acciones externas, compras, mails, Telegram, secretos, credenciales, datos sensibles no sanitizados.
- Criterio de terminado: resultado accionable, con evidencia, riesgo, decision sugerida y siguiente paso implementable por Codex principal.

## 80 delegado - trabajo del agente

Pablo debe producir estas secciones:

  - `json_schema`
  - `gate_rules`
  - `fallback_routes`
  - `script_plan`
  - `qa_examples`

Tambien debe separar evidencia, inferencia y opinion; y no cerrar con bloqueo sin rutas alternativas, limite exacto y proxima accion.

## 10 final - retorno al orquestador

El resultado debe incluir:

- `summary honesto`
- `coverage_table` o `source_counts`
  - `json_schema`
  - `gate_rules`
  - `fallback_routes`
  - `script_plan`
  - `qa_examples`
- `risks / limits`
- `recommendation`
- `confidence`
- `evidence_paths`

Validar contra `scripts/validate_result_contract.py` antes de marcarlo completado.
