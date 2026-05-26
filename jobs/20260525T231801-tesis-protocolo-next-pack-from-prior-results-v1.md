---
id: 20260525T231801-tesis-protocolo-next-pack-from-prior-results-v1
created_at: 2026-05-25T23:18:01-03:00
created_by: orchestrator
assignee: personal-xh
front: TESIS-PAPERS
model: gpt-5.5-xh
reasoning_effort: xhigh
status: queued
no_external_actions: true
no_secrets: true
---

# Workorder: tesis - paquete siguiente de protocolo y recoleccion de datos

## Contexto

El Doctor pidio que el frente tesis avance sin tocar de fondo el borrador base salvo evidencia metodologica/bibliografica real. Pablo ya genero resultados previos sobre protocolo, variables y material audiovisual.

El orquestador necesita una sintesis ejecutable, no teorica, para decidir proximas acciones sin abrir Drive ni documentos personales.

## Objetivo

Revisar resultados previos del bridge sobre tesis y armar un paquete breve de decisiones: variables de recoleccion, huecos metodologicos, riesgos de sesgo, y proximas acciones que Codex pueda ejecutar sin modificar el borrador principal.

No leer Drive/iCloud/Photos, no abrir documentos privados fuera del bridge, no tocar borrador base, no enviar Telegram, no acciones externas.

## Fuentes permitidas

- `results/20260525T124718-tesis-protocolo-datos-y-material-audiovisual.result.md`
- `results/20260525T170712-tesis-protocolo-datos-next-actions-v1.result.md`
- `results/20260525T173727-tesis-empty-template-pack-v1.result.md`
- `results/20260525T181001-tesis-decision-brief-variable-candidates-v1.result.md`
- `results/20260525T184101-tesis-protocolo-decision-gate-pack-v1.result.md`
- `results/20260525T021049-tesis-research-ops-protocol-v1.result.md`
- `context/fronts/tesis.md` si existe
- `protocol.md`

## Entregable esperado

Crear `results/20260525T231801-tesis-protocolo-next-pack-from-prior-results-v1.result.md` con:

- `summary`
- `decision_table`
- `variables_core`
- `variables_optional`
- `data_collection_protocol`
- `bias_and_quality_risks`
- `do_not_touch_draft_rules`
- `next_orchestrator_actions`
- `questions_for_doctor_only_if_needed`
- `evidence_paths`

## Reglas

- No proponer cambios de redaccion al borrador como accion directa.
- No inventar datos, N, resultados, aprobaciones ni citas.
- Separar acciones ejecutables por Codex de decisiones que requieren criterio del Doctor/tutor.
- Mantenerlo accionable y breve.
