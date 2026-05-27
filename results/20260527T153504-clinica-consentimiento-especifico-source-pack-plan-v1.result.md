---
job_id: 20260527T153504-clinica-consentimiento-especifico-source-pack-plan-v1
worker: personal-xh
status: completed
completed_at: 2026-05-27T15:49:00-03:00
front: CLINICA
no_external_actions: true
no_secrets: true
---

# Resultado - Clinica consentimiento especifico source pack plan v1

## summary

Recomendacion: **esperar source-pack humano/versionado antes de implementar el
gate completo**, pero avanzar ahora con el contrato, fixtures sinteticos y el
esqueleto detect-only/report-only.

`consentimiento_especifico_no_generico` es el siguiente P0 documental correcto:
los gates ya observados cubren diagnostico separado, datos sensibles, historia
minima y consistencia diagnostico-indicacion-procedimiento. El riesgo ahora es
que un consentimiento salga generico, incompleto o desacoplado del procedimiento
real. Aun asi, este gate no debe inventar riesgos quirurgicos, alternativas ni
wording legal. En v1 solo debe verificar presencia, especificidad y trazabilidad
a una fuente interna/oficial versionada.

Decision practica: **no tocar plantillas finales ni bloquear documentos reales**.
Primero crear source-pack minimo y fixtures; despues implementar report-only con
`needs_review` por defecto.

## coverage_table

| Fuente | Estado | Uso |
| --- | --- | --- |
| `jobs/20260527T153504-clinica-consentimiento-especifico-source-pack-plan-v1.md` | Revisada | Workorder, contexto operativo y reglas. |
| `context/fronts/clinica.md` | Revisada | Canon CLINICA y backlog corpus a gates. |
| `results/20260527T150703-clinica-consistencia-implementation-review-v1.result.md` | Revisada | Cierre del gate previo y recomendacion de pasar a consentimiento. |
| `results/20260527T030306-clinica-documental-p0-gates-detect-only-plan-v1.result.md` | Revisada | Contrato detect-only/report-only y fixtures iniciales CONS. |
| `results/20260527T010224-clinica-corpus-gates-backlog-v2.result.md` | Revisada | Frontera de fuente oficial/versionada antes de hard gate. |
| `results/20260527T063553-clinica-next-documental-p0-gate-plan-v1.result.md` | Revisada | Razon previa para posponer consentimiento hasta source-pack. |

## alcance_detect_only_report_only

```yaml
gate_id: consentimiento_especifico_no_generico
mode: detect_only_report_only
initial_real_document_severity: needs_review
synthetic_fixture_assertions: allowed
real_document_blocking: false
applies_to:
  - consentimiento
  - consentimiento_prequirurgico
  - consentimiento_anexo_procedimiento
does_not_apply_to:
  - historia_clinica
  - parte_quirurgico
  - public_summary
  - export_minimized
  - texto_para_envio
requires_at_least:
  - document_type_is_consent
  - source_pack_policy_version
  - procedure_or_family_source_ref
output_effect:
  - findings_only
  - no_template_mutation
  - no_autocomplete
forbidden_in_v1:
  - hard_block_real_document
  - invent_risk_list
  - invent_alternatives
  - rewrite_consent_text
  - validate_legal_sufficiency_as_final
```

La salida debe pedir revision y trazabilidad, no redactar el consentimiento por
su cuenta.

## source_pack_minimo

Antes de implementar checks activos, debe existir un pack versionado, aunque sea
interno y sintetico al comienzo:

```yaml
source_pack:
  id: consentimiento_especifico_no_generico_v1
  version: 2026-05-27
  status: draft_for_detect_only
  owner_review_required:
    - medico_responsable
    - revision_legal_humana_antes_de_hard_gate
  entries:
    - source_id: internal_consent_baseline_v1
      tipo: protocolo_interno
      status: draft
      applies_to: consentimiento_prequirurgico
      required_fields:
        - procedure_name_or_family
        - anatomical_region_or_level_when_applicable
        - laterality_when_applicable
        - risks_source_ref
        - alternatives_source_ref
        - patient_specific_consistency_ref
      forbidden_use: no_crea_hard_gate_legal
    - source_id: official_or_legal_source_placeholder
      tipo: norma_oficial_o_revision_legal
      status: pending
      required_before:
        - hard_block_real_document
        - wording_obligatorio
        - risk_list_mandatory_content
```

Campos minimos por fixture/documento:

```yaml
metadata:
  consent_policy_version: consentimiento_especifico_no_generico_v1
  source_pack_refs:
    procedure_specificity: internal_consent_baseline_v1
    risks: approved_risk_catalog_ref
    alternatives: approved_alternative_catalog_ref
source_fields:
  procedure_family:
  procedure_name:
  anatomical_region:
  level:
  laterality:
  risks_ref_ids: []
  alternatives_ref_ids: []
  diagnosis_ref:
  indication_ref:
rendered_text:
```

Regla clave: si `risks_ref_ids` o `alternatives_ref_ids` estan vacios, el gate
solo reporta faltante. No debe generar ni sugerir la lista.

## checks_v1_recomendados

| Check v1 | Disparo | Severidad | Regla |
| --- | --- | --- | --- |
| `generic_consent_language_detected` | Frases como "procedimiento que el medico considere" sin procedimiento especifico en el mismo documento/anexo. | `needs_review` | Detectar lenguaje generico; pasar si existe anexo especifico referenciado. |
| `procedure_specificity_present` | Falta `procedure_name` o `procedure_family` trazable al source pack. | `needs_review` | Requiere nombre/familia aprobada; no inventar tecnica. |
| `anatomical_scope_present_when_applicable` | Falta region/nivel cuando el procedimiento lo requiere segun source pack. | `needs_review` | No inferir de diagnostico; pedir revision. |
| `laterality_present_when_applicable` | Falta lateralidad cuando source pack la marca aplicable. | `needs_review` | No aplica a procedimientos no lateralizables. |
| `risk_source_refs_present` | No hay refs aprobadas para riesgos. | `needs_review` | Verificar presencia de refs, no contenido legal. |
| `alternatives_source_refs_present` | No hay refs aprobadas para alternativas. | `needs_review` | Verificar presencia de refs, no inventar alternativas. |
| `blank_or_placeholder_sections` | Texto contiene placeholders sin resolver como `<RIESGOS>` o `...`. | `needs_review` | Reportar campo incompleto. |
| `consent_matches_case_scope` | Procedimiento/nivel/lado del consentimiento contradice campos estructurados del caso. | `needs_review` | Reutilizar normalizacion de consistencia; no duplicar si el gate previo ya reporta mismatch. |

Todos los checks reales deben ser `needs_review` en v1. Los fixtures sinteticos
pueden fallar QA para asegurar deteccion.

## fixtures_sinteticos_minimos

| Fixture | Tipo | Payload sintetico | Render/payload sintetico | Esperado |
| --- | --- | --- | --- | --- |
| `CLIN-DOC-CONSENT-001-generic-only-review` | Positivo | `document_type=consentimiento; procedure_name=null; risks_ref_ids=[]; alternatives_ref_ids=[]` | "Autorizo el procedimiento que el medico considere necesario." | `needs_review` por lenguaje generico y faltantes. |
| `CLIN-DOC-CONSENT-002-procedure-family-missing-review` | Positivo | `procedure_family=null; procedure_name=null; rendered_text` con consentimiento amplio. | No hay procedimiento especifico ni familia. | `needs_review`. |
| `CLIN-DOC-CONSENT-003-risk-refs-missing-review` | Positivo | `procedure_name=microdiscectomia sintetica; risks_ref_ids=[]` | Procedimiento nombrado pero sin refs de riesgos. | `needs_review`, sin inventar riesgos. |
| `CLIN-DOC-CONSENT-004-alternatives-refs-missing-review` | Positivo | `alternatives_ref_ids=[]` | Texto dice "se explicaron alternativas" sin refs. | `needs_review`. |
| `CLIN-DOC-CONSENT-005-placeholder-review` | Positivo | `risks_ref_ids=[RISK_SYN_001]` | Texto contiene `<RIESGOS_ESPECIFICOS>` o puntos suspensivos. | `needs_review`. |
| `CLIN-DOC-CONSENT-006-specific-with-refs-pass` | Negativo | `procedure_name=microdiscectomia sintetica; level=L4-L5; laterality=derecha; risks_ref_ids=[RISK_SYN_001]; alternatives_ref_ids=[ALT_SYN_001]` | Consentimiento especifico con refs sinteticas y sin placeholders. | `pass`. |
| `CLIN-DOC-CONSENT-007-annex-specific-pass` | Negativo/frontera | Documento principal generico pero `annex_ref=consent_specific_synthetic_v1` presente y completo. | Lenguaje general mas anexo especifico trazable. | `pass` o `advisory`, no `needs_review` fuerte. |
| `CLIN-DOC-CONSENT-008-negated-generic-pass` | Negativo | Texto metadocumental: "No se usa consentimiento generico..." con campos completos. | Mencion negada de generico. | `pass`. |
| `CLIN-DOC-CONSENT-009-not-applicable-public-summary-pass` | Negativo | `document_type=public_summary` | Resumen publico con lenguaje simple. | `pass`; gate fuera de alcance. |
| `CLIN-DOC-CONSENT-010-consistency-mismatch-review` | Positivo/frontera | Caso L4-L5 derecha; consentimiento L5-S1 izquierda. | Campos estructurados contradicen alcance del consentimiento. | `needs_review` con evidence paths; coordinar con gate de consistencia. |

## falsos_positivos_medico_legales

| Riesgo | Impacto | Mitigacion |
| --- | --- | --- |
| Consentimiento general + anexo especifico valido. | Marcaria como generico un paquete documental correcto. | Soportar `annex_ref` y bundle scope antes de disparar fuerte. |
| Procedimiento no lateralizable. | Exigiria lateralidad donde no corresponde. | `laterality_when_applicable` debe venir del source pack, no de heuristica libre. |
| Procedimiento por etapas o plan posible. | Puede parecer incompleto o contradictorio. | Si `plan_pending=true`, emitir `advisory`/`needs_review`, no hard fail. |
| Riesgos/alternativas aprobados por catalogo externo. | El texto puede no listar todo en el campo renderizado. | Aceptar refs versionadas; no exigir wording completo en v1. |
| Consentimiento de anestesia o transfusion separado. | Puede faltar en este documento por estar en otro consentimiento. | Permitir `separate_consent_ref` antes de reportar faltante. |
| Lenguaje legal amplio alrededor de contenido especifico. | Frases genericas pueden coexistir con procedimiento especifico. | Disparar solo si no hay especificidad trazable en el mismo documento/bundle. |
| Secciones con placeholders redacted de prueba. | Puede confundir placeholder seguro con faltante real. | Whitelist de placeholders redacted; reportar solo placeholders operativos sin resolver. |

## reglas_no_template_no_hard_block

```yaml
implementation_guardrails:
  templates_finales: untouched
  generated_consent_text: read_only
  validator_effect: findings_only
  real_document_blocking: false
  severity_real_documents: needs_review
  matched_text_policy:
    use_short_structured_marker: true
    avoid_long_clinical_text: true
  source_boundary:
    - internal_consent_baseline_v1_for_detect_only
    - official_source_required_before_hard_gate
  promotion_to_hard_gate_requires:
    - source_pack_oficial_o_revision_legal_versionada
    - revision_medico_legal_humana
    - fixtures_false_positive_expanded
    - explicit_orchestrator_approval
```

No debe tocar plantillas ni proponer texto final. Cualquier mejora de wording va
en otro workorder, con baseline leido y revision humana.

## decision

**Esperar source-pack humano/versionado antes de implementar el gate completo.**

Implementable ahora, sin riesgo, solo:

1. Crear el archivo de source-pack draft con refs sinteticas y estado `pending`.
2. Crear fixtures `CLIN-DOC-CONSENT-001` a `010`.
3. Crear contrato de salida detect-only.

No implementaria deteccion activa sobre documentos reales hasta que exista al
menos un baseline interno aprobado para procedimiento, riesgos y alternativas.
No pediria datos de pacientes ni material real; si hace falta material humano,
debe ser un checklist anonimo/aprobado por el Doctor o una fuente legal
versionada, no chats ni documentos clinicos privados.

## recommendation

Proxima accion unica: abrir workorder de **source-pack draft + fixtures
sinteticos** para `consentimiento_especifico_no_generico`, con output
report-only y sin tocar plantillas. La implementacion del validator debe esperar
a que ese source-pack exista y declare explicitamente que no crea hard gate.

## confidence

Media-alta para el alcance, fixtures y guardrails porque derivan del backlog
CLINICA y de la secuencia de gates P0 ya observados. Media para el contenido
exacto del source-pack porque requiere revision humana/legal antes de fijar
riesgos, alternativas o wording. Baja para cualquier hard block legal sin fuente
oficial/versionada, revision humana y aprobacion explicita.

## attempted_routes

- Se hizo `git pull --rebase`.
- Se ejecuto `./scripts/personal_xh_check.sh` y se detecto el job asignado.
- Se reclamo el job con `python3 scripts/bridgectl.py claim`.
- Se reviso el workorder, `context/fronts/clinica.md` y resultados CLINICA
  previos relevantes.
- No se abrio app real, Drive/iCloud/Photos/Gmail, Telegram, datos de pacientes
  ni ObraCash.

## risks_limits

- No se verifico normativa externa ni vigencia legal.
- No se inspecciono app canonica ni plantillas reales.
- Este entregable no define riesgos quirurgicos ni alternativas concretas; solo
  exige refs aprobadas.
- El source-pack debe ser versionado antes de cualquier promocion a hard gate.

## evidence_paths

- `jobs/20260527T153504-clinica-consentimiento-especifico-source-pack-plan-v1.md`
- `claims/20260527T153504-clinica-consentimiento-especifico-source-pack-plan-v1.json`
- `context/fronts/clinica.md`
- `results/20260527T150703-clinica-consistencia-implementation-review-v1.result.md`
- `results/20260527T030306-clinica-documental-p0-gates-detect-only-plan-v1.result.md`
- `results/20260527T010224-clinica-corpus-gates-backlog-v2.result.md`
- `results/20260527T063553-clinica-next-documental-p0-gate-plan-v1.result.md`
