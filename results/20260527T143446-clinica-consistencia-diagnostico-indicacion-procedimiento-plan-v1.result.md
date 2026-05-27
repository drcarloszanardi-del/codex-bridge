---
job_id: 20260527T143446-clinica-consistencia-diagnostico-indicacion-procedimiento-plan-v1
worker: personal-xh
status: completed
completed_at: 2026-05-27T14:42:00-03:00
front: CLINICA
no_external_actions: true
no_secrets: true
---

# Resultado - Clinica consistencia diagnostico indicacion procedimiento plan v1

## summary

Recomendacion: **integrar ahora en modo detect-only/report-only**, con severidad
inicial `needs_review` y sin hard block.

`consistencia_diagnostico_indicacion_procedimiento` debe verificar que diagnostico,
indicacion, procedimiento propuesto, nivel, lateralidad y estado del plan no se
contradigan cuando esos datos estan presentes y suficientemente estructurados.
No debe decidir medicina por si solo ni inventar relaciones clinicas: en v1 solo
reporta inconsistencias documentales obvias o ambiguas para revision.

Este gate tiene sentido ahora porque ya existen observaciones para topografia,
diagnostico separado, datos sensibles e historia minima. Si faltan campos
basicos, la inconsistencia debe degradar a `advisory` o esperar a que
`historia_clinica_minima_completa` reporte los faltantes.

## coverage_table

| Fuente | Estado | Uso |
| --- | --- | --- |
| `jobs/20260527T143446-clinica-consistencia-diagnostico-indicacion-procedimiento-plan-v1.md` | Revisada | Workorder, contexto y entregables. |
| `context/fronts/clinica.md` | Revisada | Canon CLINICA y corpus a gates. |
| `results/20260527T140548-clinica-historia-minima-implementation-review-v1.result.md` | Revisada | Gate previo aceptado y candidato siguiente. |
| `results/20260527T133621-clinica-historia-clinica-minima-p0-plan-v1.result.md` | Revisada | Alcance de historia minima y frontera de faltantes. |
| `results/20260527T030306-clinica-documental-p0-gates-detect-only-plan-v1.result.md` | Revisada | Plan documental P0 y contrato detect-only. |
| `results/20260527T010224-clinica-corpus-gates-backlog-v2.result.md` | Revisada | Backlog documental P0 y limites legales. |
| `results/20260527T113720-clinica-diagnostico-separado-implementation-review-v1.result.md` | Revisada | Riesgos del gate diagnostico/indicacion ya observado. |

## alcance_detect_only_report_only

```yaml
gate_id: consistencia_diagnostico_indicacion_procedimiento
mode: detect_only_report_only
source_boundary: internal_clinical_documental_consistency_rule
initial_effect:
  synthetic_fixture_needs_review: true
  real_document_blocking: false
  report_findings_to_orchestrator: true
applies_to:
  document_type:
    - historia_clinica
    - prequirurgico_handoff
    - consentimiento
    - parte_quirurgico_draft
requires_at_least:
  - diagnosis_or_indication_present
  - procedure_or_plan_present
does_not_apply_to:
  - public_summary
  - export_minimized
  - texto_para_envio
  - documento_no_clinico
  - documents_with_missing_core_fields
allowed_statuses:
  - pass
  - needs_review
  - advisory
forbidden_in_v1:
  - hard_fail_real_document
  - auto_correct_procedure
  - infer_missing_level_or_laterality
  - legal_claim_without_source_pack
```

Si `historia_clinica_minima_completa` ya marco faltantes centrales, este gate no
debe sumar ruido como `fail`; puede emitir un unico `advisory` indicando que la
consistencia no es evaluable hasta completar campos.

## checks_v1_recomendados

| Check v1 | Disparo | Severidad inicial | Regla |
| --- | --- | --- | --- |
| `level_consistency_when_present` | Diagnostico/indicacion/procedimiento contienen niveles distintos. | `needs_review` | Solo comparar niveles explicitamente presentes; no inferir nivel faltante. |
| `laterality_consistency_when_present` | Lado/lateralidad difiere entre diagnostico, indicacion y procedimiento. | `needs_review` | Comparar derecha/izquierda/bilateral solo cuando estan presentes. |
| `procedure_matches_indication_family` | Familia de procedimiento no corresponde con familia de indicacion documentada. | `needs_review` | Usar familias amplias y conservadoras, no micro-taxonomia clinica. |
| `no_procedure_if_plan_pending_unless_marked` | Hay procedimiento concreto mientras `plan_pending=true` o conducta pendiente sin decision. | `needs_review` | Si se marca como posible/alternativa, emitir `advisory` o `pass`. |
| `no_part_contradicts_preop_scope` | Parte draft describe nivel/lado/procedimiento distinto al handoff prequirurgico. | `needs_review` | Solo si ambos documentos estan en el mismo fixture sintetico y tienen campos completos. |

Familias v1 sugeridas:

```yaml
procedure_families:
  decompression:
    terms: [descompresion, laminectomia, recalibraje]
  discectomy:
    terms: [microdiscectomia, discectomia]
  fusion:
    terms: [artrodesis, fijacion, instrumentacion]
  dural_repair:
    terms: [reparacion dural, parche dural, cierre dural]
```

Una contradiccion entre familias debe ser `needs_review`, no `fail`, porque puede
haber combinaciones reales o procedimientos complementarios.

## contrato_output

Salida sugerida:

```json
{
  "case_id": "SYN-CONSIST-001",
  "ok": false,
  "mode": "detect_only",
  "summary": {
    "fail": 0,
    "needs_review": 1,
    "advisory": 0
  },
  "findings": [
    {
      "gate_id": "consistencia_diagnostico_indicacion_procedimiento",
      "status": "needs_review",
      "severity": "needs_review",
      "check_id": "level_consistency_when_present",
      "document_type": "prequirurgico_handoff",
      "evidence_path": "$.source_fields",
      "matched_text": "<STRUCTURED_LEVEL_MISMATCH>",
      "local_context": "diagnosis.level=L4-L5; procedure.level=L5-S1",
      "source_boundary": "internal_clinical_documental_consistency_rule",
      "recommendation": "Revisar coherencia de nivel entre diagnostico, indicacion y procedimiento."
    }
  ]
}
```

Reglas de salida:

- No imprimir datos reales; usar campos sinteticos, categorias o placeholders.
- `matched_text` debe ser un marcador estructurado, no texto clinico largo.
- `evidence_path` debe apuntar a campo fuente o segmento exacto.
- `recommendation` debe pedir revision, no proponer el procedimiento correcto.
- Si faltan datos basicos, devolver `advisory` de no evaluable, no una cadena de
  falsos positivos.

## fixtures_sinteticos_minimos

| Fixture | Tipo | Input sintetico | Render/payload sintetico | Esperado |
| --- | --- | --- | --- | --- |
| `CLIN-DOC-CONSIST-005-level-mismatch-review` | Positivo | `diagnosis.level=L4-L5; indication.level=L4-L5; procedure.level=L5-S1` | Handoff prequirurgico con niveles discordantes. | `needs_review` por `level_consistency_when_present`. |
| `CLIN-DOC-CONSIST-006-laterality-mismatch-review` | Positivo | `diagnosis.laterality=derecha; procedure.laterality=izquierda` | Procedimiento propuesto con lateralidad opuesta. | `needs_review`. |
| `CLIN-DOC-CONSIST-007-family-mismatch-review` | Positivo | `indication_family=decompression; procedure_family=fusion` sin justificacion. | Indicacion de descompresion y procedimiento de artrodesis como unica conducta. | `needs_review`, no `fail`. |
| `CLIN-DOC-CONSIST-008-plan-pending-with-procedure-review` | Positivo | `plan_pending=true; procedure=microdiscectomia L4-L5` | Conducta pendiente pero procedimiento concreto redactado como decidido. | `needs_review`. |
| `CLIN-DOC-CONSIST-009-consistent-pass` | Negativo | `diagnosis=hernia L4-L5 derecha; indication=microdiscectomia; procedure=microdiscectomia L4-L5 derecha` | Diagnostico, indicacion y procedimiento coinciden. | `pass`. |
| `CLIN-DOC-CONSIST-010-missing-core-fields-advisory` | Negativo/frontera | `diagnosis=null; procedure=microdiscectomia` y gate HC marca faltante. | No hay suficientes datos para consistencia. | `advisory` o `pass`, no `needs_review` duplicado. |
| `CLIN-DOC-CONSIST-011-broad-lumbar-pass` | Negativo | `diagnosis=hernia lumbar; procedure=microdiscectomia lumbar; level=null` | Nivel no especificado en ambos lados. | `pass` o `advisory`, no mismatch. |
| `CLIN-DOC-CONSIST-012-combined-procedure-review` | Frontera | `indication=descompresion; procedure=descompresion mas artrodesis` | Familia combinada posible pero no justificada. | `needs_review`, no `fail`. |
| `CLIN-DOC-CONSIST-013-historical-mismatch-pass` | Negativo | Antecedente: cirugia previa L5-S1; actual: diagnostico/procedimiento L4-L5. | Diferencia en antecedentes historicos. | `pass` si segmentado como antecedente. |
| `CLIN-DOC-CONSIST-014-negated-mismatch-pass` | Negativo | Texto dice que no hay discordancia de nivel/lado y campos coinciden. | Negacion metadocumental. | `pass`. |

## falsos_positivos_medico_legales

| Riesgo | Impacto | Mitigacion |
| --- | --- | --- |
| Comparar contra antecedentes historicos. | Marca como contradiccion una cirugia previa o nivel antiguo. | Segmentar `antecedentes` y excluirlos de mismatch actual. |
| Inferir nivel/lado faltante. | Convierte falta de datos en contradiccion falsa. | Solo comparar cuando ambos lados tienen valor explicito. |
| Penalizar procedimientos combinados reales. | Artrodesis + descompresion puede ser correcto en algunos casos. | Familias combinadas son `needs_review`, nunca `fail`. |
| Confundir indicacion general con procedimiento final. | Una indicacion amplia puede admitir mas de un procedimiento. | Usar familias amplias y pedir revision, no correccion automatica. |
| Duplicar historia minima. | Si faltan diagnostico/plan, consistencia no es evaluable. | Degradar a `advisory` cuando falten campos centrales. |
| Duplicar topografia/no-inventar. | Topografia inventada ya tiene gate propio. | Este gate compara consistencia entre campos existentes; no decide si el dato fue inventado. |
| Bloquear consentimiento correcto por wording legal. | Consentimiento puede expresar el procedimiento con frase no tecnica. | Report-only; no hard block; usar normalizacion conservadora. |

## decision

**Integrar ahora** como plan de implementacion local.

Condiciones:

1. Solo fixtures sinteticos; ningun dato real.
2. Severidad real inicial `needs_review` o `advisory`; no hard block.
3. No tocar plantillas finales ni reescribir documentos.
4. No autocompletar nivel, lateralidad, indicacion o procedimiento.
5. No inferir contradiccion si faltan campos centrales.
6. No promover a hard gate sin revision medico-legal humana y source pack donde
   corresponda.

No pediria material humano para v1. La implementacion puede arrancar con
comparaciones estructuradas y fixtures sinteticos; la calibracion clinica fina
debe venir despues.

## criterios_no_template_no_hard_block

```yaml
implementation_guardrails:
  templates_finales: untouched
  generated_document_text: read_only
  validator_effect: findings_only
  real_document_blocking: false
  synthetic_fixture_assertions: allowed
  source_boundary: internal_clinical_documental_consistency_rule
  promotion_to_hard_gate_requires:
    - revision_medico_legal_humana
    - fixtures_false_positive_expanded
    - explicit_orchestrator_approval
    - source_pack_oficial_si_se_invoca_obligacion_legal
```

QA minimo sugerido:

```bash
node --check scripts/qa/validate_clinical_p0_gates_v1.js
node scripts/qa/validate_clinical_p0_gates_v1.js --gate consistencia_diagnostico_indicacion_procedimiento
node scripts/qa/run_clinica_core_qa.js
```

## recommendation

Proxima accion unica: crear workorder de implementacion para
`consistencia_diagnostico_indicacion_procedimiento` dentro del validator clinico
P0 existente, con fixtures `CLIN-DOC-CONSIST-005` a `CLIN-DOC-CONSIST-014`,
severidad inicial `needs_review`, salida JSON auditable y ninguna modificacion
de plantillas finales.

## confidence

Media-alta para el alcance v1 y la decision de integrar report-only, porque
deriva de la secuencia de gates CLINICA ya observados y del backlog documental.
Media para rutas exactas hasta que el orquestador inspeccione la app canonica.
Media-baja para cualquier hard gate clinico/legal sin revision humana, source
pack aplicable y material anonimizado.

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
- Las familias de procedimiento son deliberadamente amplias; no sustituyen
  criterio medico.
- Cualquier contradiccion ambigua debe ser `needs_review`, no bloqueo.

## evidence_paths

- `jobs/20260527T143446-clinica-consistencia-diagnostico-indicacion-procedimiento-plan-v1.md`
- `claims/20260527T143446-clinica-consistencia-diagnostico-indicacion-procedimiento-plan-v1.json`
- `context/fronts/clinica.md`
- `results/20260527T140548-clinica-historia-minima-implementation-review-v1.result.md`
- `results/20260527T133621-clinica-historia-clinica-minima-p0-plan-v1.result.md`
- `results/20260527T030306-clinica-documental-p0-gates-detect-only-plan-v1.result.md`
- `results/20260527T010224-clinica-corpus-gates-backlog-v2.result.md`
- `results/20260527T113720-clinica-diagnostico-separado-implementation-review-v1.result.md`
