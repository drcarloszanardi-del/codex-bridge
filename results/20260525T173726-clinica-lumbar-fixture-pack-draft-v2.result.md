---
id: 20260525T173726-clinica-lumbar-fixture-pack-draft-v2
job_id: 20260525T173726-clinica-lumbar-fixture-pack-draft-v2
created_at: 2026-05-25T17:41:08-03:00
created_by: personal-xh
worker: personal-xh
status: completed
no_external_actions: true
no_secrets: true
---

# Resultado - CLINICA lumbar fixture pack draft v2

## summary

Draft implementable de fixtures lumbares v2 para que Codex principal lo materialice en la app clinica canonica sin tocar pacientes ni datos reales. El pack convierte los gates ya definidos en 16 casos sinteticos con ejes de entrada, presencia esperada, presencia prohibida, severidad y mensaje esperado.

La idea operativa es simple: primero agregar fixtures y validator detect-only; luego hacerlos fallar contra textos malos conocidos; recien despues conectar al generador real y activar hard fail en critical/high con baja tasa de falso positivo.

## coverage_table

| Fuente permitida | Estado | Uso |
|---|---:|---|
| `results/20260525T153318-clinica-lumbar-inconsistency-gates-v2.result.md` | Revisada | Matriz de gates, ejes canonicos, frases prohibidas y mensajes de falla. |
| `results/20260525T170711-clinica-corpus-official-gates-next-integration-v1.result.md` | Revisada | Priorizacion P0, integracion con corpus oficial y batch minimo. |
| `context/fronts/clinica.md` | Revisada | Ruta canonica y regla de no tocar app real sin baseline/test focal. |

## fixture_schema

Schema recomendado para `data/derived/clinical_test_cases/lumbar_inconsistency_gates_v2.json`:

```json
{
  "pack_id": "lumbar_inconsistency_gates_v2",
  "version": 2,
  "source": "bridge_personal_xh_synthetic_fixtures",
  "cases": [
    {
      "id": "LUM-GATE-001",
      "title": "short_case_title",
      "document_type": "historia_clinica|consentimiento|parte_quirurgico",
      "severity": "critical|high|medium",
      "source_type": "synthetic_doctor_correction_fixture",
      "input_axes": {
        "diagnosis_family": "hernia|estenosis_canal|espondilolistesis|otro",
        "subtype": "extraforaminal|foraminal|degenerativa|not_informed|null",
        "level": "L4-L5",
        "laterality": "derecha|izquierda|bilateral|not_informed|not_applicable",
        "procedure_family": "microdiscectomia|fijacion_artrodesis|PLIF|TLIF|descompresion|otro",
        "direct_decompression": "yes|no|not_informed",
        "dural_patch": "yes|no|not_informed"
      },
      "expected_present": ["normalized phrase or semantic token"],
      "forbidden_present": ["normalized phrase or semantic token"],
      "gate_ids": ["validator_gate_id"],
      "expected_message": "validator failure message",
      "notes": "no patient data; synthetic only"
    }
  ]
}
```

## fixtures_json_draft

```json
{
  "pack_id": "lumbar_inconsistency_gates_v2",
  "version": 2,
  "description": "Synthetic lumbar fixtures for clinical/medicolegal QA gates. No patient data.",
  "cases": [
    {
      "id": "LUM-GATE-001",
      "title": "extraforaminal_l45_right_no_interlaminar_root_l4",
      "document_type": "parte_quirurgico",
      "severity": "critical",
      "source_type": "synthetic_doctor_correction_fixture",
      "input_axes": {
        "diagnosis_family": "hernia",
        "subtype": "extraforaminal",
        "level": "L4-L5",
        "laterality": "derecha",
        "procedure_family": "microdiscectomia",
        "approach": "extraforaminal",
        "direct_decompression": "not_informed",
        "dural_patch": "not_informed"
      },
      "expected_present": ["abordaje extraforaminal", "raiz L4 derecha"],
      "forbidden_present": ["abordaje interlaminar", "flavectomia", "receso lateral", "hombro de raiz", "raiz L5 derecha"],
      "gate_ids": ["extraforaminal_no_interlaminar", "extraforaminal_root_table"],
      "expected_message": "Hernia extraforaminal documentada con abordaje, secuencia o raiz incompatible.",
      "notes": "Synthetic only."
    },
    {
      "id": "LUM-GATE-002",
      "title": "no_inventar_topografia_si_no_declarada",
      "document_type": "historia_clinica",
      "severity": "critical",
      "source_type": "synthetic_doctor_correction_fixture",
      "input_axes": {
        "diagnosis_family": "hernia",
        "subtype": "not_informed",
        "level": "L4-L5",
        "laterality": "derecha",
        "procedure_family": "not_informed",
        "direct_decompression": "not_informed",
        "dural_patch": "not_informed"
      },
      "expected_present": ["hernia L4-L5 derecha"],
      "forbidden_present": ["posterolateral", "extraforaminal", "foraminal", "fragmento discal", "secuestro"],
      "gate_ids": ["no_inventar_diagnostico_topografia"],
      "expected_message": "La salida inventa topografia o hallazgo no informado.",
      "notes": "No inferir subtipo si el input no lo declara."
    },
    {
      "id": "LUM-GATE-003",
      "title": "radiculopatia_sin_hernia_no_inventa_hernia",
      "document_type": "historia_clinica",
      "severity": "critical",
      "source_type": "synthetic_doctor_correction_fixture",
      "input_axes": {
        "diagnosis_family": "radiculopatia",
        "subtype": "not_informed",
        "level": "not_informed",
        "laterality": "derecha",
        "affected_root": "L5",
        "procedure_family": "not_informed",
        "direct_decompression": "not_informed",
        "dural_patch": "not_informed"
      },
      "expected_present": ["radiculopatia L5 derecha"],
      "forbidden_present": ["hernia", "fragmento discal", "secuestro", "extrusion"],
      "gate_ids": ["no_inventar_diagnostico_topografia"],
      "expected_message": "La salida inventa diagnostico o hallazgo no informado.",
      "notes": "La raiz no autoriza inventar causa anatomica."
    },
    {
      "id": "LUM-GATE-004",
      "title": "espondilolistesis_degenerativa_no_istmica",
      "document_type": "historia_clinica",
      "severity": "high",
      "source_type": "synthetic_doctor_correction_fixture",
      "input_axes": {
        "diagnosis_family": "espondilolistesis",
        "subtype": "degenerativa",
        "level": "L4-L5",
        "laterality": "not_applicable",
        "procedure_family": "not_informed",
        "direct_decompression": "not_informed",
        "dural_patch": "not_informed"
      },
      "expected_present": ["espondilolistesis degenerativa L4-L5"],
      "forbidden_present": ["istmica", "pars", "lisis", "degenerativa o istmica"],
      "gate_ids": ["preservar_subtipo_espondilolistesis"],
      "expected_message": "El subtipo degenerativo fue mezclado con istmico.",
      "notes": "Preservar subtipo declarado."
    },
    {
      "id": "LUM-GATE-005",
      "title": "canal_estrecho_no_tautologico",
      "document_type": "historia_clinica",
      "severity": "medium",
      "source_type": "synthetic_doctor_correction_fixture",
      "input_axes": {
        "diagnosis_family": "estenosis_canal",
        "subtype": "not_applicable",
        "level": "L4-L5",
        "laterality": "not_applicable",
        "symptoms": ["claudicacion neurogena"],
        "procedure_family": "not_informed",
        "direct_decompression": "not_informed",
        "dural_patch": "not_informed"
      },
      "expected_present": ["estenosis de canal L4-L5", "claudicacion neurogena"],
      "forbidden_present": ["canal estrecho con compromiso del canal", "estenosis de canal con canal comprometido"],
      "gate_ids": ["canal_estrecho_no_tautologico"],
      "expected_message": "Redaccion tautologica de canal estrecho.",
      "notes": "Mejora calidad documental sin inventar hallazgos."
    },
    {
      "id": "LUM-GATE-006",
      "title": "diagnostico_puro_sin_indicacion",
      "document_type": "historia_clinica",
      "severity": "high",
      "source_type": "synthetic_doctor_correction_fixture",
      "input_axes": {
        "diagnosis_family": "espondilolistesis",
        "subtype": "degenerativa",
        "level": "L4-L5",
        "laterality": "not_applicable",
        "procedure_family": "fijacion_artrodesis",
        "direct_decompression": "not_informed",
        "dural_patch": "not_informed"
      },
      "expected_present": ["Diagnostico: espondilolistesis degenerativa L4-L5", "Indicacion quirurgica:"],
      "forbidden_present": ["diagnostico con indicacion de", "diagnostico requiere", "diagnostico se indica"],
      "gate_ids": ["diagnostico_puro_sin_indicacion"],
      "expected_message": "Diagnostico contaminado con indicacion o conducta.",
      "notes": "La indicacion debe ir en campo separado."
    },
    {
      "id": "LUM-GATE-007",
      "title": "fijacion_artrodesis_l45_sin_lateralidad_segmento",
      "document_type": "consentimiento",
      "severity": "high",
      "source_type": "synthetic_doctor_correction_fixture",
      "input_axes": {
        "diagnosis_family": "espondilolistesis",
        "subtype": "degenerativa",
        "level": "L4-L5",
        "laterality": "derecha",
        "procedure_family": "fijacion_artrodesis",
        "approach_laterality": "derecha",
        "direct_decompression": "not_informed",
        "dural_patch": "not_informed"
      },
      "expected_present": ["fijacion instrumentada y artrodesis L4-L5", "abordaje derecho"],
      "forbidden_present": ["fijacion L4-L5 derecha", "artrodesis L4-L5 derecha"],
      "gate_ids": ["segmento_fusion_sin_lateralidad"],
      "expected_message": "La fijacion o artrodesis es por segmento; mover lateralidad al abordaje, sintoma o descompresion.",
      "notes": "La lateralidad no modifica el segmento fusionado."
    },
    {
      "id": "LUM-GATE-008",
      "title": "sin_descompresion_directa_bloquea_laminectomia_flavectomia",
      "document_type": "parte_quirurgico",
      "severity": "critical",
      "source_type": "synthetic_doctor_correction_fixture",
      "input_axes": {
        "diagnosis_family": "espondilolistesis",
        "subtype": "degenerativa",
        "level": "L4-L5",
        "laterality": "not_applicable",
        "procedure_family": "fijacion_artrodesis",
        "direct_decompression": "no",
        "dural_patch": "not_informed"
      },
      "expected_present": ["no se realizo descompresion neural directa"],
      "forbidden_present": ["laminectomia", "hemilaminectomia", "flavectomia", "liberacion radicular directa", "recalibraje"],
      "gate_ids": ["sin_descompresion_directa_bloqueante"],
      "expected_message": "El caso declara sin descompresion directa y la salida describe una.",
      "notes": "Permitir menciones negadas; bloquear afirmativas."
    },
    {
      "id": "LUM-GATE-009",
      "title": "con_descompresion_directa_respeta_input",
      "document_type": "parte_quirurgico",
      "severity": "high",
      "source_type": "synthetic_doctor_correction_fixture",
      "input_axes": {
        "diagnosis_family": "estenosis_canal",
        "subtype": "not_applicable",
        "level": "L4-L5",
        "laterality": "bilateral",
        "procedure_family": "descompresion",
        "direct_decompression": "yes",
        "dural_patch": "not_informed"
      },
      "expected_present": ["descompresion directa documentada"],
      "forbidden_present": ["sin descompresion directa"],
      "gate_ids": ["respetar_input_descompresion"],
      "expected_message": "La salida contradice el input sobre descompresion directa.",
      "notes": "Control simetrico para no negar un acto informado."
    },
    {
      "id": "LUM-GATE-010",
      "title": "plif_implantes_no_duplicados",
      "document_type": "parte_quirurgico",
      "severity": "high",
      "source_type": "synthetic_doctor_correction_fixture",
      "input_axes": {
        "diagnosis_family": "espondilolistesis",
        "subtype": "degenerativa",
        "level": "L4-L5",
        "laterality": "not_applicable",
        "procedure_family": "PLIF",
        "interbody_technique": "PLIF",
        "implants": ["dos cajas", "sustituto oseo", "tornillos", "barras"],
        "direct_decompression": "yes",
        "dural_patch": "not_informed"
      },
      "expected_present": ["PLIF L4-L5", "dos cajas", "sustituto oseo"],
      "forbidden_present": ["PLIF duplicado", "TLIF no informado", "sustituto oseo duplicado", "cajas duplicadas"],
      "gate_ids": ["tecnica_implantes_no_duplicados"],
      "expected_message": "Tecnica o material duplicado/incompatible.",
      "notes": "Contar entidades normalizadas, no subtitulos."
    },
    {
      "id": "LUM-GATE-011",
      "title": "parche_dural_pre_cierre",
      "document_type": "parte_quirurgico",
      "severity": "critical",
      "source_type": "synthetic_doctor_correction_fixture",
      "input_axes": {
        "diagnosis_family": "estenosis_canal",
        "subtype": "not_applicable",
        "level": "L4-L5",
        "laterality": "not_applicable",
        "procedure_family": "descompresion",
        "direct_decompression": "yes",
        "dural_patch": "yes"
      },
      "expected_present": ["parche dural antes del cierre", "hemostasia", "cierre por planos"],
      "forbidden_present": ["cierre por planos luego parche dural", "cierre de piel luego parche dural"],
      "gate_ids": ["parche_dural_pre_cierre"],
      "expected_message": "El parche o refuerzo dural debe documentarse antes del cierre.",
      "notes": "Comparar posiciones textuales."
    },
    {
      "id": "LUM-GATE-012",
      "title": "hemostasia_recuento_antes_de_cierre",
      "document_type": "parte_quirurgico",
      "severity": "critical",
      "source_type": "synthetic_doctor_correction_fixture",
      "input_axes": {
        "diagnosis_family": "estenosis_canal",
        "subtype": "not_applicable",
        "level": "L4-L5",
        "laterality": "not_applicable",
        "procedure_family": "descompresion",
        "direct_decompression": "yes",
        "dural_patch": "no"
      },
      "expected_present": ["hemostasia", "recuento", "cierre por planos"],
      "forbidden_present": ["cierre antes de hemostasia", "cierre antes de recuento", "piel antes de recuento"],
      "gate_ids": ["orden_hemostasia_recuento_cierre"],
      "expected_message": "Hemostasia y recuento deben preceder el cierre por planos o piel.",
      "notes": "Orden quirurgico logico."
    },
    {
      "id": "LUM-GATE-013",
      "title": "no_duplicar_preparacion_inicial",
      "document_type": "parte_quirurgico",
      "severity": "medium",
      "source_type": "synthetic_doctor_correction_fixture",
      "input_axes": {
        "diagnosis_family": "hernia",
        "subtype": "posterolateral",
        "level": "L5-S1",
        "laterality": "izquierda",
        "procedure_family": "microdiscectomia",
        "direct_decompression": "yes",
        "dural_patch": "no"
      },
      "expected_present": ["decubito prono", "proteccion ocular", "acolchado"],
      "forbidden_present": ["decubito prono duplicado", "proteccion ocular duplicada", "acolchado duplicado"],
      "gate_ids": ["no_duplicar_preparacion_inicial"],
      "expected_message": "Preparacion o posicionamiento inicial duplicado.",
      "notes": "No contar checklist interno si no sale en documento final."
    },
    {
      "id": "LUM-GATE-014",
      "title": "topografia_foraminal_no_extraforaminal_si_no_se_dijo",
      "document_type": "historia_clinica",
      "severity": "high",
      "source_type": "synthetic_doctor_correction_fixture",
      "input_axes": {
        "diagnosis_family": "hernia",
        "subtype": "foraminal",
        "level": "L4-L5",
        "laterality": "derecha",
        "procedure_family": "not_informed",
        "direct_decompression": "not_informed",
        "dural_patch": "not_informed"
      },
      "expected_present": ["hernia foraminal L4-L5 derecha"],
      "forbidden_present": ["extraforaminal", "posterolateral", "central"],
      "gate_ids": ["topografia_exacta"],
      "expected_message": "La salida cambio la topografia declarada.",
      "notes": "No convertir foraminal en extraforaminal por sinonimia laxa."
    },
    {
      "id": "LUM-GATE-015",
      "title": "plif_tlif_incompatible_sin_plan_combinado",
      "document_type": "parte_quirurgico",
      "severity": "high",
      "source_type": "synthetic_doctor_correction_fixture",
      "input_axes": {
        "diagnosis_family": "espondilolistesis",
        "subtype": "degenerativa",
        "level": "L4-L5",
        "laterality": "not_applicable",
        "procedure_family": "PLIF",
        "interbody_technique": "PLIF",
        "combined_plan": false,
        "direct_decompression": "yes",
        "dural_patch": "no"
      },
      "expected_present": ["PLIF L4-L5"],
      "forbidden_present": ["TLIF", "PLIF y TLIF"],
      "gate_ids": ["tecnica_incompatible"],
      "expected_message": "PLIF y TLIF simultaneos requieren plan combinado explicito.",
      "notes": "Bloquear tecnica combinada no declarada."
    },
    {
      "id": "LUM-GATE-016",
      "title": "consentimiento_hernia_lumbar_especifico",
      "document_type": "consentimiento",
      "severity": "critical",
      "source_type": "synthetic_doctor_correction_fixture",
      "input_axes": {
        "diagnosis_family": "hernia",
        "subtype": "not_informed",
        "level": "L4-L5",
        "laterality": "derecha",
        "procedure_family": "microdiscectomia",
        "direct_decompression": "yes",
        "dural_patch": "not_informed"
      },
      "expected_present": ["procedimiento", "nivel L4-L5", "riesgos neurologicos", "LCR", "recidiva", "alternativas"],
      "forbidden_present": ["consentimiento generico", "sin nivel", "sin alternativas", "sin riesgos especificos"],
      "gate_ids": ["consentimiento_especifico_columna_v1"],
      "expected_message": "Consentimiento generico: falta procedimiento, nivel, riesgos o alternativas.",
      "notes": "Gate puede iniciar report_only si corpus oficial aun no esta aprobado para hard fail."
    }
  ]
}
```

## validator_expectations

| Gate | Expectativa minima del validator |
|---|---|
| `no_inventar_diagnostico_topografia` | Si el input no declara topografia/hallazgo, la salida no puede agregarlo en forma afirmativa. |
| `preservar_subtipo_espondilolistesis` | Si el input dice degenerativa, bloquear istmica/pars/lisis. |
| `diagnostico_puro_sin_indicacion` | En campo diagnostico, bloquear indicacion o conducta quirurgica. |
| `segmento_fusion_sin_lateralidad` | Bloquear `fijacion/artrodesis L4-L5 derecha/izquierda`; permitir lateralidad de abordaje. |
| `sin_descompresion_directa_bloqueante` | Con `direct_decompression=no`, bloquear laminectomia/hemilaminectomia/flavectomia afirmativas. |
| `extraforaminal_no_interlaminar` | En hernia extraforaminal, bloquear interlaminar/flavectomia/receso lateral como abordaje principal. |
| `extraforaminal_root_table` | Para L4-L5 extraforaminal derecha, esperar raiz L4 derecha, no L5 como raiz principal. |
| `tecnica_implantes_no_duplicados` | Contar entidades tecnicas/materiales normalizadas y bloquear duplicados no justificados. |
| `tecnica_incompatible` | PLIF y TLIF juntos requieren `combined_plan=true`. |
| `parche_dural_pre_cierre` | Si hay parche/refuerzo, debe aparecer antes de cierre. |
| `orden_hemostasia_recuento_cierre` | Hemostasia y recuento deben preceder cierre por planos/piel. |
| `no_duplicar_preparacion_inicial` | Posicion/proteccion/preparacion inicial no deben repetirse en salida final. |
| `consentimiento_especifico_columna_v1` | Requerir procedimiento, nivel, riesgos relevantes y alternativas. |

## integration_notes_for_orchestrator

1. Materializar el JSON en la app canonica, idealmente en `data/derived/clinical_test_cases/lumbar_inconsistency_gates_v2.json`.
2. Agregar un validator puro, sin tocar plantillas, para confirmar que cada `forbidden_present` falla cuando aparece en texto malo sintetico.
3. Usar deteccion contextual de negaciones. Ejemplo: `no se realizo laminectomia` no debe fallar por la palabra `laminectomia`.
4. Separar fixtures clinicos derivados de correcciones del Doctor de gates normativos/corpus. Los normativos pueden correr `report_only` hasta tener `approved_for_gate`.
5. Conectar al runner clinico existente solo despues de pasar fixtures aislados.
6. Activar hard fail primero para critical/high de bajo falso positivo: no inventar diagnostico, sin descompresion directa, extraforaminal, orden hemostasia/recuento/cierre.
7. Mantener la app real sin cambios desde este worker; esta entrega es solo draft para Codex principal.

## recommendation

Codex principal deberia implementar este pack en dos commits: primero fixtures + validator detect-only; segundo integracion al runner QA. No conviene ajustar prompts o plantillas hasta ver fallar los textos malos sinteticos contra estos fixtures.

## risks_limits

- Los fixtures son sinteticos y no contienen pacientes ni datos sensibles.
- El validator debe distinguir afirmaciones de negaciones para evitar falsos positivos.
- El gate de consentimiento especifico puede necesitar pasar por corpus oficial/revision antes de hard fail.
- La tabla raiz extraforaminal queda limitada a fixtures aprobados; no debe universalizarse sin revision clinica.
- No se inspecciono ni modifico la app clinica real.

## confidence

Alta para el draft de fixtures y la secuencia de integracion, porque deriva de resultados previos del bridge y correcciones ya convertidas en gates. Media para paths exactos en la app real hasta que Codex principal inspeccione el baseline.

## evidence_paths

- `jobs/20260525T173726-clinica-lumbar-fixture-pack-draft-v2.md`
- `results/20260525T153318-clinica-lumbar-inconsistency-gates-v2.result.md`
- `results/20260525T170711-clinica-corpus-official-gates-next-integration-v1.result.md`
- `context/fronts/clinica.md`
