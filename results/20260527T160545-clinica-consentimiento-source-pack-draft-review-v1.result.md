---
job_id: 20260527T160545-clinica-consentimiento-source-pack-draft-review-v1
worker: personal-xh
status: completed
completed_at: 2026-05-27T16:14:00-03:00
front: CLINICA
no_external_actions: true
no_secrets: true
---

# Resultado - Clinica consentimiento source-pack draft review v1

## summary

Veredicto: **aceptar el draft en observacion, con ajustes de cobertura antes de
activar un validator sobre documentos reales**.

Segun el orquestador, se agregaron un source-pack draft, fixtures sinteticos y
un validator focal para `consentimiento_especifico_no_generico`, sin conectar al
producto, sin tocar templates finales y sin hard block. El QA local declarado
paso (`validate_consentimiento_especifico_source_pack_v1` y
`run_clinica_core_qa`). Eso cumple el paso seguro recomendado: source-pack y
fixtures primero, deteccion activa despues.

No recomiendo revertir. Tampoco recomiendo saltar directo a enforcement real.
El siguiente paso puede ser un validator detect-only activo **solo si** queda
limitado a `needs_review`, `findings_only`, documentos sinteticos/anonimizados y
source-pack versionado como draft; nada de bloqueo real ni generacion de riesgos,
alternativas o wording legal.

## coverage_table

| Fuente | Estado | Uso |
| --- | --- | --- |
| `jobs/20260527T160545-clinica-consentimiento-source-pack-draft-review-v1.md` | Revisada | Workorder, archivos declarados, QA local y reglas. |
| `context/fronts/clinica.md` | Revisada | Canon CLINICA, corpus a gates y limites de fuentes. |
| `results/20260527T153504-clinica-consentimiento-especifico-source-pack-plan-v1.result.md` | Revisada | Plan previo de source-pack/fixtures y guardrails. |
| `results/20260527T150703-clinica-consistencia-implementation-review-v1.result.md` | Revisada | Secuencia P0 y frontera de consistencia. |
| `results/20260527T030306-clinica-documental-p0-gates-detect-only-plan-v1.result.md` | Revisada | Contrato general detect-only/report-only. |

## accept_adjust_revert

Decision: **aceptar draft**.

Condiciones de aceptacion:

```yaml
accept_draft:
  app_product_connection: false
  template_changes: false
  real_document_blocking: false
  validator_scope: source_pack_and_synthetic_fixtures_only
  source_pack_status: draft_for_detect_only
  active_real_document_severity_if_next_step: needs_review
  forbidden:
    - invent_risk_list
    - invent_alternatives
    - rewrite_consent
    - claim_legal_sufficiency
```

No hay motivo para revertir con la evidencia disponible. Si hubiera un ajuste
antes de continuar, seria fortalecer fixtures de frontera y schema del
source-pack, no tocar producto.

## risks_p0_p1

| Pri | Riesgo | Tipo | Mitigacion |
| --- | --- | --- | --- |
| P0 | **Draft usado como hard gate legal.** Un pack interno no equivale a fuente legal vigente ni revision humana. | Medico-legal | `status=draft_for_detect_only`; prohibir hard block y wording obligatorio hasta aprobacion explicita. |
| P0 | **Riesgos o alternativas inventados por el validator.** Si faltan refs, el sistema podria completar contenido. | Medico-legal | Reportar `missing_ref`; nunca generar lista ni sugerir texto final. |
| P0 | **Template final modificado por deriva del trabajo.** El source-pack podria usarse como excusa para editar consentimiento. | Operativo | Mantener este workstream en datos/QA; cualquier template requiere workorder separado con baseline. |
| P1 | **Consentimiento principal generico con anexo especifico.** Puede ser paquete valido si el anexo esta trazado. | Falso positivo | Soportar `annex_ref`, `bundle_id` y `specificity_source_ref`. |
| P1 | **Procedimiento no lateralizable.** Exigir lateralidad siempre genera ruido. | Falso positivo | `laterality_required` debe venir del source-pack por familia/procedimiento. |
| P1 | **Consentimientos separados.** Anestesia, transfusion u otros anexos pueden estar fuera del documento principal. | Falso positivo | Permitir `separate_consent_ref` y reportar solo si el source-pack lo exige. |
| P1 | **Placeholders seguros vs incompletos.** Tokens redacted pueden confundirse con campos sin resolver. | Falso positivo | Whitelist de redacted tokens; bloquear solo placeholders operativos (`<RIESGOS_ESPECIFICOS>`). |
| P1 | **Mala version del source-pack.** Fixture puede pasar con source-pack viejo o pendiente. | Falso negativo | Exigir `consent_policy_version` y `source_pack_hash`/`source_pack_version`. |
| P1 | **Salida con texto clinico largo.** Findings pueden persistir contenido sensible o medico largo. | Privacidad/ruido | Usar marcadores estructurados y evidence paths; contexto corto/redacted. |

## fixtures_faltantes_antes_de_validator_activo

Antes de implementar un validator activo sobre documentos reales, agregaria estos
fixtures sinteticos:

| Fixture | Tipo | Payload sintetico | Esperado |
| --- | --- | --- | --- |
| `CLIN-DOC-CONSENT-011-annex-specific-bundle-pass` | Negativo/frontera | Consentimiento principal generico + `annex_ref` completo y versionado. | `pass` o `advisory`, no `needs_review` fuerte. |
| `CLIN-DOC-CONSENT-012-non-lateralizable-pass` | Negativo | Procedimiento/familia con `laterality_required=false` y lateralidad ausente. | `pass`. |
| `CLIN-DOC-CONSENT-013-separate-anesthesia-ref-pass` | Negativo/frontera | Consentimiento quirurgico con `separate_consent_ref=anesthesia_synthetic_v1`. | No reportar faltante por anestesia separada. |
| `CLIN-DOC-CONSENT-014-source-pack-version-missing-review` | Positivo | Documento con campos completos pero sin `consent_policy_version` o `source_pack_version`. | `needs_review`. |
| `CLIN-DOC-CONSENT-015-risk-ref-unknown-review` | Positivo | `risks_ref_ids=[RISK_SYN_UNKNOWN]`. | `needs_review`, no inventar ni aceptar ref desconocida. |
| `CLIN-DOC-CONSENT-016-alternative-ref-unknown-review` | Positivo | `alternatives_ref_ids=[ALT_SYN_UNKNOWN]`. | `needs_review`. |
| `CLIN-DOC-CONSENT-017-rendered-placeholder-review` | Positivo | Refs presentes pero render conserva `<RIESGOS_ESPECIFICOS>` o `TODO`. | `needs_review`. |
| `CLIN-DOC-CONSENT-018-redacted-token-pass` | Negativo | Texto contiene `<PATIENT_REDACTED>` o `[dato omitido]` seguro. | `pass`; no confundir con placeholder incompleto. |
| `CLIN-DOC-CONSENT-019-consent-vs-case-scope-review` | Positivo | Caso/procedimiento estructurado L4-L5 derecha; consentimiento L5-S1 izquierda. | `needs_review`, coordinado con gate de consistencia. |
| `CLIN-DOC-CONSENT-020-source-pack-pending-no-hard-block` | Frontera | Source-pack `status=pending_human_review`. | Findings permitidos, hard block prohibido. |

Estos fixtures son mas importantes que ampliar patrones de texto. La prioridad
es que el validator no se exceda, no filtre contenido y no bloquee.

## avanzar_o_esperar

Decision: **avanzar a implementacion detect-only real acotada, pero esperar
revision humana para cualquier bloqueo o criterio legal fuerte**.

Alcance permitido para el proximo paso:

```yaml
next_validator_scope:
  applies_to: consentimiento
  source_pack_status_allowed:
    - draft_for_detect_only
  real_document_effect: findings_only
  severity: needs_review
  output:
    - gate_id
    - check_id
    - evidence_path
    - structured_marker
    - recommendation_review_only
  forbidden:
    - hard_fail_real_document
    - write_template
    - generate_risks_or_alternatives
    - quote_long_rendered_text
```

Esperar revision humana antes de:

- marcar consentimiento como legalmente suficiente o insuficiente;
- convertir `needs_review` en hard block;
- fijar listas obligatorias de riesgos/alternativas;
- modificar templates finales.

## recommendation

Siguiente trabajo recomendado para Pablo:
**implementation review del validator detect-only de consentimiento**, despues de
que el orquestador implemente:

1. lectura del source-pack draft;
2. checks `generic_consent_language_detected`,
   `procedure_specificity_present`, `risk_source_refs_present`,
   `alternatives_source_refs_present` y `blank_or_placeholder_sections`;
3. fixtures `CONSENT-011` a `020`;
4. salida `needs_review` report-only con contexto corto/redacted.

Si el orquestador prefiere no activar todavia, alternativa segura: pedir a
Pablo una segunda pasada de QA del source-pack schema, enfocada en versionado,
hash, refs desconocidas y placeholders.

## confidence

Media-alta para aceptar el draft en observacion, porque el cambio declarado
respeta el plan previo y QA local OK. Media para autorizar validator activo
acotado, porque no inspeccione el diff real ni el JSON de fixtures. Baja para
cualquier hard gate o afirmacion legal sin source-pack oficial/versionado,
revision medico-legal humana y aprobacion explicita.

## attempted_routes

- Se hizo `git pull --rebase`.
- Se ejecuto `./scripts/personal_xh_check.sh` y se detecto el job asignado.
- Se reclamo el job con `python3 scripts/bridgectl.py claim`.
- Se reviso el workorder, `context/fronts/clinica.md` y resultados CLINICA
  previos relevantes.
- No se abrio app real, Drive/iCloud/Photos/Gmail, Telegram, datos de pacientes
  ni ObraCash.

## risks_limits

- El QA local fue tomado como declaracion del orquestador; no se ejecuto contra
  la app real desde el bridge.
- No se verifico normativa externa ni vigencia legal.
- No se inspeccionaron los archivos reales nuevos del source-pack.
- Todo el analisis se limita a fixtures sinteticos y al diff descrito.

## evidence_paths

- `jobs/20260527T160545-clinica-consentimiento-source-pack-draft-review-v1.md`
- `claims/20260527T160545-clinica-consentimiento-source-pack-draft-review-v1.json`
- `context/fronts/clinica.md`
- `results/20260527T153504-clinica-consentimiento-especifico-source-pack-plan-v1.result.md`
- `results/20260527T150703-clinica-consistencia-implementation-review-v1.result.md`
- `results/20260527T030306-clinica-documental-p0-gates-detect-only-plan-v1.result.md`
