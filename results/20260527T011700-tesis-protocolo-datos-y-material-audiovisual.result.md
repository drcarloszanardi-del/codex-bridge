---
job_id: 20260527T011700-tesis-protocolo-datos-y-material-audiovisual
worker: personal-xh
status: completed
completed_at: 2026-05-27T01:19:00-03:00
front: TESIS
no_external_actions: true
no_secrets: true
---

# Resultado - Tesis protocolo datos y material audiovisual

## summary honesto

La mejora metodologica no debe tocar el borrador base todavia: primero hay que
definir variables, fuente exacta de cada dato, decision log y reglas para usar
video/material quirurgico solo como insumo contextual o auditoria, no como dato
primario sin protocolo. Los videos pueden ayudar a mapear pasos tecnicos,
tiempos, decisiones y calidad de documentacion, pero requieren anonimizado,
consentimiento/permiso y separacion de variables observables vs inferidas.

Evidencia: el protocolo tesis pide matriz bibliografica, variables y decision
log antes de reescrituras. Inferencia: el audiovisual debe convertirse en
variables predefinidas, no en anecdotas. Opinion: el primer avance util es una
tabla de variables con fuente y estado de validez.

No modifique el borrador, no abri material sensible y no hice acciones externas.

## coverage_table

| Fuente | Estado | Uso |
| --- | --- | --- |
| `jobs/20260527T011700-tesis-protocolo-datos-y-material-audiovisual.md` | Revisada | Entregables y restricciones. |
| `results/20260525T021049-tesis-research-ops-protocol-v1.result.md` | Revisada | Artefactos y criterio de no tocar fondo sin evidencia. |
| `decisions/tesis_research_ops_protocol_v1.md` | Revisada | Variables, matriz bibliografica, decision log y no hacer. |
| `context/fronts/presentaciones.md` | Revisada | Uso de material visual con fuentes, QA y anonimizado. |

## data_collection_protocol_improvements

- Crear `tesis/variables.md` antes de cargar datos.
- Para cada variable: definicion operacional, unidad, fuente, momento de
  medicion, valores permitidos, faltantes y criterio de exclusion.
- Crear `tesis/data_collection_protocol.md` con pasos de carga y doble revision.
- Crear `tesis/decision_log.md` para cambios de definicion o inclusion.
- Separar datos primarios, datos derivados y observaciones audiovisuales.
- Marcar todo dato audiovisual como `contextual`, `audit_support` o `candidate_variable`.

## video_to_variable_mapping

| Observacion en video/material | Variable candidata | Uso permitido |
| --- | --- | --- |
| Paso quirurgico visible | `technical_step_present` | Auditoria contextual si estaba predefinido. |
| Tiempo aproximado entre pasos | `phase_duration_estimate` | Solo si el video tiene timestamp confiable. |
| Uso de instrumental/implante | `instrumentation_seen` | Confirmacion contextual, no reemplaza parte quirurgico. |
| Complicacion visible | `intraop_event_candidate` | Requiere validacion documental/medica. |
| Calidad de visualizacion | `visual_documentation_quality` | QA de material docente, no outcome clinico. |
| Explicacion del Doctor | `expert_context_note` | Nota cualitativa separada de dato cuantitativo. |

## ethics_privacy_limits

- No usar pacientes identificables, voces, rostros, HC, nombres, fechas o
  metadata sensible en herramientas externas.
- El video quirurgico no debe convertirse en fuente unica de resultado clinico.
- Si hay material docente, registrar permiso/consentimiento y alcance de uso.
- Todo derivado debe usar ID anonimo y ruta local controlada.
- Las variables inferidas desde video deben quedar marcadas como inferencia hasta
  validacion por documento o revision del Doctor.

## draft_change_candidates

Cambios candidatos, sin tocar todavia el borrador:

1. Agregar subseccion metodologica: "Gestion y trazabilidad de datos".
2. Agregar tabla: variable, definicion, fuente, momento, criterio de faltante.
3. Agregar subseccion: "Uso de material audiovisual como soporte contextual".
4. Agregar limitacion: los videos no sustituyen documentacion clinica formal.
5. Agregar apendice de decision log y criterios de exclusion.

## questions_for_doctor

- Que variables clinicas son obligatorias y cuales son exploratorias?
- Hay videos/material quirurgico con permiso docente o solo uso interno?
- El audiovisual debe apoyar tesis, presentacion o entrenamiento interno?
- Que outcomes no deben inferirse desde video?
- Hay definiciones actuales que no deben cambiarse durante la carga?

## risks / limits

- Sin acceso al borrador ni datos, esto es protocolo y no cambio textual final.
- El audiovisual puede sesgar conclusiones si se usa como evidencia primaria sin
  muestreo definido.
- Privacidad y consentimiento son el limite principal.
- Cualquier variable nueva debe pasar por decision log antes de cargar.

## recommendation

Proxima accion: crear `tesis/variables.md` y `tesis/data_collection_protocol.md`
con 10-15 variables iniciales y una columna `source_type` que distinga historia,
parte quirurgico, imagen, video y nota experta. No reescribir el borrador hasta
tener esa tabla.

## confidence

Alta para protocolo y limites; media para cambios del borrador porque no se
inspecciono el texto base ni datos reales.

## evidence_paths

- `jobs/20260527T011700-tesis-protocolo-datos-y-material-audiovisual.md`
- `results/20260525T021049-tesis-research-ops-protocol-v1.result.md`
- `decisions/tesis_research_ops_protocol_v1.md`
- `context/fronts/presentaciones.md`
