---
id: 20260525T170712-tesis-protocolo-datos-next-actions-v1
job_id: 20260525T170712-tesis-protocolo-datos-next-actions-v1
created_at: 2026-05-25T17:18:37-03:00
created_by: personal-xh
worker: personal-xh
status: completed
no_external_actions: true
no_secrets: true
---

# Resultado - TESIS protocolo de datos y proximas acciones

## summary

El frente de tesis necesita convertirse primero en un sistema trazable de investigacion: pregunta, poblacion, criterios, variables, fuentes, faltantes, sesgos y decisiones. La recomendacion central es no tocar el borrador base hasta tener aprobados un diccionario de variables, un protocolo de recoleccion, una matriz bibliografica y un decision log minimo.

El material audiovisual puede servir como contexto tecnico o indice interno, pero no debe transformarse en dato clinico ni en conclusion sin confirmacion en fuente primaria y sin reglas eticas explicitas.

## coverage_table

| Fuente permitida | Estado | Uso en este resultado |
|---|---:|---|
| `context/fronts/tesis.md` | Ausente en el bridge | No usado; se mantiene protocolo conservador. |
| `results/20260525T021049-tesis-research-ops-protocol-v1.result.md` | Revisada | Base para research ops, matriz bibliografica y gate antes de reescritura. |
| `results/20260525T015500-mejoras-tesis-presentaciones-reels-cmp.result.md` | Revisada | Refuerza tesis como investigacion trazable y separacion de frentes. |
| `results/20260525T124718-tesis-protocolo-datos-y-material-audiovisual.result.md` | Revisada | Insumos para protocolo de datos, limites eticos y uso de videos como fuente contextual. |

## data_collection_protocol_draft

### 1. Pregunta y alcance

Antes de extraer datos, fijar en `tesis/HANDOFF.md`:

| Campo | Decision requerida |
|---|---|
| Pregunta de investigacion | Formulacion unica, sin mezclar objetivos clinicos, tecnicos y docentes. |
| Hipotesis o objetivo principal | Declarar si es descriptivo, comparativo, pronostico o de calidad tecnica. |
| Poblacion | Pacientes/casos/procedimientos incluidos, periodo, centro y fuente primaria. |
| Outcome primario | Una variable principal medible y operacional. |
| Outcomes secundarios | Variables secundarias limitadas y justificadas. |
| Unidad de analisis | Paciente, procedimiento, nivel vertebral, episodio, video o documento. |

### 2. Diccionario de variables

Crear `tesis/variables.md` antes de cargar datos. Cada variable debe tener:

| Campo | Regla |
|---|---|
| `variable_name` | Nombre estable, en snake_case. |
| `definition` | Definicion operacional, no narrativa. |
| `type` | Binaria, categorica, ordinal, numerica, fecha, texto controlado. |
| `source_origin` | Historia clinica anonimizada, parte quirurgico, imagen, video, bibliografia, entrevista, otro. |
| `unit_or_allowed_values` | Unidad, rango o lista cerrada de valores. |
| `missing_rule` | Como registrar ausente, no aplicable, no documentado o dudoso. |
| `primary_or_secondary` | Outcome principal, secundario, covariable, confusor o contexto. |
| `quality_check` | Regla de verificacion o fuente de triangulacion. |

### 3. Planilla maestra de datos

Usar una tabla inicial `tesis/data_collection_sheet.csv` con estas columnas minimas:

| Columna | Proposito |
|---|---|
| `case_id` | Identificador interno anonimo. |
| `unit_id` | Procedimiento/nivel/episodio si aplica. |
| `source_origin` | Fuente exacta del dato. |
| `source_reference` | Referencia interna no sensible: codigo de documento, segmento, folio anonimo. |
| `variable_name` | Debe existir en el diccionario. |
| `value_raw` | Valor tal como aparece en la fuente anonima. |
| `value_normalized` | Valor normalizado para analisis. |
| `collector` | Quien cargo el dato. |
| `review_status` | Pendiente, revisado, corregido, excluido. |
| `notes_non_sensitive` | Dudas metodologicas sin datos personales. |

### 4. Registro de faltantes

Crear `tesis/missing_data_log.csv`:

| Campo | Regla |
|---|---|
| `case_id` | Identificador anonimo. |
| `variable_name` | Variable afectada. |
| `missing_type` | No documentado, no aplicable, ilegible, pendiente, conflicto entre fuentes. |
| `action` | Mantener faltante, buscar fuente primaria, excluir variable, excluir caso, imputacion solo si se aprueba. |
| `decision_id` | Link al decision log si modifica criterio. |

### 5. Decision log

Crear `tesis/decision_log.md` y registrar:

| Situacion | Decision obligatoria |
|---|---|
| Cambio de criterio de inclusion/exclusion | Fecha, motivo, impacto y aprobacion humana. |
| Cambio de definicion de variable | Version anterior, version nueva y casos afectados. |
| Dato contradictorio entre fuentes | Fuente prioritaria y regla de resolucion. |
| Uso de video como insumo | Si es contexto, fuente secundaria o fuente formal; limites eticos. |
| Nuevo argumento para el borrador | Referencia, evidencia o decision explicita. |

### 6. Gate antes de modificar borrador

Ningun cambio entra al borrador base hasta cumplir estos cinco puntos:

| Gate | Evidencia minima |
|---|---|
| Variables definidas | `tesis/variables.md` estable. |
| Criterios aprobados | Inclusion/exclusion escritos y revisados. |
| Fuentes trazables | Cada dato tiene `source_origin` y referencia interna. |
| Faltantes tratados | `missing_data_log.csv` creado. |
| Bibliografia controlada | Matriz bibliografica con referencias reales, sin citas inventadas. |

## candidate_variables

Estas variables son candidatas, no definiciones finales. Deben adaptarse a la pregunta real de tesis.

### Identificacion anonima y estructura

| Variable | Tipo | Fuente probable | Observacion |
|---|---|---|---|
| `case_id` | Texto anonimo | Registro interno anonimo | Nunca usar nombre, DNI, fecha exacta identificable ni numero de HC real. |
| `procedure_id` | Texto anonimo | Parte/protocolo | Util si hay mas de un procedimiento por paciente. |
| `unit_of_analysis` | Categorica | Protocolo | Paciente, procedimiento, nivel, episodio o video. |
| `period_bucket` | Categorica | Registro anonimo | Usar periodos amplios si las fechas exactas identifican. |

### Poblacion y baseline

| Variable | Tipo | Fuente probable | Observacion |
|---|---|---|---|
| `age_band` | Categorica | HC anonimizada | Preferir rangos si hay riesgo de identificacion. |
| `sex` | Categorica | HC anonimizada | Valores cerrados y regla para no documentado. |
| `primary_diagnosis_group` | Categorica | HC/imagen/parte | Definir codificacion antes de cargar. |
| `symptom_duration_group` | Ordinal | HC anonimizada | Rangos: agudo/subagudo/cronico si aplica. |
| `prior_treatment_group` | Categorica | HC anonimizada | Conservador, infiltracion, cirugia previa, otro. |
| `comorbidity_flag` | Binaria/categorica | HC anonimizada | Solo si relevante y disponible de manera consistente. |

### Anatomia, tecnica y procedimiento

| Variable | Tipo | Fuente probable | Observacion |
|---|---|---|---|
| `spinal_region` | Categorica | Parte/imagen | Cervical, toracica, lumbar, sacra. |
| `level_or_levels` | Texto controlado | Parte/imagen | Requiere formato estable. |
| `side` | Categorica | Parte/imagen | Derecho, izquierdo, bilateral, no aplica. |
| `approach_type` | Categorica | Parte/video contextual | No inferir desde video si no esta documentado. |
| `procedure_type` | Categorica | Parte quirurgico | Definir lista cerrada. |
| `implant_or_instrument_context` | Texto controlado | Parte/video contextual | Marca/modelo solo con documento primario. |
| `sequence_confirmed` | Binaria | Parte/video contextual | Solo como contexto tecnico, no outcome. |

### Outcomes y seguimiento

| Variable | Tipo | Fuente probable | Observacion |
|---|---|---|---|
| `primary_outcome_value` | Segun outcome | Fuente clinica primaria | Debe definirse antes de cargar. |
| `pain_or_function_score` | Numerica/ordinal | HC/escala validada | Solo si escala y momento estan documentados. |
| `neurologic_status_change` | Categorica | HC seguimiento | Mejorado, igual, peor, no documentado. |
| `complication_flag` | Binaria | HC/parte/seguimiento | Definir lista y ventana temporal. |
| `reoperation_flag` | Binaria | HC/seguimiento | Definir periodo. |
| `return_to_activity_group` | Categorica | HC/seguimiento | Solo si medido de forma consistente. |
| `follow_up_duration_group` | Ordinal | HC/seguimiento | Rango, no fecha exacta si identifica. |

### Calidad de fuente y trazabilidad

| Variable | Tipo | Fuente probable | Observacion |
|---|---|---|---|
| `source_quality` | Ordinal | Revision interna | Alta, media, baja, conflicto. |
| `chart_confirmation_needed` | Binaria | Revision interna | Para datos que aparecen en videos o notas incompletas. |
| `data_conflict_flag` | Binaria | Comparacion fuentes | Requiere decision log. |
| `missing_data_reason` | Categorica | Missing log | No documentado, no aplicable, conflicto, ilegible. |
| `bibliographic_support_status` | Categorica | Matriz bibliografica | Referenciado, pendiente, no requiere, decision humana. |

## inclusion_exclusion_criteria_questions

Preguntas concretas para cerrar inclusion/exclusion:

1. La poblacion sera de pacientes, procedimientos, niveles vertebrales o casos docentes.
2. El periodo de inclusion esta definido por fecha de cirugia, fecha de consulta, fecha de diagnostico o fecha de seguimiento.
3. Se incluyen solo casos operados o tambien casos conservadores/comparativos.
4. Se incluyen revisiones, reoperaciones o cirugias previas.
5. Se incluyen pacientes con datos de seguimiento incompletos; si si, cual es el minimo aceptable.
6. Que diagnosticos quedan fuera por no pertenecer a la pregunta principal.
7. Que procedimientos combinados quedan dentro o fuera.
8. El material audiovisual es obligatorio para incluir un caso o solo insumo opcional.
9. Como se tratara un caso con video disponible pero fuente clinica incompleta.
10. Como se tratara un dato que aparece en video pero no en parte quirurgico o HC.
11. Que datos se consideran sensibles y no salen del entorno local.
12. Que variable sera outcome primario y cual es su ventana temporal.
13. Que bibliografia minima debe respaldar cada argumento metodologico.

## bias_and_confounders

| Riesgo | Como aparece | Control recomendado |
|---|---|---|
| Sesgo de seleccion | Solo se incluyen casos con mejor documentacion o mejores videos. | Registrar universo elegible, motivos de exclusion y disponibilidad de material. |
| Sesgo de supervivencia documental | Los casos con registros completos parecen mejores por calidad de fuente. | Separar calidad de dato de resultado clinico. |
| Confusion por indicacion | Casos mas complejos reciben procedimientos distintos y tienen outcomes distintos. | Registrar severidad, diagnostico, cirugia previa y comorbilidades relevantes. |
| Variacion temporal | Tecnica, equipamiento o protocolo cambian en el periodo de estudio. | Agrupar por periodo y registrar cambios de tecnica. |
| Sesgo de medicion | Escalas, follow-up o definiciones cambian entre casos. | Definir ventana y fuente de medicion antes de cargar. |
| Conflicto entre fuentes | Video, parte y HC no coinciden. | Prioridad predefinida de fuentes y decision log. |
| Sesgo del observador | Quien carga datos conoce resultado o preferencia tecnica. | Doble revision de variables criticas si es viable. |
| Confundidores clinicos | Edad, diagnostico, comorbilidades, cirugia previa, severidad inicial. | Listarlos como covariables o limites del analisis. |
| Sobreinterpretacion audiovisual | Se extraen conclusiones clinicas desde clips parciales. | Video solo contextual salvo protocolo aprobado. |
| Privacidad/metadatos | Videos o imagenes contienen datos identificables invisibles a primera vista. | Anonimizar, revisar metadatos y no subir a herramientas externas. |

## bibliography_gaps_to_search

No se agregan citas. Estos son huecos de busqueda que el orquestador debe convertir en busquedas bibliograficas reales:

| Gap | Pregunta de busqueda |
|---|---|
| Definicion de outcome primario | Que outcomes son aceptados para la patologia/procedimiento central de la tesis. |
| Escalas clinicas | Que escalas validadas corresponden al dolor, funcion o resultado neurologico elegido. |
| Ventana de seguimiento | Que ventanas de follow-up se usan en estudios comparables. |
| Criterios de inclusion/exclusion | Como estudios similares definen poblacion, cirugia previa, comorbilidades y casos mixtos. |
| Missing data | Como reportan faltantes en series retrospectivas o estudios observacionales comparables. |
| Uso de material audiovisual | Normas/guia etica para videos quirurgicos, docencia, anonimizado y consentimiento. |
| Sesgo en series clinicas | Recomendaciones STROBE u otra guia aplicable si el diseno es observacional. |
| Variables tecnicas | Que variables operatorias son relevantes y reproducibles para el procedimiento central. |
| Confounders | Factores que modifican outcome en la patologia concreta de la tesis. |
| Reporte medico-legal/privacidad | Buenas practicas locales o institucionales para anonimizar datos clinicos en tesis. |

## changes_to_avoid_in_base_draft

Evitar estos cambios hasta que exista evidencia o decision log:

| Cambio a evitar | Motivo |
|---|---|
| Reescribir hipotesis u objetivo principal | Puede desalinear todo el metodo. |
| Agregar citas desde memoria o referencias incompletas | Riesgo de bibliografia falsa. |
| Cambiar conclusiones por impresiones de videos | El video no es fuente clinica primaria por defecto. |
| Mezclar casos, procedimientos y niveles como si fueran la misma unidad | Distorsiona denominadores y analisis. |
| Declarar resultados sin ventana temporal definida | Debilita validez metodologica. |
| Usar fechas exactas o datos identificables en artefactos de trabajo | Riesgo de privacidad. |
| Cambiar criterios luego de ver resultados | Riesgo de sesgo post hoc. |
| Convertir material docente en evidencia de tesis | Requiere protocolo y permisos separados. |
| Abrir el borrador base para edicion directa | El job pide no tocarlo; las mejoras deben quedar como plan. |

## next_actions_for_orchestrator

1. Crear o pedir al Doctor un `tesis/HANDOFF.md` con pregunta, objetivo, poblacion, unidad de analisis y outcome primario.
2. Crear `tesis/variables.md` con las variables candidatas aprobadas y definiciones operacionales.
3. Crear `tesis/data_collection_protocol.md` con fuentes permitidas, prioridad de fuentes, criterios de revision y reglas de faltantes.
4. Crear `tesis/missing_data_log.csv` y `tesis/data_collection_sheet.csv` como plantillas vacias.
5. Crear `tesis/bibliography_matrix.csv` con columnas: referencia, tipo de estudio, poblacion, outcome, sesgo, uso en tesis, estado de verificacion.
6. Pedir al Doctor una decision explicita sobre el rol de videos: contexto tecnico, fuente secundaria o fuente formal de datos.
7. Definir lista corta de criterios de inclusion/exclusion y resolver las preguntas de este resultado.
8. Solo despues, preparar un patch propuesto para el borrador base, separado y revisable.

## recommendation

El proximo paso mas valioso es que el orquestador pida al Doctor cuatro decisiones: pregunta exacta, unidad de analisis, outcome primario y rol del material audiovisual. Con eso, Pablo/personal-xh puede armar los templates `tesis/variables.md`, `tesis/data_collection_protocol.md`, `tesis/missing_data_log.csv` y `tesis/bibliography_matrix.csv` sin tocar el borrador base.

## risks_limits

- Este resultado se baso solo en material del bridge, sin abrir Drive, Zotero, iCloud, Photos ni documentos personales.
- No se reviso el borrador base de tesis ni bibliografia original.
- Las variables son candidatas; no deben cargarse datos reales hasta que el Doctor confirme pregunta, poblacion y outcome.
- No se inventaron citas ni referencias; los gaps bibliograficos son tareas de busqueda, no bibliografia validada.
- El material audiovisual puede contener datos sensibles aun cuando parezca anonimo; debe tratarse como material restringido.
- Si el diseno final de tesis no es observacional o retrospectivo, el protocolo debe ajustarse.

## confidence

Alta para el plan operativo, trazabilidad, privacidad y secuencia de trabajo. Media para las variables especificas porque falta conocer la pregunta final, el borrador base y el set real de datos.

## evidence_paths

- `jobs/20260525T170712-tesis-protocolo-datos-next-actions-v1.md`
- `results/20260525T021049-tesis-research-ops-protocol-v1.result.md`
- `results/20260525T015500-mejoras-tesis-presentaciones-reels-cmp.result.md`
- `results/20260525T124718-tesis-protocolo-datos-y-material-audiovisual.result.md`
- `status/personal-xh.json`
