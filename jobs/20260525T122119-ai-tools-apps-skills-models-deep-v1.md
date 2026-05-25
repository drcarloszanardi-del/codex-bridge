---
id: 20260525T122119-ai-tools-apps-skills-models-deep-v1
assignee: personal-xh
model: gpt-5.5-xh
created_at: 2026-05-25T12:21:19-03:00
no_external_actions: true
no_secrets: true
status: pending
---

# Workorder: apps, skills, subagentes y modelos IA desde youtubers - deep extraction

## 10 inicial - direccion del orquestador

- Objetivo: extraer de todo el material Martell/Maxmaxdata una matriz accionable de apps, complementos, skills, subagentes, motores IA y usos por funcion para el ecosistema Zanardi.
- Frente: CODEX-OPS / herramientas IA.
- Contexto minimo:
  - Paquete fuente: `context/youtube_content_packs/20260525-martell-maxmaxdata/`.
  - Matriz inicial: `../docs/ai_tools_operating_matrix_youtubers_2026-05-25.md` en la Mac de trabajo, o su equivalente si no esta en bridge.
  - Resultado previo: `results/20260525T112543-youtubers-auditoria-profunda-con-pack-obligatorio-v2.result.md`.
- Preguntas que debe responder:
  - Que apps/herramientas aparecen o se infieren como utiles.
  - Que skills/habilidades hay que construir en nuestro sistema.
  - Que subagentes faltan y cuales ya existen.
  - Que motores superan a Codex/Opus en funciones especificas.
  - Que herramientas podrian mejorar o reemplazar el flujo PPT artesanal.
  - Que es humo/marketing y no conviene adoptar.
  - Que pilotos reales recomienda antes de pagar membresias.
- Herramientas permitidas: leer archivos locales del bridge y proponer matriz.
- Herramientas prohibidas: navegar, comprar, pedir login, tocar datos sensibles, publicar o contactar terceros.
- Criterio de terminado: matriz de herramientas con decision adopt/adapt/pilot/reject, impacto por frente, costo/privacidad, piloto sugerido y prioridad.

## 80 delegado - trabajo del agente

Pablo debe producir:

- `tool_matrix`
- `skills_to_build`
- `subagents_to_add_or_refine`
- `models_by_function`
- `presentation_tools_review`
- `pilot_plan`
- `reject_hype_log`
- `implementation_backlog`

## 10 final - retorno al orquestador

El resultado debe incluir:

- `summary honesto`
- `source_counts` o `coverage_table`
- `tool_matrix`
- `skills_to_build`
- `subagents_to_add_or_refine`
- `models_by_function`
- `presentation_tools_review`
- `pilot_plan`
- `reject_hype_log`
- `implementation_backlog`
- `risks / limits`
- `recommendation`
- `confidence`
- `evidence_paths`

Validar contra `scripts/validate_result_contract.py`.
