---
job_id: 20260527T192200-tesis-protocolo-datos-y-material-audiovisual
worker: personal-xh
status: completed
completed_at: 2026-05-27T19:26:06-03:00
front: TESIS
no_external_actions: true
no_secrets: true
---

# Resultado - Tesis protocolo datos y material audiovisual

## summary honesto

La tesis no debe tocar el borrador base todavia. Primero hay que fijar
variables, fuente exacta de cada dato, decision log, politica de faltantes y
reglas para usar videos/material quirurgico solo como soporte contextual o
auditoria, no como evidencia primaria sin protocolo.

Separacion pedida:

- Evidencia: `results/20260525T021049-tesis-research-ops-protocol-v1.result.md`
  pide matriz bibliografica, variables y protocolo antes de reescrituras.
- Inferencia: el audiovisual debe mapearse a variables predefinidas, no a
  anecdotas.
- Opinion: el avance mas valioso ahora es `variables.md` con `source_type` y
  `validity_status`, no una nueva redaccion.

No modifique el borrador, no abri material sensible y no hice acciones externas.

## coverage_table

| Fuente | Estado | Uso |
| --- | --- | --- |
| `jobs/20260527T192200-tesis-protocolo-datos-y-material-audiovisual.md` | Revisada | Objetivo, restricciones y secciones requeridas. |
| `results/20260525T021049-tesis-research-ops-protocol-v1.result.md` | Revisada | Protocolo de research ops y regla de variables antes de reescritura. |
| `context/fronts/presentaciones.md` | Revisada | Uso de visuales con fuentes, QA y anonimizado. |
| `results/20260527T011700-tesis-protocolo-datos-y-material-audiovisual.result.md` | Revisada como antecedente | Clasificacion de audiovisual y variables candidatas. |
| `results/20260527T073414-tesis-protocolo-template-guardrails-v1.result.md` | Revisada | Guardrails para no tocar base sin decision log. |

## data_collection_protocol_improvements

- Crear `tesis/variables.md` antes de cargar datos.
- Cada variable debe tener definicion operacional, unidad, fuente, momento de
  medicion, valores permitidos, politica de faltantes y criterio de exclusion.
- Crear `tesis/data_collection_protocol.md` con pasos de carga y doble revision.
- Crear `tesis/decision_log.md` para cambios de definicion, inclusion/exclusion o
  uso de material audiovisual.
- Separar datos primarios, derivados, inferidos y contextuales.
- Marcar cada observacion audiovisual como `contextual`, `audit_support` o
  `candidate_variable`.
- Ningun argumento nuevo entra al borrador sin `source_id` o decision explicita.

Schema sugerido:

```yaml
variable_id:
definition_version:
operational_definition:
unit_or_scale:
source_type: historia | parte_quirurgico | imagen | video | nota_experta | bibliografia
validity_status: primary | derived | inferred | contextual | pending_review
missing_policy:
review_status: draft | needs_review | approved
decision_log_id:
```

## video_to_variable_mapping

| Observacion audiovisual | Variable candidata | Uso permitido | Limite |
| --- | --- | --- | --- |
| Paso tecnico visible | `technical_step_present` | Auditoria si estaba predefinido. | No reemplaza parte quirurgico. |
| Duracion entre pasos | `phase_duration_estimate` | Solo con timestamp confiable. | Si no hay timestamp, `pending_review`. |
| Instrumental/implante visible | `instrumentation_seen` | Confirmacion contextual. | No basta para trazabilidad final. |
| Evento intraoperatorio | `intraop_event_candidate` | Senal para revision documental. | No outcome primario. |
| Calidad de visualizacion | `visual_documentation_quality` | QA docente/metodologico. | No mide resultado clinico. |
| Explicacion del Doctor | `expert_context_note` | Nota cualitativa separada. | No dato cuantitativo. |

## ethics_privacy_limits

- No usar pacientes identificables, rostros, voces, nombres, HC, fechas, turnos,
  metadata sensible ni pantallas con datos.
- No subir material sensible a herramientas externas.
- Todo derivado debe usar ID anonimo y ruta local controlada.
- El audiovisual no debe ser fuente unica de resultado clinico.
- Si hay material docente, registrar permiso, alcance y limite de uso.
- Variables inferidas desde video quedan `pending_review` hasta validacion por
  documento o revision del Doctor.

## draft_change_candidates

Cambios candidatos, sin tocar todavia el borrador:

1. Subsection metodologica: "Gestion y trazabilidad de datos".
2. Tabla: variable, definicion, fuente, momento, faltantes y criterio de
   exclusion.
3. Subsection: "Uso de material audiovisual como soporte contextual".
4. Limitacion: los videos no sustituyen documentacion clinica formal.
5. Apendice: decision log y cambios de definicion.
6. Apendice: matriz de material audiovisual con `source_type` y `validity_status`.

## questions_for_doctor

- Que variables son obligatorias y cuales exploratorias?
- Que outcomes no deben inferirse desde video?
- El material audiovisual sera para tesis, docencia, presentacion o auditoria
  interna?
- Hay permiso/consentimiento para uso docente o solo revision interna?
- Que documentos son fuente primaria: historia, parte quirurgico, imagen, video o
  nota experta?
- Que definiciones actuales del borrador no deben modificarse?

## risks / limits

- Sin borrador base ni datos reales, esto es protocolo, no cambio textual final.
- El audiovisual puede sesgar conclusiones si se usa sin muestreo definido.
- Privacidad y consentimiento son el limite principal.
- Una variable nueva sin decision log puede contaminar la metodologia.
- Ruta alternativa si falta permiso de video: usarlo solo como nota contextual
  interna y no como variable.

## recommendation

Proxima accion: crear `tesis/variables.md` y `tesis/data_collection_protocol.md`
con 10-15 variables iniciales y columna `source_type`. No reescribir el borrador
hasta tener decision log y una tabla de variables aprobada.

## confidence

Alta para protocolo y limites; media para cambios del borrador porque no se
inspecciono texto base ni datos reales.

## evidence_paths

- `jobs/20260527T192200-tesis-protocolo-datos-y-material-audiovisual.md`
- `results/20260525T021049-tesis-research-ops-protocol-v1.result.md`
- `context/fronts/presentaciones.md`
- `results/20260527T011700-tesis-protocolo-datos-y-material-audiovisual.result.md`
- `results/20260527T073414-tesis-protocolo-template-guardrails-v1.result.md`
- `claims/20260527T192200-tesis-protocolo-datos-y-material-audiovisual.json`
