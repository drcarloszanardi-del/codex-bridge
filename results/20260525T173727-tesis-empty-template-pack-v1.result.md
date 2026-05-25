---
id: 20260525T173727-tesis-empty-template-pack-v1
job_id: 20260525T173727-tesis-empty-template-pack-v1
created_at: 2026-05-25T17:41:08-03:00
created_by: personal-xh
worker: personal-xh
status: completed
no_external_actions: true
no_secrets: true
---

# Resultado - TESIS empty template pack v1

## summary

Pack de plantillas vacias para ordenar la tesis sin tocar el borrador base, sin cargar datos reales y sin inventar bibliografia. Las plantillas dejan preparado el circuito minimo: handoff, variables, protocolo de recoleccion, planilla de datos, faltantes, decision log y matriz bibliografica.

Todo debe quedar vacio hasta que el Doctor confirme cuatro decisiones: pregunta, unidad de analisis, outcome primario y rol del video.

## coverage_table

| Fuente permitida | Estado | Uso |
|---|---:|---|
| `results/20260525T170712-tesis-protocolo-datos-next-actions-v1.result.md` | Revisada | Campos, gates, variables candidatas, faltantes y proximo paso. |
| `results/20260525T021049-tesis-research-ops-protocol-v1.result.md` | Revisada | Research ops, matriz bibliografica, protocolo y decision log. |

## HANDOFF_md_template

```markdown
# TESIS HANDOFF

Estado: draft_vacio
Ultima actualizacion: YYYY-MM-DD
Responsable humano: Dr. Carlos Zanardi

## decisiones_pendientes

- [ ] Pregunta de investigacion confirmada.
- [ ] Unidad de analisis confirmada.
- [ ] Outcome primario confirmado.
- [ ] Rol del video confirmado: contexto tecnico / fuente secundaria / fuente formal.

## pregunta_de_investigacion

Pendiente de completar por decision humana.

## objetivo_principal

Pendiente.

## objetivos_secundarios

- Pendiente.

## hipotesis_o_enfoque

Pendiente. Indicar si es descriptivo, comparativo, pronostico, tecnico o mixto.

## poblacion

Pendiente. Definir universo elegible, periodo, centro/fuente y criterios generales.

## unidad_de_analisis

Pendiente. Elegir una: paciente / procedimiento / nivel vertebral / episodio / video / documento.

## outcome_primario

Pendiente. Debe ser medible y operacional.

## outcomes_secundarios

- Pendiente.

## fuentes_permitidas

- Pendiente. No incluir datos sensibles en este archivo.

## limites_privacidad

- No registrar nombres, DNI, numeros reales de historia clinica, fechas exactas identificables ni material audiovisual identificable.
- Toda duda sensible se conserva localmente y se resume sin datos personales.

## cambios_borrador_base

No modificar borrador base hasta completar variables, protocolo, faltantes, matriz bibliografica y decision log.
```

## variables_md_template

```markdown
# Diccionario de variables

Estado: vacio_hasta_aprobacion

| variable_name | definition | type | unit_or_allowed_values | source_origin | primary_or_secondary | missing_rule | quality_check | notes_non_sensitive |
|---|---|---|---|---|---|---|---|---|
| pendiente | pendiente | pendiente | pendiente | pendiente | pendiente | pendiente | pendiente | pendiente |

## reglas

- No cargar datos reales en este archivo.
- Cada variable debe tener definicion operacional antes de usarse.
- Si una variable cambia, registrar la decision en `decision_log.md`.
- Si un valor no esta documentado, no inferirlo: registrarlo como faltante segun regla aprobada.

## tipos_permitidos

- binary
- categorical
- ordinal
- numeric
- date_bucket
- controlled_text

## source_origin_permitidos

- historia_clinica_anonimizada
- parte_quirurgico_anonimizado
- imagen_anonimizada
- video_contextual_restringido
- bibliografia_verificada
- decision_humana
- no_definido
```

## data_collection_protocol_md_template

```markdown
# Protocolo de recoleccion de datos

Estado: plantilla_vacia

## alcance

Pendiente de definicion humana.

## fuentes

| fuente | uso_permitido | prioridad | restricciones |
|---|---|---|---|
| pendiente | pendiente | pendiente | pendiente |

## prioridad_de_fuentes

Pendiente. Definir que fuente prevalece si hay conflicto entre historia clinica, parte, imagen, video o bibliografia.

## criterios_de_inclusion

- Pendiente.

## criterios_de_exclusion

- Pendiente.

## reglas_de_carga

1. No cargar datos identificables.
2. No completar variables inexistentes en `variables.md`.
3. No inferir valores no documentados.
4. Registrar faltantes en `missing_data_log.csv`.
5. Registrar cambios de criterio en `decision_log.md`.

## manejo_de_video

Rol pendiente: contexto tecnico / fuente secundaria / fuente formal.

Regla provisoria: el video no genera conclusiones clinicas ni modifica el borrador base sin decision explicita.

## control_de_calidad

| control | frecuencia | responsable | salida |
|---|---|---|---|
| revision de variables criticas | pendiente | pendiente | pendiente |
| control de faltantes | pendiente | pendiente | pendiente |
| control bibliografico | pendiente | pendiente | pendiente |

## gate_para_modificar_borrador

- [ ] Pregunta confirmada.
- [ ] Unidad de analisis confirmada.
- [ ] Outcome primario confirmado.
- [ ] Variables definidas.
- [ ] Criterios inclusion/exclusion definidos.
- [ ] Faltantes tratados.
- [ ] Matriz bibliografica iniciada con referencias verificadas.
```

## data_collection_sheet_csv_header

```csv
case_id,unit_id,unit_of_analysis,source_origin,source_reference,variable_name,value_raw,value_normalized,collector,collection_date_bucket,review_status,quality_flag,notes_non_sensitive
```

## missing_data_log_csv_header

```csv
case_id,unit_id,variable_name,missing_type,source_checked,reason_non_sensitive,action,decision_id,review_status,notes_non_sensitive
```

## decision_log_md_template

```markdown
# Decision log tesis

Estado: plantilla_vacia

| decision_id | date | area | question | decision | rationale | affected_files | approved_by | follow_up |
|---|---|---|---|---|---|---|---|---|
| D000 | YYYY-MM-DD | pendiente | pendiente | pendiente | pendiente | pendiente | pendiente | pendiente |

## areas_permitidas

- pregunta
- poblacion
- unidad_de_analisis
- outcome
- variable
- inclusion_exclusion
- fuente
- video
- bibliografia
- borrador_base

## regla

Toda decision que cambie variables, criterios, fuentes, uso de video o texto del borrador debe quedar registrada antes de ejecutarse.
```

## bibliography_matrix_csv_header

```csv
reference_id,citation_full,source_status,study_type,population,intervention_or_exposure,comparator,outcome,main_finding,bias_or_limitations,use_in_thesis,verification_status,notes_non_sensitive
```

## how_orchestrator_should_materialize

1. Crear una carpeta de trabajo de tesis en el repo/proyecto que corresponda, no dentro del bridge salvo que el orquestador lo decida.
2. Materializar estas plantillas como archivos vacios, sin datos reales: `HANDOFF.md`, `variables.md`, `data_collection_protocol.md`, `data_collection_sheet.csv`, `missing_data_log.csv`, `decision_log.md`, `bibliography_matrix.csv`.
3. Mantener el borrador base fuera de cambios hasta completar las decisiones iniciales.
4. Pedir al Doctor solo las cuatro decisiones iniciales: pregunta, unidad de analisis, outcome primario, rol del video.
5. Despues de esas decisiones, convertir las variables candidatas en definiciones reales.
6. Recién entonces permitir carga de datos anonimizados y bibliografia verificada.

## recommendation

El orquestador deberia materializar primero estas plantillas vacias y abrir un unico pedido al Doctor con las cuatro decisiones pendientes. Eso evita tocar el borrador base y permite que el trabajo posterior sea metodico, trazable y sin bibliografia inventada.

## risks_limits

- No se abrio Drive, Zotero, iCloud, Photos ni documentos personales.
- Las plantillas no contienen datos reales ni bibliografia validada.
- Si el Doctor define otro diseno de tesis, los headers pueden necesitar ajuste.
- La matriz bibliografica queda vacia hasta cargar referencias verificadas.
- El material audiovisual se mantiene restringido hasta decision humana sobre su rol.

## confidence

Alta para la estructura operativa y la seguridad de no tocar el borrador. Media para campos finales porque dependen de la pregunta real, unidad de analisis, outcome y rol del video.

## evidence_paths

- `jobs/20260525T173727-tesis-empty-template-pack-v1.md`
- `results/20260525T170712-tesis-protocolo-datos-next-actions-v1.result.md`
- `results/20260525T021049-tesis-research-ops-protocol-v1.result.md`
