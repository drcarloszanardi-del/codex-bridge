---
id: 20260525T221902-clinica-lumbar-regression-pack-from-prior-results-v1
created_at: 2026-05-25T22:19:02-03:00
created_by: orchestrator
assignee: personal-xh
front: CLINICA
model: gpt-5.5-xh
reasoning_effort: xhigh
status: queued
no_external_actions: true
no_secrets: true
---

# Workorder: paquete de regresion clinica lumbar desde resultados previos

## Contexto

El Doctor marco repetidamente inconsistencias criticas en parte quirurgico, historia clinica y consentimiento:

- Diagnosticos redactados como indicaciones quirurgicas.
- Lateralidad incorrecta en artrodesis/fijacion L4-L5.
- Descompresion directa agregada cuando el caso era sin descompresion.
- Hernia extraforaminal redactada como abordaje interlaminar.
- PLIF/parche dural/hemostasia/recuento ubicados en secuencia incorrecta o duplicados.
- Frases genericas que inventan hernia posterolateral, radiculopatia o compromiso neural no indicado.

Ya existen resultados previos de Pablo sobre fixtures/gates lumbares. El orquestador necesita un paquete mas portable y ordenado para convertir en tests detect-only de la app clinica real.

## Objetivo

Armar una propuesta de fixtures y asserts detect-only para la app medico-legal, sin tocar la app real ni plantillas. Debe servir para que el orquestador porte casos a tests locales.

## Fuentes permitidas

- `results/20260525T120000-clinica-fixtures-lumbares-v1.result.md`
- `results/20260525T122941-clinica-correcciones-a-fixtures-implementacion.result.md`
- `results/20260525T153318-clinica-lumbar-inconsistency-gates-v2.result.md`
- `results/20260525T173726-clinica-lumbar-fixture-pack-draft-v2.result.md`
- `results/20260525T181000-clinica-lumbar-validator-detect-only-spec-v1.result.md`
- `results/20260525T184100-clinica-lumbar-v2-stress-artifacts-v1.result.md`
- `results/20260525T170711-clinica-corpus-official-gates-next-integration-v1.result.md`
- `context/fronts/clinica.md` si existe
- `protocol.md`

No leer Drive/iCloud/Photos, no tocar ObraCash, no abrir datos de pacientes reales, no ejecutar acciones externas.

## Entregable esperado

Crear `results/20260525T221902-clinica-lumbar-regression-pack-from-prior-results-v1.result.md` con:

- `summary`
- `fixture_tree`
- `canonical_rules`
- `fixtures_minimal_json` para casos:
  - hernia extraforaminal L4-L5 derecha
  - espondilolistesis degenerativa L4-L5 con fijacion/artrodesis sin descompresion directa
  - canal estrecho lumbar sin repetir "compromiso del canal"
  - consentimiento de fijacion L4-L5 sin lateralidad en artrodesis
  - parte con PLIF/materiales sin duplicar ni cerrar antes de hemostasia/recuento
- `detect_only_asserts`
- `forbidden_phrases_by_case`
- `required_sequence_checks`
- `integration_plan_for_orchestrator`
- `evidence_paths`

## Reglas

- No escribir documentos clinicos finales.
- No promover reglas como definitivas medico-legales; entregarlas como detect-only review gates.
- No usar "y/o" ni formulas vagas como ejemplo de salida aceptada.
- Separar inferencia de evidencia.
- Si falta evidencia, proponer placeholder seguro, no inventar datos clinicos.
