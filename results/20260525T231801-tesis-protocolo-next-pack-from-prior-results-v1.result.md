---
id: 20260525T231801-tesis-protocolo-next-pack-from-prior-results-v1
job_id: 20260525T231801-tesis-protocolo-next-pack-from-prior-results-v1
created_at: 2026-05-25T23:21:18-03:00
created_by: personal-xh
worker: personal-xh
status: completed
no_external_actions: true
no_secrets: true
---

# Resultado - TESIS protocolo next pack from prior results

## summary

Paquete ejecutivo para que el orquestador avance el frente tesis sin abrir Drive, documentos personales ni tocar el borrador base. La tesis debe quedar en modo `template_only` hasta confirmar cuatro decisiones: pregunta de investigacion, unidad de analisis, outcome primario y rol del video.

La accion segura ahora es preparar o completar plantillas vacias, decision log, diccionario de variables, protocolo de recoleccion, matriz bibliografica y registro de faltantes. No corresponde reescribir metodo, resultados, discusion ni conclusiones hasta tener datos anonimizados, bibliografia verificada y decision log.

## source_counts

| Fuente permitida | Estado | Uso |
|---|---:|---|
| `results/20260525T124718-tesis-protocolo-datos-y-material-audiovisual.result.md` | Revisada | Uso del video como contexto, limites eticos y protocolo de datos. |
| `results/20260525T170712-tesis-protocolo-datos-next-actions-v1.result.md` | Revisada | Candidatos de variables, sesgos, faltantes y acciones siguientes. |
| `results/20260525T173727-tesis-empty-template-pack-v1.result.md` | Revisada | Templates vacios y headers seguros. |
| `results/20260525T181001-tesis-decision-brief-variable-candidates-v1.result.md` | Revisada | Cuatro decisiones y tabla de variables candidatas. |
| `results/20260525T184101-tesis-protocolo-decision-gate-pack-v1.result.md` | Revisada | Gate metodologico para bloquear borrador y carga de datos. |
| `results/20260525T021049-tesis-research-ops-protocol-v1.result.md` | Revisada | Research ops, matriz bibliografica y decision log. |
| `context/fronts/tesis.md` | Ausente | Sin uso. |
| `protocol.md` | Revisado | Reglas del bridge y decision final del orquestador. |

## decision_table

| Decision | Estado recomendado | Accion Codex | Requiere Doctor/tutor |
|---|---|---|---|
| Pregunta de investigacion | Pendiente bloqueante | Preparar campo en `HANDOFF.md`; no formular definitiva. | Si. |
| Unidad de analisis | Pendiente bloqueante | Proponer opciones operativas: paciente, procedimiento, nivel, episodio, video, documento. | Si. |
| Outcome primario | Pendiente bloqueante | Listar variables candidatas; no cargar valores. | Si. |
| Rol del video | Pendiente bloqueante | Mantener default `contexto_tecnico_restringido`. | Si. |
| Diccionario de variables | Draft permitido | Crear `variables.md` con definiciones candidatas y estado `pendiente_aprobacion`. | Validacion humana antes de datos. |
| Bibliografia | Matriz vacia permitida | Crear columnas de verificacion; no inventar citas. | Tutor/Doctor define bibliografia clave. |
| Borrador base | Bloqueado | No tocar ni proponer patch directo. | Desbloqueo posterior con gate. |

## variables_core

Variables minimas para preparar el protocolo, no para cargar datos aun:

| variable_name | Tipo | Fuente permitida | Regla |
|---|---|---|---|
| `case_id` | controlled_text | decision humana | Identificador anonimo interno. |
| `unit_of_analysis` | categorical | `HANDOFF.md` | Debe coincidir con decision humana. |
| `procedure_id` | controlled_text | parte anonimo | Solo si unidad es procedimiento o episodio. |
| `period_bucket` | categorical | registro anonimizado | Usar rango amplio, no fecha exacta identificable. |
| `primary_diagnosis_group` | categorical | fuente clinica primaria anonima | No inferir diagnostico ausente. |
| `spinal_region` | categorical | parte, imagen o fuente primaria anonima | Cervical, toracica, lumbar, sacra. |
| `level_or_levels` | controlled_text | parte o imagen anonima | Formato estable, por ejemplo `L4-L5`. |
| `side` | categorical | fuente primaria anonima | Derecha, izquierda, bilateral, no aplica, no documentado. |
| `procedure_type` | categorical | parte quirurgico anonimizado | Lista cerrada aprobada. |
| `primary_outcome_value` | segun outcome | fuente clinica primaria | No usar hasta definir outcome. |
| `follow_up_duration_group` | ordinal | seguimiento anonimizado | Rango aprobado. |
| `source_quality` | ordinal | revision interna | Alta, media, baja, conflicto. |
| `missing_data_reason` | categorical | missing log | No documentado, no aplica, conflicto, pendiente. |

## variables_optional

Variables utiles solo si la pregunta final las necesita:

| variable_name | Uso | Condicion |
|---|---|---|
| `age_band` | Covariable baseline | Usar rangos si hay riesgo de identificacion. |
| `sex` | Covariable baseline | Valores cerrados y regla de no documentado. |
| `symptom_duration_group` | Severidad basal | Solo si esta documentado de forma consistente. |
| `prior_treatment_group` | Confusor clinico | Requiere fuente primaria. |
| `comorbidity_flag` | Confusor | Solo si relevante y disponible. |
| `approach_type` | Variable tecnica | No inferir desde video si fuente primaria no confirma. |
| `direct_decompression` | Variable tecnica | Debe respetar negaciones explicitas. |
| `implant_or_instrument_context` | Contexto tecnico | Marca/modelo solo con fuente primaria. |
| `pain_or_function_score` | Outcome secundario | Requiere escala y momento definidos. |
| `neurologic_status_change` | Outcome secundario | Requiere ventana temporal y fuente. |
| `complication_flag` | Outcome secundario | Definir evento y periodo. |
| `reoperation_flag` | Outcome secundario | Definir periodo. |
| `bibliographic_support_status` | Control bibliografico | Verificado, pendiente o no requiere. |

## data_collection_protocol

1. Crear o actualizar `HANDOFF.md` con pregunta, objetivo, poblacion, unidad de analisis, outcome primario y rol del video.
2. Crear `variables.md` con nombre, definicion operacional, tipo, valores permitidos, fuente, regla de faltantes y quality check.
3. Crear `data_collection_sheet.csv` vacio con columnas: `case_id`, `unit_id`, `unit_of_analysis`, `source_origin`, `source_reference`, `variable_name`, `value_raw`, `value_normalized`, `review_status`, `quality_flag`, `notes_non_sensitive`.
4. Crear `missing_data_log.csv` vacio con: `case_id`, `unit_id`, `variable_name`, `missing_type`, `source_checked`, `action`, `decision_id`, `review_status`.
5. Crear `bibliography_matrix.csv` vacio con: `reference_id`, `citation_full`, `study_type`, `population`, `outcome`, `bias_notes`, `use_in_thesis`, `verification_status`.
6. Crear `decision_log.md` y registrar cada cambio de pregunta, variable, criterio, fuente, rol del video o bibliografia.
7. Mantener video como `contexto_tecnico_restringido` salvo decision explicita distinta. Si pasa a fuente secundaria, solo marca `requiere_confirmacion`; si pasa a fuente formal, exige protocolo, permisos y anonimizado.
8. No cargar datos hasta completar cuatro decisiones y variables operacionales.

## bias_and_quality_risks

| Riesgo | Impacto | Control |
|---|---|---|
| Sesgo de seleccion | Casos con mejor documentacion o videos pueden parecer representativos. | Registrar universo elegible y motivos de exclusion. |
| Cambiar criterios luego de ver datos | Sesgo post hoc. | Decision log obligatorio antes de cargar. |
| Video como evidencia excesiva | Clips parciales pueden inducir conclusiones no medidas. | Video como contexto salvo protocolo aprobado. |
| Faltantes tratados como negativos | Distorsiona resultados. | `no documentado` nunca equivale a `no`. |
| Conflicto entre fuentes | Parte, historia, imagen o video pueden discrepar. | Prioridad de fuentes y decision log. |
| Bibliografia incompleta | Argumentos debiles o citas falsas. | Matriz con `verification_status=verified` antes de citar. |
| Mezclar unidades | Paciente, procedimiento, nivel y video tienen denominadores distintos. | Elegir una unidad primaria y registrar subunidades. |
| Privacidad/metadatos | Material audiovisual o documentos pueden contener identificadores. | No subir ni exponer; trabajar local y anonimizado. |

## do_not_touch_draft_rules

- No reescribir hipotesis, objetivos, metodo, resultados, discusion ni conclusiones.
- No agregar citas, referencias ni argumentos bibliograficos no verificados.
- No declarar N, resultados, aprobaciones, permisos ni follow-up.
- No incorporar conclusiones derivadas de videos.
- No cambiar criterios de inclusion/exclusion despues de ver datos.
- No mezclar unidad paciente/procedimiento/nivel/video sin denominador explicito.
- No cargar datos reales en plantillas hasta que el gate metodologico este en `data_ready`.

## next_orchestrator_actions

1. Crear o actualizar `HANDOFF.md` en modo vacio con las cuatro decisiones.
2. Pedir al Doctor solo: pregunta, unidad de analisis, outcome primario y rol del video.
3. Volcar la respuesta en `decision_log.md`.
4. Crear `variables.md` como draft con `variables_core` y estado `pendiente_aprobacion`.
5. Crear headers vacios para `data_collection_sheet.csv`, `missing_data_log.csv` y `bibliography_matrix.csv`.
6. Implementar o correr el gate metodologico antes de cualquier `edit_base_draft`.
7. Cuando el gate pase a `data_ready`, cargar solo datos anonimizados y trazables.
8. Preparar patch al borrador solo despues de datos, bibliografia y decision log.

## questions_for_doctor_only_if_needed

Usar solo si el orquestador no tiene ya estas respuestas:

```text
Doctor, para avanzar la tesis sin tocar el borrador necesito confirmar:
1. Pregunta de investigacion en una frase:
2. Unidad de analisis: paciente / procedimiento / nivel / episodio / video / documento:
3. Outcome primario medible:
4. Rol del video: contexto tecnico / fuente secundaria / fuente formal / no usar:
```

## risks_limits

- No se abrio Drive, iCloud, Photos, Zotero ni documentos personales.
- No se reviso el borrador base ni bibliografia original.
- No se cargaron datos reales ni sensibles.
- Las variables son candidatas y dependen de la pregunta final.
- Si el diseno final no es observacional, el protocolo debe ajustarse antes de cargar.

## recommendation

Mantener tesis en `template_only`. El siguiente paso concreto es que el orquestador materialice plantillas vacias y consiga las cuatro decisiones del Doctor; no editar el borrador base hasta que el gate metodologico pase como minimo a `data_ready`.

## confidence

Alta para el flujo operativo, reglas de bloqueo, variables core y politica de faltantes. Media para variables opcionales y estructura final del protocolo hasta conocer pregunta, outcome y diseno definitivos.

## evidence_paths

- `jobs/20260525T231801-tesis-protocolo-next-pack-from-prior-results-v1.md`
- `results/20260525T124718-tesis-protocolo-datos-y-material-audiovisual.result.md`
- `results/20260525T170712-tesis-protocolo-datos-next-actions-v1.result.md`
- `results/20260525T173727-tesis-empty-template-pack-v1.result.md`
- `results/20260525T181001-tesis-decision-brief-variable-candidates-v1.result.md`
- `results/20260525T184101-tesis-protocolo-decision-gate-pack-v1.result.md`
- `results/20260525T021049-tesis-research-ops-protocol-v1.result.md`
- `protocol.md`
