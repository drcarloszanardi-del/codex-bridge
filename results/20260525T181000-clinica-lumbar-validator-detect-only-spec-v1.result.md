---
id: 20260525T181000-clinica-lumbar-validator-detect-only-spec-v1
job_id: 20260525T181000-clinica-lumbar-validator-detect-only-spec-v1
created_at: 2026-05-25T18:15:08-03:00
created_by: personal-xh
worker: personal-xh
status: completed
no_external_actions: true
no_secrets: true
---

# Resultado - CLINICA lumbar validator detect-only spec v1

## summary

Especificacion implementable para un validator detect-only del pack lumbar v2. No modifica app real, no usa pacientes y trabaja sobre fixtures sinteticos ya materializados por Codex principal. El objetivo es detectar contradicciones clinicas/documentales antes de tocar plantillas o generacion.

El validator debe ser puro, deterministico y explicable: recibe `fixture`, `generated_text` y opcionalmente `structured_output`; devuelve `ok`, `failures`, `warnings`, `matched_spans`, `gate_id`, `severity` y `expected_message`.

## coverage_table

| Fuente permitida | Estado | Uso |
|---|---:|---|
| `results/20260525T173726-clinica-lumbar-fixture-pack-draft-v2.result.md` | Revisada | Fixture schema, 16 casos sinteticos y expected/forbidden tokens. |
| `results/20260525T153318-clinica-lumbar-inconsistency-gates-v2.result.md` | Revisada | Gates clinicos, negaciones, orden quirurgico y falsos positivos esperables. |
| `results/20260525T170711-clinica-corpus-official-gates-next-integration-v1.result.md` | Revisada | Batch P0, secuencia de integracion y cautela con corpus legal. |
| `context/fronts/clinica.md` | Revisada | Ruta canonica y regla de no tocar app real sin baseline/test focal. |

## validator_contract

```ts
type LumbarFixture = {
  id: string;
  title: string;
  document_type: "historia_clinica" | "consentimiento" | "parte_quirurgico";
  severity: "critical" | "high" | "medium";
  input_axes: Record<string, unknown>;
  expected_present?: string[];
  forbidden_present?: string[];
  gate_ids: string[];
  expected_message: string;
};

type ValidationFailure = {
  fixture_id: string;
  gate_id: string;
  severity: "critical" | "high" | "medium";
  message: string;
  matched_text?: string;
  start?: number;
  end?: number;
  context?: string;
};

type ValidationResult = {
  ok: boolean;
  fixture_id: string;
  failures: ValidationFailure[];
  warnings: ValidationFailure[];
  checked_gates: string[];
};
```

Contrato operativo:

| Entrada | Regla |
|---|---|
| `fixture` | Debe ser el caso sintetico del JSON lumbar v2. |
| `generated_text` | Texto final de HC, consentimiento o parte. |
| `structured_output` | Opcional; si existe, usarlo antes que regex textual. |
| Salida `ok=false` | Si hay failure critical/high/medium segun modo. |
| Salida `warnings` | Para corpus oficial aun no aprobado como hard gate. |
| Modo inicial | `detect_only`: reporta, no modifica texto ni bloquea guardado. |

## normalization_rules

1. Convertir a minusculas.
2. Normalizar acentos: `fijacion`, `artrodesis`, `hemilaminectomia`, `flavectomia`.
3. Unificar guiones y espacios: `L4-L5`, `L4 L5`, `L4/L5` -> `l4-l5`.
4. Colapsar espacios multiples.
5. Mantener offset original mediante mapa `normalized_index -> original_index` para spans.
6. Normalizar sinonimos clinicos solo para deteccion, no para reescritura:

| Canon | Variantes |
|---|---|
| `laminectomia` | laminectomia, laminectomia descompresiva |
| `hemilaminectomia` | hemi-laminectomia, hemilaminectomia |
| `flavectomia` | flavectomia, reseccion de ligamento amarillo |
| `descompresion_directa` | liberacion radicular directa, recalibraje, descompresion neural directa |
| `cierre` | cierre por planos, cierre de piel, sutura de piel |
| `recuento` | recuento de gasas, recuento instrumental, conteo |
| `parche_dural` | parche dural, refuerzo dural, sustituto dural |

## negation_handling_rules

El validator debe bloquear afirmaciones, no negaciones. Para cada token prohibido, evaluar ventana de negacion alrededor del match.

Regla conservadora:

```text
negation_window_before = 8 tokens
negation_window_after = 4 tokens
negators = ["no", "sin", "niega", "ausencia de", "no se realizo", "no se evidencia", "no se describe"]
affirmation_breakers = ["se realiza", "se efectua", "se practica", "se completa", "se documenta"]
```

Ejemplos:

| Texto | Resultado |
|---|---|
| `no se realizo laminectomia` | No falla para `sin_descompresion_directa_bloqueante`. |
| `sin flavectomia ni liberacion directa` | No falla. |
| `se realiza hemilaminectomia` | Falla si `direct_decompression=no`. |
| `no se describe parche dural` | No falla por `parche dural`. |
| `se coloca parche dural` con `dural_patch=not_informed` | Falla por `no_inventar_parche_dural`. |

Si hay negacion y afirmacion en el mismo parrafo, la afirmacion gana solo si el verbo afirmativo esta mas cerca del token prohibido que el negador.

## order_detection_rules

Aplicar solo a `parte_quirurgico`.

### parche dural antes de cierre

```text
patch_index = first_affirmative(["parche dural", "refuerzo dural", "sustituto dural"])
closure_index = first_affirmative(["cierre por planos", "cierre de piel", "sutura de piel"])
fail if fixture.input_axes.dural_patch == "yes" and patch_index > closure_index
fail if fixture.input_axes.dural_patch in ["no", "not_informed"] and patch_index exists affirmative
```

### hemostasia, recuento y cierre

```text
hemostasis_index = first_affirmative(["hemostasia"])
count_index = first_affirmative(["recuento de gasas", "recuento instrumental", "recuento"])
closure_index = first_affirmative(["cierre por planos", "cierre de piel", "sutura de piel"])

fail if closure_index exists and hemostasis_index exists and closure_index < hemostasis_index
fail if closure_index exists and count_index exists and closure_index < count_index
fail if regex /cierre.{0,120}(hemostasia|recuento)/ matches affirmative sequence
```

Mensajes:

| Gate | Mensaje |
|---|---|
| `parche_dural_pre_cierre` | `El parche o refuerzo dural debe documentarse antes del cierre.` |
| `no_inventar_parche_dural` | `La salida inventa parche o refuerzo dural no informado.` |
| `orden_hemostasia_recuento_cierre` | `Hemostasia y recuento deben preceder el cierre por planos o piel.` |

## duplicate_detection_rules

### PLIF, TLIF y materiales

Normalizar entidades:

```text
technique_entities = ["plif", "tlif"]
material_entities = ["caja", "cajas", "tornillo", "tornillos", "barra", "barras", "sustituto oseo"]
```

Reglas:

1. Si aparecen `plif` y `tlif` y `combined_plan != true`, falla `tecnica_incompatible`.
2. Si `plif` aparece mas de una vez en cuerpo narrativo, falla salvo que uno sea titulo/seccion.
3. Si material aparece en listas separadas pero mismo paso narrativo, contar una vez.
4. Si material aparece como nuevo implante en dos pasos diferentes sin input que lo permita, falla.

### preparacion inicial

Tokens:

```text
preparation_entities = ["decubito prono", "proteccion ocular", "acolchado", "proteccion de prominencias"]
```

Regla:

```text
fail if count_affirmative(entity, document_body_without_checklist) > 1
```

No contar:

- Titulos.
- Checklist interno no renderizado.
- Repeticion dentro de `expected_present` del fixture.

## critical_gates_first_batch

| Orden | Gate | Severity | Por que primero |
|---:|---|---|---|
| 1 | `no_inventar_diagnostico_topografia` | critical | Evita hechos clinicos no informados. |
| 2 | `sin_descompresion_directa_bloqueante` | critical | Evita documentar acto quirurgico no realizado. |
| 3 | `extraforaminal_no_interlaminar` | critical | Corrige incompatibilidad anatomica/tecnica. |
| 4 | `extraforaminal_root_table` | critical | Evita raiz incorrecta en fixture aprobado. |
| 5 | `orden_hemostasia_recuento_cierre` | critical | Secuencia quirurgica basica. |
| 6 | `parche_dural_pre_cierre` | critical | Evento/material dural debe estar antes del cierre. |
| 7 | `diagnostico_puro_sin_indicacion` | high | Separa diagnostico de conducta. |
| 8 | `segmento_fusion_sin_lateralidad` | high | Evita lateralidad incorrecta en artrodesis/fijacion. |

## false_positive_risks

| Riesgo | Mitigacion |
|---|---|
| Bloquear frase negada como `no se realizo laminectomia`. | Ventana de negacion y verbos afirmativos cercanos. |
| Contar PLIF duplicado por titulo y cuerpo. | Excluir headings y contar entidades en cuerpo narrativo. |
| Bloquear checklist interno no visible. | Validar solo texto final renderizado o marcar secciones excluidas. |
| Interpretar `foraminal` como `extraforaminal`. | Topografia exacta, no sinonimia laxa. |
| Bloquear consentimiento especifico por corpus legal aun no aprobado. | Correr `report_only` hasta `approved_for_gate`. |
| Orden textual no refleja orden quirurgico si hay resumen final. | Aplicar a seccion tecnica, no a resumen/diagnostico. |
| Tabla raiz extraforaminal demasiado amplia. | Limitar a fixtures aprobados: L3-L4->L3, L4-L5->L4, L5-S1->L5. |

## minimal_test_matrix

| Fixture | Texto malo sintetico minimo | Debe fallar gate |
|---|---|---|
| `LUM-GATE-001` | `Hernia extraforaminal L4-L5 derecha por abordaje interlaminar con flavectomia sobre raiz L5.` | `extraforaminal_no_interlaminar`, `extraforaminal_root_table` |
| `LUM-GATE-002` | `Hernia posterolateral/extraforaminal L4-L5 derecha` sin topografia en input. | `no_inventar_diagnostico_topografia` |
| `LUM-GATE-003` | `Radiculopatia L5 derecha por hernia discal extruida.` | `no_inventar_diagnostico_topografia` |
| `LUM-GATE-004` | `Espondilolistesis degenerativa o istmica L4-L5 con lisis.` | `preservar_subtipo_espondilolistesis` |
| `LUM-GATE-006` | `Diagnostico: espondilolistesis degenerativa L4-L5 con indicacion de fijacion.` | `diagnostico_puro_sin_indicacion` |
| `LUM-GATE-007` | `Consentimiento para artrodesis L4-L5 derecha.` | `segmento_fusion_sin_lateralidad` |
| `LUM-GATE-008` | `Se realiza hemilaminectomia y flavectomia` con `direct_decompression=no`. | `sin_descompresion_directa_bloqueante` |
| `LUM-GATE-010` | `PLIF L4-L5... se completa PLIF L4-L5... TLIF L4-L5.` | `tecnica_implantes_no_duplicados`, `tecnica_incompatible` |
| `LUM-GATE-011` | `Cierre por planos. Luego se coloca parche dural.` | `parche_dural_pre_cierre` |
| `LUM-GATE-012` | `Cierre de piel. Hemostasia y recuento correctos.` | `orden_hemostasia_recuento_cierre` |
| `LUM-GATE-013` | `Decubito prono... proteccion ocular... decubito prono... proteccion ocular.` | `no_duplicar_preparacion_inicial` |
| `LUM-GATE-016` | `Consentimiento generico para cirugia lumbar` sin nivel/riesgos/alternativas. | `consentimiento_especifico_columna_v1` |

## implementation_sequence_for_orchestrator

1. Crear `scripts/qa/validate_lumbar_inconsistency_gates_v2.js` como validator puro.
2. Cargar el JSON sintetico desde `data/derived/clinical_test_cases/lumbar_inconsistency_gates_v2.json`.
3. Implementar normalizacion con mapa de offsets.
4. Implementar `isNegated(match, tokens)` antes de cualquier forbidden token.
5. Implementar gates critical del primer batch.
6. Agregar textos malos sinteticos embebidos en test fixture, no pacientes.
7. Ejecutar validator aislado y exigir que los malos fallen y los positivos pasen.
8. Conectar a `scripts/qa/run_clinica_core_qa.js` en modo `report_only`.
9. Pasar a hard fail solo critical/high con falsos positivos resueltos.
10. Recien despues ajustar plantillas/generador.

## recommendation

Codex principal deberia implementar primero el validator con 4 helpers puros: `normalizeText`, `isNegated`, `findOrderedEvent`, `countContextualEntity`. Con eso cubre los riesgos grandes sin tocar plantillas clinicas.

## risks_limits

- Este worker no inspecciono ni modifico la app real.
- La deteccion textual debe validarse contra salida final renderizada, no contra borradores internos.
- La negacion en castellano puede ser ambigua; conviene mantener spans y contexto en cada failure.
- Los gates normativos/corpus deben correr `report_only` hasta revision oficial.
- Los fixtures son sinteticos; no contienen ni deben contener pacientes.

## confidence

Alta para contrato, orden de implementacion y gates critical derivados de fixtures. Media para ubicacion exacta de archivos en app real hasta que Codex principal inspeccione baseline.

## evidence_paths

- `jobs/20260525T181000-clinica-lumbar-validator-detect-only-spec-v1.md`
- `results/20260525T173726-clinica-lumbar-fixture-pack-draft-v2.result.md`
- `results/20260525T153318-clinica-lumbar-inconsistency-gates-v2.result.md`
- `results/20260525T170711-clinica-corpus-official-gates-next-integration-v1.result.md`
- `context/fronts/clinica.md`
