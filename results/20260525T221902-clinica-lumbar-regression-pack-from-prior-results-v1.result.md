---
id: 20260525T221902-clinica-lumbar-regression-pack-from-prior-results-v1
job_id: 20260525T221902-clinica-lumbar-regression-pack-from-prior-results-v1
created_at: 2026-05-25T22:22:44-03:00
created_by: personal-xh
worker: personal-xh
status: completed
no_external_actions: true
no_secrets: true
---

# Resultado - CLINICA lumbar regression pack from prior results v1

## summary

Paquete portable de fixtures y asserts detect-only para que el orquestador lo convierta en tests locales de la app medico-legal. No se leyeron datos de pacientes, no se tocaron plantillas ni app real, y todo queda como gates de revision, no como regla medico-legal definitiva.

El pack cubre cinco fallas criticas ya repetidas en resultados previos: hernia extraforaminal L4-L5 derecha mal llevada a interlaminar o raiz L5, fijacion/artrodesis L4-L5 con descompresion directa inventada, canal estrecho redactado con tautologia, consentimiento con artrodesis lateralizada y parte quirurgico PLIF con materiales duplicados o cierre antes de hemostasia/recuento.

## source_counts

| Fuente permitida | Estado | Uso |
|---|---:|---|
| `results/20260525T120000-clinica-fixtures-lumbares-v1.result.md` | Revisada | Casos LUM-DOC sobre extraforaminal, raiz, artrodesis, descompresion y secuencia. |
| `results/20260525T122941-clinica-correcciones-a-fixtures-implementacion.result.md` | Revisada | Orden de implementacion y tests focales antes de tocar plantillas. |
| `results/20260525T153318-clinica-lumbar-inconsistency-gates-v2.result.md` | Revisada | Gates canonicos, matriz de fixture y reglas de evidencia. |
| `results/20260525T173726-clinica-lumbar-fixture-pack-draft-v2.result.md` | Revisada | Schema de fixture, ids LUM-GATE y estructura JSON previa. |
| `results/20260525T181000-clinica-lumbar-validator-detect-only-spec-v1.result.md` | Revisada | Contrato de validator, negaciones, duplicados y orden quirurgico. |
| `results/20260525T184100-clinica-lumbar-v2-stress-artifacts-v1.result.md` | Revisada | Controles buenos/malos para falsos positivos y falsos negativos. |
| `results/20260525T170711-clinica-corpus-official-gates-next-integration-v1.result.md` | Revisada | Priorizacion P0, modo report_only y separacion de corpus/gates. |
| `context/fronts/clinica.md` y `protocol.md` | Revisadas | Ruta canonica, seguridad y contrato operativo del bridge. |

## fixture_tree

```text
fixtures/clinica/lumbar_regression_v1/
  README.md
  cases/
    hernia_extraforaminal_l45_derecha.json
    espondilolistesis_degenerativa_l45_fijacion_sin_descompresion.json
    canal_estrecho_lumbar_no_tautologia.json
    consentimiento_fijacion_l45_sin_lateralidad_artrodesis.json
    parte_plif_materiales_secuencia_no_duplicados.json
  assertions/
    lumbar_detect_only_asserts.json
    forbidden_phrases_by_case.json
    required_sequence_checks.json
  runner_contract/
    expected_gate_outcomes.json
```

Convencion: cada caso debe ser sintetico, sin identificadores, con `input_axes`, `evidence_basis`, `approved_fixture_inference`, `expected_present`, `forbidden_present`, `gate_ids`, `severity` y `expected_detect_only_message`.

## canonical_rules

1. El diagnostico describe patologia y nivel; la indicacion, conducta o tecnica van en campos separados.
2. Toda salida debe trazarse a `explicit_input`, `approved_fixture_inference` o `template_required_field`.
3. Si falta evidencia, usar placeholder seguro del tipo `no informado en la fuente`, no inventar topografia, raiz, hernia, secuestro, material ni evento dural.
4. En hernia extraforaminal L4-L5 derecha, la inferencia aprobada para fixture es raiz L4 derecha; no raiz L5.
5. Una hernia extraforaminal no debe transformarse en abordaje interlaminar, hemilaminectomia, flavectomia ni hombro de raiz salvo input explicito compatible.
6. `sin descompresion directa` bloquea documentar como realizado laminectomia, hemilaminectomia, flavectomia, recalibraje o liberacion radicular directa.
7. La fijacion o artrodesis se expresa por segmento, por ejemplo `L4-L5`; no como `artrodesis L4-L5 derecha`.
8. La lateralidad de abordaje puede existir si esta separada del segmento fusionado.
9. Canal estrecho lumbar no debe repetir tautologias como `canal estrecho con compromiso del canal`.
10. PLIF, materiales, tornillos, barras, cajas e injerto deben documentarse una vez por entidad logica, salvo input que justifique repeticion.
11. Hemostasia y recuento deben preceder cierre por planos o piel en la seccion tecnica.
12. Parche o refuerzo dural solo aparece si el input lo informa, y debe aparecer antes del cierre.

## fixtures_minimal_json

```json
{
  "pack_id": "clinica_lumbar_regression_detect_only_v1",
  "source_type": "prior_personal_xh_results_only",
  "mode": "detect_only_review_gate",
  "cases": [
    {
      "id": "LUM-REG-001",
      "slug": "hernia_extraforaminal_l45_derecha",
      "document_types": ["historia_clinica", "parte_quirurgico"],
      "severity": "critical",
      "input_axes": {
        "diagnosis": "hernia discal extraforaminal L4-L5 derecha",
        "level": "L4-L5",
        "side": "derecha",
        "topography": "extraforaminal"
      },
      "evidence_basis": {
        "explicit_input": ["hernia discal", "extraforaminal", "L4-L5", "derecha"],
        "approved_fixture_inference": ["raiz L4 derecha"],
        "not_evidenced": ["raiz L5 derecha", "abordaje interlaminar", "hemilaminectomia", "flavectomia"]
      },
      "expected_present": ["extraforaminal", "L4-L5", "derecha", "raiz L4 derecha"],
      "forbidden_present": ["interlaminar", "hemilaminectomia", "flavectomia", "hombro de raiz", "raiz L5 derecha"],
      "gate_ids": ["extraforaminal_no_interlaminar", "extraforaminal_root_table"],
      "expected_detect_only_message": "Hernia extraforaminal L4-L5 derecha no debe derivar en tecnica interlaminar ni raiz L5."
    },
    {
      "id": "LUM-REG-002",
      "slug": "espondilolistesis_degenerativa_l45_fijacion_sin_descompresion",
      "document_types": ["historia_clinica", "parte_quirurgico"],
      "severity": "critical",
      "input_axes": {
        "diagnosis": "espondilolistesis degenerativa L4-L5",
        "procedure": "fijacion instrumentada y artrodesis L4-L5",
        "direct_decompression": "no",
        "level": "L4-L5"
      },
      "evidence_basis": {
        "explicit_input": ["espondilolistesis degenerativa", "L4-L5", "fijacion", "artrodesis", "sin descompresion directa"],
        "approved_fixture_inference": [],
        "not_evidenced": ["espondilolistesis istmica", "laminectomia", "hemilaminectomia", "flavectomia", "liberacion radicular directa"]
      },
      "expected_present": ["espondilolistesis degenerativa", "L4-L5", "fijacion", "artrodesis"],
      "forbidden_present": ["istmica", "laminectomia", "hemilaminectomia", "flavectomia", "recalibraje", "liberacion radicular directa", "fijacion L4-L5 derecha", "artrodesis L4-L5 derecha"],
      "gate_ids": ["preservar_subtipo_espondilolistesis", "sin_descompresion_directa_bloqueante", "segmento_fusion_sin_lateralidad"],
      "expected_detect_only_message": "Caso L4-L5 degenerativo sin descompresion directa: bloquear subtipo, tecnica o lateralidad inventada."
    },
    {
      "id": "LUM-REG-003",
      "slug": "canal_estrecho_lumbar_no_tautologia",
      "document_types": ["historia_clinica", "consentimiento"],
      "severity": "high",
      "input_axes": {
        "diagnosis": "canal estrecho lumbar",
        "level": "PLACEHOLDER_NIVEL_SI_NO_INFORMADO"
      },
      "evidence_basis": {
        "explicit_input": ["canal estrecho lumbar"],
        "approved_fixture_inference": [],
        "not_evidenced": ["hernia discal", "radiculopatia", "compromiso neural especifico"]
      },
      "expected_present": ["canal estrecho lumbar"],
      "forbidden_present": ["canal estrecho con compromiso del canal", "estenosis de canal con canal comprometido", "compromiso del canal por canal estrecho", "hernia discal no informada"],
      "gate_ids": ["canal_estrecho_no_tautologico", "no_inventar_diagnostico_topografia"],
      "expected_detect_only_message": "Canal estrecho lumbar debe redactarse sin tautologia y sin agregar patologia no informada."
    },
    {
      "id": "LUM-REG-004",
      "slug": "consentimiento_fijacion_l45_sin_lateralidad_artrodesis",
      "document_types": ["consentimiento"],
      "severity": "high",
      "input_axes": {
        "procedure": "fijacion instrumentada y artrodesis L4-L5",
        "level": "L4-L5",
        "approach_laterality": "derecha_si_el_input_la_informa",
        "fusion_segment_laterality": "none"
      },
      "evidence_basis": {
        "explicit_input": ["fijacion instrumentada", "artrodesis", "L4-L5"],
        "approved_fixture_inference": [],
        "not_evidenced": ["artrodesis L4-L5 derecha como segmento"]
      },
      "expected_present": ["fijacion", "artrodesis", "L4-L5", "riesgos especificos", "alternativas"],
      "forbidden_present": ["artrodesis L4-L5 derecha", "fijacion L4-L5 derecha", "fusion L4-L5 derecha", "consentimiento generico para cirugia lumbar"],
      "gate_ids": ["segmento_fusion_sin_lateralidad", "consentimiento_especifico_columna_v1"],
      "expected_detect_only_message": "Consentimiento L4-L5 especifico: el segmento de fusion no debe lateralizarse."
    },
    {
      "id": "LUM-REG-005",
      "slug": "parte_plif_materiales_secuencia_no_duplicados",
      "document_types": ["parte_quirurgico"],
      "severity": "critical",
      "input_axes": {
        "procedure": "PLIF L4-L5",
        "level": "L4-L5",
        "materials": ["cajas intersomaticas", "tornillos", "barras", "sustituto oseo"],
        "sequence": ["preparacion", "exposicion", "PLIF", "materiales", "hemostasia", "recuento", "cierre"],
        "dural_patch": "not_informed"
      },
      "evidence_basis": {
        "explicit_input": ["PLIF", "L4-L5", "materiales segun input"],
        "approved_fixture_inference": [],
        "not_evidenced": ["TLIF", "parche dural", "cierre antes de hemostasia", "cierre antes de recuento"]
      },
      "expected_present": ["PLIF", "L4-L5", "hemostasia", "recuento", "cierre"],
      "forbidden_present": ["TLIF sin plan combinado", "PLIF duplicado como nuevo acto", "parche dural no informado", "cierre antes de hemostasia", "cierre antes de recuento"],
      "gate_ids": ["tecnica_implantes_no_duplicados", "tecnica_incompatible", "no_inventar_parche_dural", "orden_hemostasia_recuento_cierre"],
      "expected_detect_only_message": "Parte PLIF debe evitar duplicados/materiales inventados y respetar hemostasia/recuento antes del cierre."
    }
  ]
}
```

## detect_only_asserts

```json
{
  "assertion_contract": {
    "input": ["fixture", "generated_text", "structured_output_optional"],
    "output": ["ok", "failures", "warnings", "matched_spans", "gate_id", "severity", "message"],
    "default_mode": "detect_only"
  },
  "assertions": [
    {
      "id": "assert_not_contains_affirmed_forbidden_phrase",
      "logic": "fail if a forbidden phrase appears as an affirmed fact, after negation handling",
      "negation_window_before_tokens": 8,
      "negation_window_after_tokens": 4,
      "negators": ["no", "sin", "niega", "ausencia de", "no se realizo", "no se evidencia", "no se describe"]
    },
    {
      "id": "assert_extraforaminal_l45_right_root_l4",
      "scope": "LUM-REG-001",
      "logic": "if topography=extraforaminal and level=L4-L5 and side=derecha, require raiz L4 derecha and fail affirmed raiz L5 derecha"
    },
    {
      "id": "assert_no_interlaminar_terms_for_extraforaminal",
      "scope": "LUM-REG-001",
      "logic": "fail affirmed interlaminar, hemilaminectomia, flavectomia or hombro de raiz when extraforaminal is the only supported topography"
    },
    {
      "id": "assert_no_direct_decompression_when_denied",
      "scope": "LUM-REG-002",
      "logic": "fail affirmed laminectomia, hemilaminectomia, flavectomia, recalibraje or liberacion radicular directa when direct_decompression=no"
    },
    {
      "id": "assert_no_lateralized_fusion_segment",
      "scope": ["LUM-REG-002", "LUM-REG-004"],
      "logic": "fail if lateralidad is attached to fijacion, fusion or artrodesis segment L4-L5; allow lateralidad attached to abordaje if explicit"
    },
    {
      "id": "assert_no_canal_estrecho_tautology",
      "scope": "LUM-REG-003",
      "logic": "fail tautologies that repeat canal as both diagnosis and compromised structure"
    },
    {
      "id": "assert_entity_count_at_most_once_in_body",
      "scope": "LUM-REG-005",
      "logic": "count PLIF and material entities in narrative body; ignore headings, fixture labels and internal checklist"
    },
    {
      "id": "assert_before_in_technical_section",
      "scope": "LUM-REG-005",
      "logic": "first affirmed hemostasia and recuento must appear before first affirmed cierre by planes or piel"
    }
  ]
}
```

## forbidden_phrases_by_case

| Caso | Frases prohibidas afirmadas | Nota anti falso positivo |
|---|---|---|
| `LUM-REG-001` | `interlaminar`, `hemilaminectomia`, `flavectomia`, `hombro de raiz`, `raiz L5 derecha` | No fallar si el texto dice `no se realizo abordaje interlaminar`. |
| `LUM-REG-002` | `istmica`, `laminectomia`, `hemilaminectomia`, `flavectomia`, `recalibraje`, `liberacion radicular directa`, `artrodesis L4-L5 derecha` | La afirmacion posterior gana sobre una negacion lejana. |
| `LUM-REG-003` | `canal estrecho con compromiso del canal`, `estenosis de canal con canal comprometido`, `hernia discal no informada`, `radiculopatia no informada` | El gate detecta mala redaccion e invencion, no corrige estilo. |
| `LUM-REG-004` | `artrodesis L4-L5 derecha`, `fijacion L4-L5 derecha`, `fusion L4-L5 derecha`, `consentimiento generico para cirugia lumbar` | Permitido: `abordaje derecho para artrodesis L4-L5`, si el input informa abordaje. |
| `LUM-REG-005` | `TLIF` sin plan combinado, `PLIF` duplicado como nuevo acto, `parche dural` no informado, `cierre` antes de `hemostasia`, `cierre` antes de `recuento` | Excluir titulos y resumen final para conteo/orden. |

## required_sequence_checks

| Check | Scope | Regla | Failure message |
|---|---|---|---|
| `hemostasia_before_closure` | `parte_quirurgico` | `index(hemostasia) < index(cierre)` en seccion tecnica. | `Hemostasia debe preceder el cierre.` |
| `count_before_closure` | `parte_quirurgico` | `index(recuento) < index(cierre)` en seccion tecnica. | `Recuento debe preceder el cierre.` |
| `dural_patch_before_closure_if_present` | `parte_quirurgico` | Si `dural_patch=yes`, el parche/refuerzo dural debe preceder el cierre. | `Parche o refuerzo dural debe documentarse antes del cierre.` |
| `no_dural_patch_if_not_evidenced` | `parte_quirurgico` | Si `dural_patch=not_informed`, cualquier parche afirmado falla. | `La salida inventa parche o refuerzo dural no informado.` |
| `plif_count_once_in_body` | `parte_quirurgico` | `PLIF` puede figurar como titulo y como acto una vez; no como acto nuevo repetido. | `PLIF aparece duplicado como acto quirurgico.` |
| `materials_not_reintroduced_as_new_step` | `parte_quirurgico` | Cajas, tornillos, barras e injerto no deben reaparecer como nuevos materiales sin input. | `Materiales aparecen duplicados o reintroducidos sin evidencia.` |

## integration_plan_for_orchestrator

1. Crear el fixture JSON en la app real solo despues de leer la ruta canonica y baseline.
2. Implementar helpers puros: normalizacion, negacion, `firstAffirmedIndex`, conteo por cuerpo narrativo y exclusion de headings/checklists.
3. Correr los cinco fixtures contra textos malos sinteticos para confirmar que fallan.
4. Correr textos buenos sinteticos de control para evitar falsos positivos, en especial negaciones y lateralidad de abordaje.
5. Conectar el validator al generador en `report_only`, sin modificar plantillas.
6. Promover a hard fail solo gates critical con baja tasa de falso positivo: extraforaminal, raiz L4, sin descompresion directa, hemostasia/recuento antes de cierre.
7. Mantener consentimiento especifico y duplicados/materiales primero como `report_only` si hay dudas de parsing.
8. Recién despues de evidencia local, ajustar prompts o plantillas, con commit separado y QA focal.

## risks_limits

- Este pack no valida medicina real ni reemplaza revision clinica o legal; solo detecta contradicciones textuales y hechos no soportados.
- La tabla raiz extraforaminal queda limitada a fixtures aprobados por resultados previos; no generalizar fuera de L3-L4, L4-L5 y L5-S1 sin revision.
- Regex simples pueden fallar con negaciones; por eso el primer helper obligatorio es deteccion contextual de afirmacion.
- Secuencia quirurgica debe evaluarse en la seccion tecnica, no en resumen, checklist interno ni titulo.
- Si el generador usa sinonimos no cubiertos, deben entrar primero como warning con `matched_span` para revision.

## recommendation

Portar este pack como primer smoke test detect-only de CLINICA. La primera victoria concreta es impedir que la app produzca: extraforaminal L4-L5 derecha como interlaminar o raiz L5, `sin descompresion directa` con laminectomia/flavectomia afirmada, artrodesis L4-L5 lateralizada, canal estrecho tautologico y parte PLIF con cierre antes de hemostasia/recuento.

## confidence

Alta para los cinco casos pedidos, porque derivan de resultados previos consistentes del bridge. Media para consentimiento especifico y duplicados/materiales hasta ver salida real del generador y ajustar exclusion de headings, listas y resumenes.

## evidence_paths

- `jobs/20260525T221902-clinica-lumbar-regression-pack-from-prior-results-v1.md`
- `protocol.md`
- `context/fronts/clinica.md`
- `results/20260525T120000-clinica-fixtures-lumbares-v1.result.md`
- `results/20260525T122941-clinica-correcciones-a-fixtures-implementacion.result.md`
- `results/20260525T153318-clinica-lumbar-inconsistency-gates-v2.result.md`
- `results/20260525T173726-clinica-lumbar-fixture-pack-draft-v2.result.md`
- `results/20260525T181000-clinica-lumbar-validator-detect-only-spec-v1.result.md`
- `results/20260525T184100-clinica-lumbar-v2-stress-artifacts-v1.result.md`
- `results/20260525T170711-clinica-corpus-official-gates-next-integration-v1.result.md`
