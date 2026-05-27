---
job_id: 20260527T003215-clinica-correcciones-a-fixtures-implementacion
worker: personal-xh
status: completed
completed_at: 2026-05-27T00:37:30-03:00
front: CLINICA
no_external_actions: true
no_secrets: true
---

# Resultado - Clinica correcciones a fixtures implementacion

## summary honesto

La integracion debe ser chica, testeable y sin refactors: primero ubicar el
punto unico donde la app arma la ruta/parte clinico, despues cargar fixtures
sinteticos de correcciones del Doctor, luego activar gates deterministicos y
finalmente correr regresion. No conviene tocar plantillas clinicas a ciegas ni
mezclar esto con UI.

La evidencia local indica que los errores de mayor riesgo son: abordaje
interlaminar inventado para extraforaminal, raiz equivocada en L4-L5
extraforaminal, descompresion directa agregada donde se explicita que no hubo,
diagnostico mezclado con indicacion y orden quirurgico incorrecto de cierre.

## coverage_table

| Fuente | Estado | Uso |
| --- | --- | --- |
| `jobs/20260527T003215-clinica-correcciones-a-fixtures-implementacion.md` | Revisada | Entregables y restricciones. |
| `context/fronts/clinica.md` | Revisada | Ruta canonica, reglas de seguridad y foco clinico. |
| `results/20260525T120000-clinica-fixtures-lumbares-v1.result.md` | Revisada | Matriz LUM-DOC y asserts. |
| `results/20260525T084316-clinica-integration-checklist-route-guard-fixtures-v2.result.md` | Revisada | Orden previo de integracion, archivos probables y rollback. |

## integration_plan

1. Crear rama clinica aislada en la app real. No mezclar UI, copy ni refactors.
2. Inspeccionar flujo de generacion: input clinico -> diagnostico -> indicacion
   -> procedimiento -> parte quirurgico.
3. Agregar fixtures como datos, no como prompts. Cada caso debe incluir
   `input`, `expected_present`, `forbidden_present`, `risk_level` y
   `doctor_bug_id`.
4. Implementar helper de route guard tipo `normalizeClinicalRoute(input)` que no
   complete campos ausentes.
5. Activar gates critical primero: LUM-DOC-001, 002, 003, 006, 011 y 013.
6. Validar texto final visible; no alcanza testear solo objetos intermedios.
7. Subir en commits por capa: route guard, fixtures, gates, QA.

## files_to_inspect

```text
app/app.js
app/product.html
scripts/jarvis/clinical_document_handoff.js
scripts/qa/validate_clinica_route_guard.js
scripts/qa/validate_clinical_inconsistency_audit.js
scripts/qa/validate_20_pathology_scenarios.js
data/derived/clinical_test_cases/lumbar_gates_v1.json
data/derived/clinical_test_cases/lumbar_negative_assertions_v1.json
```

Si no existen esos nombres exactos, buscar equivalentes por `rg "route|lumbar|gate|clinical"` en la app real.

## test_cases

| Id | Input sintetico | Debe fallar si aparece | Debe pasar si aparece |
| --- | --- | --- | --- |
| `LUM-DOC-001` | Hernia extraforaminal L4-L5 derecha | `interlaminar`, `hemilaminotomia`, `flavectomia` como via principal | abordaje foraminal/extraforaminal/Wiltse compatible |
| `LUM-DOC-002` | Extraforaminal L4-L5 derecha con radiculopatia | raiz L5 como raiz principal | raiz L4 derecha |
| `LUM-DOC-003` | Caso dice `sin descompresion directa` | laminectomia, flavectomia, liberacion directa | frase explicita de no descompresion directa |
| `LUM-DOC-004` | Fijacion L4-L5 con sintomas derechos | `fijacion L4-L5 derecha` | segmento L4-L5 sin lateralidad de fijacion |
| `LUM-DOC-006` | Campo diagnostico | `con indicacion de`, `requiere cirugia` | diagnostico puro |
| `LUM-DOC-011` | Parte con cierre | hemostasia/recuento despues de cierre de piel | hemostasia y recuento antes de cierre |
| `LUM-DOC-013` | Sin durotomia/parche indicado | parche dural inventado | ausencia de parche o `needs_review` si falta fuente |

## risk_order

1. Critical: hechos quirurgicos inventados o incompatibles con input.
2. Critical: raiz/nivel/lateralidad equivocada por inferencia.
3. Critical: secuencia operatoria imposible o medico-legalmente riesgosa.
4. High: diagnostico contaminado con indicacion terapeutica.
5. High: duplicado semantico de tecnica, material o nivel.
6. Medium: tautologias y estilo que no cambian el hecho clinico.

## acceptance_criteria

- Cada fixture critical falla contra una salida vieja/control y pasa con el patch.
- Ningun `forbidden_present` aparece en el documento final salvo negacion controlada.
- Cada afirmacion clinica importante puede rastrearse a una frase de entrada.
- Campos ausentes quedan vacios, `null` o `needs_review`; nunca se completan por costumbre quirurgica.
- El runner QA sale con codigo distinto de cero si falla cualquier critical.
- No hay cambios de UI ni de copy general en el mismo commit.

## risks / limits

- Este resultado no edita la app real; define secuencia de bajo impacto.
- Algunas frases prohibidas requieren regex contextual para no bloquear negaciones correctas.
- La regla de raiz L4 aplica solo al caso extraforaminal L4-L5 derecho definido.

## recommendation

Primera accion implementable: crear `data/derived/clinical_test_cases/lumbar_doctor_corrections_v1.json`
con los fixtures critical y un runner `scripts/qa/validate_lumbar_doctor_corrections_v1.js`.
No tocar plantillas hasta que ese runner exista.

## confidence

Alta para el orden y los casos critical; media para rutas exactas hasta inspeccionar la app real.

## evidence_paths

- `jobs/20260527T003215-clinica-correcciones-a-fixtures-implementacion.md`
- `context/fronts/clinica.md`
- `results/20260525T120000-clinica-fixtures-lumbares-v1.result.md`
- `results/20260525T084316-clinica-integration-checklist-route-guard-fixtures-v2.result.md`
