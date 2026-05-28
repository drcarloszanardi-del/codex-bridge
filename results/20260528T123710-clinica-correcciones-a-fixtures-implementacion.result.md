---
job_id: 20260528T123710-clinica-correcciones-a-fixtures-implementacion
worker: personal-xh
status: completed
completed_at: 2026-05-28T12:42:18-03:00
front: CLINICA
no_external_actions: true
no_secrets: true
---

# Resultado - implementacion plan clinico correcciones a fixtures

## summary honesto

Se convirtio el material clinico previo en una secuencia de integracion para la app real, sin modificar la app canonica ni leer datos sensibles. La recomendacion es integrar en capas pequenas: primero inspeccion, despues route guard/normalizacion, luego fixtures sinteticos de las correcciones del Doctor, despues gates deterministicos y finalmente regression QA.

## coverage_table

| Seccion pedida | Estado | Evidencia usada |
|---|---|---|
| `integration_plan` | cubierto | `results/20260525T120000-clinica-fixtures-lumbares-v1.result.md`, `results/20260525T084316-clinica-integration-checklist-route-guard-fixtures-v2.result.md` |
| `files_to_inspect` | cubierto | Snapshot/contexto previo con archivos candidatos de app y QA. |
| `test_cases` | cubierto | Matriz `LUM-DOC-001` a `LUM-DOC-013`. |
| `risk_order` | cubierto | Severidades critical/high/medium ya definidas. |
| `acceptance_criteria` | cubierto | Criterios de gates, no inferencia y trazabilidad. |

## evidencia

- El frente clinico exige ruta canonica, manifiesto valido y QA medico-legal antes de tocar consentimiento, historia clinica o parte quirurgico.
- El resultado de fixtures lumbares ya define 13 fixtures `LUM-DOC-*` con asserts negativos/positivos y severidades.
- El checklist previo recomienda orden: route guard, fixtures, gates deterministicos y regression QA.
- La app canonica esta declarada como `/Users/jarvis/.openclaw/workspace/clinica/app-clinica-medicolegal`, pero este worker no la modifico.

## inferencias

- El punto de menor impacto es agregar tests/fixtures antes de cambiar textos clinicos, porque permite demostrar que la version previa falla y la nueva pasa.
- La integracion debe evitar prompts sueltos; las correcciones del Doctor deben vivir como datos de fixtures y gates deterministicos.
- El primer patch debe ser reversible y no mezclar UI, copy general ni refactors.

## opinion

Mi preferencia tecnica es tratar este trabajo como hardening medico-legal, no como mejora narrativa. Primero bloquear hechos clinicos falsos; despues, si hace falta, mejorar redaccion.

## integration_plan

1. Crear una rama aislada en la app canonica y registrar baseline de QA actual.
2. Inspeccionar el flujo real de entrada a documento: normalizacion, generacion, render/guardado y QA.
3. Agregar o ubicar una funcion unica tipo `normalizeClinicalRoute(input)` que preserve solo datos dados o trazables.
4. Agregar archivo de fixtures sinteticos con las 13 correcciones del Doctor: `lumbar_doctor_corrections_v1.json`.
5. Agregar runner focal `validate_lumbar_doctor_corrections_v1.js` que ejecute cada fixture contra la salida final.
6. Integrar gates critical antes del render final: no inventar abordaje, raiz, descompresion, diagnostico, implantes ni secuencia.
7. Agregar los casos al runner clinico principal solo cuando el runner focal pase.
8. Ejecutar regression: route guard, inconsistency audit, 20 pathology scenarios y fixtures lumbares nuevos.
9. Revisar manualmente salidas finales de los casos critical con foco en documento final, no solo objeto intermedio.
10. Commit por capa: fixtures, validator, gates, wiring QA.

## files_to_inspect

```text
app/product.html
app/app.js
scripts/jarvis/clinical_document_handoff.js
scripts/qa/validate_clinica_route_guard.js
scripts/qa/validate_clinical_inconsistency_audit.js
scripts/qa/validate_20_pathology_scenarios.js
scripts/qa/run_clinica_core_qa.js
data/derived/clinical_test_cases/lumbar_gates_v1.json
data/derived/clinical_test_cases/lumbar_negative_assertions_v1.json
data/derived/clinical_test_cases/lumbar_doctor_corrections_v1.json
docs/clinical_gate_doctor_corrections.md
```

Si alguno no existe, crear solo el minimo local equivalente siguiendo los nombres/patrones reales de la app.

## test_cases

| Prioridad | Fixture | Assert principal | Tipo esperado |
|---|---|---|---|
| P0 | `LUM-DOC-001` | Hernia extraforaminal L4-L5 derecha no debe volverse interlaminar/hemilaminotomia/flavectomia. | hard fail |
| P0 | `LUM-DOC-002` | Hernia extraforaminal L4-L5 derecha debe comprometer raiz L4 derecha, no L5. | hard fail |
| P0 | `LUM-DOC-003` | Caso `sin descompresion directa` no puede narrar laminectomia/liberacion directa. | hard fail |
| P0 | `LUM-DOC-006` | Campo diagnostico no puede contener indicacion terapeutica. | hard fail |
| P0 | `LUM-DOC-007` | No inventar hernia posterolateral derecha ni topografia no informada. | hard fail |
| P0 | `LUM-DOC-011` | Hemostasia y recuento deben quedar antes del cierre de piel. | hard fail |
| P0 | `LUM-DOC-013` | Parche dural/refuerzo solo si fue indicado y en secuencia correcta. | hard fail |
| P1 | `LUM-DOC-004` | Fijacion/artrodesis L4-L5 no lleva lateralidad como si fuera lado del segmento. | hard fail |
| P1 | `LUM-DOC-005` | No duplicar descompresion/recalibraje como hechos separados sin fuente. | hard fail o needs_review |
| P1 | `LUM-DOC-008` | Preservar espondilolistesis degenerativa si fue especificada. | hard fail |
| P1 | `LUM-DOC-012` | No duplicar PLIF, cages, tornillos, barras ni materiales. | hard fail |
| P2 | `LUM-DOC-009` | Evitar tautologia `canal estrecho con compromiso del canal`. | warning/fail segun salida |
| P2 | `LUM-DOC-010` | No duplicar posicion/proteccion ocular/puntos de apoyo. | warning/fail segun salida |

## risk_order

1. `critical`: hechos quirurgicos no realizados o secuencia incompatible.
2. `critical`: anatomia/topografia/raiz equivocada o inventada.
3. `high`: diagnostico contaminado con indicacion, lateralidad mal aplicada o subtipo cambiado.
4. `high`: duplicacion de tecnicas/materiales que altere trazabilidad.
5. `medium`: tautologias y duplicados de estilo que no cambian el hecho clinico.

## acceptance_criteria

- Cada fixture P0 falla contra la salida vulnerable o queda demostrado como protegido por test existente.
- Cada fixture P0/P1 pasa contra la salida nueva en texto final visible.
- Cada frase clinica relevante tiene fuente en input o queda marcada `needs_review`.
- No se agrega diagnostico, abordaje, descompresion, raiz, material ni evento intraoperatorio por inferencia.
- El runner focal y el runner clinico principal pasan antes del commit final.
- El cambio queda aislado de UI, marketing, copy no clinico y refactors.

## risks_limits

- Este resultado no inspecciono la app canonica real; propone secuencia y archivos candidatos desde contexto bridge.
- Los nombres de archivos pueden variar; la implementacion debe adaptarse a la estructura real encontrada.
- Algunas frases prohibidas necesitan regex contextual para no bloquear textos negados como `no se realizo laminectomia`.
- La tabla de raiz/topografia no debe generalizarse mas alla de los casos explicitamente cubiertos sin revision clinica.

## recommendation

Implementar primero los P0 como fixtures y gates detect-only. Solo despues cambiar la generacion. El primer merge aceptable debe demostrar que ningun documento final inventa hechos clinicos ni cambia la secuencia quirurgica.

## confidence

Alta para el orden de integracion y los casos P0/P1, porque salen de resultados previos ya especificados. Media para rutas exactas de archivos hasta inspeccionar la app canonica real.

## evidence_paths

- `jobs/20260528T123710-clinica-correcciones-a-fixtures-implementacion.md`
- `context/fronts/clinica.md`
- `results/20260525T120000-clinica-fixtures-lumbares-v1.result.md`
- `results/20260525T084316-clinica-integration-checklist-route-guard-fixtures-v2.result.md`

