---
id: 20260525T015334-clinica-app-snapshot-auditoria-integral-v1
job_id: 20260525T015334-clinica-app-snapshot-auditoria-integral-v1
created_at: 2026-05-25T01:59:19-03:00
created_by: personal-xh
status: completed
no_external_actions: true
no_secrets: true
---

# clinica app snapshot auditoria integral v1 result

## summary

Snapshot descomprimido en `tmp/clinica_app_snapshot_review/`. La app tiene una base madura: ruta canonica con redaction shield, QA core/full, corpus legal y matriz de familias. El riesgo principal es drift entre rutas/generadores, y que fuentes secundarias o artefactos stale se promuevan sin trazabilidad oficial.

## findings

### P1 - Ruta no canonica conserva generador lumbar inseguro

- Evidencia: `tmp/clinica_app_snapshot_review/app/app.js` genera microdiscectomia lumbar con "Abordaje interlaminar", "flavectomia" y "fragmento discal" de forma fija.
- Riesgo: si esa ruta se usa fuera de QA/demo, puede reintroducir el bug de hernia extraforaminal o inventar hernia/topografia.
- Propuesta: declarar `app/product.html` + `scripts/jarvis/clinical_document_handoff.js` como ruta canonica; bloquear envio desde `app/app.js` o pasarlo por el mismo redaction shield.
- Test: fixture extraforaminal L4-L5 derecha debe fallar en cualquier ruta que emita interlaminar/flavectomia.

### P1 - Corpus mezcla estados de confiabilidad

- Evidencia: `jurisprudence_neuro_spine_corpus_latest.json` tiene 19 records con estados como `official_judiciary_full_text`, `official_saij_summary`, `secondary_full_text_pending_official_copy` y `official_pending_merits_non_precedential`.
- Riesgo: convertir candidatos secundarios en gates fuertes antes de obtener copia oficial.
- Propuesta: gates activos solo desde `official_judiciary_full_text` u `official_saij_summary` revisado; secundarios quedan como cola.
- Test: secret/gate build debe fallar si `source_status=secondary_pending_official` intenta `status=active`.

### P1 - Falta claim/ownership en bridge previo al snapshot operativo

- Evidencia: el bridge listaba por resultado faltante, sin `claims/`.
- Riesgo: doble procesamiento si hay varios workers.
- Propuesta: implementado en este batch con `claims/<job_id>.json`.

### P2 - Snapshot incluye logs/cache y rutas absolutas de work-mac

- Evidencia: `state/app_server.err.log`, `state/app_server.out.log`, `scripts/exports/__pycache__/`, `scripts/launchd/ai.clinica.app-local.plist` con `/Users/jarvis/...`.
- Riesgo: ruido, rutas no portables y posible fuga accidental de contexto operativo.
- Propuesta: empaquetador de snapshot debe excluir `state/*.log`, `__pycache__`, `.pid` y mantener un manifest de rutas canonicas.

### P2 - QA pasa, pero debe probar bugs reales como regression fixtures

- Evidencia: `clinica_core_qa_latest.md` y `clinica_full_qa_latest.md` estan OK; `validate_20_pathology_scenarios.js` ya cubre extraforaminal.
- Riesgo: casos reales del Dr. Zanardi quedan como comentario si no entran a fixtures.
- Propuesta: agregar `lumbar_gates_v1.json` con casos de no invencion, extraforaminal, sin descompresion directa, lateralidad artrodesis y cierre.

## recommendation

Integrar primero route guard canonico + fixtures lumbares. Luego promover corpus a gates solo con `source_status` y revision.

## confidence

Alta para arquitectura/QA. Media para evaluacion clinica fina sin ejecutar la app real.

## evidence_paths

- `tmp/clinica_app_snapshot_review/app/app.js`
- `tmp/clinica_app_snapshot_review/app/product.html`
- `tmp/clinica_app_snapshot_review/scripts/jarvis/clinical_document_handoff.js`
- `tmp/clinica_app_snapshot_review/qa/approval_gates/clinica_core_qa_latest.md`
- `tmp/clinica_app_snapshot_review/qa/approval_gates/clinica_full_qa_latest.md`
- `tmp/clinica_app_snapshot_review/data/derived/jurisprudence_neuro_spine/jurisprudence_neuro_spine_corpus_latest.json`
