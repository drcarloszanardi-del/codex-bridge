# Resultado - 20260526T124354-clinica-p0-sin-descompresion-detect-only-plan-v1

## summary

Plan minimo para sumar el segundo P0 `sin_descompresion_directa_bloqueante`: integrarlo como gate detect-only con dos salidas diferenciadas.

- `fail` en QA/fixture y en flujo canonico solo cuando el input declare `direct_decompression=no` y el output afirme un acto de descompresion directa como realizado.
- `needs_review` cuando la frase sea ambigua, historica, planificada, discutida o este fuera de la seccion tecnica operatoria.
- `pass` cuando los terminos aparezcan negados: `no se realizo laminectomia`, `sin flavectomia`, `no hubo liberacion radicular directa`.

No recomiendo tocar plantillas finales ni reescribir texto automaticamente. El patch debe limitarse a fixtures sinteticos, lista estrecha de terminos, helper de afirmacion por oracion/seccion y reporte con contexto local.

## coverage_table

| Fuente permitida | Estado | Uso |
| --- | --- | --- |
| `jobs/20260526T124354-clinica-p0-sin-descompresion-detect-only-plan-v1.md` | Revisada | Contrato del segundo P0, terminos obligatorios y pruebas recientes del primer gate. |
| `results/20260526T111217-clinica-p0-gates-local-integration-review-v1.result.md` | Revisada | Priorizacion original: `sin_descompresion_directa_bloqueante` como segundo P0 critico. |
| `results/20260526T121531-clinica-p0-gates-implementation-review-v1.result.md` | Revisada | Criterio de avanzar solo tras fixtures de negacion/afirmacion del primer gate. |
| `results/20260525T153318-clinica-lumbar-inconsistency-gates-v2.result.md` | Revisada | Matriz `LUM-GATE-008`, frases prohibidas y regla de no inventar tecnica negada. |
| `results/20260525T184100-clinica-lumbar-v2-stress-artifacts-v1.result.md` | Revisada | `GOOD-LUM-005`, `BAD-LUM-007`, readiness 9/10 y trampas de falso positivo/negativo. |
| `protocol.md` | Revisado | Alcance: recomendacion, sin acciones externas, sin datos reales ni decision final. |

## minimal_synthetic_fixtures

Todos los fixtures deben ser sinteticos, sin pacientes reales, sin fechas reales, sin matriculas y sin documentos libres.

| Fixture | Tipo | Input sintetico | Output sintetico | Esperado |
| --- | --- | --- | --- | --- |
| `CLIN-P0-014-no-direct-decompression-bad-laminectomy` | Bad | `procedimiento: fijacion/artrodesis L4-L5. direct_decompression: no.` | `se realiza laminectomia L4-L5 y liberacion radicular directa` | `fail` por laminectomia + liberacion afirmadas. |
| `CLIN-P0-015-no-direct-decompression-good-negated` | Good | `procedimiento: fijacion/artrodesis L4-L5. direct_decompression: no.` | `no se realizo laminectomia, hemilaminectomia, flavectomia ni liberacion radicular directa` | `pass` por negacion local. |
| `CLIN-P0-016-affirmation-after-negation` | Bad | `procedimiento: artrodesis L4-L5. direct_decompression: no.` | `sin descompresion directa planificada. Durante el acto se realiza hemilaminectomia y flavectomia amplia` | `fail`; afirmacion posterior gana sobre negacion anterior. |
| `CLIN-P0-017-discussed-plan-not-performed` | Ambiguous/good | `direct_decompression: no.` | `se discutio laminectomia como alternativa, pero no se realizo descompresion directa` | `pass` o `needs_review`, no hard fail. |
| `CLIN-P0-018-direct-decompression-declared-pass` | Good | `direct_decompression: yes.` | `se realiza laminectomia y foraminotomia directa` | `pass`, porque el input lo declaro. |
| `CLIN-P0-019-recalibraje-bad` | Bad | `direct_decompression: no.` | `se efectua recalibraje del canal y liberacion de recesos laterales` | `fail` por actos afirmados de descompresion directa. |
| `CLIN-P0-020-historical-prior-surgery-review` | Review | `direct_decompression: no; antecedente: cirugia previa no detallada.` | `antecedente referido de laminectomia previa; en este acto no se realizo descompresion directa` | `needs_review` o pass si la seccion antecedente esta claramente separada. |
| `CLIN-P0-021-negation-boundary-bad` | Bad | `direct_decompression: no.` | `no se realizo laminectomia. Se realiza flavectomia y liberacion de receso lateral` | `fail` por afirmacion en nueva oracion. |

Smoke minimo recomendado para el primer patch:

```text
CLIN-P0-014
CLIN-P0-015
CLIN-P0-016
CLIN-P0-018
CLIN-P0-021
```

## affirmed_failure_terms

Estos terminos/procedimientos deben fallar solo si estan afirmados como acto realizado en el documento actual y `direct_decompression=no`:

| Grupo | Terminos/patrones iniciales | Modo |
| --- | --- | --- |
| Laminectomia | `laminectomia`, `laminectomia descompresiva` | `fail` si afirmado. |
| Hemilaminectomia | `hemilaminectomia`, `hemi-laminectomia` | `fail` si afirmado. |
| Flavectomia/ligamento amarillo | `flavectomia`, `reseccion de ligamento amarillo`, `reseccion del ligamento amarillo`, `apertura de ligamento amarillo` | `fail` si afirmado. |
| Liberacion neural directa | `liberacion radicular directa`, `liberacion de raiz`, `liberacion neural directa`, `neurolysis directa` | `fail` si afirmado. |
| Foraminotomia directa | `foraminotomia`, `foraminotomia directa`, `ampliacion foraminal` | `fail` si afirmado, `needs_review` si se menciona como posibilidad. |
| Recesos laterales | `liberacion de recesos laterales`, `descompresion de recesos laterales` | `fail` si afirmado. |
| Recalibraje/canal | `recalibraje`, `recalibraje del canal`, `descompresion del canal` | `fail` si afirmado. |
| Genericos fuertes | `descompresion neural directa`, `descompresion directa`, `descompresion radicular directa` | `fail` si afirmado como realizada; pass si negado. |

Terminos que dejaria inicialmente en `needs_review` si aparecen sin verbo claro de realizacion: `descompresion indirecta`, `descompresion por reduccion`, `liberacion indirecta`, `maniobra indirecta`, porque pueden ser compatibles con artrodesis/fijacion sin descompresion directa.

## negation_controls

Controles que deben pasar:

| Texto | Resultado correcto |
| --- | --- |
| `no se realizo laminectomia ni flavectomia` | No falla. |
| `sin descompresion directa` | No falla. |
| `no hubo hemilaminectomia` | No falla. |
| `no se efectuo liberacion radicular directa` | No falla. |
| `se descarto foraminotomia directa` | No falla. |
| `no se realizo reseccion del ligamento amarillo` | No falla. |

Control que debe fallar:

```text
Sin descompresion directa planificada. Se realiza hemilaminectomia y flavectomia amplia.
```

La negacion no debe cruzar limite de oracion. Un verbo afirmativo de acto realizado en una oracion posterior gana sobre una negacion previa.

## act_performed_vs_history_or_plan

Regla central: bloquear solo actos realizados, no menciones historicas o planes descartados.

| Contexto | Indicadores | Resultado recomendado |
| --- | --- | --- |
| Acto realizado actual | `se realiza`, `se efectua`, `se practica`, `se lleva a cabo`, `se completa`, `se procede a`, `se reseca`, `se libera`, `se descomprime` cerca del termino | `fail` si `direct_decompression=no`. |
| Negacion del acto actual | `no se realizo`, `sin`, `no hubo`, `no se efectuo`, `se descarta` cerca del termino | `pass`. |
| Plan o alternativa | `se considero`, `se discutio`, `planificado`, `alternativa`, `podria requerir` | `needs_review` o pass si queda claro que no fue realizado. |
| Antecedente/historia | `antecedente`, `cirugia previa`, `historia de`, `realizada previamente` | `needs_review` salvo seccion claramente separada y frase actual negada. |
| Indicacion futura | `se indica`, `se planifica`, `eventual`, `en caso de requerir` | No hard fail; `needs_review` si aparece en parte quirurgico final. |
| Titulo/checklist | Heading o item interno no renderizado | Excluir de hard fail si el texto final no lo afirma. |

El helper deberia evaluar por oracion o clausula, devolver `matched_text`, `local_context`, `section`, `affirmation_trigger` y `negation_trigger`.

## recommended_mode

Recomendacion exacta:

```text
Integrar `sin_descompresion_directa_bloqueante` como detect-only con `fail` para fixtures y para afirmaciones claras de acto realizado cuando direct_decompression=no; usar `needs_review` para historico/plan/ambiguedad; no usar report_only como modo unico porque el riesgo clinico-medico-legal es P0.
```

En la practica:

1. En QA sintetico: `BAD` debe fallar y `GOOD` debe pasar.
2. En flujo canonico pre-render: `fail` solo para afirmacion clara de acto realizado.
3. En salida ambigua: `needs_review`, con evidencia, sin auto-rewrite.
4. Tras una corrida verde del core QA con los fixtures nuevos, se puede promover el caso claro a hard fail permanente.

## bounded_patch_plan

Patch minimo para el orquestador:

1. Agregar fixtures `CLIN-P0-014` a `CLIN-P0-021` al archivo sintetico actual o a un archivo `clinical_p0_sin_descompresion_v1.json`.
2. Reusar normalizacion y segmentacion por oracion del primer gate.
3. Agregar helper `findAffirmedDirectDecompressionActs(text, section)` con lista estrecha de terminos y verbos de acto realizado.
4. Agregar helper `isNegatedInSameSentence(match)`; no permitir que la negacion cruce punto/cambio de oracion.
5. Agregar clasificador simple `classifyMentionContext`: `performed`, `negated`, `history`, `plan_or_alternative`, `ambiguous`.
6. Reportar cada match con `fixture_id`, `gate_id`, `severity`, `mode`, `matched_text`, `local_context`, `section`, `classification`.
7. Conectar al core QA despues del primer gate, sin tocar templates finales.
8. Ejecutar:

```bash
node scripts/qa/validate_clinical_p0_gates_v1.js
node scripts/qa/run_clinica_core_qa.js
```

Si el orquestador separa validators, usar un comando especifico `validate_clinical_p0_sin_descompresion_v1.js`, pero mantenerlo dentro del core QA.

## overblocking_risks

| Riesgo | Mitigacion |
| --- | --- |
| Bloquear menciones negadas | Exigir verbo afirmativo y negar solo dentro de la misma oracion/clausula. |
| Bloquear antecedentes quirurgicos previos | Clasificar `antecedente/cirugia previa` como `needs_review`, no hard fail. |
| Bloquear plan discutido pero no ejecutado | Detectar `se discutio/se considero/alternativa` y no hard fail. |
| Confundir descompresion indirecta con directa | Mantener `descompresion indirecta` fuera de fail inicial. |
| Confundir headings/checklists con texto renderizado | Validar texto final o excluir headings internos. |
| Ampliar sinonimos demasiado rapido | Versionar lista de terminos; sinonimos nuevos empiezan como `needs_review`. |
| Falta de estructura/seccion tecnica | Si no hay seccion, aplicar solo a frases con verbos de acto realizado; lo ambiguo va a `needs_review`. |

## recommendation

Siguiente accion unica para el orquestador: agregar el segundo P0 con los fixtures `CLIN-P0-014` a `CLIN-P0-021`, mantenerlo detect-only, y configurar `fail` solo para afirmaciones claras de acto realizado contra `direct_decompression=no`. No tocar templates finales. No sumar todavia `extraforaminal_no_interlaminar` en el mismo patch.

## attempted_routes

- Se hizo `git pull --rebase`.
- Se reclamo el job con `python3 scripts/bridgectl.py claim`.
- Se reviso `jobs/20260526T124354-clinica-p0-sin-descompresion-detect-only-plan-v1.md`.
- Se revisaron las fuentes permitidas: resultados `20260526T111217`, `20260526T121531`, `20260525T153318`, `20260525T184100` y `protocol.md`.
- No se abrio Drive, iCloud, Photos, Gmail, Telegram real, Downloads, ObraCash ni bibliotecas completas.
- No se usaron datos reales de pacientes ni fuentes externas.

## risks_limits

- No se inspecciono codigo real de la app canonica; el plan se basa en el workorder y fuentes del bridge.
- Los fixtures son sinteticos y no reemplazan revision clinica humana.
- La frontera mas delicada es distinguir acto realizado actual vs antecedente/plan; por eso propongo `needs_review` para esas zonas.
- El gate no debe reescribir documentos; solo bloquear o pedir revision con evidencia.
- La promocion a hard fail completo debe depender de core QA verde y de cero falsos positivos en los controles de negacion.

## confidence

Alta para integrar el segundo P0 en modo detect-only con fail para afirmaciones claras, porque las fuentes previas le dan readiness 9/10 y el Doctor marco la regla como critica. Media para sinonimos amplios y contextos historicos/planificados, que deben entrar primero como `needs_review`.

## evidence_paths

- `jobs/20260526T124354-clinica-p0-sin-descompresion-detect-only-plan-v1.md`
- `results/20260526T111217-clinica-p0-gates-local-integration-review-v1.result.md`
- `results/20260526T121531-clinica-p0-gates-implementation-review-v1.result.md`
- `results/20260525T153318-clinica-lumbar-inconsistency-gates-v2.result.md`
- `results/20260525T184100-clinica-lumbar-v2-stress-artifacts-v1.result.md`
- `protocol.md`
