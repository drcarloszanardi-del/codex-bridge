# Resultado - tesis protocolo datos y material audiovisual

Job: `20260525T124718-tesis-protocolo-datos-y-material-audiovisual`
Worker: `personal-xh` / Pablo
Fecha: `2026-05-25`

## summary honesto

La mejora metodologica debe ordenar recoleccion de datos y uso de material audiovisual como insumo contextual, no como fuente libre para reescribir la tesis. Los videos pueden ayudar a identificar variables tecnicas, secuencia operatoria y calidad de descripcion, pero no deben introducir datos personales, conclusiones no medidas ni cambios al borrador base sin decision log.

## source_counts

| Fuente | Archivos revisados | Uso |
|---|---:|---|
| `results/20260525T021049-tesis-research-ops-protocol-v1.result.md` | 1 | Protocolo research ops y recomendacion de matriz/variables. |
| `decisions/tesis_research_ops_protocol_v1.md` | 1 | Artefactos, matriz bibliografica y protocolo de recoleccion. |
| `context/fronts/presentaciones.md` | 1 | Pipeline de fuente, narrativa, deck editable y QA con datos anonimizados. |

## data_collection_protocol_improvements

| Mejora | Implementacion | Razon |
|---|---|---|
| Diccionario de variables antes de cargar | `tesis/variables.md` con nombre, definicion, tipo, fuente, unidad, valores permitidos, faltantes | Evita cambiar definiciones a mitad de trabajo. |
| Registro de fuente exacta por dato | Columna `source_origin`: historia clinica anonimizada, parte, imagen, video, bibliografia, entrevista | Permite auditoria y limita inferencias. |
| Criterios de inclusion/exclusion operativos | Tabla con criterio, evidencia requerida y quien decide | Evita sesgo por conveniencia. |
| Missing data log | `tesis/missing_data_log.csv` con variable, caso, motivo y accion | Separa dato ausente de dato negativo. |
| Decision log obligatorio | `tesis/decision_log.md` para cada cambio de variable, outcome o criterio | Mantiene trazabilidad metodologica. |
| Separar datos de contexto | Variables cuantitativas/cualitativas medidas vs observaciones audiovisuales | Evita que el video pese como resultado no validado. |

## video_to_variable_mapping

| Observacion audiovisual | Variable posible | Uso permitido | Limite |
|---|---|---|---|
| Secuencia operatoria visible | `sequence_confirmed` / checklist tecnico | Contexto para completar descripcion metodologica | No reemplaza parte quirurgico ni registro formal. |
| Nivel/lado/abordaje mencionados o rotulados | `procedure_level_side_source_video` | Triangulacion con parte/HC anonimizada | No usar si hay duda o datos identificables. |
| Instrumental o implante visible | `implant_or_instrument_context` | Descripcion tecnica general | No inferir marca/modelo si no esta documentado. |
| Duracion aproximada o cortes relevantes | `video_segment_reference` | Indexar material para revision interna | No publicar ni compartir sin anonimizar y aprobar. |
| Complicacion o evento intraoperatorio | `event_flag_needs_chart_confirmation` | Marcar pregunta de revision | No convertir en resultado sin fuente clinica primaria. |
| Calidad pedagogica del clip | `teaching_asset_candidate` | Posible material de presentacion anonimo | Requiere consentimiento/permisos y QA visual. |

## ethics_privacy_limits

- Todo material debe estar anonimizado o quedarse fuera de herramientas externas.
- No subir videos con pacientes, audio identificable, pantallas, HC, nombres, fechas o metadatos sensibles.
- El video es fuente contextual secundaria salvo que el protocolo aprobado lo defina como fuente de dato.
- Si hay uso docente/publicable, requiere circuito separado de permisos, consentimiento, anonimizado y aprobacion humana.
- No modificar el borrador base con conclusiones derivadas solo del video.

## draft_change_candidates

| Cambio candidato | Donde | Tipo | Condicion para integrar |
|---|---|---|---|
| Agregar subseccion "Protocolo de recoleccion y trazabilidad" | Metodos | Mejora metodologica | Variables y fuentes definidas. |
| Agregar "Uso de material audiovisual" | Metodos o anexos | Aclaracion de fuente contextual | Limites eticos y privacidad aprobados. |
| Agregar tabla de variables | Metodos/anexo | Estructura | Diccionario estable. |
| Agregar missing data handling | Metodos | Robustez | Definir faltantes y exclusion. |
| Agregar decision log como anexo interno | Operaciones de tesis | Trazabilidad | No necesariamente visible en version final. |

## questions_for_doctor

1. Que variables clinicas/resultados quiere considerar outcome primario y secundarios.
2. Si los videos seran solo contexto tecnico o fuente formal de datos.
3. Que material audiovisual existe, en que formato y si esta anonimizado.
4. Que permisos/consentimientos hay para uso docente, tesis o presentacion.
5. Que campos del parte quirurgico considera obligatorios para triangulacion.
6. Que datos no deben salir nunca del entorno local.

## risks / limits

- No se reviso el borrador base ni videos reales.
- Usar videos como fuente puede introducir sesgo si solo hay clips de casos seleccionados.
- El material audiovisual puede contener datos sensibles aun cuando parezca anonimo.
- Cambios metodologicos deben integrarse sin alterar hipotesis o conclusiones sin evidencia.

## recommendation

Crear primero `tesis/variables.md`, `tesis/data_collection_protocol.md`, `tesis/missing_data_log.csv` y `tesis/video_index_template.csv`. Luego el orquestador puede decidir que cambios metodologicos pasan al borrador, sin tocar todavia el texto base.

## confidence

Alta para protocolo y limites de privacidad. Media para mapeo especifico hasta conocer tesis, variables reales y material audiovisual disponible.

## evidence_paths

- `jobs/20260525T124718-tesis-protocolo-datos-y-material-audiovisual.md`
- `results/20260525T021049-tesis-research-ops-protocol-v1.result.md`
- `decisions/tesis_research_ops_protocol_v1.md`
- `context/fronts/presentaciones.md`
