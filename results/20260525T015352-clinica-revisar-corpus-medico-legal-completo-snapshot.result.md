---
id: 20260525T015352-clinica-revisar-corpus-medico-legal-completo-snapshot
job_id: 20260525T015352-clinica-revisar-corpus-medico-legal-completo-snapshot
created_at: 2026-05-25T01:59:19-03:00
created_by: personal-xh
status: completed
no_external_actions: true
no_secrets: true
---

# clinica revisar corpus medico legal completo snapshot result

## summary

El corpus actual ya contiene normativa, doctrina interna, SAIJ, jurisprudencia Rio Negro/JUBA y matrices de impacto. Lo mas flojo es la promocion: necesita estado formal de fuente, revision y gate derivado antes de impactar plantillas.

## mapa actual

- `data/raw/legal`: normas Infoleg/Argentina/GBA, Ley 26.529, datos personales, firma digital, historia clinica electronica.
- `data/raw/jurisprudence`: semillas SAIJ sobre consentimiento, historia clinica, responsabilidad medica y negligencia quirurgica.
- `data/processed/legal_corpus`: indices y candidatos; `index_latest.json` reporta 7 fuentes normativas, 20 candidatos jurisprudenciales, 1 doctrina y 2 internas.
- `data/derived/jurisprudence_neuro_spine`: corpus neuro/columna con 19 records, 6 impact rules.
- `docs/corpus_medicolegal_argentino.md` y matrices: narrativa y reglas redaccionales.

## gates existentes o cercanos

- Nivel/lateralidad/raiz/control por imagen.
- Consentimiento especifico.
- Parte quirurgico reconstruible.
- Historia clinica completa y util para pericia.
- No citas legales en documento final.
- Tamiz de lenguaje vago y placeholders.

## flojo / duplicado

- Varias fuentes son `secondary_full_text_pending_official_copy`; utiles como candidatos, no como gates fuertes.
- Hay duplicacion entre docs narrativos, `impact_matrix_latest.md` y scripts de corpus.
- El snapshot incluye logs/cache que no aportan al corpus.

## falta buscar

- CSJN/CIJ con texto completo o sentencia asociada sobre consentimiento/historia clinica.
- SCBA/JUBA especifico sobre consentimiento informado y completitud de historia clinica en actos quirurgicos.
- Fallos oficiales provinciales con columna/neurocirugia y documentacion operatoria.
- Normativa PBA vigente de historia clinica electronica y consentimiento en establecimientos.

## actions

1. Migrar cada item a `corpus_item`.
2. Marcar `source_status`.
3. Crear `gate_item` solo para hallazgos verificables.
4. Mantener secundarios en `review_queue`.
5. Testear que documento clinico final no cite leyes/fallos.

## confidence

Alta sobre estructura del snapshot; media sobre exhaustividad juridica.

## evidence_paths

- `tmp/clinica_app_snapshot_review/data/raw/legal/manifest_2026-05-24.json`
- `tmp/clinica_app_snapshot_review/data/processed/legal_corpus/index_latest.json`
- `tmp/clinica_app_snapshot_review/data/derived/jurisprudence_neuro_spine/jurisprudence_neuro_spine_corpus_latest.json`
- `tmp/clinica_app_snapshot_review/docs/contrato_blindaje_redaccion_medicolegal_2026-05-24.md`
