---
id: 20260525T181001-tesis-decision-brief-variable-candidates-v1
job_id: 20260525T181001-tesis-decision-brief-variable-candidates-v1
created_at: 2026-05-25T18:15:08-03:00
created_by: personal-xh
worker: personal-xh
status: completed
no_external_actions: true
no_secrets: true
---

# Resultado - TESIS decision brief y variables candidatas v1

## summary

Brief corto para que Codex principal le pida al Doctor solo las decisiones inevitables antes de cargar datos o tocar el borrador: pregunta, unidad de analisis, outcome primario y rol del video. Se agrega una tabla de variables candidatas compatible con las plantillas vacias, sin datos reales ni bibliografia inventada.

Recomendacion central: mantener el borrador base cerrado hasta que estas cuatro decisiones esten respondidas y registradas en `HANDOFF.md` y `decision_log.md`.

## coverage_table

| Fuente permitida | Estado | Uso |
|---|---:|---|
| `results/20260525T173727-tesis-empty-template-pack-v1.result.md` | Revisada | Templates vacios y headers de trabajo. |
| `results/20260525T170712-tesis-protocolo-datos-next-actions-v1.result.md` | Revisada | Variables candidatas, faltantes, sesgos y decision sobre video. |
| `results/20260525T021049-tesis-research-ops-protocol-v1.result.md` | Revisada | Research ops, matriz bibliografica y gate antes de reescritura. |
| `context/fronts/tesis.md` | Ausente | No usado. |

## four_decisions_for_doctor

Estas son las cuatro preguntas exactas para el Doctor:

1. Cual es la pregunta de investigacion en una frase.
2. Cual sera la unidad de analisis: paciente, procedimiento, nivel vertebral, episodio, video o documento.
3. Cual sera el outcome primario medible.
4. Que rol tendra el video: contexto tecnico, fuente secundaria o fuente formal de datos.

Formato sugerido para pedir respuesta:

```text
Doctor, para avanzar sin tocar el borrador necesito confirmar:
1. Pregunta de investigacion:
2. Unidad de analisis:
3. Outcome primario:
4. Rol del video:
```

## recommended_default_options

| Decision | Opcion conservadora recomendada | Pros | Contras |
|---|---|---|---|
| Pregunta | Formularla como descriptiva/metodologica hasta tener bibliografia y datos. | Reduce riesgo de prometer comparaciones no sustentadas. | Puede quedar menos ambiciosa si el Doctor quiere hipotesis comparativa. |
| Unidad de analisis | Procedimiento. | Suele ser trazable con parte, tecnica y seguimiento. | Si hay multiples niveles por paciente, puede requerir subunidad `nivel`. |
| Outcome primario | Resultado clinico documentado en fuente primaria, con ventana definida. | Medible y auditable. | Requiere saber si hay seguimiento suficiente. |
| Rol del video | Contexto tecnico restringido, no fuente formal inicial. | Protege privacidad y evita sobreinterpretacion. | Limita uso analitico del material audiovisual hasta nueva decision. |

## variable_candidates_table

| variable_name | definition_draft | type | allowed_values_or_unit | source_origin | primary_or_secondary | missing_rule | quality_check |
|---|---|---|---|---|---|---|---|
| `case_id` | Identificador anonimo interno. | controlled_text | codigo no identificable | decision_humana | trazabilidad | obligatorio | no debe contener nombre, DNI, HC real ni fecha exacta |
| `procedure_id` | Identificador anonimo del procedimiento. | controlled_text | codigo no identificable | parte_quirurgico_anonimizado | trazabilidad | obligatorio si unidad es procedimiento | unico por procedimiento |
| `unit_of_analysis` | Unidad elegida para el analisis. | categorical | paciente/procedimiento/nivel/episodio/video/documento | HANDOFF | metodo | obligatorio | debe coincidir con decision humana |
| `period_bucket` | Periodo amplio de inclusion. | categorical | anio/rango aprobado | registro_anonimizado | covariable | no documentado | evitar fecha exacta identificable |
| `age_band` | Rango etario. | categorical | rangos aprobados | historia_clinica_anonimizada | covariable | no documentado | no usar edad exacta si identifica |
| `sex` | Sexo registrado si corresponde. | categorical | valores aprobados/no documentado | historia_clinica_anonimizada | covariable | no documentado | valor controlado |
| `primary_diagnosis_group` | Grupo diagnostico principal. | categorical | lista aprobada | HC/imagen/parte anonimizados | covariable | no documentado | no inferir diagnostico ausente |
| `spinal_region` | Region anatomica. | categorical | cervical/toracica/lumbar/sacra | parte/imagen anonimizados | covariable | no documentado | debe estar documentada |
| `level_or_levels` | Nivel o niveles involucrados. | controlled_text | formato Lx-Ly | parte/imagen anonimizados | covariable | no documentado | formato uniforme |
| `side` | Lateralidad si aplica. | categorical | derecha/izquierda/bilateral/no aplica/no documentado | parte/imagen anonimizados | covariable | no documentado | no transferir lateralidad a artrodesis/fijacion |
| `procedure_type` | Tipo de procedimiento. | categorical | lista aprobada | parte_quirurgico_anonimizado | exposicion | no documentado | validar contra parte |
| `approach_type` | Abordaje si esta documentado. | categorical | posterior/foraminal/extraforaminal/Wiltse/otro | parte/video_contextual_restringido | covariable | no documentado | video no debe inventar si parte no confirma |
| `direct_decompression` | Si hubo descompresion directa. | binary/categorical | yes/no/not_informed | parte_quirurgico_anonimizado | tecnica | not_informed | respetar negaciones explicitas |
| `implant_or_instrument_context` | Implantes/materiales documentados. | controlled_text | lista aprobada | parte_quirurgico_anonimizado | tecnica | no documentado | no inferir marca/modelo |
| `primary_outcome_value` | Valor del outcome primario. | depends_on_outcome | pendiente | fuente_clinica_primaria | outcome_primario | missing_log | no cargar hasta definir outcome |
| `pain_or_function_score` | Escala de dolor o funcion, si existe. | numeric/ordinal | escala validada | HC/seguimiento anonimizado | outcome_secundario | missing_log | requiere escala y momento |
| `neurologic_status_change` | Cambio neurologico documentado. | categorical | mejor/igual/peor/no documentado | HC/seguimiento anonimizado | outcome_secundario | missing_log | fuente y ventana definidas |
| `complication_flag` | Complicacion documentada en ventana aprobada. | binary | yes/no/no documentado | HC/parte/seguimiento | outcome_secundario | missing_log | definir ventana temporal |
| `reoperation_flag` | Reoperacion en periodo definido. | binary | yes/no/no documentado | HC/seguimiento | outcome_secundario | missing_log | periodo aprobado |
| `follow_up_duration_group` | Duracion de seguimiento en rangos. | ordinal | rangos aprobados | seguimiento anonimizado | calidad_dato | missing_log | no usar fecha exacta identificable |
| `source_quality` | Calidad de la fuente para el dato. | ordinal | alta/media/baja/conflicto | revision_interna | calidad_dato | obligatorio por variable critica | registrar conflictos |
| `data_conflict_flag` | Indica conflicto entre fuentes. | binary | yes/no | comparacion_fuentes | calidad_dato | no | si yes, requiere decision_log |
| `bibliographic_support_status` | Estado de respaldo bibliografico del argumento. | categorical | verificado/pendiente/no_requiere | bibliography_matrix | bibliografia | pendiente | no inventar citas |

## missing_data_policy_draft

Politica inicial:

| Situacion | Registro | Accion |
|---|---|---|
| Dato no aparece en fuente primaria | `missing_type=no_documentado` | No inferir; registrar en `missing_data_log.csv`. |
| Dato no aplica por diseno | `missing_type=no_aplica` | Mantener como no aplica, no como negativo. |
| Fuente ilegible o incompleta | `missing_type=ilegible` | Marcar revision humana. |
| Video muestra algo no confirmado por parte/HC | `missing_type=requiere_confirmacion` | No convertir en dato hasta confirmacion. |
| Fuentes contradicen | `missing_type=conflicto_entre_fuentes` | Crear decision en `decision_log.md`. |
| Dato bibliografico pendiente | `verification_status=pendiente` | No entrar al borrador base como cita. |

Regla: faltante no es negativo. `no documentado` no equivale a `no`.

## video_role_decision_tree

```text
Si el video contiene datos identificables:
  -> No usar fuera del entorno local. Requiere anonimizado/permisos.

Si el Doctor lo define como contexto tecnico:
  -> Puede orientar preguntas y checklist, pero no cargar outcomes ni conclusiones.

Si lo define como fuente secundaria:
  -> Puede marcar variables como "requiere confirmacion", nunca reemplazar fuente primaria.

Si lo define como fuente formal:
  -> Requiere protocolo explicito, consentimiento/permisos, anonimizado, variables especificas y control de sesgo.
```

Recomendacion provisoria: `contexto tecnico restringido`.

## what_not_to_change_in_base_draft

| No cambiar | Motivo |
|---|---|
| Hipotesis u objetivo principal | Dependen de pregunta y outcome. |
| Metodo | Depende de unidad de analisis, fuentes y criterios. |
| Resultados | No hay carga de datos aprobada. |
| Discusion | Requiere bibliografia verificada. |
| Conclusiones | No deben derivar de video ni de datos no cargados. |
| Citas | Riesgo de bibliografia inventada. |
| Criterios de inclusion/exclusion | Deben aprobarse antes de ver datos. |

## next_safe_actions_for_orchestrator

1. Materializar o actualizar `HANDOFF.md` con las cuatro preguntas.
2. Pedir al Doctor solo esas cuatro decisiones, sin abrir frentes nuevos.
3. Volcar la respuesta en `decision_log.md`.
4. Convertir esta tabla en `variables.md` como `draft`, no definitiva.
5. Crear headers vacios `data_collection_sheet.csv`, `missing_data_log.csv` y `bibliography_matrix.csv`.
6. No cargar datos reales hasta confirmar criterios de inclusion/exclusion y privacidad.
7. No tocar el borrador base hasta que el gate metodologico este completo.

## recommendation

El pedido al Doctor debe ser breve y cerrado. La opcion conservadora inicial es: tesis descriptiva/metodologica, unidad `procedimiento`, outcome primario documentado en fuente clinica primaria y video solo como contexto tecnico restringido.

## risks_limits

- No se abrio Drive, iCloud, Photos, Zotero ni documentos personales.
- No se cargaron datos reales ni sensibles.
- No se invento bibliografia.
- Las variables son candidatas; dependen de la pregunta final.
- El video puede contener datos sensibles aunque parezca anonimo.
- Si el Doctor elige unidad `paciente` o `nivel vertebral`, habra que ajustar la planilla.

## confidence

Alta para el brief de decisiones y la politica de faltantes. Media para variables candidatas hasta conocer pregunta, outcome y diseno final.

## evidence_paths

- `jobs/20260525T181001-tesis-decision-brief-variable-candidates-v1.md`
- `results/20260525T173727-tesis-empty-template-pack-v1.result.md`
- `results/20260525T170712-tesis-protocolo-datos-next-actions-v1.result.md`
- `results/20260525T021049-tesis-research-ops-protocol-v1.result.md`
