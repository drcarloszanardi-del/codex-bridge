---
job_id: 20260528T132759-tesis-protocolo-datos-y-material-audiovisual
worker: personal-xh
status: completed
completed_at: 2026-05-28T13:28:18-03:00
front: TESIS
no_external_actions: true
no_secrets: true
---

# Resultado - Tesis protocolo datos y material audiovisual

## summary honesto

La tesis no necesita una reescritura todavia; necesita trazabilidad. Primero hay que definir variables, fuentes, faltantes, decision log y rol exacto del material audiovisual. El video quirurgico puede servir como contexto tecnico, auditoria o candidato de variable, pero no como evidencia primaria ni como permiso para cambiar conclusiones sin protocolo, anonimizado y revision del Doctor.

## coverage_table

| Requisito | Estado | Evidencia |
|---|---|---|
| `data_collection_protocol_improvements` | cubierto | Research ops protocol y guardrails de TESIS. |
| `video_to_variable_mapping` | cubierto | Resultados previos de audiovisual y material metodologico. |
| `ethics_privacy_limits` | cubierto | Reglas de anonimizado, fuente y QA visual. |
| `draft_change_candidates` | cubierto | Cambios candidatos sin tocar borrador base. |
| `questions_for_doctor` | cubierto | Preguntas de definicion y permisos. |

## evidencia

- `results/20260525T021049-tesis-research-ops-protocol-v1.result.md` recomienda matriz bibliografica y variables antes de reescrituras.
- `decisions/tesis_research_ops_protocol_v1.md` define artefactos: `variables.md`, `bibliography_matrix.csv`, `data_collection_protocol.md`, `decision_log.md` y `open_questions.md`.
- `results/20260527T011700-tesis-protocolo-datos-y-material-audiovisual.result.md` clasifica audiovisual como contexto, auditoria o variable candidata.
- `results/20260527T073414-tesis-protocolo-template-guardrails-v1.result.md` bloquea tocar borrador base sin decision log.
- `context/fronts/presentaciones.md` refuerza fuentes trazables, anonimizado, QA y separacion entre visual y evidencia.

## inferencia

- Si una variable nace desde video, debe arrancar como `contextual`, `audit_support` o `pending_review`.
- El borrador base solo deberia cambiar despues de que variables y criterios esten aprobados.
- La matriz audiovisual debe indexar clips y observaciones sin exponer material sensible en el bridge.

## opinion

La mayor mejora metodologica ahora es humilde: que cada dato tenga apellido, fuente y estado. Sin eso, cualquier parrafo lindo de metodologia se vuelve fragil.

## data_collection_protocol_improvements

Artefactos minimos:

```text
tesis/variables.md
tesis/data_collection_protocol.md
tesis/missing_data_log.csv
tesis/video_index_template.csv
tesis/decision_log.md
tesis/open_questions.md
```

Campos obligatorios por variable:

```yaml
variable_id:
definition_version:
operational_definition:
unit_or_scale:
source_type: historia | parte_quirurgico | imagen | video | nota_experta | bibliografia
source_id:
source_path_or_reference:
validity_status: primary | derived | inferred | contextual | pending_review
measurement_timepoint:
allowed_values:
missing_policy: unknown | not_applicable | not_recorded | excluded
review_status: draft | needs_review | approved
decision_log_id:
```

Mejoras accionables:

- Crear diccionario de 10-15 variables iniciales antes de cargar datos.
- Separar datos primarios, derivados, inferidos y contextuales.
- Registrar fuente exacta por dato y version de definicion.
- Mantener `missing_data_log.csv`; dato ausente no equivale a dato negativo.
- Todo cambio de definicion, inclusion, exclusion u outcome requiere `decision_log_id`.
- Doble revision de variables criticas: una carga, una revision.

## video_to_variable_mapping

| Observacion audiovisual | Variable candidata | Uso permitido | Limite |
|---|---|---|---|
| Paso tecnico visible | `technical_step_present` | Auditoria contextual si el paso estaba predefinido. | No reemplaza parte quirurgico. |
| Secuencia de pasos | `technical_sequence_observed` | Control de coherencia metodologica. | Si hay cortes, queda `pending_review`. |
| Tiempo aproximado entre fases | `phase_duration_estimate` | Solo si hay timestamp confiable. | No usar en outcome si el video no es continuo. |
| Instrumental/implante visible | `instrumentation_seen` | Contexto o pregunta de verificacion. | No infiere marca/modelo/trazabilidad. |
| Evento intraoperatorio | `intraop_event_candidate` | Senal para revisar documento formal. | No outcome primario sin validacion. |
| Calidad del clip | `visual_documentation_quality` | QA docente o de presentacion. | No mide resultado clinico. |
| Explicacion del Doctor | `expert_context_note` | Nota cualitativa separada. | No dato cuantitativo. |

Template de indice audiovisual:

```csv
clip_id,anon_case_id,local_path_ref,permission_status,source_type,observed_item,variable_candidate,validity_status,needs_doctor_review,notes_redacted
```

## ethics_privacy_limits

- No subir ni compartir material con pacientes identificables, voz, rostro, HC, nombres, fechas, turnos, metadata sensible o pantallas con datos.
- El bridge debe guardar solo rutas/IDs anonimos, no videos ni capturas sensibles.
- El video quirurgico no sustituye historia clinica, parte quirurgico ni documentacion formal.
- Si el uso sera docente/publicable, requiere permiso/consentimiento y QA visual separado.
- Las observaciones derivadas de video arrancan `pending_review` salvo protocolo aprobado.
- No modificar el borrador base con conclusiones derivadas solo de audiovisual.

## draft_change_candidates

Cambios candidatos, sin aplicar todavia:

1. En Metodos: subseccion `Gestion y trazabilidad de datos`.
2. En Metodos/anexo: tabla de variables con definicion, fuente, unidad, faltantes y decision log.
3. En Metodos o limitaciones: `Uso de material audiovisual como soporte contextual`.
4. En Limitaciones: aclarar que video no sustituye documentacion clinica formal.
5. En Anexos internos: `missing_data_log`, `video_index_template` y decision log.
6. En Bibliografia/metodo: matriz bibliografica con decision `usar|revisar|descartar`.

Condicion para tocar borrador:

```yaml
before_draft_change:
  variables_md_exists: true
  data_collection_protocol_exists: true
  decision_log_entry: required
  source_id_for_every_new_claim: true
  audiovisual_role_declared: contextual_or_audit_support
```

## questions_for_doctor

- Cuales son outcome primario y secundarios?
- Que variables son obligatorias y cuales exploratorias?
- El material audiovisual sera fuente formal, soporte contextual, docencia o presentacion?
- Que videos tienen permiso/consentimiento y cuales son solo revision interna?
- Que outcomes no deben inferirse desde video?
- Que documento manda si hay conflicto: historia, parte quirurgico, imagen, video o nota experta?
- Que definiciones del borrador no deben modificarse sin aprobacion explicita?

## risks / limits

- No se reviso el borrador base, datos reales ni videos.
- El audiovisual puede sesgar la muestra si hay clips solo de casos seleccionados.
- Material aparentemente anonimo puede contener metadata o datos visibles.
- Una variable nueva sin decision log puede cambiar la metodologia sin control.
- Ruta alternativa si no hay permiso audiovisual: usar video solo como nota contextual interna y no como variable.

## recommendation

Proxima accion unica: crear `tesis/variables.md`, `tesis/data_collection_protocol.md`, `tesis/missing_data_log.csv` y `tesis/video_index_template.csv` con 10-15 variables iniciales y estados `primary/derived/inferred/contextual/pending_review`. No tocar el borrador base hasta que exista decision log y aprobacion del orquestador.

## confidence

Alta para protocolo, limites y campos minimos porque derivan de guardrails locales. Media para cambios concretos del borrador porque no se inspecciono texto base ni datos reales.

## evidence_paths

- `jobs/20260528T132759-tesis-protocolo-datos-y-material-audiovisual.md`
- `results/20260525T021049-tesis-research-ops-protocol-v1.result.md`
- `decisions/tesis_research_ops_protocol_v1.md`
- `context/fronts/presentaciones.md`
- `results/20260527T011700-tesis-protocolo-datos-y-material-audiovisual.result.md`
- `results/20260527T073414-tesis-protocolo-template-guardrails-v1.result.md`
- `results/20260527T192200-tesis-protocolo-datos-y-material-audiovisual.result.md`
