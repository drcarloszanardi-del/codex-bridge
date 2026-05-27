---
job_id: 20260527T183421-clinica-correcciones-a-fixtures-implementacion
worker: personal-xh
status: completed
completed_at: 2026-05-27T18:38:00-03:00
front: CLINICA
no_external_actions: true
no_secrets: true
---

# Resultado - Implementacion plan clinico: correcciones a fixtures

## summary honesto

Plan accionable para integrar las correcciones clinicas del Doctor en la app real
sin mezclar refactors: primero ubicar el punto unico de normalizacion clinica,
luego agregar fixtures lumbares del Doctor, despues gates deterministicos, y
finalmente sumarlos al runner QA. No toque la app real ni datos sensibles.

## coverage_table

| Fuente | Estado | Uso |
| --- | --- | --- |
| `jobs/20260527T183421-clinica-correcciones-a-fixtures-implementacion.md` | Revisada | Workorder y secciones requeridas. |
| `context/fronts/clinica.md` | Revisada | Canon: app real, QA medico-legal, correcciones como gates. |
| `results/20260525T120000-clinica-fixtures-lumbares-v1.result.md` | Revisada | Matriz LUM-DOC-001 a LUM-DOC-013. |
| `results/20260525T084316-clinica-integration-checklist-route-guard-fixtures-v2.result.md` | Revisada | Orden de integracion, archivos probables y criterios. |

## evidence_inference_opinion

| Tipo | Contenido |
| --- | --- |
| Evidencia | Los resultados previos ya definen fixtures critical: extraforaminal no interlaminar, raiz L4, sin descompresion directa, diagnostico sin indicacion, cierre ordenado y parche dural solo si indicado. |
| Inferencia | La app deberia tener un punto de normalizacion/generacion y runners QA donde insertar fixtures antes de tocar templates. |
| Opinion | El menor riesgo es integrar en commits por capa: fixtures primero, gates despues, runner al final. |

## integration_plan

1. Crear rama limpia en la Mac de trabajo y confirmar baseline de la app:
   `app-clinica-medicolegal`.
2. Inspeccionar rutas candidatas y localizar el punto unico donde se arma el
   documento clinico antes del render final.
3. Agregar dataset sintetico:
   `data/derived/clinical_test_cases/lumbar_doctor_corrections_v1.json`.
4. Portar la matriz `LUM-DOC-001` a `LUM-DOC-013` con campos:
   `id`, `source_sentence`, `fixture_type`, `risk_level`,
   `expected_present`, `forbidden_present`, `doctor_bug_id`,
   `applies_when`, `notes`.
5. Crear helper de gates:
   `scripts/qa/validate_lumbar_gate_helpers.js`.
6. Crear runner focal:
   `scripts/qa/validate_lumbar_doctor_corrections_v1.js`.
7. Integrar ese runner al QA core solo cuando pase aislado.
8. Agregar documentacion corta:
   `docs/clinical_gate_doctor_corrections.md`.
9. Ejecutar primero pruebas que deben fallar contra version vieja; luego aplicar
   gates y verificar que pasen.
10. Commit por capa: `fixtures`, `gate helpers`, `qa runner`, `docs`.

## files_to_inspect

```text
/Users/jarvis/.openclaw/workspace/clinica/app-clinica-medicolegal/app/app.js
/Users/jarvis/.openclaw/workspace/clinica/app-clinica-medicolegal/app/product.html
/Users/jarvis/.openclaw/workspace/clinica/app-clinica-medicolegal/scripts/jarvis/clinical_document_handoff.js
/Users/jarvis/.openclaw/workspace/clinica/app-clinica-medicolegal/scripts/qa/validate_20_pathology_scenarios.js
/Users/jarvis/.openclaw/workspace/clinica/app-clinica-medicolegal/scripts/qa/validate_clinical_inconsistency_audit.js
/Users/jarvis/.openclaw/workspace/clinica/app-clinica-medicolegal/scripts/qa/validate_clinica_route_guard.js
/Users/jarvis/.openclaw/workspace/clinica/app-clinica-medicolegal/data/derived/clinical_test_cases/
```

Si alguno no existe, buscar por `validate_*clinical*`, `pathology`,
`lumbar`, `consent`, `diagnostico`, `indicacion`, `parte quirurgico`.

## test_cases

Prioridad 1, hard fail:

| Fixture | Gate | Test |
| --- | --- | --- |
| `LUM-DOC-001` | Hernia extraforaminal L4-L5 derecha no puede generar abordaje interlaminar/hemilaminotomia/flavectomia. | `test_extraforaminal_l45_der_no_interlaminar` |
| `LUM-DOC-002` | Hernia extraforaminal L4-L5 derecha compromete raiz L4, no L5. | `test_extraforaminal_l45_der_root_l4` |
| `LUM-DOC-003` | Si input dice sin descompresion directa, bloquear laminectomia/liberacion directa. | `test_sin_descompresion_directa_bloquea_descompresion` |
| `LUM-DOC-006` | Diagnostico no puede contener indicacion terapeutica. | `test_diagnostico_no_contiene_indicacion` |
| `LUM-DOC-011` | Hemostasia y recuento antes del cierre de piel. | `test_hemostasia_recuento_antes_cierre_piel` |
| `LUM-DOC-013` | Parche/refuerzo dural solo si fue indicado y en secuencia correcta. | `test_parche_dural_solo_si_indicado_y_en_secuencia` |

Prioridad 2:

| Fixture | Gate |
| --- | --- |
| `LUM-DOC-004` | Fijacion/artrodesis por segmento, sin lateralidad falsa. |
| `LUM-DOC-005` | No duplicar descompresion/recalibraje como sinonimos. |
| `LUM-DOC-007` | No inventar hernia posterolateral derecha. |
| `LUM-DOC-008` | Preservar espondilolistesis degenerativa si fue especificada. |
| `LUM-DOC-009` | Evitar tautologia de canal estrecho. |
| `LUM-DOC-010` | No duplicar posicion/protecciones. |
| `LUM-DOC-012` | No duplicar PLIF/implantes/materiales. |

## risk_order

1. `critical`: texto quirurgico con hechos no realizados.
2. `critical`: nivel/raiz/lateralidad incorrectos.
3. `critical`: diagnostico contaminado con indicacion.
4. `critical`: secuencia quirurgica imposible o fuera de orden.
5. `high`: duplicado de materiales, PLIF, nivel o abordaje.
6. `medium`: estilo tautologico o repeticion no peligrosa.

## acceptance_criteria

- El runner focal pasa en limpio.
- Los fixtures critical fallan contra una salida vieja conocida o fixture de
  control negativo.
- Cada frase clinica relevante se rastrea a input o queda en `needs_review`.
- No hay templates clinicos tocados sin test focal asociado.
- No se agregan reglas hard desde jurisprudencia/doctrina no oficial.
- El QA core incluye el nuevo runner y falla si cualquiera de los critical falla.

## risks / limits

- No inspeccione la app real; las rutas candidatas pueden variar.
- Los `forbidden_present` necesitan regex contextual para no bloquear frases como
  "no se realizo laminectomia".
- La regla raiz L4 aplica al caso extraforaminal L4-L5 derecho, no debe
  generalizarse sin tabla anatomica verificada.

## recommendation

Codex principal deberia implementar primero `LUM-DOC-001`, `002`, `003`, `006`,
`011` y `013` como suite focal. Si eso pasa, integrar el resto. No mezclar esta
ronda con UI, copy o corpus legal.

## confidence

Alta para el orden y fixtures prioritarios porque derivan de resultados previos
del bridge. Media para nombres exactos de archivos hasta inspeccionar la app real.

## evidence_paths

- `jobs/20260527T183421-clinica-correcciones-a-fixtures-implementacion.md`
- `context/fronts/clinica.md`
- `results/20260525T120000-clinica-fixtures-lumbares-v1.result.md`
- `results/20260525T084316-clinica-integration-checklist-route-guard-fixtures-v2.result.md`
