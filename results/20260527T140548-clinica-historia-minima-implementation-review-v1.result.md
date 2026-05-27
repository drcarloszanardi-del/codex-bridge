---
job_id: 20260527T140548-clinica-historia-minima-implementation-review-v1
worker: personal-xh
status: completed
completed_at: 2026-05-27T14:12:00-03:00
front: CLINICA
no_external_actions: true
no_secrets: true
---

# Resultado - Clinica historia minima implementation review v1

## summary

Veredicto: **aceptar en observacion con ajustes menores de alcance y ruido**.

Segun el orquestador, `historia_clinica_minima_completa` fue integrado localmente
en modo detect-only/report-only dentro de `validate_clinical_p0_gates_v1.js`,
con fixtures `CLIN-DOC-HC-005` a `CLIN-DOC-HC-014`, y paso
`validate_clinical_p0_gates_v1` + `run_clinica_core_qa` con warning esperado
`core_only`. Eso es aceptable para observacion: cubre faltantes de diagnostico,
sintomas/evolucion, examen/imagenes, plan, profesional/fecha, caso completo,
out-of-scope publico, prequirurgico sin nivel, diagnostico pendiente y negacion.

No recomiendo revertir. El principal riesgo restante no es P0 tecnico, sino
**ruido documental**: marcar como incompleta una nota breve, resumen minimizado,
evolucion parcial o documento que no afirma ser historia clinica completa. Antes
de considerarlo estable, conviene agregar fixtures que validen `document_subtype`
o `claims_complete_history` y que prueben agrupacion de multiples faltantes.

## coverage_table

| Fuente | Estado | Uso |
| --- | --- | --- |
| `jobs/20260527T140548-clinica-historia-minima-implementation-review-v1.md` | Revisada | Workorder, estado declarado y validaciones locales. |
| `context/fronts/clinica.md` | Revisada | Canon CLINICA y corpus a gates. |
| `results/20260527T133621-clinica-historia-clinica-minima-p0-plan-v1.result.md` | Revisada | Alcance, fixtures y contrato del gate. |
| `results/20260527T123551-clinica-datos-sensibles-implementation-review-v1.result.md` | Revisada | Secuencia P0 previa y criterios de observacion. |
| `results/20260527T030306-clinica-documental-p0-gates-detect-only-plan-v1.result.md` | Revisada | Contrato base detect-only/report-only. |
| `results/20260527T010224-clinica-corpus-gates-backlog-v2.result.md` | Revisada | Backlog P0 documental y limites legales. |
| `results/20260527T113720-clinica-diagnostico-separado-implementation-review-v1.result.md` | Revisada | Patron de gate documental aceptado en observacion. |

## risks_p0_p1

| Pri | Riesgo | Tipo | Mitigacion |
| --- | --- | --- | --- |
| P0 | **Promocion accidental a hard block.** Un gate de completitud puede frenar documentos reales por criterios todavia no legalizados. | Operativo/legal | Mantener `needs_review` para documentos reales; `fail` solo si algun fixture sintetico lo exige explicitamente. |
| P0 | **Autocompletado o reescritura de campos faltantes.** El validator podria incentivar llenar diagnostico/plan con texto inferido. | Medico-legal | El gate solo reporta faltantes; no crea contenido ni modifica plantillas finales. |
| P1 | **Aplicacion a documento fuera de alcance.** Public summary, export minimizado, consentimiento o nota breve pueden no tener todos los campos. | Falso positivo/ruido | Activar por `document_type` y, para completitud fuerte, por `metadata.claims_complete_history=true`. |
| P1 | **Nota de evolucion parcial marcada como historia incompleta.** Una evolucion puede documentar solo cambios y plan. | Ruido documental | Agregar `document_subtype=evolucion_parcial` como out-of-scope o `advisory`. |
| P1 | **Examen fisico vs imagenes.** Exigir ambos puede marcar historias validas que solo resumen estudios o teleconsulta. | Falso positivo | Mantener alternativa `exam_or_imaging_summary_present`; no exigir ambos en v1. |
| P1 | **Plan pendiente o diagnostico pendiente.** Casos en estudio pueden no tener diagnostico/plan final. | Falso positivo | Usar `needs_review` acotado y aceptar markers `diagnosis_pending`, `plan_pending` como no-hard-block. |
| P1 | **Ruido por multiples findings.** Un documento muy incompleto puede generar 6 hallazgos repetitivos. | Ruido | Agrupar faltantes por documento con `missing_fields[]` cuando falten tres o mas campos. |
| P1 | **Duplicacion con otros gates.** Diagnostico contaminado o datos sensibles pueden aparecer como faltante o inconsistencia. | Ruido/falso positivo | Este gate solo verifica presencia; calidad/contaminacion queda para `diagnostico_separado_de_indicacion` y privacidad. |
| P1 | **Fechas confundidas.** Fecha de documento vs fecha de nacimiento o fechas clinicas. | Falso positivo/fuga | Buscar `document_date`/version; no leer ni requerir DOB. |
| P1 | **Responsable/profesional demasiado legalista.** Validar matricula real o firma excede v1. | Falso positivo/legal | V1 solo comprueba presencia de responsable placeholder o autor interno, no validez legal. |

No veo P0 conceptual con la evidencia disponible. El limite: no inspeccione la app
canonica ni el diff real; tomo como dato la validacion local declarada por el
orquestador.

## additional_fixtures

Imprescindibles antes de cerrar como estable:

| Fixture | Tipo | Payload sintetico | Esperado |
| --- | --- | --- | --- |
| `CLIN-DOC-HC-015-evolucion-parcial-out-of-scope` | Negativo/frontera | `document_type=historia_clinica; document_subtype=evolucion_parcial; claims_complete_history=false` con solo evolucion y plan. | `pass` o `advisory`, no `needs_review` por todos los campos minimos. |
| `CLIN-DOC-HC-016-multiple-missing-grouped-review` | Positivo/ruido | Historia que declara `claims_complete_history=true` y omite tres o mas campos. | Un finding agrupado `needs_review` con `missing_fields[]`, no spam de hallazgos. |
| `CLIN-DOC-HC-017-imaging-without-exam-pass` | Negativo | Tiene diagnostico, sintomas, imagenes resumidas, plan, profesional y fecha; `exam=null`. | `pass`, porque `exam_or_imaging_summary_present` acepta alternativa. |
| `CLIN-DOC-HC-018-plan-pending-review-not-fail` | Frontera | Diagnostico y evaluacion presentes; `plan_pending=true` o conducta pendiente. | `needs_review`, no `fail` ni autocompletado. |

Utiles pero no bloqueantes:

| Fixture | Esperado |
| --- | --- |
| `CLIN-DOC-HC-019-diagnosis-present-but-contaminated` con diagnostico que contiene indicacion. | Este gate cuenta presencia y deja finding de calidad al gate `diagnostico_separado_de_indicacion`. |
| `CLIN-DOC-HC-020-professional-present-date-missing` | `needs_review` focal solo por fecha/version. |

## accept_adjust_revert

Decision: **aceptar en observacion**.

Condiciones de observacion:

```yaml
accept_observation:
  no_template_changes: true
  report_only_for_real_documents: true
  real_document_severity: needs_review
  synthetic_fixture_assertions_allowed: true
  core_qa_ok_declared: true
  add_noise_control_fixtures:
    - CLIN-DOC-HC-015-evolucion-parcial-out-of-scope
    - CLIN-DOC-HC-016-multiple-missing-grouped-review
    - CLIN-DOC-HC-017-imaging-without-exam-pass
    - CLIN-DOC-HC-018-plan-pending-review-not-fail
```

No conviene revertir porque el set actual cubre la estructura minima y respeta
modo report-only. No conviene promover a hard block hasta tener source pack
oficial, revision medico-legal y calibracion con ejemplos anonimizados.

## next_p0_documental

Si este gate queda aceptado en observacion, el siguiente P0 documental recomendado
es **`consistencia_diagnostico_indicacion_procedimiento` en detect-only/report-only**.

Motivo:

- Ahora ya existen gates para no inventar topografia, separar diagnostico de
  indicacion, minimizar datos sensibles y detectar historia incompleta.
- La siguiente frontera de riesgo es que diagnostico, indicacion, procedimiento,
  nivel/lado y alcance prequirurgico no se contradigan.
- Puede empezar con severidad `needs_review`, fixtures sinteticos y sin fuente
  legal externa amplia.

Alcance inicial sugerido:

```yaml
gate_id: consistencia_diagnostico_indicacion_procedimiento
mode: detect_only_report_only
initial_severity: needs_review
checks_v1:
  - level_consistency_when_present
  - laterality_consistency_when_present
  - procedure_matches_indication_family
  - no_procedure_if_plan_pending_unless_marked
does_not_apply_to:
  - public_summary
  - export_minimized
  - documents_with_missing_core_fields
```

`consentimiento_especifico_no_generico` sigue siendo importante, pero lo dejaria
despues de un source pack oficial/versionado porque el wording legal y la lista
de riesgos/alternativas requieren mas calibracion normativa.

## recommendation

Mantener `historia_clinica_minima_completa` aceptado en observacion, agregar
fixtures `HC-015` a `HC-018`, y exigir que documentos reales sigan en
`needs_review` report-only. Despues, abrir el siguiente workorder P0 para
`consistencia_diagnostico_indicacion_procedimiento` con severidad inicial
`needs_review`.

## confidence

Media-alta para aceptar en observacion porque el estado declarado por el
orquestador coincide con el plan previo y QA local OK. Media para certificar la
implementacion concreta porque no inspeccione la app canonica ni el JSON real de
fixtures. Media-baja para cualquier promocion a hard block legal sin source pack
oficial, revision humana y material anonimizado.

## attempted_routes

- Se hizo `git pull --rebase`.
- Se ejecuto `./scripts/personal_xh_check.sh` y se detecto el job asignado.
- Se creo claim local bajo `claims/`.
- Se reviso el workorder, `context/fronts/clinica.md` y resultados CLINICA
  previos relevantes.
- No se abrio app real, Drive/iCloud/Photos/Gmail, Telegram, datos de pacientes
  ni ObraCash.

## risks_limits

- El resultado local de QA fue tomado como declaracion del orquestador; no se
  ejecuto contra la app real desde el bridge.
- Este resultado usa fixtures sinteticos y placeholders, no datos reales.
- La definicion exacta de historia minima puede variar por documento; por eso v1
  debe conservar alcance estrecho y severidad `needs_review`.
- Cualquier regla legal universal exige fuente oficial y revision humana.

## evidence_paths

- `jobs/20260527T140548-clinica-historia-minima-implementation-review-v1.md`
- `claims/20260527T140548-clinica-historia-minima-implementation-review-v1.json`
- `context/fronts/clinica.md`
- `results/20260527T133621-clinica-historia-clinica-minima-p0-plan-v1.result.md`
- `results/20260527T123551-clinica-datos-sensibles-implementation-review-v1.result.md`
- `results/20260527T030306-clinica-documental-p0-gates-detect-only-plan-v1.result.md`
- `results/20260527T010224-clinica-corpus-gates-backlog-v2.result.md`
- `results/20260527T113720-clinica-diagnostico-separado-implementation-review-v1.result.md`
