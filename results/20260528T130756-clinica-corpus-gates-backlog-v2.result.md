---
job_id: 20260528T130756-clinica-corpus-gates-backlog-v2
worker: personal-xh
status: completed
completed_at: 2026-05-28T13:08:18-03:00
front: CLINICA
no_external_actions: true
no_secrets: true
---

# Resultado - Clinica corpus gates backlog v2

## summary honesto

El corpus medico-legal debe seguir entrando como fabrica de gates verificables, no como texto legal decorativo. Con la evidencia local, la prioridad ya no es descubrir una lista nueva: es ordenar que queda activo en observacion, que falta endurecer con fixtures, y que no debe integrarse hasta tener fuente oficial/versionada y revision humana. Los P0 documentales ya avanzaron en modo detect-only/report-only; el siguiente valor esta en consolidar registry, source requirements y QA de estabilidad antes de convertir cualquier cosa en hard block real.

## coverage_table

| Requisito | Estado | Evidencia |
|---|---|---|
| `gate_backlog` | cubierto | Backlogs corpus 2026-05-26/27 y reviews de P0 documentales. |
| `official_source_requirements` | cubierto | Taxonomia de corpus y regla canonica: ninguna fuente no oficial crea hard gate. |
| `template_impact` | cubierto | Historia clinica, consentimiento, parte quirurgico, export/handoff y corpus registry. |
| `qa_priority` | cubierto | Secuencia de validators, fixtures faltantes y gates en observacion. |
| `do_not_integrate_yet` | cubierto | Jurisprudencia/doctrina no verificada, hard blocks legales y cambios de template sin baseline. |

## evidencia

- `context/fronts/clinica.md` fija que historia clinica, consentimiento y parte quirurgico deben pasar por ruta canonica, manifiesto valido y QA medico-legal.
- `results/20260525T013125-corpus-jurisprudencia-leyes-gates-app-clinica.result.md` define taxonomia, metadatos minimos y conversion de fuente a regla accionable.
- `results/20260527T010224-clinica-corpus-gates-backlog-v2.result.md` prioriza consentimiento especifico, historia minima, diagnostico separado, consistencia, privacidad y trazabilidad.
- Los reviews del 2026-05-27/28 declaran varios gates ya integrados en observacion detect-only/report-only: diagnostico separado, datos sensibles, historia minima, consistencia, ayudantes, hemostasia y trazabilidad de materiales.
- `results/20260527T160545-clinica-consentimiento-source-pack-draft-review-v1.result.md` acepta solo un draft/source-pack de consentimiento, no enforcement real ni hard block.

## inferencia

- El backlog debe distinguir tres estados: `active_observation`, `ready_next_fixture_patch` y `review_queue_only`.
- Las reglas documentales internas y correcciones del Doctor pueden producir findings de QA antes que la jurisprudencia.
- La normativa/jurisprudencia solo debe pasar a hard gate si tiene fuente oficial/versionada, metadatos completos, criterio testeable y aprobacion medico-legal.

## opinion

La tentacion es "sumar corpus"; la mejora real es cerrar el circuito: source item, gate item, fixture, validator, finding redacted y decision de observacion. Sin ese circuito, el corpus aumenta ruido y riesgo.

## gate_backlog

| Prioridad | Gate | Estado recomendado | Plantillas / area | Fuente habilitante | Proxima accion |
|---|---|---|---|---|---|
| P0 | `datos_sensibles_minimizados` | `active_observation` | export, handoff, texto para envio, QA | normativa privacidad + frente clinica | Agregar fixtures de redaccion/anidados y leak-check stdout/stderr. |
| P0 | `diagnostico_separado_de_indicacion` | `active_observation` | historia, parte, consentimiento | correcciones Doctor + criterio documental | Agregar fixtures acentos y `source_fields.diagnosis`. |
| P0 | `historia_clinica_minima_completa` | `active_observation` | historia, prequirurgico | criterio documental + observacion | Agregar fixtures de evolucion parcial, missing agrupado, imagen sin examen y plan pendiente. |
| P0 | `consistencia_diagnostico_indicacion_procedimiento` | `active_observation` | historia, consentimiento, parte | protocolo interno + QA medico | Agregar fixtures de normalizacion nivel/lado, plan pendiente y cross-document. |
| P0 | `no_invencion_hechos_quirurgicos_lumbar` | `active_observation` | parte quirurgico, historia | correcciones Doctor | Mantener como release blocker sintetico; real docs solo report-only hasta aprobacion. |
| P0 | `ayudantes_no_duplican_cirujano` | `active_observation` | parte quirurgico estructurado | documental/protocolo interno | No nuevo ciclo; opcional fixtures de frontera antes de promocion futura. |
| P0 | `secuencia_acto_principal_antes_hemostasia` | `active_observation` | parte quirurgico | protocolo/documentacion quirurgica | Cerrar ciclo; observar findings y mantener separado de recuento/cierre. |
| P1 | `consentimiento_especifico_no_generico` | `source_pack_draft_only` | consentimiento | source-pack draft + futura revision | Activar validator real solo `needs_review/findings_only`; no generar riesgos ni alternativas. |
| P1 | `trazabilidad_implantes_materiales` | `active_observation` | parte quirurgico | protocolo interno + documentacion tecnica | Mantener fixtures 064-068; no hard block real. |
| P1 | `complicacion_manejo_estado_final` | `plan_next_after_registry` | parte, evolucion | documental/protocolo | Preparar fixture pack condicional: complicacion presente exige manejo, estado final y comunicacion si aplica. |
| P1 | `corpus_item_gate_item_schema` | `must_do_before_more_corpus` | corpus, registry, review queue | fuente oficial/versionada o protocolo interno | Implementar schema/registry antes de sumar jurisprudencia. |
| P2 | `jurisprudencia_tematica_advisory` | `review_queue_only` | lenguaje/riesgo | CIJ/JUBA/SAIJ u oficial equivalente, versionado | No hard gate; solo advisory hasta revision legal. |
| P2 | `legibilidad_sin_sobrelegalizar` | `warning_only` | todas | QA editorial | Score de ruido/longitud como warning. |

## official_source_requirements

Estados permitidos:

| Estado | Puede crear hard gate sintetico | Puede bloquear documento real | Requisitos |
|---|---|---|---|
| `official_verified` | Si, con fixture | Solo con aprobacion explicita | Fuente oficial/versionada, jurisdiccion, organismo, fecha, vigencia, criterio testeable y revision legal/clinica. |
| `internal_protocol` | Si, con fixture | No en v1; observacion primero | Correccion del Doctor o protocolo interno con alcance claro, fixture sintetico, no autocompletar contenido. |
| `draft_for_detect_only` | Si, como `needs_review` | No | Source-pack versionado como draft, salida findings-only y sin claim legal. |
| `doctrine_review` | No | No | Separada de ley/fallo; sirve para comentario editorial o advisory. |
| `unverified_do_not_gate` | No | No | Sin fuente oficial, sin vigencia, sin jurisdiccion o sin criterio verificable. |

Metadatos obligatorios por `corpus_item`:

```yaml
source_id:
source_class: official_verified | internal_protocol | draft_for_detect_only | doctrine_review | unverified_do_not_gate
tipo: norma | fallo | doctrina | protocolo_interno | correccion_doctor
jurisdiccion:
organismo_tribunal:
fecha:
estado: vigente | historico | dudoso | derogado_no_usar | draft
tema:
source_path_or_url:
hash_or_version:
hecho_relevante:
criterio_util:
gate_derivado:
plantilla_afectada:
nivel_confianza:
requiere_revision_legal: true|false
review_status: pending | approved_for_advisory | approved_for_gate | rejected
```

Regla de proteccion: si falta `source_class`, `estado`, `source_path_or_url`, `hash_or_version` o `review_status`, el item no puede entrar a `active_gate`. Como maximo queda en `review_queue`.

## template_impact

| Area | Impacto permitido ahora | Impacto prohibido ahora |
|---|---|---|
| Historia clinica | Findings report-only por faltantes minimos, diagnostico contaminado, consistencia y datos sensibles. | Autocompletar diagnostico, plan, examen o fecha; hard block legal. |
| Consentimiento | Source-pack draft, fixtures sinteticos, deteccion de generico/especificidad como `needs_review`. | Reescribir consentimiento, inventar riesgos/alternativas, declarar suficiencia legal. |
| Parte quirurgico | Observacion de hechos inventados, secuencia, ayudantes, implantes/materiales y complicaciones futuras. | Corregir tecnica, agregar material, asumir ayudantes o bloquear documentos reales sin aprobacion. |
| Export/handoff | Privacidad/minimizacion con leak-check y findings redacted. | Enviar por canales externos o guardar identificadores crudos en findings/logs. |
| Corpus medico-legal | Schema + registry + review queue separados. | Mezclar normativa, doctrina, jurisprudencia e inferencia como si tuvieran igual fuerza. |

## qa_priority

1. `validate_corpus_item_gate_registry`: falla si `corpus_item` o `gate_item` no separa oficial, doctrina, protocolo e inferencia.
2. `validate_sensitive_data_minimization`: mantener P0 transversal; agregar fixtures de redaccion/anidados antes de estabilidad.
3. `validate_diagnostico_separado_de_indicacion`: cerrar acentos y campo fuente contaminado.
4. `validate_historia_clinica_minima_completa`: bajar ruido con `document_subtype`, `claims_complete_history` y missing agrupado.
5. `validate_document_consistency_gate`: agregar normalizacion y cross-document cuando existan documentos vinculados.
6. `validate_lumbar_doctor_corrections_v1`: mantener fixtures criticos como release blockers sinteticos.
7. `validate_consentimiento_especifico_no_generico`: siguiente paso solo detect-only real acotado, con source-pack draft y severidad `needs_review`.
8. `validate_trazabilidad_implantes_materiales`: mantener observacion; no nuevo ciclo salvo ruido real.
9. `validate_complicacion_manejo_estado_final`: preparar proximo pack condicional despues del registry.

Comandos esperados en la app canonica cuando Codex principal implemente:

```bash
node -c scripts/qa/validate_clinical_p0_gates_v1.js
node scripts/qa/validate_clinical_p0_gates_v1.js
node scripts/qa/run_clinica_core_qa.js
```

## do_not_integrate_yet

- Jurisprudencia o doctrina como hard gate sin fuente oficial, metadatos completos y revision legal.
- Consentimiento como bloqueo real o declaracion de suficiencia legal.
- Cualquier gate que invente riesgos, alternativas, diagnostico, indicacion, procedimiento, lateralidad, ayudantes o materiales.
- Templates finales modificados sin baseline/ruta canonica/test focal.
- Datos reales o identificadores en fixtures, corpus, findings, logs o QA.
- Reglas que lean `qa_note`, instrucciones, historial o comentarios como cuerpo clinico.
- Autocorreccion de documentos clinicos; los validators reportan, no reescriben.
- Promocion de `report_only` a hard block real sin aprobacion explicita del orquestador/Doctor y evidencia anonimizadora.

## risks / limits

- No se consultaron fuentes externas ni se verifico vigencia normativa; todo este resultado usa evidencia local del bridge.
- Varios estados de implementacion fueron tomados como declaracion del orquestador en resultados previos; no se inspecciono la app canonica desde esta Mac.
- Los gates legales/documentales pueden generar falsos positivos si se aplican a documentos fuera de alcance.
- El primer hardening debe seguir siendo observacional: findings claros, redacted, con evidence paths y sin cambios de plantilla.
- Ruta alternativa si falta fuente oficial: mantener el item como `advisory` o `review_queue_only`, no integrarlo.

## recommendation

Proxima accion unica: implementar o consolidar un `corpus_item/gate_item registry` con estados (`official_verified`, `internal_protocol`, `draft_for_detect_only`, `doctrine_review`, `unverified_do_not_gate`) y conectar ahi los gates ya en observacion. Despues, activar el validator detect-only de consentimiento solo como `needs_review/findings_only`, y preparar el pack condicional de complicaciones. No promover ningun gate a bloqueo real todavia.

## confidence

Media-alta para backlog y orden de QA porque deriva de resultados locales consistentes. Media para estados reales de implementacion porque no se inspecciono la app canonica. Media-baja para cualquier hard gate legal hasta tener fuente oficial vigente y revision humana.

## evidence_paths

- `jobs/20260528T130756-clinica-corpus-gates-backlog-v2.md`
- `context/fronts/clinica.md`
- `results/20260525T013125-corpus-jurisprudencia-leyes-gates-app-clinica.result.md`
- `results/20260525T122941-clinica-correcciones-a-fixtures-implementacion.result.md`
- `results/20260527T010224-clinica-corpus-gates-backlog-v2.result.md`
- `results/20260527T113720-clinica-diagnostico-separado-implementation-review-v1.result.md`
- `results/20260527T123551-clinica-datos-sensibles-implementation-review-v1.result.md`
- `results/20260527T140548-clinica-historia-minima-implementation-review-v1.result.md`
- `results/20260527T150703-clinica-consistencia-implementation-review-v1.result.md`
- `results/20260527T160545-clinica-consentimiento-source-pack-draft-review-v1.result.md`
- `results/20260527T232903-clinica-ayudantes-no-duplicar-implementation-review-v1.result.md`
- `results/20260527T230844-clinica-hemostasia-secuencia-postfixture-review-v2.result.md`
- `results/20260528T000957-clinica-trazabilidad-frontier-implementation-review-v1.result.md`
