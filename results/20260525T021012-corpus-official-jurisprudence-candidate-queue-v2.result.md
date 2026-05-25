---
id: 20260525T021012-corpus-official-jurisprudence-candidate-queue-v2
job_id: 20260525T021012-corpus-official-jurisprudence-candidate-queue-v2
created_at: 2026-05-25T03:51:15-03:00
created_by: personal-xh
status: completed
no_external_actions: true
no_secrets: true
---

# corpus official jurisprudence candidate queue v2 result

## summary

Cola oficial creada con normas, JUBA, CIJ, SAIJ y Fallos Rio Negro. Se usaron fuentes publicas oficiales y no se copiaron textos largos.

## findings

- La cola separa `official_norm`, `official_judiciary_full_text`, `official_judiciary_pdf` y `official_saij_summary`.
- Cada candidato incluye posible gate derivado y si requiere copia completa.

## recommendation

Work-mac debe convertir candidatos aprobados en `corpus_item` y solo despues en `gate_item`.

## confidence

Media-alta.

## evidence_paths

- `decisions/corpus_official_candidate_queue_20260525.md`
- `tmp/clinica_app_snapshot_review/data/derived/jurisprudence_neuro_spine/jurisprudence_neuro_spine_corpus_latest.json`
