---
job_id: 20260527T110517-clinica-documental-p0-next-implementation-audit-v1
worker: personal-xh
status: completed
completed_at: 2026-05-27T11:13:00-03:00
front: CLINICA
no_external_actions: true
no_secrets: true
---

# Resultado - Clinica documental P0 next implementation audit v1

## summary

Recomendacion unica: **integrar ahora
`diagnostico_separado_de_indicacion` en modo detect-only/report-only**.

Es el siguiente P0 documental con mejor relacion valor/riesgo porque ya tiene
plan, implementation pack, fixtures sinteticos y fronteras de falsos positivos.
Ademas no exige inventar normativa externa: es una regla documental interna
estrecha que separa el hecho diagnostico del plan terapeutico. Los otros P0
documentales son importantes, pero requieren source pack oficial o mayor
calibracion antes de promoverlos.

No toque app real, plantillas finales, Drive/iCloud/Photos/Gmail, Telegram,
datos de pacientes ni ObraCash. Esta revision usa solo bridge y resultados
previos.

## coverage_table

| Fuente | Estado | Uso |
| --- | --- | --- |
| `jobs/20260527T110517-clinica-documental-p0-next-implementation-audit-v1.md` | Revisada | Workorder, limites y entregable. |
| `context/fronts/clinica.md` | Revisada | Canon CLINICA y lista de corpus a gates. |
| `results/20260527T030306-clinica-documental-p0-gates-detect-only-plan-v1.result.md` | Revisada | Backlog documental P0 y contrato detect-only. |
| `results/20260527T063553-clinica-next-documental-p0-gate-plan-v1.result.md` | Revisada | Candidato unico recomendado y criterios. |
| `results/20260527T070409-clinica-diagnostico-separado-implementation-pack-v1.result.md` | Revisada | Fixture JSON, pseudocodigo, severidades y QA commands. |
| `results/20260527T010224-clinica-corpus-gates-backlog-v2.result.md` | Revisada | Priorizacion documental y limites de fuentes oficiales. |
| `results/20260526T145636-clinica-p0-extraforaminal-no-interlaminar-plan-v1.result.md` | Revisada | Patron de gate estrecho, detect-only y control de falso positivo. |

## next_p0_recommendation

| Gate | Decision | Motivo |
| --- | --- | --- |
| `diagnostico_separado_de_indicacion` | **Integrar** | Ya tiene pack implementable, regla interna estrecha, fixtures positivos/negativos y bajo riesgo de dependencia legal externa. |
| `consentimiento_especifico_no_generico` | Esperar | Importante, pero antes de hard gate necesita source pack oficial/versionado y calibracion de wording legal. |
| `historia_clinica_minima_completa` | Esperar | Puede sobregenerar falsos positivos si no esta mapeado por tipo documental y fuente oficial. |
| `consistencia_diagnostico_indicacion_procedimiento` | Esperar | Requiere mas criterio clinico y topografia/procedimiento estructurados; conviene despues del gate de diagnostico separado. |
| `datos_sensibles_minimizados` | Esperar batch especifico | Es P0 real de privacidad, pero pertenece mejor a un gate de export/handoff con politica de audiencia, no al primer validator documental. |

## detect_only_report_only_criteria

```yaml
gate_id: diagnostico_separado_de_indicacion
mode: detect_only_report_only
source_boundary: internal_documental_rule
applies_to:
  document_type:
    - historia_clinica
    - consentimiento
    - parte_quirurgico
  segment:
    - diagnostico
    - diagnosis
    - dx
does_not_apply_to:
  - plan
  - indicacion
  - procedimiento
  - antecedentes
  - consentimiento_general_text_outside_diagnosis
  - texto_libre_sin_segmento_identificable_as_fail
initial_effect:
  synthetic_fixture_fail: true
  real_document_blocking: false
  report_findings_to_orchestrator: true
```

Condicion de disparo estrecha:

```text
Fallar solo si un marcador terapeutico afirmado aparece dentro del segmento
Diagnostico/Dx, por ejemplo "con indicacion de", "se indica", "requiere
descompresion quirurgica", "se programa", "candidato a", "tratamiento
quirurgico".
```

Si falta seccion diagnostico, si el texto es ambiguo, o si el marcador aparece
en antecedentes/plan/procedimiento, devolver `needs_review` o `pass`, no `fail`.

## minimal_fixtures

| Fixture | Tipo | Input sintetico | Render sintetico | Esperado |
| --- | --- | --- | --- | --- |
| `CLIN-DOC-DX-005-indication-in-diagnosis` | Positivo | `diagnosis=hernia L4-L5 derecha; indication=microdiscectomia L4-L5 derecha` | `Diagnostico: hernia L4-L5 derecha con indicacion de microdiscectomia.` | `fail` |
| `CLIN-DOC-DX-006-requires-surgery-in-diagnosis` | Positivo | `diagnosis=canal estrecho lumbar; indication=descompresion` | `Diagnostico: canal estrecho lumbar que requiere descompresion quirurgica.` | `fail` |
| `CLIN-DOC-DX-007-separated-pass` | Negativo | `diagnosis=hernia L4-L5 derecha; indication=microdiscectomia L4-L5 derecha` | `Diagnostico: hernia L4-L5 derecha. Indicacion: microdiscectomia L4-L5 derecha.` | `pass` |
| `CLIN-DOC-DX-008-negated-pass` | Negativo | `diagnosis=hernia L4-L5 derecha; indication=null` | `Diagnostico: hernia L4-L5 derecha. No se consigna indicacion dentro del diagnostico.` | `pass` |
| `CLIN-DOC-DX-009-history-marker-pass` | Negativo | `diagnosis=hernia L4-L5; antecedent=cirugia indicada en otro centro` | `Antecedentes: se habia indicado cirugia en otro centro. Diagnostico: hernia L4-L5.` | `pass` o `needs_review`, nunca `fail` |
| `CLIN-DOC-DX-010-ambiguous-requires-review` | Frontera | `diagnosis=canal estrecho` | `Diagnostico: canal estrecho; requiere correlacion con imagenes.` | `needs_review` |

## medico_legal_false_positive_risks

| Riesgo | Impacto | Mitigacion |
| --- | --- | --- |
| Marcar `requiere` no terapeutico. | Puede bloquear frases diagnosticas validas como "requiere correlacion". | `requires` solo `fail` si esta cerca de cirugia/procedimiento; si no, `needs_review`. |
| Evaluar todo el consentimiento como diagnostico. | Falsos positivos masivos por lenguaje de autorizacion. | Segmentar por headings; este gate solo mira Diagnostico/Dx. |
| Marcar antecedentes historicos. | Confunde historia previa con indicacion actual. | Clasificar Antecedentes/Historia previa como `pass` o `needs_review`. |
| Confundir regla documental con norma legal. | Sobrerreclamo medico-legal sin fuente oficial. | `source_boundary=internal_documental_rule`; no citar normativa no verificada. |
| Bloquear documento real antes de calibrar. | Riesgo operativo y legal por automatismo. | En v1 solo QA sintetico y reporte; no hard block de documento real. |
| Fallar por falta de seccion diagnostico. | Plantillas viejas o texto libre pueden quedar mal castigados. | `needs_review` por parseo incompleto, no `fail`. |

## decision

**Integrar** en la app canonica como workorder local de implementacion, con estas
condiciones:

1. Agregar fixtures sinteticos bajo el pack documental.
2. Implementar validator puro; sin tocar plantillas finales.
3. Conectar a QA core como reporte detect-only.
4. Fallar solo fixtures sinteticos `fail`; documentos reales producen findings.
5. Versionar salida JSON con `matched_text`, `local_context`,
   `evidence_path`, `source_boundary` y `recommendation`.
6. No promover a bloqueo real hasta pasar QA focal, QA core y revision del
   orquestador/Doctor.

## recommendation

Proxima accion unica: crear el workorder de implementacion para
`diagnostico_separado_de_indicacion` con los fixtures sinteticos listados,
validator detect-only/report-only y conexion a QA core solo como reporte. No
tocar plantillas finales ni convertirlo en bloqueo real todavia.

## qa_commands

Comandos sugeridos en la app canonica, no ejecutados desde el bridge:

```bash
node -c scripts/qa/validate_documental_p0_gates_v1.js
node scripts/qa/validate_documental_p0_gates_v1.js --fixture data/derived/clinical_test_cases/documental_p0_gates_v1.json --gate diagnostico_separado_de_indicacion
node -c scripts/qa/validate_clinical_p0_gates_v1.js
node scripts/qa/validate_clinical_p0_gates_v1.js
node scripts/qa/run_clinica_core_qa.js
```

Validaciones bridge para este resultado:

```bash
python3 scripts/validate_result_contract.py results/20260527T110517-clinica-documental-p0-next-implementation-audit-v1.result.md
git diff --check
python3 scripts/secret_scan.py
```

## attempted_routes

- Se hizo `git pull --rebase`.
- Se inspeccionaron jobs asignados con `./scripts/personal_xh_check.sh`.
- Se reclamo el job con `python3 scripts/bridgectl.py claim`.
- Se reviso el workorder y los resultados CLINICA indicados.
- Se reviso contexto canonico `context/fronts/clinica.md` y backlog documental.
- No se abrio app real, Drive/iCloud/Photos/Gmail, Telegram, datos de pacientes
  ni ObraCash.

## risks_limits

- No se certifica estado local de la app canonica; el workorder declara tres
  gates ya integrados, pero el bridge no contiene esa app ni su diff.
- No se verifico normativa externa; por eso la regla queda interna y report-only.
- Si el orquestador ya integro `diagnostico_separado_de_indicacion` despues del
  pack previo, entonces el siguiente candidato seria `datos_sensibles_minimizados`
  como batch separado de export/handoff; con la evidencia disponible, no consta
  esa integracion.

## confidence

Media-alta para recomendar `diagnostico_separado_de_indicacion`, porque ya hay
plan, fixtures y pack de implementacion en el bridge. Media para rutas exactas y
estado real de integracion, porque no se inspecciono la app canonica ni QA local.

## evidence_paths

- `jobs/20260527T110517-clinica-documental-p0-next-implementation-audit-v1.md`
- `claims/20260527T110517-clinica-documental-p0-next-implementation-audit-v1.json`
- `context/fronts/clinica.md`
- `results/20260527T030306-clinica-documental-p0-gates-detect-only-plan-v1.result.md`
- `results/20260527T063553-clinica-next-documental-p0-gate-plan-v1.result.md`
- `results/20260527T070409-clinica-diagnostico-separado-implementation-pack-v1.result.md`
- `results/20260527T010224-clinica-corpus-gates-backlog-v2.result.md`
- `results/20260526T145636-clinica-p0-extraforaminal-no-interlaminar-plan-v1.result.md`
