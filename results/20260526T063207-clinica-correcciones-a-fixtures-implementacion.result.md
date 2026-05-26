# Resultado - 20260526T063207-clinica-correcciones-a-fixtures-implementacion

## summary honesto

Se propone una secuencia de integracion de bajo impacto para convertir correcciones clinicas del Doctor en fixtures y gates de la app medico-legal. No se modifico la app real ni se leyeron datos sensibles. La prioridad es bloquear hechos clinicos inventados antes de cualquier mejora de copy o UI.

**Evidencia:** los resultados previos ya definen 13 fixtures `LUM-DOC-*`, ruta canonica de app y orden recomendado: route guard, fixtures, gates, QA.

**Inferencia:** el punto de menor riesgo es integrar primero normalizacion/route guard y fixtures negativos, antes de tocar plantillas de salida.

**Opinion:** esta rama debe tratarse como patch medico-legal aislado, con commits por capa y rollback facil.

## coverage_table

| fuente | uso | limite |
| --- | --- | --- |
| `context/fronts/clinica.md` | Estado canonico, app real y regla de no tocar plantillas sin baseline/test. | No inspecciona app real. |
| `results/20260525T120000-clinica-fixtures-lumbares-v1.result.md` | Matriz `LUM-DOC-*`, asserts positivos/negativos y severidades. | Es especificacion, no implementacion ejecutada. |
| `results/20260525T084316-clinica-integration-checklist-route-guard-fixtures-v2.result.md` | Orden de integracion, archivos probables, rollback y criterios de aceptacion. | Ubicaciones exactas deben confirmarse en work-mac. |

## integration_plan

1. Crear rama aislada `clinica/lumbar-doctor-corrections`.
2. Inspeccionar baseline real y ubicar el punto unico donde se transforma input clinico en documento/parte.
3. Agregar o reforzar `normalizeClinicalRoute(input)` sin cambiar plantillas visibles.
4. Crear `data/derived/clinical_test_cases/lumbar_doctor_corrections_v1.json` con fixtures `LUM-DOC-001` a `LUM-DOC-013`.
5. Implementar helpers deterministicos de forbidden/required phrases con contexto, no solo busqueda literal global.
6. Integrar `scripts/qa/validate_lumbar_doctor_corrections_v1.js`.
7. Conectar el runner al QA clinico existente.
8. Ejecutar primero tests que deben fallar con version vieja; luego patch; luego verificar que pasan.
9. Commit por capa: `route_guard`, `fixtures`, `gates`, `qa_runner`.
10. Validar manualmente salidas finales de los casos critical antes de tocar UI o copy general.

## files_to_inspect

```text
/Users/jarvis/.openclaw/workspace/clinica/app-clinica-medicolegal/app/product.html
/Users/jarvis/.openclaw/workspace/clinica/app-clinica-medicolegal/app/app.js
/Users/jarvis/.openclaw/workspace/clinica/app-clinica-medicolegal/scripts/jarvis/clinical_document_handoff.js
/Users/jarvis/.openclaw/workspace/clinica/app-clinica-medicolegal/scripts/qa/validate_clinical_inconsistency_audit.js
/Users/jarvis/.openclaw/workspace/clinica/app-clinica-medicolegal/scripts/qa/validate_20_pathology_scenarios.js
/Users/jarvis/.openclaw/workspace/clinica/app-clinica-medicolegal/scripts/qa/validate_clinica_route_guard.js
/Users/jarvis/.openclaw/workspace/clinica/app-clinica-medicolegal/data/derived/clinical_test_cases/
```

Si alguno no existe, buscar el equivalente por funcion: generacion de documento, QA clinico, fixtures derivados y handoff medico-legal.

## test_cases

| prioridad | fixture | assert que bloquea |
| --- | --- | --- |
| P0 | `LUM-DOC-001` | Hernia extraforaminal L4-L5 derecha no puede redactarse como interlaminar/hemilaminotomia/flavectomia. |
| P0 | `LUM-DOC-002` | Extradural/extraforaminal L4-L5 derecha compromete raiz L4, no raiz L5 como principal. |
| P0 | `LUM-DOC-003` | Si input dice sin descompresion directa, no inventar laminectomia/liberacion directa. |
| P0 | `LUM-DOC-006` | Diagnostico no contiene indicacion quirurgica ni "requiere". |
| P0 | `LUM-DOC-007` | No inventar hernia posterolateral derecha si no fue informada. |
| P0 | `LUM-DOC-011` | Hemostasia y recuento antes de cierre de piel. |
| P0 | `LUM-DOC-013` | Parche dural solo si fue indicado y en secuencia correcta. |
| P1 | `LUM-DOC-004` | Fijacion/artrodesis por segmento no lleva lateralidad. |
| P1 | `LUM-DOC-005` | No duplicar descompresion/recalibraje como sinonimos. |
| P1 | `LUM-DOC-008` | Preservar espondilolistesis degenerativa si fue especificada. |
| P2 | `LUM-DOC-009/010/012` | Evitar tautologias, duplicados de posicion/materiales/PLIF. |

## risk_order

1. Hecho quirurgico inventado o incompatible con input.
2. Nivel/raiz/lateralidad incorrectos.
3. Diagnostico contaminado con indicacion terapeutica.
4. Secuencia operatoria incoherente.
5. Duplicados que generen ambiguedad medico-legal.
6. Falsos positivos por regex demasiado literal.

## acceptance_criteria

- Los fixtures P0 fallan en baseline si el bug existe y pasan despues del patch.
- Ningun documento final contiene forbidden phrases activadas por su fixture.
- Cada frase clinica relevante puede rastrearse al input o queda `needs_review`.
- Si un dato falta, el sistema no lo completa por costumbre quirurgica.
- QA clinico corre con un comando unico y bloquea release ante critical fail.
- No hay cambios de UI/copy mezclados con gates clinicos.

## risks_limits

- No se ejecuto la app real desde este worker.
- Ubicaciones exactas deben confirmarse en la Mac de trabajo.
- Regex clinicos deben ser contextuales para no bloquear frases negadas como "no se realizo laminectomia".
- La regla de raiz L4 aplica al caso extraforaminal L4-L5 derecho indicado, no a todos los casos lumbares.

## recommendation

Implementar primero los siete P0 como gate deterministico y dejar los P1/P2 para segunda capa. Si un P0 genera falso positivo, degradarlo solo a `needs_review` con justificacion clinica concreta, no eliminarlo.

## confidence

Alta para orden, fixtures y criterios; media para archivos exactos hasta inspeccionar la app real.

## evidence_paths

- `jobs/20260526T063207-clinica-correcciones-a-fixtures-implementacion.md`
- `context/fronts/clinica.md`
- `results/20260525T120000-clinica-fixtures-lumbares-v1.result.md`
- `results/20260525T084316-clinica-integration-checklist-route-guard-fixtures-v2.result.md`
