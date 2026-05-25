---
id: 20260525T153318-clinica-lumbar-inconsistency-gates-v2
job_id: 20260525T153318-clinica-lumbar-inconsistency-gates-v2
created_at: 2026-05-25T15:34:37-03:00
created_by: personal-xh
worker: personal-xh
status: completed
no_external_actions: true
no_secrets: true
---

# Resultado - CLINICA lumbar gates contra inconsistencias graves v2

Job: `20260525T153318-clinica-lumbar-inconsistency-gates-v2`
Worker: `personal-xh` / Pablo
Fecha: `2026-05-25`

## summary honesto

Se consolido un pack implementable para bloquear inconsistencias graves en historia clinica, consentimiento y parte quirurgico lumbar. La propuesta convierte las correcciones del Doctor en ejes canonicos, frases prohibidas por contexto, templates seguros, una matriz de fixtures sinteticos y gates deterministicos detect-only. No se modifico la app real: el Codex principal debe integrar y ejecutar estos gates en la Mac de trabajo.

El criterio central es conservador: si el input no declara diagnostico, subtipo, topografia, lateralidad, tecnica, implante o evento dural, la salida no debe inventarlo. Si el input declara una negacion clinica relevante, como `sin descompresion directa`, la salida debe respetarla aunque el procedimiento lumbar habitual pudiera sugerir otra cosa.

## source_counts

| Fuente | Archivos revisados | Uso |
|---|---:|---|
| `jobs/20260525T153318-clinica-lumbar-inconsistency-gates-v2.md` | 1 | Contrato, problemas clinicos obligatorios y secciones exigidas. |
| `context/fronts/clinica.md` | 1 | Estado canonico: convertir correcciones del Doctor en fixtures/gates. |
| `results/20260525T015336-simulacion-clinica-60-casos-columna-inconsistencias.result.md` | 1 | Resumen del pack de 60 casos sinteticos. |
| `results/20260525T015336-simulacion-clinica-60-casos-columna-inconsistencias.cases.json` | 1 | Casos base C001-C060 para matriz y gates. |
| `results/20260525T120000-clinica-fixtures-lumbares-v1.result.md` | 1 | Fixtures LUM-DOC-001 a LUM-DOC-013 y asserts previos. |
| `results/20260525T122941-clinica-correcciones-a-fixtures-implementacion.result.md` | 1 | Orden de integracion seguro en app real. |
| `results/20260525T124545-clinica-corpus-gates-backlog-v2.result.md` | 1 | Prioridad P0/P1 y separacion hard gate vs needs_review. |

## coverage_table

| Problema cubierto | Mecanismo propuesto | Severidad | Evidencia |
|---|---|---:|---|
| No inventar diagnosticos/topografia | `no_inventar_diagnostico_topografia` + axes obligatorios | critical | Workorder + C005/C006/C027 |
| Degenerativa vs istmica | `preservar_subtipo_espondilolistesis` | high | Workorder + C009 |
| Diagnostico separado de indicacion | `diagnostico_puro_sin_indicacion` | high | Workorder + LUM-DOC-006 |
| Canal estrecho sin tautologia | `canal_estrecho_no_tautologico` | medium | Workorder + C007/C008 |
| Consentimiento L4-L5 sin lateralidad de fijacion/artrodesis | `segmento_fusion_sin_lateralidad` | high | Workorder + C010 |
| Sin descompresion directa | `sin_descompresion_directa_bloqueante` | critical | Workorder + C011/C016 |
| Hernia extraforaminal no interlaminar | `extraforaminal_no_interlaminar` | critical | Workorder + C001/C055 |
| PLIF/implantes sin duplicar | `tecnica_implantes_no_duplicados` | high | Workorder + C013/C014/C056 |
| Parche dural en orden logico | `parche_dural_pre_cierre` | critical | Workorder + C017-C019 |
| Hemostasia/recuento antes del cierre | `orden_hemostasia_recuento_cierre` | critical | Workorder + C020/C021 |
| Repeticiones de posicion/proteccion | `no_duplicar_preparacion_inicial` | medium | Workorder + LUM-DOC-010 |
| Corpus y hard gates seguros | separar `correccion_doctor` de jurisprudencia/doctrina | high | `results/20260525T124545...` |

## evidencia clinica inferencia opinion

| Tipo | Contenido | Uso permitido |
|---|---|---|
| Evidencia clinica del caso | Diagnostico declarado, nivel, lado, topografia, sintomas, hallazgos, indicacion, tecnica, implantes, evento dural y secuencia quirurgica explicitada en el input. | Puede aparecer en documento final y activar gates. |
| Inferencia controlada | Raiz probable solo si existe tabla anatomica/caso fixture aprobado: por ejemplo extraforaminal L4-L5 derecha -> raiz L4 derecha en los fixtures del Doctor. | Puede usarse como assert/gate contextual, con metadata `derived_from=approved_fixture`. |
| Opinion o criterio interno | Priorizacion P0/P1, orden de implementacion, umbral de bloqueo, necesidades de revision medico-legal. | Puede guiar backlog; no debe inventar hechos clinicos ni volverse hard gate sin fixture. |

## canonical_case_axes

Variables canonicas minimas para cada generacion lumbar:

```json
{
  "case_id": "synthetic_or_real_id_without_patient_data",
  "document_type": "historia_clinica|consentimiento|parte_quirurgico|evolucion",
  "diagnosis": {
    "family": "hernia|estenosis_canal|espondilolistesis|quiste_facetario|dolor_lumbar|otro",
    "subtype": "extraforaminal|foraminal|posterolateral|central|degenerativa|istmica|null",
    "levels": ["L4-L5"],
    "laterality": "derecha|izquierda|bilateral|sin_lado|no_informado",
    "topography_source": "explicit_input|approved_fixture_inference|not_available"
  },
  "clinical_axes": {
    "symptoms": ["radiculopatia", "claudicacion", "dolor_lumbar"],
    "affected_root": "L3|L4|L5|S1|no_informada|inferida_por_fixture",
    "neurologic_deficit": "present|absent|not_informed",
    "imaging_basis": "present|missing|not_required_for_fixture"
  },
  "indication": {
    "text": "separate_from_diagnosis",
    "surgery_indicated": true,
    "must_not_be_inside_diagnosis": true
  },
  "procedure": {
    "family": "microdiscectomia|descompresion|fijacion_artrodesis|TLIF|PLIF|MISS|revision|otro",
    "levels": ["L4-L5"],
    "approach": "extraforaminal|foraminal|interlaminar|Wiltse|posterior|not_informed",
    "approach_laterality": "derecha|izquierda|bilateral|not_applicable|not_informed",
    "direct_decompression": "yes|no|not_informed",
    "fusion": "yes|no",
    "interbody_technique": "PLIF|TLIF|none|not_informed",
    "implants_materials": ["tornillos", "barras", "caja", "sustituto_oseo", "drill"],
    "materials_source": "explicit_input|not_informed"
  },
  "dural_event": {
    "durotomy": "yes|no|not_informed",
    "patch_or_reinforcement": "yes|no|not_informed",
    "patch_timing": "before_closure|required_if_used"
  },
  "sequence": {
    "preparation_once": true,
    "hemostasis_before_closure": true,
    "count_before_skin_closure": true,
    "closure_last": true
  },
  "consent": {
    "procedure_specific": true,
    "level_specific": true,
    "fusion_segment_has_no_laterality": true,
    "risks_and_alternatives_present": true
  }
}
```

Regla operativa: cada frase del documento final debe poder trazarse a `explicit_input`, `approved_fixture_inference` o `template_required_field`. Si no puede trazarse, el gate debe bloquearla o enviarla a revision.

## forbidden_phrases_by_context

| Contexto | Frases/patrones prohibidos | Razon clinica/medicolegal | Nota anti falso positivo |
|---|---|---|---|
| Diagnostico | `con indicacion de`, `requiere instrumentacion`, `requiere descompresion`, `se indica cirugia` | Mezcla diagnostico con conducta/indicacion. | Permitido solo en campo `indicacion`, no en `diagnostico`. |
| Topografia no informada | `hernia posterolateral derecha`, `hernia extraforaminal`, `fragmento discal`, `secuestro` | Inventar anatomia cambia diagnostico, consentimiento y tecnica. | No bloquear si aparece negado: `no se informa hernia...`. |
| Espondilolistesis degenerativa | `istmica`, `pars`, `lisis`, `degenerativa o istmica` | Cambia etiologia y puede alterar indicacion. | Bloquear si input fija `degenerativa`; si input no define subtipo, pedir precision. |
| Canal estrecho | `canal estrecho con compromiso del canal`, `estenosis de canal con canal comprometido` | Tautologia pobre y potencialmente confusa. | Reemplazar por `estenosis de canal lumbar` + nivel/sintomas. |
| Fijacion/artrodesis L4-L5 | `fijacion L4-L5 derecha`, `artrodesis L4-L5 derecha` | La fusion es por segmento; la lateralidad corresponde a abordaje, sintomas o descompresion. | Permitido: `abordaje derecho para fijacion L4-L5`. |
| Sin descompresion directa | `laminectomia`, `hemilaminectomia`, `flavectomia`, `liberacion radicular directa`, `recalibraje` | Contradice negacion expresa y registra acto no realizado. | Permitido solo en negacion clara: `no se realizo laminectomia`. |
| Hernia extraforaminal | `abordaje interlaminar`, `flavectomia`, `receso lateral`, `hombro de raiz` | Describe logica central/lateral recesal incompatible con extraforaminal como eje principal. | No aplicar globalmente a hernias no extraforaminales. |
| PLIF/implantes | `PLIF` repetido sin nuevo paso, `TLIF y PLIF` sin plan combinado, duplicar `caja`, `tornillos`, `sustituto oseo` | Duplicacion o tecnica incoherente dificulta trazabilidad. | Contar por entidad tecnica/material, no por subtitulo explicativo. |
| Parche dural | `parche dural` si no fue informado; `cierre por planos... parche dural` | Inventar material/evento o ubicarlo luego del cierre. | Si hay durotomia/parche informado, debe ir antes de cierre. |
| Cierre | `cierre.*hemostasia`, `cierre.*recuento`, `piel.*recuento` | Hemostasia y recuento deben preceder cierre por planos/piel. | Usar comparacion de posiciones, no solo regex lineal. |
| Preparacion | Doble `decubito prono`, doble `proteccion ocular`, doble `acolchado` | Repeticion afecta calidad y credibilidad del parte. | Permitir mencion unica y no contar tabla/checklist interna. |

## positive_templates

### Historia clinica - diagnostico puro

```text
Diagnostico: {patologia} {nivel} {lateralidad/topografia si fue informada}.
Indicacion / conducta: {conducta quirurgica o conservadora}, separada del diagnostico.
```

Ejemplo seguro:

```text
Diagnostico: espondilolistesis degenerativa L4-L5 con estenosis de canal.
Indicacion quirurgica: fijacion instrumentada y artrodesis L4-L5, segun correlacion clinico-imagenologica.
```

### Consentimiento - fijacion/artrodesis L4-L5

```text
Se informa procedimiento de fijacion instrumentada y artrodesis L4-L5. La lateralidad, si corresponde, se limita al abordaje, sintomas o maniobra descompresiva especifica, no al segmento fusionado.
```

### Parte quirurgico - hernia extraforaminal

```text
Se realiza abordaje foraminal/extraforaminal {lado} a nivel {nivel}, orientado a la raiz {raiz} segun topografia declarada. No se describe abordaje interlaminar ni flavectomia salvo que el caso lo indique de forma explicita y compatible.
```

### Parte quirurgico - sin descompresion directa

```text
Se efectua fijacion instrumentada y artrodesis {nivel}. No se realizo descompresion neural directa, laminectomia, hemilaminectomia ni flavectomia, de acuerdo con la indicacion registrada.
```

### Parte quirurgico - PLIF / implantes / materiales

```text
Tras la exposicion y preparacion correspondiente, se realiza {PLIF/TLIF} {nivel} con colocacion de {cajas/implantes informados}. Luego se completa fijacion con {tornillos/barras/materiales informados}. Cada implante o material se menciona una vez y con trazabilidad si fue provista.
```

### Parte quirurgico - parche dural y cierre

```text
Ante zona dural expuesta o evento dural informado, se coloca refuerzo/parche dural antes del cierre. Se verifica hemostasia, se realiza recuento de gasas e instrumental y luego cierre por planos y piel.
```

### Canal estrecho

```text
Diagnostico: estenosis de canal lumbar {nivel} con {clinica informada}.
```

## fixture_matrix

| Fixture id | Input sintetico | Documento | Debe pasar | Debe fallar | Gate principal |
|---|---|---|---|---|---|
| `LUM-GATE-001` | Hernia extraforaminal L4-L5 derecha. Microdiscectomia extraforaminal. | parte | `abordaje extraforaminal/foraminal`, `raiz L4 derecha` | `interlaminar`, `flavectomia`, `raiz L5 derecha` | `extraforaminal_no_interlaminar` |
| `LUM-GATE-002` | Hernia L4-L5 derecha sin topografia declarada. | HC/parte | `hernia L4-L5 derecha` sin topografia inventada | `posterolateral`, `extraforaminal`, `fragmento discal` | `no_inventar_topografia` |
| `LUM-GATE-003` | Radiculopatia L5 derecha sin hernia informada. | HC | `radiculopatia L5 derecha` | `hernia`, `fragmento discal`, `secuestro` | `no_inventar_diagnostico_topografia` |
| `LUM-GATE-004` | Espondilolistesis degenerativa L4-L5. | HC | `espondilolistesis degenerativa` | `istmica`, `lisis`, `pars` | `preservar_subtipo_espondilolistesis` |
| `LUM-GATE-005` | Canal estrecho L4-L5 con claudicacion neurogena. | HC/consent | `estenosis de canal L4-L5` | `canal estrecho con compromiso del canal`, `hernia` | `canal_estrecho_no_tautologico` |
| `LUM-GATE-006` | Diagnostico: espondilolistesis degenerativa L4-L5; indicacion: fijacion. | HC | diagnostico separado de indicacion | `diagnostico... con indicacion de fijacion` | `diagnostico_puro_sin_indicacion` |
| `LUM-GATE-007` | Fijacion instrumentada y artrodesis L4-L5 con abordaje derecho. | consentimiento | `fijacion/artrodesis L4-L5`, `abordaje derecho` | `fijacion L4-L5 derecha`, `artrodesis L4-L5 derecha` | `segmento_fusion_sin_lateralidad` |
| `LUM-GATE-008` | Fijacion L4-L5 sin descompresion directa. | parte | `no se realizo descompresion neural directa` | `laminectomia`, `hemilaminectomia`, `flavectomia`, `liberacion directa` | `sin_descompresion_directa_bloqueante` |
| `LUM-GATE-009` | Fijacion L4-L5 con descompresion directa informada. | parte | descompresion directa documentada una vez | `sin descompresion directa` | `respetar_input_descompresion` |
| `LUM-GATE-010` | PLIF L4-L5 con dos cajas y sustituto oseo. | parte | PLIF una vez, cajas y sustituto en orden logico | PLIF duplicado, TLIF no informado, materiales repetidos | `tecnica_implantes_no_duplicados` |
| `LUM-GATE-011` | Parte con parche dural usado como refuerzo sobre zona dural expuesta. | parte | parche/refuerzo antes de cierre | parche luego de cierre; parche sin input | `parche_dural_pre_cierre` |
| `LUM-GATE-012` | Hemostasia completa, recuento correcto, cierre por planos y piel. | parte | hemostasia -> recuento -> cierre | cierre antes de recuento/hemostasia | `orden_hemostasia_recuento_cierre` |
| `LUM-GATE-013` | Parte con posicionamiento y proteccion inicial. | parte | una sola mencion de posicion/protecciones | posicionamiento, proteccion ocular o acolchado duplicados | `no_duplicar_preparacion_inicial` |
| `LUM-GATE-014` | Hernia foraminal L4-L5 derecha. | HC/parte | topografia foraminal y raiz compatible segun tabla aprobada | `extraforaminal` si no se dijo | `topografia_exacta` |
| `LUM-GATE-015` | Parte con PLIF y TLIF simultaneos sin plan combinado. | parte | bloqueo con mensaje de tecnica incompatible | aprobar como tecnica unica | `tecnica_incompatible` |
| `LUM-GATE-016` | Consentimiento hernia lumbar L4-L5. | consentimiento | nivel, procedimiento, riesgos neurologicos, LCR, recidiva, alternativas | consentimiento generico sin nivel/riesgos/alternativas | `consentimiento_especifico` |

## gate_rules

Reglas deterministicos detect-only. Deben operar sobre texto normalizado y, si existe estructura, sobre JSON paths antes de render/guardado.

| Gate | Condicion | Deteccion sugerida | Mensaje de falla |
|---|---|---|---|
| `diagnostico_puro_sin_indicacion` | `$.document.type in ["HC","consentimiento"]` y campo diagnostico existe | En `$.clinical.diagnosis.text`: regex `\\b(con indicacion de|requiere|se indica|conducta quirurgica|instrumentacion|descompresion)\\b` | `Diagnostico contaminado con indicacion/conducta. Separar diagnostico de indicacion.` |
| `no_inventar_diagnostico_topografia` | `$.case.diagnosis.topography_source == "not_available"` | En salida final: regex afirmativa `\\b(hernia (posterolateral|extraforaminal|foraminal)|fragmento discal|secuestro)\\b` sin negacion cercana | `La salida inventa topografia o hallazgo no informado.` |
| `preservar_subtipo_espondilolistesis` | `$.case.diagnosis.subtype == "degenerativa"` | Regex salida `\\b(istmic[ao]|pars|lisis|degenerativa o istmica)\\b` | `El subtipo degenerativo fue mezclado con istmico.` |
| `canal_estrecho_no_tautologico` | `$.case.diagnosis.family == "estenosis_canal"` | Regex `\\b(canal estrecho con compromiso del canal|estenosis de canal con canal comprometido)\\b` | `Redaccion tautologica de canal estrecho.` |
| `segmento_fusion_sin_lateralidad` | `$.procedure.fusion == true` y `$.procedure.levels contains "L4-L5"` | Regex `\\b(fijacion|artrodesis)\\s+L4[- ]L5\\s+(derecha|izquierda)\\b` | `La fijacion/artrodesis es por segmento; mover lateralidad al abordaje/sintoma/descompresion.` |
| `sin_descompresion_directa_bloqueante` | `$.procedure.direct_decompression == "no"` | Regex afirmativa no negada `\\b(laminectomia|hemilaminectomia|flavectomia|liberacion radicular directa|recalibraje)\\b` | `El caso declara sin descompresion directa y la salida describe una.` |
| `extraforaminal_no_interlaminar` | `$.case.diagnosis.subtype == "extraforaminal"` | Regex `\\b(interlaminar|flavectomia|receso lateral|hombro de raiz)\\b` en descripcion del abordaje principal | `Hernia extraforaminal documentada con abordaje/secuencia incompatible.` |
| `extraforaminal_root_table` | `$.case.diagnosis.subtype == "extraforaminal"` y nivel/lado conocido | Tabla: L3-L4 -> L3, L4-L5 -> L4, L5-S1 -> L5; bloquear raiz inferior si aparece como principal | `Raiz no compatible con topografia extraforaminal aprobada.` |
| `tecnica_implantes_no_duplicados` | `$.procedure.interbody_technique in ["PLIF","TLIF"]` o implantes presentes | AST/lista de entidades: conteo de tecnica/material > 1 salvo subtitulo permitido; regex `\\bPLIF\\b` count contextual | `Tecnica o material duplicado/incompatible.` |
| `tecnica_incompatible` | PLIF y TLIF aparecen juntos sin `$.procedure.combined_plan == true` | Entidades normalizadas contiene ambos `PLIF` y `TLIF` | `PLIF y TLIF simultaneos requieren plan combinado explicito.` |
| `parche_dural_pre_cierre` | `$.dural_event.patch_or_reinforcement == "yes"` | Posicion textual `index(parche|refuerzo dural) < index(cierre por planos|cierre de piel)` | `El parche/refuerzo dural debe documentarse antes del cierre.` |
| `no_inventar_parche_dural` | `$.dural_event.patch_or_reinforcement in ["no","not_informed"]` | Regex afirmativa `\\b(parche dural|refuerzo dural|sustituto dural)\\b` | `La salida inventa parche/refuerzo dural no informado.` |
| `orden_hemostasia_recuento_cierre` | `$.document.type == "parte_quirurgico"` | Posiciones: `hemostasia < cierre` y `recuento < cierre`; bloquear `cierre.*(hemostasia|recuento)` | `Hemostasia y recuento deben preceder el cierre por planos/piel.` |
| `no_duplicar_preparacion_inicial` | `$.document.type == "parte_quirurgico"` | Conteos normalizados de `decubito prono`, `proteccion ocular`, `acolchado` > 1 | `Preparacion/posicionamiento duplicado.` |
| `consentimiento_especifico` | `$.document.type == "consentimiento"` | JSON required: `procedure`, `levels`, `main_risks`, `alternatives`; faltantes -> fail | `Consentimiento generico: falta procedimiento, nivel, riesgos o alternativas.` |

## expected_failures

| Caso que debe fallar | Mensaje esperado |
|---|---|
| `Diagnostico: hernia posterolateral derecha con indicacion de instrumentacion` cuando el input solo dice radiculopatia. | `Diagnostico contaminado e inventa topografia no informada.` |
| `Espondilolistesis degenerativa/istmica L4-L5` cuando el Doctor declaro degenerativa. | `Subtipo degenerativo mezclado con istmico.` |
| `Canal estrecho con compromiso del canal` | `Redaccion tautologica de canal estrecho.` |
| `Consentimiento para fijacion L4-L5 derecha` | `La lateralidad no corresponde al segmento fusionado.` |
| `Se realizo hemilaminectomia y flavectomia` en caso `sin descompresion directa`. | `El caso declara sin descompresion directa.` |
| `Hernia extraforaminal L4-L5 derecha tratada por abordaje interlaminar con flavectomia` | `Abordaje/secuencia incompatible para extraforaminal.` |
| `PLIF L4-L5... se completa PLIF L4-L5... TLIF` sin plan combinado. | `Tecnica duplicada o incompatible.` |
| `Cierre por planos. Luego se coloca parche dural.` | `Parche/refuerzo dural despues del cierre.` |
| `Cierre de piel. Hemostasia y recuento correctos.` | `Hemostasia y recuento deben preceder cierre.` |
| Doble parrafo de posicionamiento/proteccion ocular. | `Preparacion inicial duplicada.` |

## integration_plan

1. En la app real canonica `/Users/jarvis/.openclaw/workspace/clinica/app-clinica-medicolegal`, crear rama aislada tipo `clinica/lumbar-inconsistency-gates-v2`.
2. Agregar fixtures sinteticos en `data/derived/clinical_test_cases/lumbar_inconsistency_gates_v2.json`, con los campos: `id`, `document_type`, `input_axes`, `expected_present`, `forbidden_present`, `risk_level`, `gate_ids`, `doctor_correction_source`.
3. Agregar helpers puros en `scripts/qa/validate_lumbar_gate_helpers.js`: normalizacion, deteccion de negaciones cercanas, conteo contextual de entidades, comparacion de posiciones y tabla raiz/topografia aprobada.
4. Crear `scripts/qa/validate_lumbar_inconsistency_gates_v2.js` que pueda validar texto sintetico primero y luego salidas del generador real.
5. Integrar el runner en `scripts/qa/run_clinica_core_qa.js` con modo bloqueante para `critical` y `high`, y modo `needs_review` para reglas legales no revisadas.
6. Colocar los gates antes del render/guardado final de HC, consentimiento y parte quirurgico, no solo como QA posterior.
7. Ejecutar batch minimo antes de tocar plantillas: `LUM-GATE-001`, `003`, `004`, `007`, `008`, `010`, `011`, `012`, `016`.
8. Una vez que el gate falle contra salidas malas conocidas, recien ajustar prompts/plantillas/generador.
9. Verificar regresion: fixtures lumbares previos, route guard, 20/40 pathology scenarios y snapshot clinico.
10. Mantener corpus legal/jurisprudencial como `needs_review` salvo normativa oficial o correccion directa del Doctor convertida a fixture.

## risks / limits

- Los regex deben ser contextuales; una busqueda literal puede marcar como error frases negadas del tipo `no se realizo laminectomia`.
- La tabla de raiz en extraforaminal debe quedar limitada a fixtures aprobados; no universalizar sin revision clinica.
- La app real puede tener paths distintos o runners adicionales; este worker no los modifico.
- Los hard gates deben nacer de correcciones del Doctor, fixtures sinteticos o normativa oficial validada. Jurisprudencia/doctrina amplia debe entrar primero como alerta revisable.
- Un gate demasiado amplio puede bloquear textos correctos; por eso cada regla necesita `doctor_correction_source`, severidad y ejemplo positivo/negativo.

## recommendation

Implementar como primer patch P0 los gates `diagnostico_puro_sin_indicacion`, `no_inventar_diagnostico_topografia`, `segmento_fusion_sin_lateralidad`, `sin_descompresion_directa_bloqueante`, `extraforaminal_no_interlaminar`, `parche_dural_pre_cierre` y `orden_hemostasia_recuento_cierre`. Son los que reducen mas riesgo medico-legal y cubren los errores que el Doctor marco como inaceptables.

Despues agregar duplicados/estilo y corpus backlog. La secuencia correcta es: fixtures que fallan -> helpers detect-only -> gates bloqueantes -> ajuste de generacion -> regresion completa.

## confidence

Alta para la matriz, los ejes y las reglas detect-only porque derivan directamente del workorder y resultados previos del bridge. Media para la ubicacion exacta de integracion hasta que Codex principal inspeccione la app real en la Mac de trabajo.

## evidence_paths

- `jobs/20260525T153318-clinica-lumbar-inconsistency-gates-v2.md`
- `context/fronts/clinica.md`
- `results/20260525T015336-simulacion-clinica-60-casos-columna-inconsistencias.result.md`
- `results/20260525T015336-simulacion-clinica-60-casos-columna-inconsistencias.cases.json`
- `results/20260525T120000-clinica-fixtures-lumbares-v1.result.md`
- `results/20260525T122941-clinica-correcciones-a-fixtures-implementacion.result.md`
- `results/20260525T124545-clinica-corpus-gates-backlog-v2.result.md`
