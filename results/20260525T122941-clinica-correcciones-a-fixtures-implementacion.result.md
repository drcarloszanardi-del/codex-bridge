# Resultado - clinica correcciones a fixtures implementacion

Job: `20260525T122941-clinica-correcciones-a-fixtures-implementacion`
Worker: `personal-xh` / Pablo
Fecha: `2026-05-25`

## summary honesto

La integracion debe hacerse como patch clinico aislado y de bajo impacto: primero fixtures sinteticos, despues helpers de deteccion, luego gates deterministicos, finalmente inclusion en el runner QA. No conviene tocar UI, copy general ni plantillas amplias en el mismo cambio. El objetivo no es "mejorar redaccion"; es impedir que la app genere hechos clinicos no indicados por el Doctor.

## source_counts

| Fuente | Archivos revisados | Uso |
|---|---:|---|
| `jobs/20260525T122941-clinica-correcciones-a-fixtures-implementacion.md` | 1 | Contrato y secciones exigidas. |
| `context/fronts/clinica.md` | 1 | Estado canonico y regla de convertir correcciones en gates. |
| `results/20260525T120000-clinica-fixtures-lumbares-v1.result.md` | 1 | Matriz LUM-DOC-001 a LUM-DOC-013. |
| `results/20260525T084316-clinica-integration-checklist-route-guard-fixtures-v2.result.md` | 1 | Orden de integracion y archivos probables. |
| `decisions/clinica_patch_proposals_v1/*` | 4 | Fixtures, gates, QA changes y propuestas previas. |

## coverage_table

| Area | Estado | Evidencia |
|---|---|---|
| Correcciones lumbares del Doctor | cubierto | `results/20260525T120000...` lista fixtures y asserts. |
| Orden de integracion | cubierto | `results/20260525T084316...` ya define route guard -> fixtures -> gates -> QA. |
| App real | no tocada | El worker solo propone; implementa Codex principal en Mac de trabajo. |
| Datos sensibles | no usados | Todos los fixtures son sinteticos. |

## integration_plan

1. Crear rama aislada en la app real: `clinica/doctor-lumbar-fixtures-v1`.
2. Agregar fixture data sin cambiar logica: `data/derived/clinical_test_cases/lumbar_doctor_corrections_v1.json`.
3. Agregar validator inicial que lea fixtures y falle por frases prohibidas: `scripts/qa/validate_lumbar_doctor_corrections_v1.js`.
4. Ejecutar validator contra salidas actuales si hay generador disponible; si no, usar snapshots sintenticos de texto.
5. Agregar helpers puros: `scripts/qa/validate_lumbar_gate_helpers.js`.
6. Recién despues integrar gates deterministicos antes de render/guardado final.
7. Conectar al runner `scripts/qa/run_clinica_core_qa.js`.
8. Ejecutar regresion completa.
9. Commit separado por capa: fixtures, helpers, gates, runner.
10. Si falla por falsos positivos, bajar ese gate a `needs_review`, nunca permitir hecho clinico inventado.

## files_to_inspect

```text
app/app.js
app/app.data.js
app/product.html
scripts/jarvis/clinical_document_handoff.js
scripts/qa/run_clinica_core_qa.js
scripts/qa/validate_clinica_route_guard.js
scripts/qa/validate_20_pathology_scenarios.js
scripts/qa/validate_clinical_inconsistency_audit.js
data/derived/clinical_test_cases/
```

## test_cases

| Test | Debe fallar si aparece | Debe pasar si contiene |
|---|---|---|
| `test_extraforaminal_l45_der_no_interlaminar` | interlaminar, hemilaminotomia, flavectomia, hombro de raiz | abordaje foraminal/extraforaminal/Wiltse |
| `test_extraforaminal_l45_der_root_l4` | raiz L5 como raiz principal | raiz L4 derecha |
| `test_sin_descompresion_directa` | laminectomia, hemilaminectomia, flavectomia, liberacion directa | no se realizo descompresion neural directa |
| `test_artrodesis_segmento_sin_lateralidad` | fijacion/artrodesis L4-L5 derecha | fijacion/artrodesis L4-L5 |
| `test_diagnostico_puro` | con indicacion de, requiere instrumentacion | diagnostico sin indicacion agregada |
| `test_no_inventa_topografia` | hernia posterolateral derecha no informada | solo patologia informada |
| `test_secuencia_cierre` | cierre antes de hemostasia/recuento | hemostasia -> recuento -> cierre |
| `test_parche_dural_secuencia` | parche inventado o luego del cierre | parche solo si indicado y antes del cierre |

## risk_order

1. `critical`: hechos quirurgicos no realizados: descompresion directa, laminectomia, parche, abordaje.
2. `critical`: raiz/nivel/lateralidad incorrectos.
3. `high`: diagnostico contaminado con indicacion.
4. `high`: artrodesis/fijacion con lateralidad mal aplicada.
5. `high`: duplicacion de PLIF/materiales.
6. `medium`: tautologias y duplicados de posicion/proteccion.

## acceptance_criteria

- Los fixtures `critical` bloquean release si fallan.
- Cada fixture tiene `input`, `expected_present`, `forbidden_present`, `risk_level`, `doctor_bug_id`.
- Un cambio que corrige texto pero elimina trazabilidad no pasa.
- El runner QA falla con exit code no cero ante cualquier `critical`.
- No se mezclan cambios clinicos con UI/refactors.
- El resultado final no contiene pacientes ni datos reales.

## risks / limits

- La ubicacion exacta depende de la app real; este worker no la modifica.
- Algunas frases requieren regex contextual para no fallar cuando aparecen negadas.
- No se debe generalizar anatomia fuera de los casos indicados por el Doctor.
- Si el generador actual no permite fixtures end-to-end, empezar con validator de texto y luego conectar a generador.

## recommendation

Codex principal debe implementar primero fixtures y validator, sin tocar generacion. Despues agregar gates `critical` en el punto previo a render/guardado. La prueba inicial obligatoria es extraforaminal L4-L5 derecha: no interlaminar y raiz L4.

## confidence

Alta para orden, tests y riesgos. Media para paths exactos hasta inspeccionar la app real en la Mac de trabajo.

## evidence_paths

- `jobs/20260525T122941-clinica-correcciones-a-fixtures-implementacion.md`
- `context/fronts/clinica.md`
- `results/20260525T120000-clinica-fixtures-lumbares-v1.result.md`
- `results/20260525T084316-clinica-integration-checklist-route-guard-fixtures-v2.result.md`
- `decisions/clinica_patch_proposals_v1/lumbar_fixtures.json`
- `decisions/clinica_patch_proposals_v1/deterministic_gates.diff.md`
- `decisions/clinica_patch_proposals_v1/qa_changes.md`

