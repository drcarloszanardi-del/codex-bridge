---
job_id: 20260525T084316-clinica-integration-checklist-route-guard-fixtures-v2
worker: personal-xh
status: completed
completed_at: 2026-05-25T08:52:07-03:00
front: CLINICA
---

# Result

## summary

Checklist de integracion para work-mac: primero route guard canonico, luego fixtures lumbares, despues gates deterministicos y por ultimo QA regression. No se debe tocar la app real desde esta Mac. La integracion debe bloquear explicitamente los bugs medico-legales indicados por el Doctor.

## findings con evidencia

- `decisions/clinica_patch_proposals_v1/README.md` ya define prioridad: route guard, fixtures lumbares critical, gates deterministicos y QA regression.
- El job exige separar diagnostico de indicacion y evitar inferencias quirurgicas no dictadas.
- Los bugs prioritarios son de seguridad semantica: inventar abordajes, lateralidad, diagnosticos o pasos quirurgicos puede producir documentos clinicos falsos.

## checklist de integracion local

1. Crear rama y snapshot limpio en work-mac.
2. Revisar el flujo actual de generacion de documento clinico y ubicar el punto unico de normalizacion antes de redactar.
3. Integrar route guard canonico antes de cualquier mejora de estilo.
4. Agregar fixtures lumbares negativas y positivas.
5. Agregar gates deterministicos que fallen antes de generar o guardar texto clinico.
6. Ejecutar QA regression completa.
7. Validar manualmente 7 casos criticos con salida final visible.
8. Commit por capa: route guard, fixtures, gates, QA.

## archivos probables

```text
app/product.html
app/app.js
scripts/jarvis/clinical_document_handoff.js
scripts/qa/validate_clinical_inconsistency_audit.js
scripts/qa/validate_20_pathology_scenarios.js
scripts/qa/validate_clinica_route_guard.js
data/derived/clinical_test_cases/lumbar_gates_v1.json
data/derived/clinical_test_cases/lumbar_negative_assertions_v1.json
```

## gates obligatorios

- Extradural/extraforaminal no debe convertirse en interlaminar si no fue indicado.
- No inventar hernia posterolateral o PL cuando la entrada no la trae.
- No agregar descompresion directa si el caso explicita que no se realizo.
- Mantener diagnostico separado de indicacion quirurgica.
- Artrodesis L4-L5 no debe agregar lateralidad si no fue dictada.
- Hemostasia y recuento deben aparecer antes del cierre.
- No duplicar diagnosticos, niveles, abordajes ni pasos.
- Todo agregado inferido debe quedar bloqueado o marcado como `needs_review`, no como hecho clinico.

## orden de cambios recomendado

### 1. Route guard

Crear una capa unica tipo `normalizeClinicalRoute(input) -> route`. Debe devolver:

```json
{
  "diagnosis": [],
  "indication": [],
  "approach": null,
  "levels": [],
  "laterality": null,
  "direct_decompression": null,
  "requires_review": [],
  "negative_assertions": []
}
```

Regla: si un campo no existe en el input, queda `null` o vacio. Nunca se completa por costumbre quirurgica.

### 2. Fixtures

Agregar fixtures de regresion con input breve, expected positives y forbidden phrases. Cada fixture debe incluir `source_sentence`, `expected_present`, `forbidden_present`, `risk_level` y `doctor_bug_id`.

### 3. Gates deterministicos

Antes de renderizar:

- `forbidden_present` falla hard.
- Campo clinico inferido sin fuente falla hard.
- Inconsistencia entre diagnostico e indicacion falla hard.
- Ausencia de hemostasia/recuento antes de cierre falla hard.
- Duplicado exacto o semantico de nivel/diagnostico falla hard.

### 4. QA

Agregar un comando unico de regresion local:

```bash
node scripts/qa/validate_clinica_route_guard.js
node scripts/qa/validate_clinical_inconsistency_audit.js
node scripts/qa/validate_20_pathology_scenarios.js
```

## criterios de aceptacion

- Los 7 bugs prioritarios fallan con la version vieja y pasan con el patch.
- El documento final no contiene frases prohibidas en fixtures.
- Cada frase clinica relevante puede rastrearse a una fuente de entrada.
- Si falta fuente, el sistema pide revision en vez de completar.
- No hay cambios de copy general mezclados con gates clinicos.

## rollback

- Si falla route guard: revertir solo commit `route guard`.
- Si fallan fixtures: mantener route guard y revertir fixture conflictivo.
- Si fallan gates por falsos positivos: degradar ese gate a `needs_review` solo si bloquea casos reales confirmados.
- Si se detecta texto clinico inventado: rollback total del batch clinico y congelar generacion automatica hasta revision.

## riesgos medico-legales

- Mayor riesgo: documento operatorio con hechos no realizados.
- Riesgo alto: lateralidad o nivel agregado por inferencia.
- Riesgo alto: mezclar diagnostico con indicacion y alterar causalidad.
- Riesgo medio: duplicados que generen ambiguedad.
- Mitigacion: negative assertions, trazabilidad por fuente, gates antes del render final.

## recommendation

Integrar en work-mac solo como patch clinico aislado, sin mezclar UI ni refactors. La primera prueba debe ser extraforaminal sin interlaminar porque detecta el error mas peligroso: completar una via quirurgica no indicada.

## confidence

High. La prioridad ya esta documentada en `decisions/clinica_patch_proposals_v1` y los criterios del Doctor son suficientemente concretos para fixtures deterministas.

## evidence_paths

- `decisions/clinica_patch_proposals_v1/README.md`
- `decisions/clinica_patch_proposals_v1/route_guard.diff.md`
- `decisions/clinica_patch_proposals_v1/lumbar_fixtures.json`
- `decisions/clinica_patch_proposals_v1/deterministic_gates.diff.md`
- `decisions/clinica_patch_proposals_v1/qa_changes.md`
- `jobs/20260525T084316-clinica-integration-checklist-route-guard-fixtures-v2.md`
