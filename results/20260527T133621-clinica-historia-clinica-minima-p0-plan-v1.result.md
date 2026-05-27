---
job_id: 20260527T133621-clinica-historia-clinica-minima-p0-plan-v1
worker: personal-xh
status: completed
completed_at: 2026-05-27T13:48:00-03:00
front: CLINICA
no_external_actions: true
no_secrets: true
---

# Resultado - Clinica historia clinica minima P0 plan v1

## summary

Recomendacion: **integrar ahora en modo detect-only/report-only**, con severidad
inicial `needs_review` para documentos reales y sin hard block.

`historia_clinica_minima_completa` es el siguiente P0 documental correcto porque
reduce riesgo medico-legal basico sin inventar normativa externa: verifica que
una historia clinica o handoff prequirurgico tenga los campos estructurales
minimos antes de avanzar a plantillas finales. La regla debe reportar ausencias,
no completar contenido, no reescribir texto y no bloquear documentos reales en
v1.

No hace falta pedir material humano para la primera version: los fixtures
sinteticos bastan para validar el contrato. La promocion a hard gate legal debe
esperar fuente oficial/versionada, revision humana y ejemplos anonimizados.

## coverage_table

| Fuente | Estado | Uso |
| --- | --- | --- |
| `jobs/20260527T133621-clinica-historia-clinica-minima-p0-plan-v1.md` | Revisada | Workorder, contexto y entregables. |
| `context/fronts/clinica.md` | Revisada | Canon CLINICA y corpus a gates. |
| `results/20260527T123551-clinica-datos-sensibles-implementation-review-v1.result.md` | Revisada | Secuencia P0 y recomendacion de este gate como siguiente. |
| `results/20260527T120441-clinica-datos-sensibles-minimizados-p0-plan-v1.result.md` | Revisada | Contrato report-only y criterios de no tocar plantillas. |
| `results/20260527T030306-clinica-documental-p0-gates-detect-only-plan-v1.result.md` | Revisada | Plan documental P0, fixtures base y severidades. |
| `results/20260527T010224-clinica-corpus-gates-backlog-v2.result.md` | Revisada | Backlog P0 y frontera de fuentes oficiales. |
| `results/20260527T113720-clinica-diagnostico-separado-implementation-review-v1.result.md` | Revisada | Patron de aceptacion en observacion para gate documental previo. |

## alcance_detect_only_report_only

```yaml
gate_id: historia_clinica_minima_completa
mode: detect_only_report_only
source_boundary: internal_documental_completeness_rule
initial_effect:
  synthetic_fixture_needs_review: true
  real_document_blocking: false
  report_findings_to_orchestrator: true
applies_to:
  document_type:
    - historia_clinica
    - prequirurgico_handoff
    - clinical_case_summary_internal
does_not_apply_to:
  - public_summary
  - export_minimized
  - texto_para_envio
  - consentimiento
  - parte_quirurgico_final
  - documento_no_clinico
allowed_statuses:
  - pass
  - needs_review
  - advisory
forbidden_in_v1:
  - hard_fail_real_document
  - auto_fill_missing_fields
  - template_rewrite
  - legal_claim_without_source_pack
```

El gate debe evaluar campos fuente cuando existan y, como respaldo, segmentos
renderizados. Si el documento no pretende ser una historia clinica completa,
debe salir de alcance o devolver `advisory`, no `needs_review` automatico.

## campos_minimos_v1

| Campo v1 | Evidencia aceptable | Severidad inicial si falta | Notas |
| --- | --- | --- | --- |
| `diagnosis_present` | `source_fields.diagnosis` o segmento `Diagnostico` no vacio. | `needs_review` | No inventar diagnostico; si hay diagnostico mezclado con indicacion, delega al gate existente. |
| `symptoms_or_evolution_present` | Motivo de consulta, sintomas, evolucion o cuadro clinico sintetico. | `needs_review` | No exigir wording unico; aceptar evolucion breve. |
| `exam_or_imaging_summary_present` | Examen fisico, neurologico, estudios o imagenes resumidas. | `needs_review` | Si el caso es administrativo, fuera de alcance. |
| `indication_or_plan_present` | Indicacion, plan, conducta o decision clinica separada. | `needs_review` | Debe estar separada de diagnostico cuando aplique. |
| `procedure_or_scope_present_when_prequirurgico` | Procedimiento propuesto, nivel/lado si aplica. | `needs_review` | Solo para handoff/prequirurgico, no para historia inicial general. |
| `professional_present` | Profesional, matricula sintetica, autor o responsable interno. | `needs_review` | No validar matricula legal real en v1. |
| `date_or_version_present` | Fecha sintetica, version o timestamp de documento. | `needs_review` | Evitar confundir con fecha de nacimiento; no aplica a export minimizado. |

No incluir en v1 como obligatorio universal:

- Firma manuscrita real, matricula verificada, source pack legal o jurisdiccion.
- Riesgos especificos de consentimiento.
- Implantes/materiales, salvo que otro gate los trate despues.
- Identificadores del paciente: privacidad ya los limita en exports.

## contrato_output

Salida sugerida, sin completar contenido faltante:

```json
{
  "case_id": "SYN-HC-001",
  "ok": false,
  "mode": "detect_only",
  "summary": {
    "fail": 0,
    "needs_review": 2,
    "advisory": 0
  },
  "findings": [
    {
      "gate_id": "historia_clinica_minima_completa",
      "status": "needs_review",
      "severity": "needs_review",
      "document_type": "historia_clinica",
      "missing_field": "diagnosis_present",
      "evidence_path": "$.source_fields.diagnosis",
      "matched_text": "<MISSING>",
      "local_context": "Historia clinica sintetica sin diagnostico consignado.",
      "source_boundary": "internal_documental_completeness_rule",
      "recommendation": "Consignar diagnostico o marcar explicitamente que queda pendiente de revision."
    }
  ]
}
```

Reglas de salida:

- `matched_text` puede ser `<MISSING>` o un placeholder sintetico; no debe
  imprimir datos reales.
- `evidence_path` debe indicar el campo o segmento faltante exacto.
- `recommendation` no debe inventar contenido clinico; solo pedir completarlo o
  revisarlo.
- Varios campos faltantes pueden agruparse en un finding si el documento esta
  claramente fuera de alcance, para evitar ruido.

## fixtures_sinteticos_minimos

| Fixture | Tipo | Input sintetico | Render/payload sintetico | Esperado |
| --- | --- | --- | --- | --- |
| `CLIN-DOC-HC-005-no-diagnosis` | Positivo | `document_type=historia_clinica; diagnosis=null; symptoms=radiculalgia; plan=evaluar conducta` | `Historia clinica: dolor lumbar irradiado. Plan: evaluar conducta.` | `needs_review` por `diagnosis_present`. |
| `CLIN-DOC-HC-006-no-symptoms-or-evolution` | Positivo | `diagnosis=hernia L4-L5; symptoms=null; evolution=null` | `Diagnostico: hernia L4-L5. Plan: microdiscectomia.` | `needs_review`. |
| `CLIN-DOC-HC-007-no-exam-or-imaging` | Positivo | `diagnosis=canal estrecho; exam=null; imaging_summary=null` | `Diagnostico e indicacion consignados sin examen ni imagenes resumidas.` | `needs_review`. |
| `CLIN-DOC-HC-008-no-plan-or-indication` | Positivo | `diagnosis=hernia L4-L5; symptoms=radiculalgia; plan=null` | `Historia completa en diagnostico y examen, sin plan ni conducta.` | `needs_review`. |
| `CLIN-DOC-HC-009-no-professional-or-date` | Positivo | `professional=null; document_date=null` | `Historia clinica sintetica con campos clinicos completos sin responsable ni fecha.` | `needs_review`. |
| `CLIN-DOC-HC-010-complete-pass` | Negativo | Campos minimos completos con placeholders sinteticos. | `Diagnostico, sintomas, examen/imagen, plan, profesional y fecha sintetica separados.` | `pass`. |
| `CLIN-DOC-HC-011-public-summary-out-of-scope-pass` | Negativo | `document_type=public_summary; diagnosis=null` | `Resumen publico minimizado sin pretension de historia completa.` | `pass` o `advisory`, no `needs_review`. |
| `CLIN-DOC-HC-012-prequirurgico-missing-level-review` | Positivo frontera | `document_type=prequirurgico_handoff; procedure=microdiscectomia; level=null` | `Handoff prequirurgico sin nivel/lado cuando aplica.` | `needs_review`. |
| `CLIN-DOC-HC-013-known-pending-diagnosis-review` | Frontera | `diagnosis_pending=true; diagnosis=null` | `Diagnostico pendiente de revision por estudios.` | `needs_review`, no `fail`. |
| `CLIN-DOC-HC-014-negated-missing-pass` | Negativo | Campos presentes; texto dice `no faltan datos clinicos minimos`. | `No faltan datos clinicos minimos; diagnostico, evolucion, examen y plan consignados.` | `pass`. |

## falsos_positivos_medico_legales

| Riesgo | Impacto | Mitigacion |
| --- | --- | --- |
| Aplicar el gate a resumenes publicos o exports minimizados. | Falsos positivos masivos: esos textos deben omitir datos por privacidad. | Activar solo por `document_type` interno. |
| Exigir todos los campos a una nota breve de evolucion. | Convierte una nota parcial en historia completa obligatoria. | `document_subtype` o `metadata.claims_complete_history=true` para aplicar v1 completo. |
| Marcar falta de plan cuando el caso esta en etapa diagnostica. | Ruido medico-legal. | Permitir `plan_pending` o `diagnosis_pending` como `needs_review` acotado, no hard fail. |
| Exigir examen fisico cuando hay solo informe de imagen/teleconsulta. | Bloqueo injustificado. | Aceptar `exam_or_imaging_summary_present` como alternativa v1. |
| Confundir fecha clinica con fecha de nacimiento. | Interfiere con gate de privacidad. | Este gate solo verifica fecha/version del documento; privacidad valida DOB en export. |
| Duplicar findings con diagnostico separado de indicacion. | Ruido y recomendaciones contradictorias. | Si diagnostico existe pero esta contaminado, dejar que dispare `diagnostico_separado_de_indicacion`; aqui cuenta como presente con advisory. |
| Pretender validar matricula/firma legal real. | Requiere fuentes y datos reales. | V1 solo verifica placeholder de responsable/fecha; no valida legalidad. |

## decision

**Integrar ahora** como plan de implementacion local, con condiciones estrictas:

1. Solo fixtures sinteticos; ningun dato real.
2. `needs_review` por defecto; no `fail` para documentos reales.
3. No tocar plantillas finales ni rutas de generacion.
4. No autocompletar campos faltantes.
5. No convertir a hard block sin fuente oficial y revision humana.
6. Activar solo en documentos que declaran ser historia clinica o handoff
   prequirurgico interno.

No pediria material humano para v1. Si el orquestador quiere calibrar
obligatoriedad legal fina, ahi si debe abrir otro workorder con source pack
oficial y ejemplos anonimizados.

## criterios_no_template_no_hard_block

```yaml
implementation_guardrails:
  templates_finales: untouched
  generated_document_text: read_only
  validator_effect: findings_only
  real_document_blocking: false
  synthetic_fixture_assertions: allowed
  source_boundary: internal_documental_completeness_rule
  promotion_to_hard_gate_requires:
    - source_pack_oficial_versionado
    - revision_medico_legal_humana
    - fixtures_false_positive_expanded
    - explicit_orchestrator_approval
```

QA minimo sugerido:

```bash
node --check scripts/qa/validate_clinical_p0_gates_v1.js
node scripts/qa/validate_clinical_p0_gates_v1.js --gate historia_clinica_minima_completa
node scripts/qa/run_clinica_core_qa.js
```

## recommendation

Proxima accion unica: crear workorder de implementacion para
`historia_clinica_minima_completa` dentro del validator clinico P0 existente,
con fixtures `CLIN-DOC-HC-005` a `CLIN-DOC-HC-014`, severidad inicial
`needs_review`, salida JSON auditable y ninguna modificacion de plantillas
finales.

## confidence

Media-alta para el alcance v1, campos minimos y decision de integrar report-only:
deriva de los resultados CLINICA previos y del backlog documental. Media para
rutas exactas hasta que el orquestador inspeccione la app canonica. Media-baja
para cualquier hard gate legal sin fuente oficial, revision humana y material
anonimizado.

## attempted_routes

- Se hizo `git pull --rebase`.
- Se ejecuto `./scripts/personal_xh_check.sh` y se detecto el job asignado.
- Se creo claim local bajo `claims/`.
- Se reviso el workorder, `context/fronts/clinica.md` y resultados CLINICA
  previos relevantes.
- No se abrio app real, Drive/iCloud/Photos/Gmail, Telegram, datos de pacientes
  ni ObraCash.

## risks_limits

- Este entregable es plan/contrato desde el bridge; no valida el diff real de la
  app canonica.
- No verifica normativa externa vigente; por eso v1 queda como regla interna y
  report-only.
- Los fixtures son sinteticos y no sustituyen revision legal ni clinica.
- La definicion exacta de historia completa puede variar por tipo documental;
  v1 debe ser conservador y reportar para revision.

## evidence_paths

- `jobs/20260527T133621-clinica-historia-clinica-minima-p0-plan-v1.md`
- `claims/20260527T133621-clinica-historia-clinica-minima-p0-plan-v1.json`
- `context/fronts/clinica.md`
- `results/20260527T123551-clinica-datos-sensibles-implementation-review-v1.result.md`
- `results/20260527T120441-clinica-datos-sensibles-minimizados-p0-plan-v1.result.md`
- `results/20260527T030306-clinica-documental-p0-gates-detect-only-plan-v1.result.md`
- `results/20260527T010224-clinica-corpus-gates-backlog-v2.result.md`
- `results/20260527T113720-clinica-diagnostico-separado-implementation-review-v1.result.md`
