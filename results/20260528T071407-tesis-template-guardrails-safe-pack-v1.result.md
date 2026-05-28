---
job_id: 20260528T071407-tesis-template-guardrails-safe-pack-v1
worker: personal-xh
status: completed
completed_at: 2026-05-28T07:18:13-03:00
front: TESIS
no_external_actions: true
no_secrets: true
---

# Resultado - TESIS template guardrails safe pack v1

## summary

Pack seguro de guardrails para plantillas de TESIS, armado solo con contexto del
bridge y criterios metodologicos generales. La regla central se mantiene:
plantillas, matriz, protocolo y decision log primero; borrador base despues y
solo si existe necesidad metodologica o bibliografica real.

No se abrio Drive, iCloud, Photos, Zotero local, bibliotecas completas ni
documentos personales. No se modifico ningun archivo operativo ni borrador base.

## coverage_table

| Fuente | Estado | Uso |
| --- | --- | --- |
| `jobs/20260528T071407-tesis-template-guardrails-safe-pack-v1.md` | Revisada | Workorder, alcance y entregables. |
| `results/20260527T073414-tesis-protocolo-template-guardrails-v1.result.md` | Revisada | Guardrails previos para plantillas/protocolo. |
| `results/20260525T173727-tesis-empty-template-pack-v1.result.md` | Revisada | Templates vacios y regla de no tocar borrador base. |
| `results/20260525T170712-tesis-protocolo-datos-next-actions-v1.result.md` | Revisada | Protocolo de datos, variables, faltantes y bibliografia. |
| `results/20260525T184101-tesis-protocolo-decision-gate-pack-v1.result.md` | Revisada | Gate metodologico antes de editar borrador. |
| `context/fronts/tesis.md` | Ausente | Se mantiene enfoque conservador y detect-only/review-only. |

## evidencia_verificada

- Resultados previos de TESIS recomiendan no tocar el borrador base hasta tener
  pregunta, unidad de analisis, outcome primario, rol del video, variables,
  protocolo de recoleccion, matriz bibliografica y decision log.
- El pack de plantillas vacias define `HANDOFF.md`, `variables.md`,
  `data_collection_protocol.md`, planilla de datos, missing log, decision log y
  bibliography matrix sin datos reales.
- El gate metodologico previo bloquea `edit_base_draft` si faltan decisiones
  minimas, variables con definicion operacional, bibliografia verificada o
  privacidad resuelta.
- No hay en el bridge un `context/fronts/tesis.md` canonico; por eso este
  resultado no inventa estructura nueva ni contenido academico.

## inferencias

- Infiero que los guardrails deben empezar como `detect-only` o `review-only`,
  porque el objetivo es evitar ediciones no justificadas sin bloquear trabajo
  seguro de preparacion metodologica.
- Infiero que el mayor riesgo P0 es mezclar escritura cosmetica con cambios de
  fondo: una mejora de estilo puede alterar hipotesis, metodo, poblacion,
  variables o conclusiones sin trazabilidad.
- Infiero que las referencias incompletas deben quedar como backlog de busqueda,
  no como citas utilizables.

## proposed_guardrails

| Gate | Severidad | Tipo | Regla |
| --- | --- | --- | --- |
| `tesis_no_touch_base_without_decision_log` | P0 | detect-only | Detectar cualquier cambio al borrador base sin `decision_log_id`, motivo, evidencia y alcance. |
| `tesis_no_unverified_citation_as_valid` | P0 | detect-only | Detectar citas usadas en texto si no tienen `reference_id`, cita completa y `verification_status=verified`. |
| `tesis_no_claim_without_data_or_source` | P0 | detect-only | Detectar conclusion, resultado o afirmacion causal que no mapee a dato, matriz bibliografica o decision humana. |
| `tesis_no_method_variable_drift` | P0 | detect-only | Detectar cambio de pregunta, outcome, unidad de analisis, criterio de inclusion/exclusion o definicion de variable sin decision log. |
| `tesis_no_sensitive_or_real_data_in_templates` | P0 | detect-only | Detectar nombres, DNI, HC, fechas exactas identificables, voces, rostros, metadata sensible o rutas privadas en plantillas del bridge. |
| `tesis_variable_definition_complete_before_use` | P1 | review-only | Marcar variable usada sin definicion operacional, unidad/valores, fuente, regla de faltantes y version. |
| `tesis_source_type_and_validity_required` | P1 | review-only | Marcar datos o notas sin `source_type` y `validity_status` primario/derivado/inferido/contextual/pending. |
| `tesis_video_not_primary_without_protocol` | P1 | review-only | Marcar uso de video como evidencia primaria si no existe decision explicita, protocolo, privacidad y confirmacion en fuente primaria. |
| `tesis_cosmetic_edit_separate_from_method_edit` | P1 | review-only | Exigir clasificar cada propuesta como estilo, metodo, bibliografia, variable, datos o conclusion antes de aplicarla. |
| `tesis_overclaim_from_available_data` | P1 | review-only | Marcar conclusiones que exceden denominador, ventana temporal, follow-up, muestra o calidad de fuente disponible. |

## safe_next_action

Crear un workorder de implementacion para un validador local
`template_guardrails` en modo report-only/detect-only con fixtures sinteticos.
Debe leer plantillas vacias o artefactos sinteticos y devolver findings P0/P1,
sin tocar el borrador base ni cargar datos reales.

## do_not_touch

- No modificar el borrador base por estilo, claridad o entusiasmo editorial.
- No agregar citas desde memoria ni referencias incompletas.
- No cambiar hipotesis, pregunta, poblacion, unidad de analisis, outcomes,
  variables, criterios o conclusiones sin decision log.
- No convertir videos, notas docentes o material audiovisual en dato formal sin
  protocolo y privacidad aprobados.
- No cargar datos personales o identificables en el bridge.

## recommendation

Proxima accion unica: implementar el validador local report-only/detect-only con
fixtures sinteticos para los gates P0/P1 anteriores. El orquestador deberia
cerrar cualquier intento de editar el borrador base hasta que el reporte muestre
cero P0 y exista decision log para cambios de fondo.

## confidence

Media-alta para los guardrails porque derivan de resultados TESIS previos y
mantienen una politica conservadora. Media para el shape exacto del validador
porque falta una estructura canonica visible de TESIS en `context/fronts/`.

## attempted_routes

- Se hizo `git pull --rebase origin main`.
- Se ejecuto `./scripts/personal_xh_check.sh` y se detecto el job asignado.
- Se reviso el workorder actual.
- Se buscaron resultados previos de TESIS en el bridge con `rg`.
- Se revisaron resultados previos sobre plantillas vacias, protocolo de datos,
  decision gate y template guardrails.
- No se uso Telegram, Gmail, Drive, Calendar, iCloud, Photos, Zotero local,
  bibliotecas completas, adjuntos reales ni servicios externos.

## risks_limits

- Resultado declarativo: no implementa validator ni fixtures reales.
- No valida el borrador base, referencias originales ni bibliografia real.
- No decide contenido academico final; solo propone controles de proceso.
- Si el orquestador materializa una estructura TESIS distinta, los nombres de
  gates pueden mapearse sin relajar severidad.

## evidence_paths

- `jobs/20260528T071407-tesis-template-guardrails-safe-pack-v1.md`
- `results/20260528T071407-tesis-template-guardrails-safe-pack-v1.result.md`
- `results/20260527T073414-tesis-protocolo-template-guardrails-v1.result.md`
- `results/20260525T173727-tesis-empty-template-pack-v1.result.md`
- `results/20260525T170712-tesis-protocolo-datos-next-actions-v1.result.md`
- `results/20260525T184101-tesis-protocolo-decision-gate-pack-v1.result.md`
