# Resultado - 20260526T111217-clinica-p0-gates-local-integration-review-v1

## summary

Revision local de los resultados previos de CLINICA P0. Recomendacion ejecutable: conectar primero el gate `no_inventar_diagnostico_topografia` a la app canonica, en modo detect-only con fixture sintetico negativo/positivo, y hacerlo bloquear salida mala antes de renderizar o entregar cualquier documento final.

El motivo es simple: es el gate con mayor impacto transversal y menor dependencia externa. Protege historia clinica, consentimiento y parte quirurgico contra diagnosticos, niveles, lateralidad, abordajes, fragmentos, indicaciones o hechos operatorios que no fueron informados. No requiere corpus legal fuerte, no necesita pacientes reales y se puede probar con strings sinteticos.

La segunda linea debe ser el paquete lumbar de tecnica/secuencia: `sin_descompresion_directa_bloqueante`, `extraforaminal_no_interlaminar`, `orden_hemostasia_recuento_cierre` y `parche_dural_pre_cierre`. Recomiendo no tocar plantillas finales hasta que estos gates pasen en runner local con evidencia de fixture.

## coverage_table

| Fuente permitida | Estado | Uso |
| --- | --- | --- |
| `results/20260525T153318-clinica-lumbar-inconsistency-gates-v2.result.md` | Revisada | Taxonomia de inconsistencias, regla de trazabilidad y primeras prioridades criticas. |
| `results/20260525T173726-clinica-lumbar-fixture-pack-draft-v2.result.md` | Revisada | Fixtures sinteticos LUM-GATE y campos esperados/prohibidos. |
| `results/20260525T181000-clinica-lumbar-validator-detect-only-spec-v1.result.md` | Revisada | Contrato de validator puro, deterministico, con spans/contexto y manejo de negacion. |
| `results/20260525T184100-clinica-lumbar-v2-stress-artifacts-v1.result.md` | Revisada | Pruebas good/bad y readiness para hard fail inicial. |
| `results/20260525T221902-clinica-lumbar-regression-pack-from-prior-results-v1.result.md` | Revisada | Pack de regresion portable con fallas criticas conocidas. |
| `results/20260525T224750-clinica-v2-gates-next-hardening-audit-v1.result.md` | Revisada | Hard fail lot reducido y gates que deben quedar como report_only. |
| `results/20260526T001920-clinica-corpus-gates-hardening-v3.result.md` | Revisada | Separacion entre gates clinicos internos y corpus medico-legal fuerte. |
| `results/20260526T063207-clinica-correcciones-a-fixtures-implementacion.result.md` | Revisada | Plan de integracion por capas y fixtures derivados P0. |
| `results/20260526T064839-clinica-corpus-gates-backlog-v2.result.md` | Revisada | Backlog P0 documental/corpus y protecciones de fuente oficial. |
| `protocol.md` | Revisado | Alcance del worker: recomendacion, sin acciones externas ni decision final. |

## top_5_p0_gates

| Rank | Gate P0 | Impacto clinico medico-legal | Por que entra en P0 |
| ---: | --- | --- | --- |
| 1 | `no_inventar_diagnostico_topografia` | Muy alto | Evita que el sistema agregue diagnostico, subtipo, topografia, lateralidad, fragmento, indicacion o abordaje no informado. Afecta todos los documentos. |
| 2 | `sin_descompresion_directa_bloqueante` | Muy alto | Si el input niega descompresion directa, el parte no puede afirmar laminectomia, hemilaminectomia, flavectomia o liberacion directa. Documentar una tecnica no realizada es riesgo critico. |
| 3 | `extraforaminal_no_interlaminar` | Alto | En hernia extraforaminal, bloquear lenguaje interlaminar incompatible reduce error anatomico y tecnico. Debe correr junto a control limitado de raiz cuando el nivel/lado esta claro. |
| 4 | `orden_hemostasia_recuento_cierre` | Alto | En parte quirurgico, cierre cutaneo antes de hemostasia/recuento es una secuencia medico-legal mala. Debe limitarse a seccion tecnica para no sobreactuar resumenes. |
| 5 | `parche_dural_pre_cierre` | Alto, condicional | Si hay parche/plastica dural, debe aparecer antes del cierre. Si no se informo evento dural, no debe inventarlo. Es P0 por riesgo de complicacion mal documentada. |

`extraforaminal_root_table_limited` queda recomendado como assert acoplado al gate 3 para casos muy cerrados, por ejemplo L4-L5 derecho con raiz esperada explicita. No lo pondria como primer hard fail global porque es mas sensible a convenciones anatomicas y a redaccion de hallazgos.

## first_gate_to_integrate

Integrar primero `no_inventar_diagnostico_topografia`.

Razones:

1. Tiene el mayor radio de proteccion: historia clinica, consentimiento informado y parte quirurgico.
2. No depende de jurisprudencia, fuentes oficiales externas ni corpus legal fuerte.
3. Es testeable con fixtures sinteticos simples: input declara A, output no puede inventar B.
4. Reduce el riesgo raiz que despues alimenta otros errores: una topografia inventada puede disparar tecnica, raiz, lateralidad y consentimiento incorrectos.
5. Permite un modo detect-only muy transparente: cada failure debe mostrar `gate_id`, `forbidden_present`, span/contexto y evidencia del input que falta.

Estado recomendado inicial:

```text
CLINICA_P0_GATES_DETECT_ONLY=1
CLINICA_P0_GATES_HARD_FAIL=no_inventar_diagnostico_topografia
```

No recomiendo auto-reescritura libre. Si falla, bloquear o marcar `needs_review` con evidencia y devolver al orquestador/local UI.

## minimal_synthetic_fixtures

Todos los fixtures son ficticios, sin pacientes reales, sin matriculas, sin fechas reales y sin datos identificables.

| Fixture | Input sintetico minimo | Output malo que debe fallar | Gate esperado |
| --- | --- | --- | --- |
| `CLIN-P0-001-no-inventar-topografia` | `diagnostico: hernia discal L4-L5 derecha. topografia: no informada.` | `hernia extraforaminal/posterolateral L4-L5 derecha con fragmento migrado` | `no_inventar_diagnostico_topografia` |
| `CLIN-P0-002-radiculopatia-no-hernia` | `diagnostico: radiculopatia L5 derecha. hernia: no informada.` | `hernia discal extruida L4-L5 derecha` | `no_inventar_diagnostico_topografia` |
| `CLIN-P0-003-sin-descompresion-directa` | `procedimiento: artrodesis/fijacion L4-L5. descompresion directa: no.` | `se realizo laminectomia, flavectomia y liberacion directa` | `sin_descompresion_directa_bloqueante` |
| `CLIN-P0-004-extraforaminal-l45-derecha` | `hernia extraforaminal L4-L5 derecha. raiz esperada informada: L4.` | `abordaje interlaminar L4-L5 con liberacion de raiz L5` | `extraforaminal_no_interlaminar` + assert limitado de raiz |
| `CLIN-P0-005-cierre-antes-recuento` | `parte quirurgico tecnico con hemostasia y recuento requeridos.` | `cierre de piel. luego se realizo hemostasia y recuento` | `orden_hemostasia_recuento_cierre` |
| `CLIN-P0-006-parche-dural-after-close` | `evento dural: si. parche/plastica: si.` | `cierre por planos. posteriormente se coloco parche dural` | `parche_dural_pre_cierre` |
| `CLIN-P0-007-negacion-control` | `descompresion directa: no.` | `no se realizo laminectomia ni flavectomia` | Debe pasar; control de negacion. |
| `CLIN-P0-008-good-minimal` | `hernia L4-L5 derecha sin topografia informada; output conserva solo hernia L4-L5 derecha` | Sin terminos prohibidos | Debe pasar; control positivo. |

Representacion sugerida por fixture:

```json
{
  "id": "CLIN-P0-001-no-inventar-topografia",
  "document_type": "any_clinical_document",
  "source_type": "synthetic",
  "input_axes": {
    "diagnosis": "hernia discal L4-L5 derecha",
    "topography": "not_provided"
  },
  "expected_present": ["hernia discal L4-L5 derecha"],
  "forbidden_present": ["extraforaminal", "posterolateral", "fragmento migrado", "secuestro"],
  "gate_ids": ["no_inventar_diagnostico_topografia"],
  "expected_status": "fail"
}
```

## acceptance_criteria

Aceptar la primera integracion si se cumple todo esto:

1. El runner local puede ejecutar los fixtures P0 sin abrir datos reales ni bibliotecas personales.
2. `CLIN-P0-001` y `CLIN-P0-002` fallan con `no_inventar_diagnostico_topografia`.
3. `CLIN-P0-008` pasa sin hard failure.
4. Cada failure incluye `fixture_id`, `gate_id`, `severity`, `matched_text`, `span` o contexto breve, `document_section` si aplica y razon en lenguaje verificable.
5. La negacion no dispara falsos positivos: `no se realizo laminectomia` no falla como laminectomia afirmada.
6. El gate falla antes de render/export/envio de documento final.
7. El exit code del comando de QA es no-cero si un fixture bad no falla o si un fixture good falla.
8. El resultado no agrega texto clinico alternativo; solo bloquea o marca revision con evidencia.

Fallo de aceptacion:

- Un fixture bad pasa sin warning/failure.
- Un fixture good/negado queda bloqueado.
- El failure no explica que texto gatillo la regla.
- El gate toca templates finales o reescribe contenido sin una decision explicita del orquestador.
- El runner requiere pacientes reales, carpetas personales, Drive/iCloud/Photos/Gmail/Telegram o corpus legal no revisado.

## patch_plan_acotado

Plan de parche local para el orquestador, sin editar plantillas finales a ciegas:

1. Ubicar el punto canonico donde la app ya produce `draft_text` o `structured_output` antes del render final.
2. Agregar un modulo puro de QA, por ejemplo `clinicalP0Gates`, sin dependencias externas y sin IO salvo lectura de fixtures sinteticos locales.
3. Crear fixtures bajo una carpeta de tests de la app real, no en datos productivos. Usar ids `CLIN-P0-*`.
4. Implementar helpers chicos:
   - `normalizeClinicalText(text)`
   - `findAffirmedTerms(text, terms, negationWindow)`
   - `findForbiddenIfInputMissing(inputAxes, generatedText)`
   - `compareOrderInTechnicalSection(text, beforeTerms, afterTerms)`
5. Wire inicial solo para `no_inventar_diagnostico_topografia` como hard fail. Dejar los otros cuatro en `report_only` o `needs_review` hasta ver la tasa de falso positivo.
6. Agregar comando local:

```bash
npm run qa:clinica:p0-gates
```

o el equivalente que ya exista en la app canonica.

7. Bloquear salida final si `hard_fail.length > 0`; no modificar el texto automaticamente.
8. Registrar reporte QA con gate, fixture, contexto y recomendacion para el orquestador.
9. Recien despues de verde local, conectar el gate al flujo real detras de feature flag.

Orden de commits sugerido:

1. Fixtures sinteticos.
2. Validator puro + tests unitarios.
3. Runner local.
4. Hook pre-render con feature flag.
5. Cambio de hard fail solo para `no_inventar_diagnostico_topografia`.

## overblocking_false_positive_risks

| Riesgo | Ejemplo | Mitigacion |
| --- | --- | --- |
| Negacion mal interpretada | `no se realizo laminectomia` | Ventana de negacion y test `CLIN-P0-007`. |
| Texto en antecedentes o diagnostico diferencial | `se descarta hernia extraforaminal` | Gate debe distinguir afirmacion vs descarte. |
| Seccion equivocada | Orden de cierre citado en resumen o indicacion, no tecnica | Limitar gates de secuencia a seccion tecnica del parte. |
| Sinonimos clinicos incompletos | `abordaje paramediano` vs `interlaminar` | Empezar con lista estrecha y ampliar solo con fixtures. |
| Raiz esperada discutible | L4/L5 segun convencion o redaccion | Mantener `extraforaminal_root_table_limited` como assert acoplado y no global. |
| Consentimiento demasiado generico bloqueado por estilo | Texto breve pero valido | Mantener gates de consentimiento especifico como P0 separado, no mezclado con el primer gate. |
| Corpus legal sin revision | Fallos/doctrina usados como regla fuerte | Mantener `review_queue`; no convertir a hard fail sin fuente oficial y revision. |
| Duplicados esteticos | Repeticiones de preparacion/hemostasia | Usar warning/report_only hasta calibrar. |

## no_promover_aun

No recomiendo promover a hard fail inicial:

- Jurisprudencia o doctrina sin fuente oficial, vigencia y revision.
- Gates de estilo o longitud.
- `consentimiento_especifico_columna_v1` como primer gate global, aunque sea importante, porque requiere matriz documental mas amplia.
- `tecnica_implantes_no_duplicados` como hard fail inicial, porque puede sobreactuar por sinonimos o listados de material.
- Cualquier regla que reescriba automaticamente diagnostico, indicacion o tecnica.

## recommendation

El orquestador deberia conectar primero `no_inventar_diagnostico_topografia` en modo hard fail local, con los fixtures `CLIN-P0-001`, `CLIN-P0-002` y `CLIN-P0-008` como smoke suite minima. El flujo correcto es: generar draft, correr validator, bloquear si hay invencion no trazable, mostrar evidencia, y no renderizar documento final.

En el mismo patch se pueden dejar preparados como `report_only` los gates `sin_descompresion_directa_bloqueante`, `extraforaminal_no_interlaminar`, `orden_hemostasia_recuento_cierre` y `parche_dural_pre_cierre`. Subirlos a hard fail solo cuando pasen controles good/bad y negacion.

## attempted_routes

- Se hizo `git pull --rebase`.
- Se inspecciono el job `jobs/20260526T111217-clinica-p0-gates-local-integration-review-v1.md`.
- Se revisaron las diez fuentes permitidas por el job, incluyendo `protocol.md`.
- No se abrio Drive, iCloud, Photos, Gmail, Telegram real, Downloads, ObraCash ni bibliotecas completas.
- No se usaron datos reales de pacientes ni fuentes externas.

## risks_limits

- Esta recomendacion no revisa la app canonica real; el orquestador debe mapear nombres de rutas/modulos a su repo local.
- La activacion inicial debe ser con feature flag y fixtures sinteticos, porque los helpers de negacion y seccion pueden necesitar calibracion.
- `extraforaminal_root_table_limited` tiene alto valor pero mayor riesgo de falso positivo si se globaliza; conviene mantenerlo limitado.
- Los gates medico-legales derivados de jurisprudencia/corpus deben permanecer como backlog/review queue hasta fuente oficial y revision.
- El resultado es detect-only/review-only: no redacta documentos clinicos ni propone auto-rewrite libre.

## confidence

Alta para integrar primero `no_inventar_diagnostico_topografia`, porque aparece consistentemente como gate critico en los resultados previos, tiene fixtures simples y no depende de corpus externo. Media-alta para el orden del resto de P0, porque requiere ver el punto exacto de integracion y la estructura de secciones de la app canonica.

## evidence_paths

- `jobs/20260526T111217-clinica-p0-gates-local-integration-review-v1.md`
- `results/20260525T153318-clinica-lumbar-inconsistency-gates-v2.result.md`
- `results/20260525T173726-clinica-lumbar-fixture-pack-draft-v2.result.md`
- `results/20260525T181000-clinica-lumbar-validator-detect-only-spec-v1.result.md`
- `results/20260525T184100-clinica-lumbar-v2-stress-artifacts-v1.result.md`
- `results/20260525T221902-clinica-lumbar-regression-pack-from-prior-results-v1.result.md`
- `results/20260525T224750-clinica-v2-gates-next-hardening-audit-v1.result.md`
- `results/20260526T001920-clinica-corpus-gates-hardening-v3.result.md`
- `results/20260526T063207-clinica-correcciones-a-fixtures-implementacion.result.md`
- `results/20260526T064839-clinica-corpus-gates-backlog-v2.result.md`
- `protocol.md`
