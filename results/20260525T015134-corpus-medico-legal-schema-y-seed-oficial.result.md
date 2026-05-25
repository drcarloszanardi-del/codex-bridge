---
id: 20260525T015134-corpus-medico-legal-schema-y-seed-oficial
job_id: 20260525T015134-corpus-medico-legal-schema-y-seed-oficial
created_at: 2026-05-25T01:59:19-03:00
created_by: personal-xh
status: completed
no_external_actions: true
no_secrets: true
---

# corpus medico legal schema y seed oficial result

## summary

Schema propuesto para separar fuente oficial, revision y gate derivado. La app no deberia consumir fallos/normas directamente: debe consumir `gate_item` revisados.

## folders

```text
data/corpus/items/normative/
data/corpus/items/jurisprudence/
data/corpus/items/doctrine/
data/corpus/gates/
data/corpus/review_queue/
data/corpus/indexes/
```

## corpus_item schema

```json
{
  "id": "norm_ley_26529_infoleg",
  "type": "norm|case|doctrine|internal",
  "jurisdiction": "AR|PBA|CABA|RN|...",
  "official_url": "https://...",
  "alternate_urls": [],
  "source_status": "official|secondary_pending_official|internal|discarded",
  "title": "...",
  "court_or_body": "...",
  "date": "YYYY-MM-DD",
  "topics": ["consentimiento", "historia_clinica"],
  "relevant_criteria": [],
  "app_impact": [],
  "review_status": "seed|needs_review|approved_for_gate|rejected",
  "reviewer": "orchestrator|doctor|legal_advisor",
  "sha256": "...",
  "notes": ""
}
```

## gate_item schema

```json
{
  "id": "gate_consentimiento_especifico_columna_v1",
  "derived_from": ["norm_ley_26529_infoleg", "case_juba_161074"],
  "domain": "consentimiento|historia_clinica|parte_quirurgico|evolucion",
  "severity": "critical|high|medium|low",
  "condition": "procedimiento_columna_programado == true",
  "must_include": ["diagnostico", "procedimiento", "nivel", "riesgos especificos", "alternativas", "revocacion"],
  "must_not_include": ["citas legales en documento clinico final"],
  "test_cases": [],
  "status": "draft|approved|active|deprecated"
}
```

## seed oficial

- Ley 26.529 Derechos del Paciente, Historia Clinica y Consentimiento Informado: https://servicios.infoleg.gob.ar/infolegInternet/anexos/160000-164999/160432/texact.htm
- Decreto 1089/2012 reglamentario de Ley 26.529: https://servicios.infoleg.gob.ar/infolegInternet/anexos/195000-199999/199296/norma.htm
- Ley 25.326 Proteccion de Datos Personales: https://servicios.infoleg.gob.ar/infolegInternet/anexos/60000-64999/64790/texact.htm
- Codigo Civil y Comercial Ley 26.994: https://servicios.infoleg.gob.ar/infolegInternet/anexos/235000-239999/235975/texact.htm
- Ley 17.132 ejercicio de la medicina: https://servicios.infoleg.gob.ar/infolegInternet/anexos/15000-19999/19429/texact.htm
- Ley PBA 14.494 Historia Clinica Electronica Unica: https://normas.gba.gob.ar/ar-b/ley/2013/14494/11338
- Decreto PBA 1600/2024 reglamentario Ley 14.494: https://normas.gba.gob.ar/ar-b/decreto/2024/1600/451942
- SAIJ dossier Mala Praxis Medica: https://www.saij.gob.ar/dossier
- JUBA texto completo, consentimiento informado: https://juba.scba.gov.ar/VerTextoCompleto.aspx?idFallo=161074
- JUBA texto completo, historia clinica como prueba: https://juba.scba.gov.ar/VerTextoCompleto.aspx?idFallo=25519

## criterios

- Fuente oficial obligatoria para gate fuerte.
- Fuente secundaria solo entra como `secondary_pending_official`.
- Cada fuente debe producir gate, plantilla o cola de revision; si no produce control verificable, queda como nota no operacional.

## recommendation

Implementar primero el schema y migrar el corpus actual a `source_status`. Despues activar gates solo desde items `approved_for_gate`.

## confidence

Media-alta. URLs oficiales iniciales verificadas parcialmente; requiere revision legal antes de produccion.

## evidence_paths

- `jobs/20260525T015134-corpus-medico-legal-schema-y-seed-oficial.md`
- `tmp/clinica_app_snapshot_review/data/raw/legal/manifest_2026-05-24.json`
- `tmp/clinica_app_snapshot_review/data/processed/legal_corpus/index_latest.json`
