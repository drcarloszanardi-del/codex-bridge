---
id: 20260526T065253-radares-source-recovery-playbook
assignee: personal-xh
model: gpt-5.5-xh
created_at: 2026-05-26T06:52:53-03:00
front: INVERSIONES
no_external_actions: true
no_secrets: true
status: pending
---

# Workorder: Radares inmobiliaria/instrumental: playbook anti bloqueo de fuentes

## 10 inicial - direccion del orquestador

- Objetivo: Disenar un playbook operativo para que los radares no cierren con 'no pude': rutas alternativas, fuentes espejo, cache/snippets, navegador real, comparables y condiciones para escalar a Pablo.
- Frente: INVERSIONES
- Contexto minimo:
  - `context/fronts/radares.md`
  - `results/20260525T122941-radar-anti-empty-script-spec.result.md`
  - `results/20260525T120001-radares-anti-informe-vacio-v1.result.md`
- Herramientas permitidas: leer archivos locales del bridge, analizar, sintetizar y proponer implementacion.
- Herramientas prohibidas: acciones externas, compras, mails, Telegram, secretos, credenciales, datos sensibles no sanitizados.
- Criterio de terminado: resultado accionable, con evidencia, riesgo, decision sugerida y siguiente paso implementable por Codex principal.

## 80 delegado - trabajo del agente

Pablo debe producir estas secciones:

  - `source_recovery_routes`
  - `front_specific_thresholds`
  - `examples`
  - `automation_hooks`
  - `failure_language_ban`

Tambien debe separar evidencia, inferencia y opinion; y no cerrar con bloqueo sin rutas alternativas, limite exacto y proxima accion.

## 10 final - retorno al orquestador

El resultado debe incluir:

- `summary honesto`
- `coverage_table` o `source_counts`
  - `source_recovery_routes`
  - `front_specific_thresholds`
  - `examples`
  - `automation_hooks`
  - `failure_language_ban`
- `risks / limits`
- `recommendation`
- `confidence`
- `evidence_paths`

Validar contra `scripts/validate_result_contract.py` antes de marcarlo completado.
