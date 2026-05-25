---
id: 20260525T122120-presentaciones-ai-pilot-premium-v1
assignee: personal-xh
model: gpt-5.5-xh
created_at: 2026-05-25T12:21:20-03:00
no_external_actions: true
no_secrets: true
status: pending
---

# Workorder: piloto presentaciones IA premium vs PPT artesanal

## 10 inicial - direccion del orquestador

- Objetivo: diseñar un piloto concreto para mejorar presentaciones medicas del Doctor usando IA sin perder deck editable.
- Frente: PRESENTACIONES.
- Contexto minimo:
  - Contexto canonico: `context/fronts/presentaciones.md`.
  - Rubrica local si aparece en repo: `docs/rubricas/presentaciones_ai_rubrica.md`.
  - Paquete youtubers: `context/youtube_content_packs/20260525-martell-maxmaxdata/`.
- Pregunta CEO:
  - Como hacemos presentaciones mas estrategicas y visuales que PPT artesanal.
  - Que herramienta usar para cada parte.
  - Que podemos hacer ya localmente y que requiere membresia.
  - Que piloto real deberia pedirle al Doctor.
- Herramientas permitidas: leer bridge/context/results; proponer flujo y criterios.
- Herramientas prohibidas: crear cuentas, pagar, subir archivos externos, acceder a Drive privado.
- Criterio de terminado: pipeline paso a paso, decision de herramientas, template de brief, estructura de carpetas, QA checklist y piloto recomendado.

## 80 delegado - trabajo del agente

Pablo debe producir:

- `presentation_pipeline`
- `tool_choices`
- `brief_template`
- `folder_structure`
- `qa_checklist`
- `pilot_candidate`
- `membership_decision`

## 10 final - retorno al orquestador

El resultado debe incluir:

- `summary honesto`
- `coverage_table`
- `presentation_pipeline`
- `tool_choices`
- `brief_template`
- `folder_structure`
- `qa_checklist`
- `pilot_candidate`
- `membership_decision`
- `risks / limits`
- `recommendation`
- `confidence`
- `evidence_paths`

Validar contra `scripts/validate_result_contract.py`.
