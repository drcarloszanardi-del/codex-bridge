# Resultado - 20260526T065253-tesis-protocolo-datos-y-material-audiovisual

## summary honesto

La tesis necesita primero un sistema trazable de datos: pregunta, poblacion, variables, fuentes, faltantes, sesgos y decisiones. El material audiovisual puede ayudar como contexto tecnico o indice interno, pero no debe introducir conclusiones ni datos clinicos sin fuente primaria y reglas eticas claras.

**Evidencia:** el protocolo research ops previo recomienda matriz bibliografica y variables antes de reescrituras. El frente presentaciones exige fuentes/citas trazables y datos sensibles anonimizados.

**Inferencia:** el mayor riesgo no es escribir poco, sino editar el borrador antes de fijar definiciones y denominadores.

**Opinion:** el proximo trabajo debe producir plantillas vacias y decision log, no tocar el texto base todavia.

## coverage_table

| Fuente | Uso | Limite |
| --- | --- | --- |
| `results/20260525T021049-tesis-research-ops-protocol-v1.result.md` | Base research ops: matriz, variables, decision log. | Resumen corto, sin variables detalladas. |
| `context/fronts/presentaciones.md` | Pipeline con fuentes trazables, QA y datos anonimizados. | Es frente presentaciones, no tesis pura. |
| `results/20260525T124718-tesis-protocolo-datos-y-material-audiovisual.result.md` | Protocolo anterior para videos, privacidad y cambios candidatos. | No revisa borrador ni videos reales. |

## data_collection_protocol_improvements

| Mejora | Implementacion | Razon |
| --- | --- | --- |
| Diccionario de variables antes de cargar | `tesis/variables.md`: nombre, definicion, tipo, fuente, unidad, valores permitidos, regla de faltantes. | Evita cambiar definiciones a mitad del analisis. |
| Fuente exacta por dato | Columna `source_origin`: HC anonimizada, parte, imagen, video, bibliografia, entrevista. | Permite auditoria y limita inferencias. |
| Criterios de inclusion/exclusion operativos | Tabla con criterio, evidencia requerida y responsable de decision. | Evita sesgo por conveniencia. |
| Missing data log | `tesis/missing_data_log.csv`: variable, caso, motivo y accion. | Separa dato ausente de dato negativo. |
| Decision log | `tesis/decision_log.md` para cambios de variable, outcome o criterio. | Mantiene trazabilidad metodologica. |
| Separar dato de contexto | Variables medidas vs observaciones audiovisuales. | Evita que un video pese como resultado no validado. |

## video_to_variable_mapping

| Observacion audiovisual | Variable posible | Uso permitido | Limite |
| --- | --- | --- | --- |
| Secuencia operatoria visible | `sequence_context_confirmed` | Contexto para describir tecnica o revisar consistencia. | No reemplaza parte quirurgico. |
| Nivel/lado/abordaje mencionado | `procedure_level_side_video_note` | Triangulacion con fuente primaria. | No usar si hay duda o datos identificables. |
| Instrumental o implante visible | `implant_or_instrument_context` | Descripcion tecnica general. | No inferir marca/modelo si no esta documentado. |
| Segmento relevante | `video_segment_reference` | Indice interno para revision local. | No publicar ni subir sin anonimizar/aprobar. |
| Evento intraoperatorio | `event_flag_needs_chart_confirmation` | Marcar pregunta para revisar HC/parte. | No convertir en outcome sin fuente primaria. |
| Valor docente del clip | `teaching_asset_candidate` | Posible material de presentacion anonimo. | Requiere permisos, consentimiento y QA visual. |

## ethics_privacy_limits

- Todo material audiovisual debe tratarse como restringido aunque parezca anonimo.
- No subir videos con pacientes, audio identificable, pantallas, HC, nombres, fechas o metadatos sensibles a herramientas externas.
- El video es fuente contextual secundaria salvo que el protocolo aprobado lo defina de otro modo.
- Uso docente/publicable requiere circuito separado de consentimiento, anonimizado, permisos y aprobacion humana.
- No modificar hipotesis, resultados o conclusiones desde impresiones de video.
- Si se usan clips como indice interno, registrar solo referencias no sensibles.

## draft_change_candidates

| Cambio candidato | Donde | Tipo | Condicion para integrar |
| --- | --- | --- | --- |
| "Protocolo de recoleccion y trazabilidad" | Metodos | Mejora metodologica | Variables y fuentes definidas. |
| "Uso de material audiovisual" | Metodos o anexo | Aclaracion de fuente contextual | Limites eticos aprobados. |
| Tabla de variables | Metodos/anexo | Estructura | Diccionario estable. |
| Manejo de datos faltantes | Metodos | Robustez | Missing log y reglas definidos. |
| Decision log | Anexo interno | Trazabilidad | Puede no ser visible en version final. |
| Matriz bibliografica | Anexo de trabajo | Control de citas | Referencias reales verificadas. |

## questions_for_doctor

1. Cual es la pregunta exacta de tesis.
2. Cual sera el outcome primario y cual sera la ventana temporal.
3. La unidad de analisis sera paciente, procedimiento, nivel vertebral, episodio o video.
4. Los videos seran contexto tecnico, fuente secundaria o fuente formal de datos.
5. Que material audiovisual existe y si ya esta anonimizado.
6. Que permisos o consentimientos existen para uso docente, tesis o presentacion.
7. Que datos no deben salir nunca del entorno local.
8. Que fuente primaria tiene prioridad si HC, parte, imagen y video no coinciden.

## risks_limits

- No se reviso el borrador base ni videos reales.
- No se inventaron citas ni referencias.
- Las variables son candidatas hasta que el Doctor confirme pregunta, poblacion y outcome.
- El material audiovisual puede contener datos sensibles invisibles a primera vista, incluidos metadatos.
- Si el diseno final no es observacional/retrospectivo, el protocolo debe ajustarse.

## recommendation

Crear primero `tesis/variables.md`, `tesis/data_collection_protocol.md`, `tesis/missing_data_log.csv`, `tesis/video_index_template.csv` y `tesis/decision_log.md`. Luego pedir al Doctor cuatro decisiones: pregunta exacta, unidad de analisis, outcome primario y rol de los videos. Solo despues preparar cambios al borrador base.

## confidence

Alta para protocolo, trazabilidad y privacidad. Media para variables especificas hasta conocer tesis, borrador y material real.

## evidence_paths

- `jobs/20260526T065253-tesis-protocolo-datos-y-material-audiovisual.md`
- `results/20260525T021049-tesis-research-ops-protocol-v1.result.md`
- `context/fronts/presentaciones.md`
- `results/20260525T124718-tesis-protocolo-datos-y-material-audiovisual.result.md`
- `results/20260525T170712-tesis-protocolo-datos-next-actions-v1.result.md`
