---
job_id: 20260527T123551-clinica-datos-sensibles-implementation-review-v1
worker: personal-xh
status: completed
completed_at: 2026-05-27T12:44:00-03:00
front: CLINICA
no_external_actions: true
no_secrets: true
---

# Resultado - Clinica datos sensibles implementation review v1

## summary

Veredicto: **aceptar en observacion con un ajuste chico de fixtures de
redaccion**.

Segun el orquestador, `datos_sensibles_minimizados` fue integrado localmente en
modo detect-only/report-only dentro de `validate_clinical_p0_gates_v1.js`, con
fixtures `CLIN-DOC-PRIV-005` a `CLIN-DOC-PRIV-016`, leak-check sobre el JSON
latest y QA core OK con warning esperado `core_only`. Eso alcanza para
observacion: cubre categorias principales, documentos internos permitidos,
tokens redacted, negacion, edad/fecha clinica y nombre heuristico como frontera.

No recomiendo revertir. El unico ajuste que considero importante antes de
dejarlo estable es reforzar pruebas de **redaccion del output**, no ampliar
patrones. El riesgo mas grave de este gate no es que se escape un fixture
positivo, sino que el propio validator guarde o imprima el identificador crudo
en `matched_text`, `local_context` o logs auxiliares.

## coverage_table

| Fuente | Estado | Uso |
| --- | --- | --- |
| `jobs/20260527T123551-clinica-datos-sensibles-implementation-review-v1.md` | Revisada | Workorder, estado declarado y validaciones locales. |
| `context/fronts/clinica.md` | Revisada | Canon CLINICA y corpus a gates. |
| `results/20260527T120441-clinica-datos-sensibles-minimizados-p0-plan-v1.result.md` | Revisada | Alcance v1, patrones, fixtures y contrato redacted. |
| `results/20260527T113720-clinica-diagnostico-separado-implementation-review-v1.result.md` | Revisada | Gate previo aceptado y secuencia documental P0. |
| `results/20260527T030306-clinica-documental-p0-gates-detect-only-plan-v1.result.md` | Revisada | Contrato base detect-only/report-only. |
| `results/20260527T010224-clinica-corpus-gates-backlog-v2.result.md` | Revisada | Backlog P0 documental y privacidad en exports. |

## risks_p0_p1

| Pri | Riesgo | Tipo | Mitigacion |
| --- | --- | --- | --- |
| P0 | **Fuga por output del validator.** El gate puede detectar bien, pero persistir el valor crudo en `matched_text`, `local_context`, JSON latest, logs o assertion messages. | Fuga de datos | Redactar antes de construir findings; leak-check sobre todo el JSON y sobre stdout/stderr; no guardar `raw_match`. |
| P0 | **Alcance sobre expediente bruto.** Si se evalua todo `source_case` en vez de payload exportado, reporta identificadores internos necesarios y aumenta superficie de fuga. | Falso positivo/fuga | Limitar a `rendered_text`, payload de export/handoff, mensajes y captions; excluir campos fuente no seleccionados. |
| P0 | **Report-only accidentalmente bloqueante.** Por ser P0, puede terminar frenando documentos reales antes de calibracion. | Operativo/legal | Mantener fail solo para fixtures sinteticos; documentos reales producen findings y recomendacion. |
| P1 | **Numeros clinicos confundidos con identificadores.** Niveles, fechas de control, edades, codigos de material o conteos pueden parecer IDs. | Falso positivo | Requerir etiqueta cercana para DNI/HC/afiliado; fechas solo fallan si son nacimiento/DOB/FN. |
| P1 | **Telefonos sin etiqueta vs numeros largos.** Un numero largo puede ser telefono, ID de estudio o artefacto de fixture. | Falso positivo | `fail` con etiqueta telefono/WhatsApp/celular; sin etiqueta usar `needs_review` salvo patron telefonico muy claro. |
| P1 | **Nombre de paciente por heuristica textual.** Puede marcar medico, institucion o texto capitalizado. | Falso positivo | `fail` solo si viene de campo estructurado de paciente; texto libre queda `needs_review`. |
| P1 | **Placeholders incompletos vuelven a disparar.** Variantes como `<PHONE_REDACTED>`, `[dato omitido]` o `anonimizado` pueden no estar whitelisted. | Falso positivo | Ampliar whitelist de tokens redacted con fixture dedicado. |
| P1 | **Canales anidados no evaluados.** Si el payload real usa arrays de mensajes, captions o `export_payload` anidado, el gate puede mirar solo `rendered_text`. | Falso negativo | Fixtures con `messages[*].body`, `attachments[*].caption` y `export_payload.patient_name`. |
| P1 | **Redaccion parcial con multiples categorias.** Local context puede redactar el primer match pero dejar un segundo identificador crudo. | Fuga/falso negativo | Fixture multi-identificador y assertion de ausencia de patrones crudos en todo el finding serializado. |

Con la evidencia disponible no veo P0 conceptual que obligue a revertir: el
orquestador declara leak-check OK y core QA OK. El limite es fuerte: no inspeccione
la app canonica ni el diff real desde el bridge.

## additional_fixtures

Imprescindibles antes de cerrar como estable:

| Fixture | Tipo | Payload sintetico | Esperado |
| --- | --- | --- | --- |
| `CLIN-DOC-PRIV-017-multiple-identifiers-redacted-context` | Positivo/redaccion | Un mismo texto de export con categorias `patient_name`, `dni`, `phone` y `address`, expresadas solo como placeholders en el fixture. | `fail`; `matched_text` y `local_context` deben quedar 100% redacted, sin ningun valor crudo ni segundo identificador sin reemplazar. |
| `CLIN-DOC-PRIV-018-structured-patient-name-export-payload` | Positivo | `export_payload.patient_name=<PATIENT_NAME>` aunque `rendered_text` este minimizado. | `fail` o `needs_review` con `evidence_path=$.export_payload.patient_name`, nunca `pass` silencioso. |
| `CLIN-DOC-PRIV-019-nested-message-and-caption` | Positivo | Identificador placeholder dentro de `messages[*].body` y `attachments[*].caption`. | `fail` con evidence path exacto y output redacted. |
| `CLIN-DOC-PRIV-020-redacted-token-variants-pass` | Negativo | Variantes de placeholder ya anonimizado: `<DNI_REDACTED>`, `<PHONE_REDACTED>`, `[dato omitido]`, `anonimizado`. | `pass`. |

Utiles pero no bloqueantes:

| Fixture | Esperado |
| --- | --- |
| `CLIN-DOC-PRIV-021-clinical-code-not-identifier-pass` con nivel, lado, edad y fecha clinica sintetica sin etiquetas de identidad. | `pass` o `advisory`, no `fail`. |
| `CLIN-DOC-PRIV-022-membership-label-review` con etiqueta ambigua de cobertura sin numero. | `needs_review` o `pass`, no `fail`. |

## accept_adjust_revert

Decision: **aceptar en observacion**.

Condiciones de observacion:

```yaml
accept_observation:
  no_template_changes: true
  report_only_for_real_documents: true
  synthetic_failures_allowed_to_fail_qa: true
  core_qa_ok_declared: true
  leak_check_ok_declared: true
  add_redaction_fixture_patch:
    - CLIN-DOC-PRIV-017-multiple-identifiers-redacted-context
    - CLIN-DOC-PRIV-018-structured-patient-name-export-payload
    - CLIN-DOC-PRIV-019-nested-message-and-caption
    - CLIN-DOC-PRIV-020-redacted-token-variants-pass
```

No conviene revertir porque el set actual ataca el riesgo transversal correcto:
identificadores en exports/handoffs/resumenes/textos para envio. Tampoco conviene
ampliar agresivamente patrones todavia. La calibracion debe ir primero sobre
redaccion, paths anidados y falsos positivos numericos.

## next_p0_documental

Si este gate queda aceptado en observacion, el siguiente P0 documental recomendado
es **`historia_clinica_minima_completa` en detect-only/report-only**, con salida
`needs_review` por defecto y sin hard block legal.

Motivo:

- Es mas estructurable que `consentimiento_especifico_no_generico`, que requiere
  source pack oficial/versionado para definir wording obligatorio.
- Reduce riesgo documental basico: diagnostico, evolucion/sintomas, examen,
  indicacion/plan, profesional, fecha/firma o equivalente.
- Puede arrancar con fixtures sinteticos y campos fuente, reportando ausencias
  sin tocar plantillas finales.

Alcance inicial sugerido:

```yaml
gate_id: historia_clinica_minima_completa
mode: detect_only_report_only
initial_severity: needs_review
applies_to:
  - historia_clinica
  - prequirurgico_handoff
checks_v1:
  - diagnosis_present
  - symptoms_or_evolution_present
  - exam_or_imaging_summary_present
  - indication_or_plan_present
  - professional_and_date_present
does_not_apply_to:
  - public_summary
  - export_minimized
  - consentimiento
```

`consentimiento_especifico_no_generico` queda como siguiente candidato despues
de tener fuente oficial y criterios de wording menos ambiguos. `consistencia`
debe esperar a que diagnostico, indicacion, procedimiento y nivel/lado esten mas
estructurados.

## recommendation

Mantener `datos_sensibles_minimizados` aceptado en observacion, agregar fixtures
`PRIV-017` a `PRIV-020`, y exigir que el leak-check cubra JSON latest completo y
stdout/stderr. Despues, abrir workorder P0 para `historia_clinica_minima_completa`
en modo report-only con severidad inicial `needs_review`.

## confidence

Media-alta para aceptar en observacion porque el estado declarado por el
orquestador coincide con el plan previo, los fixtures esperados y leak-check OK.
Media para certificar implementacion concreta porque no inspeccione la app
canonica ni los archivos reales modificados. Media-baja para cualquier promocion
a hard block legal sin source pack oficial, revision humana y evidencia
anonimizada.

## attempted_routes

- Se hizo `git pull --rebase`.
- Se ejecuto `./scripts/personal_xh_check.sh` y se detecto el job asignado.
- Se creo claim local bajo `claims/`.
- Se reviso el workorder, `context/fronts/clinica.md` y resultados CLINICA
  previos relevantes.
- No se abrio app real, Drive/iCloud/Photos/Gmail, Telegram, datos de pacientes
  ni ObraCash.

## risks_limits

- El resultado local de QA y leak-check fue tomado como declaracion del
  orquestador; no se ejecuto contra la app real desde el bridge.
- No se usaron datos reales ni se imprimieron identificadores reales.
- Los fixtures propuestos deben mantenerse sinteticos y con placeholders.
- Los adjuntos binarios, PDFs, imagenes y OCR siguen fuera de v1 salvo captions
  o texto asociado.

## evidence_paths

- `jobs/20260527T123551-clinica-datos-sensibles-implementation-review-v1.md`
- `claims/20260527T123551-clinica-datos-sensibles-implementation-review-v1.json`
- `context/fronts/clinica.md`
- `results/20260527T120441-clinica-datos-sensibles-minimizados-p0-plan-v1.result.md`
- `results/20260527T113720-clinica-diagnostico-separado-implementation-review-v1.result.md`
- `results/20260527T030306-clinica-documental-p0-gates-detect-only-plan-v1.result.md`
- `results/20260527T010224-clinica-corpus-gates-backlog-v2.result.md`
