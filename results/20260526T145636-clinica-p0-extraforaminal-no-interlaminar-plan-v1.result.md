---
job_id: 20260526T145636-clinica-p0-extraforaminal-no-interlaminar-plan-v1
worker: personal-xh
status: completed
completed_at: 2026-05-26T15:16:07-03:00
front: CLINICA
no_external_actions: true
no_secrets: true
---

# Resultado - clinica P0 extraforaminal no interlaminar plan v1

## summary

Veredicto: **implementar ahora en modo detect-only/review-only**, sin tocar
plantillas finales. El tercer P0 `extraforaminal_no_interlaminar` esta listo
para entrar como gate estrecho, activado solo cuando el input estructurado declare
`topography=extraforaminal`. La regla no debe inferir topografia desde el output
ni disparar por menciones anatomicas sueltas.

El objetivo clinico es acotado: una hernia extraforaminal no debe quedar redactada
con tecnica principal interlaminar/hemilaminectomia/flavectomia/receso lateral/
hombro de raiz. Lo ambiguo, mixto, historico o negado debe ir a `needs_review`
o `pass`, no a hard fail inicial.

## coverage_table

| Fuente permitida | Estado | Uso |
| --- | --- | --- |
| `jobs/20260526T145636-clinica-p0-extraforaminal-no-interlaminar-plan-v1.md` | Revisada | Workorder, alcance y fixtures exigidos. |
| `results/20260526T131451-clinica-p0-sin-descompresion-implementation-review-v1.result.md` | Revisada | Recomendacion previa de preparar este tercer P0 separado y detect-only. |
| `results/20260526T124354-clinica-p0-sin-descompresion-detect-only-plan-v1.result.md` | Revisada | Patron de gate: fail solo para acto afirmado claro, needs_review para historia/plan/ambiguedad. |
| `results/20260525T173726-clinica-lumbar-fixture-pack-draft-v2.result.md` | Revisada | Fixture `LUM-GATE-001`, terminos prohibidos y raiz esperada para extraforaminal L4-L5. |
| `results/20260525T181000-clinica-lumbar-validator-detect-only-spec-v1.result.md` | Revisada | Contrato del validator, negaciones, spans y riesgos de falso positivo. |
| `protocol.md` | Revisado | Reglas del bridge: sin acciones externas, sin datos reales, resultado como recomendacion. |

## gate_contract

### Aplica

El gate aplica solo si todas estas condiciones son verdaderas:

| Campo | Condicion |
| --- | --- |
| `diagnosis_family` | `hernia` o equivalente estructurado aprobado. |
| `topography` / `subtype` | `extraforaminal` declarado en input, no inferido del output. |
| `document_type` | `parte_quirurgico` o texto tecnico quirurgico final. |
| `generated_text` | Texto final renderizado o texto de fixture sintetico, no checklist interno. |

Cuando aplica, el gate clasifica menciones en el output como:

| Clasificacion | Estado recomendado |
| --- | --- |
| Termino interlaminar afirmado como tecnica principal actual | `fail` en fixture/QA. |
| Termino prohibido negado localmente | `pass`. |
| Termino en plan, historia, anatomia general, revision o tecnica mixta | `needs_review`. |
| Raiz incompatible en fixture aprobado con nivel/lado claro | `needs_review` inicialmente; `fail` solo si el orquestador aprueba tabla acotada. |

### No aplica

El gate no aplica si:

- `topography` no esta informada.
- `topography` es `foraminal`, `central`, `paracentral`, `posterolateral` u otra no
  extraforaminal.
- El documento es historia clinica o consentimiento sin tecnica operatoria final.
- Los terminos aparecen solo en un checklist interno no renderizado.
- El output dice que no se realizo abordaje interlaminar, flavectomia o receso
  lateral.

### Needs review

Debe devolver `needs_review`, con `matched_text` y `local_context`, cuando:

- El output describe abordaje combinado o conversion de abordaje.
- Hay revision quirurgica, cicatriz previa o antecedente donde aparece
  interlaminar/hemilaminectomia.
- El texto menciona raiz distinta sin tabla activa aprobada.
- La frase es nominal sin verbo de acto realizado, por ejemplo
  `hombro de raiz L5 identificado` sin indicar tecnica principal.
- Hay conflicto entre input extraforaminal y texto parcialmente compatible pero
  incompleto.

## forbidden_terms_extraforaminal_only

Lista minima de terminos prohibidos **solo cuando `topography=extraforaminal`** y
la mencion esta afirmada como tecnica principal actual:

| Grupo | Terminos iniciales | Estado inicial |
| --- | --- | --- |
| Abordaje interlaminar | `abordaje interlaminar`, `via interlaminar`, `ventana interlaminar` | `fail` si afirmado como abordaje principal. |
| Hemilaminectomia/laminectomia | `hemilaminectomia`, `hemi-laminectomia`, `laminectomia` | `fail` si afirmado como paso principal de acceso/descompresion. |
| Ligamento amarillo | `flavectomia`, `reseccion del ligamento amarillo`, `apertura del ligamento amarillo` | `fail` si afirmado como tecnica principal. |
| Receso lateral | `receso lateral`, `liberacion de receso lateral`, `descompresion de receso lateral` | `fail` si afirmado como objetivo principal. |
| Hombro de raiz | `hombro de raiz`, `axila de raiz` | `needs_review` por defecto; `fail` solo si el fixture lo acota como incompatible. |

Terminos que no recomiendo poner como hard fail inicial:

- `foraminotomia`: puede aparecer en variantes foraminales/extraforaminales y debe
  quedar en `needs_review` hasta calibrar.
- `liberacion radicular`: demasiado generico; usar solo si se combina con receso
  lateral/interlaminar.
- `microdiscectomia`: puede ser correcta si el abordaje es extraforaminal.

## minimal_synthetic_fixtures

Todos los fixtures deben ser sinteticos, sin datos reales, sin nombres, sin fechas
y sin documentos clinicos libres.

| Fixture | Input sintetico | Output sintetico | Esperado | Motivo |
| --- | --- | --- | --- | --- |
| `CLIN-P0-025-extraforaminal-bad-interlaminar` | `diagnosis_family: hernia; topography: extraforaminal; level: L4-L5; laterality: derecha; document_type: parte_quirurgico` | `Se realiza abordaje interlaminar L4-L5 derecho, hemilaminectomia, flavectomia y liberacion del receso lateral.` | `fail` | Afirma tecnica interlaminar principal incompatible con extraforaminal. |
| `CLIN-P0-026-extraforaminal-good-negated` | `diagnosis_family: hernia; topography: extraforaminal; level: L4-L5; laterality: derecha; document_type: parte_quirurgico` | `Se realiza abordaje extraforaminal derecho. No se realizo abordaje interlaminar, hemilaminectomia, flavectomia ni liberacion de receso lateral.` | `pass` | Terminos prohibidos estan negados localmente y la tecnica principal es extraforaminal. |
| `CLIN-P0-027-non-extraforaminal-not-applicable` | `diagnosis_family: hernia; topography: not_informed; level: L4-L5; laterality: derecha; document_type: parte_quirurgico` | `No se especifica topografia extraforaminal. No se describe abordaje interlaminar.` | `pass` | El gate no debe inferir extraforaminal ni disparar por negacion. |
| `CLIN-P0-028-extraforaminal-root-limited-review` | `diagnosis_family: hernia; topography: extraforaminal; level: L4-L5; laterality: derecha; expected_root_fixture: L4` | `Se identifica y libera raiz L5 derecha durante la reseccion del fragmento extraforaminal.` | `needs_review` | La tabla de raiz debe quedar limitada; no promover a fail hasta aprobacion explicita. |

Fixture opcional si el orquestador quiere frontera extra:

| Fixture | Input sintetico | Output sintetico | Esperado |
| --- | --- | --- | --- |
| `CLIN-P0-029-extraforaminal-mixed-approach-review` | `topography: extraforaminal; revision_surgery: true` | `Se evalua conversion a via interlaminar por anatomia cicatrizal; se completa reseccion por via extraforaminal.` | `needs_review`, no hard fail inicial. |

## validator_output_contract

Cada match debe devolver informacion auditables:

```json
{
  "gate_id": "extraforaminal_no_interlaminar",
  "fixture_id": "CLIN-P0-025-extraforaminal-bad-interlaminar",
  "status": "fail",
  "classification": "performed_primary_technique",
  "matched_text": "abordaje interlaminar",
  "local_context": "Se realiza abordaje interlaminar L4-L5 derecho...",
  "input_topography": "extraforaminal",
  "document_type": "parte_quirurgico"
}
```

Si el output no puede distinguir contexto, debe devolver:

```json
{
  "status": "needs_review",
  "reason": "ambiguous_context_or_mixed_approach"
}
```

## implementation_plan

Patch minimo recomendado:

1. Agregar los fixtures `CLIN-P0-025` a `CLIN-P0-028` al pack sintetico clinico.
2. Implementar helper puro `shouldRunExtraforaminalNoInterlaminar(inputAxes, documentType)`.
3. Reusar normalizacion, segmentacion y negacion del validator lumbar.
4. Agregar `classifyExtraforaminalForbiddenMention(sentence, match)` con salidas
   `performed_primary_technique`, `negated`, `history_or_plan`,
   `mixed_or_ambiguous`, `root_limited_review`.
5. Integrar al core QA como detect-only/review-only.
6. Ejecutar:

```bash
node -c scripts/qa/validate_clinical_p0_gates_v1.js
node scripts/qa/validate_clinical_p0_gates_v1.js
node scripts/qa/run_clinica_core_qa.js
```

7. No tocar plantillas finales.
8. No activar tabla de raiz como hard fail global en este patch.

## false_positive_risks

| Riesgo | Mitigacion |
| --- | --- |
| Bloquear menciones negadas como `sin abordaje interlaminar`. | Negacion local por oracion; fixture `CLIN-P0-026`. |
| Bloquear caso no extraforaminal por texto ambiguo. | Activar solo por input estructurado `topography=extraforaminal`; fixture `CLIN-P0-027`. |
| Bloquear abordaje mixto o conversion justificada. | `needs_review` para `mixed_or_ambiguous`, no hard fail inicial. |
| Bloquear historia quirurgica previa. | Clasificar secciones `antecedente`, `cirugia previa`, `revision`; no hard fail. |
| Bloquear checklist interno. | Validar texto final renderizado o excluir secciones internas. |
| Hard fail por raiz antes de calibrar tabla. | `CLIN-P0-028` queda `needs_review` hasta aprobacion explicita. |

## false_negative_risks

| Riesgo | Mitigacion |
| --- | --- |
| Sinonimos no cubiertos: `ventana interlaminar`, `ligamento amarillo`, `hombro radicular`. | Agregar como `needs_review` primero; promover solo tras fixtures. |
| Frases sin verbo: `flavectomia amplia L4-L5`. | `needs_review` si aparece con topografia extraforaminal. |
| Tecnica principal distribuida en varias oraciones. | Devolver contexto por parrafo y combinar matches cercanos. |
| Topografia extraforaminal esta en texto libre y no en input estructurado. | No inferir en v1; agregar `needs_review_missing_structured_topography` si el orquestador lo desea. |
| Raiz incorrecta no detectada. | Mantener tabla acotada por fixture y sumar gates de raiz en workorder separado si hace falta. |

## recommendation

Recomendacion exacta para el orquestador:

```text
Implementar ahora `extraforaminal_no_interlaminar` como P0 detect-only/review-only, con hard fail solo para `CLIN-P0-025` y equivalentes estrechos: topography=extraforaminal + texto final de parte + afirmacion de tecnica interlaminar principal. Mantener `CLIN-P0-028` como needs_review. No tocar plantillas finales ni activar tabla de raiz global.
```

No bloquear el avance. No ajustaria antes salvo que los controles recientes
`CLIN-P0-022` y `CLIN-P0-023` hayan fallado, cosa que el workorder reporta como
verde en core QA.

## attempted_routes

- Se hizo `git pull --rebase`.
- Se reclamo el job con `python3 scripts/bridgectl.py claim`.
- Se reviso `jobs/20260526T145636-clinica-p0-extraforaminal-no-interlaminar-plan-v1.md`.
- Se revisaron las fuentes permitidas listadas en `coverage_table`.
- No se abrio Drive, iCloud, Photos, Gmail, Telegram real, Downloads, ObraCash ni bibliotecas completas.
- No se usaron datos reales de pacientes ni fuentes externas.

## risks_limits

- No se inspecciono codigo real de la app canonica; el plan queda como contrato
  para implementacion del orquestador.
- Los fixtures son sinteticos y deben seguir asi.
- El gate no debe redactar documentos ni corregir texto: solo detectar, fallar en
  QA sintetico o pedir revision con evidencia.
- La tabla de raiz extraforaminal es sensible; mantenerla limitada a fixtures
  aprobados.
- Si el input estructurado no trae topografia, el gate no debe inferirla desde
  el output en la primera version.

## confidence

Media-alta. Las fuentes previas ya ubicaban `extraforaminal_no_interlaminar`
como critical P0 y el workorder reporta core QA verde tras los controles de
frontera del segundo P0. La cautela principal es la raiz y los abordajes mixtos:
ambos deben arrancar como `needs_review`.

## evidence_paths

- `jobs/20260526T145636-clinica-p0-extraforaminal-no-interlaminar-plan-v1.md`
- `results/20260526T131451-clinica-p0-sin-descompresion-implementation-review-v1.result.md`
- `results/20260526T124354-clinica-p0-sin-descompresion-detect-only-plan-v1.result.md`
- `results/20260525T173726-clinica-lumbar-fixture-pack-draft-v2.result.md`
- `results/20260525T181000-clinica-lumbar-validator-detect-only-spec-v1.result.md`
- `protocol.md`
