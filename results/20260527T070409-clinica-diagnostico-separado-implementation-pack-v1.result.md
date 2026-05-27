---
job_id: 20260527T070409-clinica-diagnostico-separado-implementation-pack-v1
worker: personal-xh
status: completed
completed_at: 2026-05-27T07:05:30-03:00
front: CLINICA
no_external_actions: true
no_secrets: true
---

# Resultado - Clinica diagnostico separado implementation pack v1

## summary

Implementation pack de bajo riesgo para integrar
`diagnostico_separado_de_indicacion` como gate documental P0
detect-only/report-only. La implementacion debe agregar fixtures sinteticos y un
validator puro, sin tocar plantillas finales ni convertir el gate en bloqueo de
documento real.

Evidencia: `context/fronts/clinica.md` exige convertir correcciones del Doctor en
reglas/fixtures/gates y lista "diagnostico separado de indicacion" como gate
documental. El resultado previo
`results/20260527T063553-clinica-next-documental-p0-gate-plan-v1.result.md`
recomienda este gate como candidato unico. Inferencia: el paquete debe ser
estrecho por secciones para evitar falsos positivos. Opinion: el valor esta en
fallar QA sintetico cuando el diagnostico contiene plan terapeutico, no en
opinar sobre legalidad.

## coverage_table

| Fuente | Estado | Uso |
| --- | --- | --- |
| `jobs/20260527T070409-clinica-diagnostico-separado-implementation-pack-v1.md` | Revisada | Workorder, limites y entregables. |
| `results/20260527T063553-clinica-next-documental-p0-gate-plan-v1.result.md` | Revisada | Gate, contrato JSON, fixtures y controles de falsos positivos. |
| `context/fronts/clinica.md` | Revisada | Canon CLINICA, ruta canonica y regla de no tocar plantillas sin QA focal. |

## findings

| Item | Decision | Evidencia | Implementacion sugerida |
| --- | --- | --- | --- |
| Alcance | Detect-only/report-only. | Frente CLINICA pide QA medico-legal y el plan previo prohibe bloqueo real inicial. | Validator emite JSON y falla solo fixtures sinteticos. |
| Activacion | Solo seccion/campo diagnostico. | El riesgo principal del plan previo es falso positivo fuera de diagnostico. | Segmentar por headings y evaluar `diagnostico|diagnosis|dx`. |
| Regex | Lista corta de indicadores terapeuticos. | Plan previo enumera `se indica`, `con indicacion de`, `requiere`, `se programa`, `candidato a`, `tratamiento quirurgico`. | Mantener lista acotada y crecer solo con fixtures. |
| Resultado ambiguo | `needs_review`, no `fail`. | El frente separa evidencia, inferencia y corpus; no inventar normativa. | Si falta seccion diagnostico o hay antecedente historico, reportar revision. |

## fixture_json_structure

Archivo sugerido:
`data/derived/clinical_test_cases/documental_p0_gates_v1.json`.

```json
{
  "schema": "documental_p0_gates_v1",
  "source_boundary": "internal_documental_rule",
  "mode": "detect_only",
  "fixtures": [
    {
      "fixture_id": "CLIN-DOC-DX-005-indication-in-diagnosis",
      "gate_id": "diagnostico_separado_de_indicacion",
      "expected_status": "fail",
      "document_type": "historia_clinica",
      "source_fields": {
        "diagnosis": "hernia L4-L5 derecha",
        "indication": "microdiscectomia L4-L5 derecha",
        "procedure": "microdiscectomia L4-L5 derecha"
      },
      "rendered_text": "Diagnostico: hernia L4-L5 derecha con indicacion de microdiscectomia.",
      "expected_findings": [
        {
          "severity": "fail",
          "matched_pattern": "con indicacion de",
          "evidence_path": "$.rendered_text"
        }
      ]
    },
    {
      "fixture_id": "CLIN-DOC-DX-006-requires-surgery-in-diagnosis",
      "gate_id": "diagnostico_separado_de_indicacion",
      "expected_status": "fail",
      "document_type": "consentimiento",
      "source_fields": {
        "diagnosis": "canal estrecho lumbar",
        "indication": "descompresion"
      },
      "rendered_text": "Diagnostico: canal estrecho lumbar que requiere descompresion quirurgica.",
      "expected_findings": [
        {
          "severity": "fail",
          "matched_pattern": "requiere",
          "evidence_path": "$.rendered_text"
        }
      ]
    },
    {
      "fixture_id": "CLIN-DOC-DX-007-separated-pass",
      "gate_id": "diagnostico_separado_de_indicacion",
      "expected_status": "pass",
      "document_type": "historia_clinica",
      "source_fields": {
        "diagnosis": "hernia L4-L5 derecha",
        "indication": "microdiscectomia L4-L5 derecha"
      },
      "rendered_text": "Diagnostico: hernia L4-L5 derecha.\nIndicacion: microdiscectomia L4-L5 derecha.",
      "expected_findings": []
    },
    {
      "fixture_id": "CLIN-DOC-DX-008-negated-pass",
      "gate_id": "diagnostico_separado_de_indicacion",
      "expected_status": "pass",
      "document_type": "historia_clinica",
      "source_fields": {
        "diagnosis": "hernia L4-L5 derecha",
        "indication": null
      },
      "rendered_text": "Diagnostico: hernia L4-L5 derecha. No se consigna indicacion dentro del diagnostico.",
      "expected_findings": []
    }
  ]
}
```

## pseudocode_regex

Pseudocodigo acotado:

```javascript
const GATE_ID = "diagnostico_separado_de_indicacion";

const DIAGNOSIS_HEADINGS = /^(diagnostico|diagnosis|dx)\s*[:.-]?\s*/i;
const STOP_HEADINGS = /^(indicacion|plan|procedimiento|tecnica|tratamiento|antecedentes|evolucion|consentimiento)\s*[:.-]?\s*/i;
const THERAPEUTIC_MARKERS = [
  /\bcon\s+indicacion\s+de\b/i,
  /\bse\s+indica\b/i,
  /\brequiere\b/i,
  /\bse\s+programa\b/i,
  /\bcandidato\s+a\b/i,
  /\btratamiento\s+quirurgico\b/i,
  /\bcirugia\s+indicada\b/i
];
const NEGATED_MARKERS = [
  /\bno\s+se\s+consigna\s+indicacion\b/i,
  /\bsin\s+indicacion\s+terapeutica\b/i,
  /\bno\s+se\s+indica\b/i
];

function validateDiagnosticoSeparado(caseInput) {
  const text = normalizeWhitespace(caseInput.rendered_text || "");
  const segments = splitByKnownHeadings(text);
  const diagnosisSegments = segments.filter(s => DIAGNOSIS_HEADINGS.test(s.heading));

  if (diagnosisSegments.length === 0) {
    return needsReview("diagnosis_section_missing", "$.rendered_text");
  }

  const findings = [];
  for (const segment of diagnosisSegments) {
    const body = segment.body;
    if (NEGATED_MARKERS.some(rx => rx.test(body))) continue;
    for (const rx of THERAPEUTIC_MARKERS) {
      const match = body.match(rx);
      if (match) {
        findings.push({
          gate_id: GATE_ID,
          status: "fail",
          severity: "fail",
          evidence_path: "$.rendered_text",
          matched_text: clipAround(body, match.index, 140),
          local_context: segmentToContext(segment),
          source_boundary: "internal_documental_rule",
          reason: "El diagnostico mezcla indicacion terapeutica.",
          recommendation: "Separar Diagnostico e Indicacion en secciones distintas."
        });
      }
    }
  }
  return findings.length ? fail(findings) : pass();
}
```

Notas de implementacion:

- `splitByKnownHeadings` debe cortar en headings conocidos; no evaluar todo el
  documento como diagnostico.
- Si existe `source_fields.diagnosis`, tambien puede validarse ese campo como
  fuente primaria y usar `rendered_text` para evidencia.
- `fail` significa fail de QA sintetico; para documentos reales iniciales usar
  reporte y revision del orquestador.

## false_positives_to_test

| Caso frontera | Esperado | Motivo |
| --- | --- | --- |
| `Diagnostico: hernia. Indicacion: microdiscectomia.` | `pass` | Separacion correcta por heading. |
| `Diagnostico: hernia. No se consigna indicacion dentro del diagnostico.` | `pass` | Negacion local/metadocumental. |
| `Antecedentes: se habia indicado cirugia en otro centro. Diagnostico: hernia.` | `pass` o `needs_review` | Marcador terapeutico fuera de diagnostico. |
| `Diagnostico probable: dolor lumbar. Plan: evaluar indicacion quirurgica.` | `pass` | Plan separado. |
| `Diagnostico: canal estrecho; requiere correlacion con imagenes.` | `needs_review` | `requiere` no siempre es indicacion quirurgica. |
| `Consentimiento: acepto tratamiento quirurgico. Diagnostico: hernia L4-L5.` | `pass` para este gate | El tratamiento esta fuera del segmento diagnostico. |
| Documento sin heading diagnostico pero con texto clinico libre. | `needs_review` | No hard fail por parseo incompleto. |

## severities_detect_only

| Severidad | Cuando usar | Efecto inicial |
| --- | --- | --- |
| `fail` | Marcador terapeutico afirmado dentro de seccion diagnostico en fixture sintetico. | Falla validator/QA del fixture. |
| `needs_review` | Falta seccion diagnostico, marcador ambiguo o parseo dudoso. | Reporta al orquestador; no bloquea documento real. |
| `advisory` | Mejora de estilo o estructura sin riesgo documental claro. | Informativo. |
| `pass` | Secciones separadas, negaciones locales o marcador fuera de diagnostico. | Sin findings. |

## rg_commands

Comandos para que el orquestador ubique integracion real en la app canonica:

```bash
rg -n "clinical_p0|documental_p0|p0_gates|validate_.*gates|run_clinica_core_qa" /Users/jarvis/.openclaw/workspace/clinica/app-clinica-medicolegal
rg -n "diagnostico|diagnosis|indicacion|indication|procedure|rendered_text|document_type" /Users/jarvis/.openclaw/workspace/clinica/app-clinica-medicolegal
rg -n "clinical_test_cases|derived|fixtures|expected_status|expected_findings" /Users/jarvis/.openclaw/workspace/clinica/app-clinica-medicolegal
rg -n "normalize|segment|heading|negacion|negation|matched_text|local_context" /Users/jarvis/.openclaw/workspace/clinica/app-clinica-medicolegal/scripts
```

## qa_commands

QA focal sugerido:

```bash
node -c scripts/qa/validate_documental_p0_gates_v1.js
node scripts/qa/validate_documental_p0_gates_v1.js --fixture data/derived/clinical_test_cases/documental_p0_gates_v1.json --gate diagnostico_separado_de_indicacion
```

QA de no regresion clinica:

```bash
node -c scripts/qa/validate_clinical_p0_gates_v1.js
node scripts/qa/validate_clinical_p0_gates_v1.js
node scripts/qa/run_clinica_core_qa.js
```

Contrato bridge:

```bash
python3 scripts/validate_result_contract.py results/20260527T070409-clinica-diagnostico-separado-implementation-pack-v1.result.md
git diff --check
python3 scripts/secret_scan.py
```

## attempted_routes

- Se hizo `git pull --rebase`.
- Se reclamo el job con `python3 scripts/bridgectl.py claim`.
- Se reviso `jobs/20260527T070409-clinica-diagnostico-separado-implementation-pack-v1.md`.
- Se reviso el plan previo
  `results/20260527T063553-clinica-next-documental-p0-gate-plan-v1.result.md`.
- Se reviso `context/fronts/clinica.md`.
- No se abrio ObraCash, Drive, iCloud, Gmail, Photos, Downloads ni acciones
  externas.
- No se tocaron plantillas finales ni app canonica real.

## risks_limits

- El pack es portable y de bajo riesgo; no valida rutas reales hasta que el
  orquestador inspeccione la app canonica.
- No usa normativa externa; por eso el gate queda como regla documental interna.
- Regex demasiado amplio puede marcar plan/consentimiento como diagnostico; la
  segmentacion por headings es obligatoria.
- `requiere` es ambiguo; si aparece sin cirugia/procedimiento cercano, conviene
  `needs_review` antes de `fail`.

## recommendation

Proxima accion unica: integrar los cuatro fixtures sinteticos y un validator
`validate_documental_p0_gates_v1.js` detect-only para
`diagnostico_separado_de_indicacion`, conectado al core QA solo como reporte.
No tocar plantillas finales y no bloquear documentos reales hasta pasar QA focal,
QA core y revision del orquestador.

## confidence

Media-alta para el contrato, fixtures y regex acotada porque derivan del plan
previo y del frente CLINICA. Media para nombres/rutas exactas hasta que el
orquestador localice validators reales en la app canonica.

## evidence_paths

- `jobs/20260527T070409-clinica-diagnostico-separado-implementation-pack-v1.md`
- `results/20260527T063553-clinica-next-documental-p0-gate-plan-v1.result.md`
- `context/fronts/clinica.md`
- `claims/20260527T070409-clinica-diagnostico-separado-implementation-pack-v1.json`
