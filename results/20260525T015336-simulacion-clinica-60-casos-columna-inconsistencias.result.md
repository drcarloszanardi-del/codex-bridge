---
id: 20260525T015336-simulacion-clinica-60-casos-columna-inconsistencias
job_id: 20260525T015336-simulacion-clinica-60-casos-columna-inconsistencias
created_at: 2026-05-25T01:59:19-03:00
created_by: personal-xh
status: completed
no_external_actions: true
no_secrets: true
---

# simulacion clinica 60 casos columna inconsistencias result

## summary

Se propone pack de 60 casos sinteticos para historia clinica, consentimiento y parte quirurgico. El archivo JSON-like queda en `results/20260525T015336-simulacion-clinica-60-casos-columna-inconsistencias.cases.json`.

## coverage

- Hernia extraforaminal, foraminal, posterolateral y topografia no informada.
- Canal estrecho, espondilolistesis, fijacion MISS/Wiltse, TLIF/PLIF.
- Casos con y sin descompresion directa.
- Implantes, parche dural, durotomia, hemostasia/recuento/cierre.
- Consentimiento y documentacion medico-legal.

## recommendation

Importar este pack como fixtures. Cada caso debe tener salida esperada, errores prohibidos, severidad y gate responsable.

## confidence

Alta como set sintetico inicial; requiere ajuste por Dr. Zanardi antes de convertirlo en suite clinica definitiva.

## evidence_paths

- `results/20260525T015336-simulacion-clinica-60-casos-columna-inconsistencias.cases.json`
- `tmp/clinica_app_snapshot_review/scripts/qa/validate_20_pathology_scenarios.js`
- `tmp/clinica_app_snapshot_review/scripts/qa/validate_40_pathology_family_matrix.js`
