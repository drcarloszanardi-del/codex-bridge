---
id: 20260525T184101-tesis-protocolo-decision-gate-pack-v1
job_id: 20260525T184101-tesis-protocolo-decision-gate-pack-v1
created_at: 2026-05-25T18:45:08-03:00
created_by: personal-xh
worker: personal-xh
status: completed
no_external_actions: true
no_secrets: true
---

# Resultado - TESIS protocolo decision gate pack v1

## summary

Gate metodologico simple para impedir ediciones del borrador base si faltan decisiones criticas, variables con definicion operacional, bibliografia verificable o reglas de privacidad para video. No carga datos, no abre documentos personales y no inventa bibliografia.

La regla central: si no estan confirmadas pregunta, unidad de analisis, outcome primario y rol del video, el sistema debe bloquear cambios al borrador y permitir solo trabajo en plantillas vacias, decision log y preparacion metodologica.

## coverage_table

| Fuente permitida | Estado | Uso |
|---|---:|---|
| `results/20260525T181001-tesis-decision-brief-variable-candidates-v1.result.md` | Revisada | Cuatro decisiones, variables candidatas y politica de faltantes. |
| `results/20260525T173727-tesis-empty-template-pack-v1.result.md` | Revisada | Templates vacios, headers y decision log. |
| `results/20260525T170712-tesis-protocolo-datos-next-actions-v1.result.md` | Revisada | Gate antes de modificar borrador, variables y riesgos. |
| `results/20260525T021049-tesis-research-ops-protocol-v1.result.md` | Revisada | Research ops y matriz bibliografica antes de reescrituras. |

## methodology_gate_contract

Entrada esperada:

```json
{
  "handoff": {},
  "variables": [],
  "bibliography_matrix": [],
  "decision_log": [],
  "target_action": "edit_base_draft|load_data|update_templates|ask_doctor",
  "video_policy": {}
}
```

Salida esperada:

```json
{
  "ok_to_edit_base_draft": false,
  "ok_to_load_data": false,
  "allowed_actions": ["ask_doctor", "update_empty_templates", "write_decision_log"],
  "blocking_reasons": [],
  "warnings": [],
  "report_topic": "TESIS"
}
```

Estados:

| Estado | Significado |
|---|---|
| `blocked` | No editar borrador ni cargar datos. |
| `template_only` | Solo plantillas vacias, headers y decision log. |
| `data_ready` | Decisiones y variables minimas completas; datos anonimizados pueden cargarse. |
| `draft_patch_ready` | Datos, bibliografia y decision log permiten proponer patch revisable al borrador. |

## required_decisions_checklist

Bloquear `edit_base_draft` y `load_data` si falta cualquiera:

| Decision | Campo sugerido | Regla |
|---|---|---|
| Pregunta | `handoff.research_question` | No vacio, una frase, sin datos sensibles. |
| Unidad de analisis | `handoff.unit_of_analysis` | Uno de `paciente`, `procedimiento`, `nivel`, `episodio`, `video`, `documento`. |
| Outcome primario | `handoff.primary_outcome` | Medible y con fuente primaria candidata. |
| Rol del video | `handoff.video_role` | Uno de `contexto_tecnico`, `fuente_secundaria`, `fuente_formal`, `no_usar`. |

Mensaje bloqueante:

```text
Gate metodologico bloquea la edicion: faltan decisiones minimas de tesis.
```

## variable_definition_gate

Cada variable usada para cargar datos debe cumplir:

| Campo | Regla |
|---|---|
| `variable_name` | snake_case, unico, no vacio. |
| `definition` | Operacional, no `pendiente`, no narrativa vaga. |
| `type` | binary/categorical/ordinal/numeric/date_bucket/controlled_text. |
| `allowed_values_or_unit` | Valores cerrados o unidad definida. |
| `source_origin` | Fuente permitida y no sensible. |
| `missing_rule` | Define no documentado/no aplica/conflicto. |
| `quality_check` | Regla de revision o trazabilidad. |

Bloquear si:

- `definition` contiene `pendiente`, `por definir`, `a completar`.
- `source_origin` no esta permitido.
- variable de outcome no tiene `primary_or_secondary`.
- `value_raw` existe en planilla pero variable no existe en `variables.md`.

## bibliography_entry_gate

No permitir cita o argumento bibliografico en borrador si la matriz no tiene:

| Campo | Regla |
|---|---|
| `reference_id` | Unico y estable. |
| `citation_full` | Completa, no `pendiente`. |
| `source_status` | `verified` o `official/peer_reviewed` segun criterio del orquestador. |
| `study_type` | Definido si se usa como evidencia. |
| `use_in_thesis` | Metodo, introduccion, discusion, limitacion, no usar. |
| `verification_status` | `verified`; si es `pending`, solo backlog. |

Mensaje bloqueante:

```text
Bibliografia no verificada: no ingresar cita ni argumento al borrador base.
```

## video_privacy_gate

Reglas por rol:

| Rol | Permitido | Bloqueado |
|---|---|---|
| `no_usar` | Nada relacionado con video. | Cualquier carga o inferencia desde video. |
| `contexto_tecnico` | Preguntas, checklist, indice interno no identificable. | Outcomes, conclusiones, datos clinicos formales. |
| `fuente_secundaria` | Marcar `requiere_confirmacion`. | Reemplazar parte/HC o fuente primaria. |
| `fuente_formal` | Solo con protocolo, consentimiento/permisos y anonimizado. | Uso sin decision log y sin privacidad aprobada. |

Bloquear siempre si hay nombres, DNI, HC real, fechas exactas identificables, audio identificable, pantallas con datos, metadatos sensibles o material fuera del entorno local.

## draft_base_lock_rules

| Target action | Condicion para permitir |
|---|---|
| `ask_doctor` | Siempre permitido. |
| `update_empty_templates` | Permitido si no agrega datos reales. |
| `write_decision_log` | Permitido si no imprime secretos ni datos sensibles. |
| `load_data` | Requiere cuatro decisiones, variables definidas y politica de privacidad. |
| `edit_base_draft` | Requiere decisiones, variables, bibliografia verificada, decision log y datos anonimizados. |
| `add_citation_to_draft` | Requiere `verification_status=verified`. |
| `use_video_as_data` | Requiere `video_role=fuente_formal` y protocolo aprobado. |

## minimal_validator_pseudocode

```python
def validate_tesis_gate(state, target_action):
    reasons = []
    warnings = []

    required = [
        ("research_question", state.handoff.get("research_question")),
        ("unit_of_analysis", state.handoff.get("unit_of_analysis")),
        ("primary_outcome", state.handoff.get("primary_outcome")),
        ("video_role", state.handoff.get("video_role")),
    ]
    for name, value in required:
        if not value or str(value).strip().lower() in {"pendiente", "por definir"}:
            reasons.append(f"missing_required_decision:{name}")

    for variable in state.variables:
        if is_used(variable) and not has_operational_definition(variable):
            reasons.append(f"variable_without_operational_definition:{variable.name}")
        if variable.source_origin not in ALLOWED_SOURCE_ORIGINS:
            reasons.append(f"invalid_source_origin:{variable.name}")

    if target_action in {"edit_base_draft", "add_citation_to_draft"}:
        for entry in state.bibliography_matrix:
            if entry.use_in_thesis and entry.verification_status != "verified":
                reasons.append(f"bibliography_not_verified:{entry.reference_id}")

    if video_has_identifiable_risk(state.video_policy):
        reasons.append("video_privacy_not_cleared")

    allowed = not reasons
    if target_action in {"ask_doctor", "update_empty_templates", "write_decision_log"}:
        allowed = True

    return {
        "ok": allowed,
        "blocking_reasons": reasons,
        "warnings": warnings,
        "allowed_actions": allowed_actions_from(reasons),
    }
```

## telegram_topic_report_format

No enviar Telegram desde este worker. Formato para que el orquestador lo use si corresponde:

```text
TESIS gate metodologico:
Estado: BLOCKED / TEMPLATE_ONLY / DATA_READY / DRAFT_PATCH_READY
Bloqueos:
- missing_required_decision: research_question
- variable_without_operational_definition: primary_outcome_value
Accion segura:
- pedir al Doctor pregunta, unidad, outcome y rol del video
No tocar:
- borrador base
- citas
- datos reales
```

## next_actions_for_orchestrator

1. Implementar validator simple sobre `HANDOFF.md`, `variables.md`, `bibliography_matrix.csv` y `decision_log.md`.
2. Correrlo antes de cualquier accion `edit_base_draft`.
3. Si bloquea, pedir al Doctor solo la decision faltante.
4. Mantener `template_only` hasta completar cuatro decisiones.
5. Permitir carga de datos solo anonimizados y solo con variables completas.
6. Permitir patch al borrador solo cuando bibliografia y decision log esten verificados.

## recommendation

Activar este gate como preflight obligatorio antes de editar borrador. La version inicial puede bloquear todo `edit_base_draft` salvo que `HANDOFF.md` tenga las cuatro decisiones y `variables.md` no tenga ningun `pendiente` en variables usadas.

## risks_limits

- No se abrio Drive, iCloud, Photos ni documentos personales.
- No se cargaron datos reales ni bibliografia.
- El gate puede ser conservador y bloquear trabajo valido; mejor desbloquear por decision log que relajar privacidad.
- Si el diseno final cambia, se actualizan campos permitidos pero no se elimina el bloqueo metodologico.

## confidence

Alta para reglas de bloqueo metodologico y privacidad. Media para shape exacto del parser hasta ver archivos materializados por Codex principal.

## evidence_paths

- `jobs/20260525T184101-tesis-protocolo-decision-gate-pack-v1.md`
- `results/20260525T181001-tesis-decision-brief-variable-candidates-v1.result.md`
- `results/20260525T173727-tesis-empty-template-pack-v1.result.md`
- `results/20260525T170712-tesis-protocolo-datos-next-actions-v1.result.md`
- `results/20260525T021049-tesis-research-ops-protocol-v1.result.md`
