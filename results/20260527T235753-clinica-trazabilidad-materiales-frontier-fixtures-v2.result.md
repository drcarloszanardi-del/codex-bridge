---
job_id: 20260527T235753-clinica-trazabilidad-materiales-frontier-fixtures-v2
worker: personal-xh
status: completed
completed_at: 2026-05-27T23:59:36-03:00
front: CLINICA
no_external_actions: true
no_secrets: true
---

# Resultado - Clinica trazabilidad materiales frontier fixtures v2

## summary

Recomendacion: **integrar ahora como tests sinteticos de estabilidad** los
fixtures `CLIN-P0-064` a `CLIN-P0-068`, manteniendo el gate
`trazabilidad_implantes_materiales` en detect-only/report-only.

Los cinco casos son de bajo riesgo porque no cambian plantillas, no tocan
documentos reales y solo estabilizan fronteras ya identificadas: material
estructurado completo, descartables no implantables, injerto autologo, familia
quirurgica ambigua y texto instructivo fuera del cuerpo clinico. No justifican
hard block ni autocorreccion.

## coverage_table

| Fuente | Estado | Uso |
| --- | --- | --- |
| `jobs/20260527T235753-clinica-trazabilidad-materiales-frontier-fixtures-v2.md` | Revisada | Objetivo, reglas, entregable y casos frontera solicitados. |
| `results/20260527T235024-clinica-trazabilidad-materiales-implementation-review-v1.result.md` | Revisada | Veredicto de observacion, riesgos y cinco fixtures propuestos. |
| `results/20260527T233900-clinica-next-p0-gates-prioritization-after-ayudantes-v1.result.md` | Revisada | Contrato base del gate y fixtures `CLIN-P0-054` a `063`. |
| `context/fronts/clinica.md` | Revisada | Canon CLINICA y regla de no tocar plantillas sin baseline/test focal. |

## fixture_pack

| Fixture | Payload sintetico minimo | Expected status | Criterio | Falso positivo que previene | Severidad recomendada |
| --- | --- | --- | --- | --- | --- |
| `CLIN-P0-064-structured-material-complete-text-silent-pass` | `document_type=parte_quirurgico; procedure_family=fijacion_lumbar; technical_body="se realiza fijacion segun tecnica"; materials=[{family:tornillo_pedicular, qty:4, levels:L4-L5, ref:REF_SYN},{family:barra, qty:2, levels:L4-L5, ref:REF_SYN}]` | `pass` | La trazabilidad estructurada completa puede satisfacer el gate aunque el cuerpo tecnico sea escueto. | Evita exigir duplicacion narrativa cuando los campos estructurados ya estan completos. | Sin finding; estabilidad. |
| `CLIN-P0-065-disposable-material-not-implant-pass` | `document_type=parte_quirurgico; procedure_family=hernia_lumbar; technical_body="se utilizan gasas y sutura de cierre"; materials=[]` | `pass` | Sutura, gasas y descartables no implantables quedan fuera de trazabilidad de implantes/materiales implantables. | Evita que la palabra generica "material" o insumos de cierre disparen revision. | Sin finding; estabilidad. |
| `CLIN-P0-066-autologous-graft-source-review` | `document_type=parte_quirurgico; procedure_family=injerto_oseo; technical_body="se coloca injerto oseo autologo"; materials=[{family:injerto_autologo, source_site:null, qty:QTY_SYN}]` | `needs_review` | Injerto autologo requiere origen/sitio donante cuando aplique, no lote/modelo comercial generico. | Evita falso fail por pedir lote a material autologo y evita falso pass con origen ausente. | P1 report-only. |
| `CLIN-P0-067-family-suggests-instrumentation-no-material-review` | `document_type=protocolo_quirurgico; procedure_family=instrumentacion; technical_body="se realiza abordaje y preparacion quirurgica sin mencion clara de implantes"; materials=[]` | `needs_review` | La familia sugiere material, pero sin mencion afirmativa ni campos estructurados no debe ser `fail`. | Evita hard fail por familia sola y marca ambiguedad documental. | P1 report-only. |
| `CLIN-P0-068-correction-note-ignored-pass` | `document_type=parte_quirurgico; procedure_family=hernia_lumbar; technical_body="microdiscectomia sin implantes"; qa_note="corregir: si hubo implantes registrar tornillos y barras"; materials=[]; ignored_fields=["qa_note"]` | `pass` | Texto instructivo/correccion fuera del cuerpo clinico no debe alimentar el detector. | Evita que notas internas o instrucciones contaminen hallazgos clinicos. | Sin finding; si dispara, P1. |

## risks_p0_p1

| Pri | Riesgo | Impacto | Mitigacion con fixtures |
| --- | --- | --- | --- |
| P0 | El gate se promueve por error a hard block real. | Podria bloquear documentos por criterios todavia observacionales. | Mantener `mode=report_only` en todos los nuevos casos y fallar solo tests sinteticos. |
| P1 | Material descartable/no implantable se confunde con implante. | Alertas ruidosas en partes con sutura, gasas o insumos de cierre. | `CLIN-P0-065` debe pasar/no aplicar. |
| P1 | Texto instructivo o nota de correccion se analiza como cuerpo clinico. | Hallazgos falsos por palabras "implante", "tornillos" o "barras" fuera del acto quirurgico. | `CLIN-P0-068` delimita `source_boundary` e `ignored_fields`. |
| P1 | Familia instrumentacion sin material explicito se trata como fail. | Falso positivo en documentos incompletos o clasificacion amplia. | `CLIN-P0-067` exige `needs_review`, no `fail`. |
| P1 | Injerto autologo se valida con campos de implante comercial. | Falso fail por lote/modelo o falso pass sin sitio de origen. | `CLIN-P0-066` diferencia `source_site` de `lot_or_batch`. |

No veo un P0 nuevo inherente al pack si se conserva report-only. El P0 aparece
solo si alguien usa estos fixtures como excusa para bloquear documentos reales.

## implementation_notes

Campos de salida esperados para los cinco casos:

```yaml
gate_id: trazabilidad_implantes_materiales
mode: report_only
document_type: required
procedure_family: required
material_family: required_when_applicable
missing_fields: array
evidence_path: exact_field_or_segment
source_boundary: structured_materials | technical_body | ignored_non_clinical_note
recommendation: concise_review_instruction
```

Regla de oro: el detector debe leer solo fuentes clinicas admitidas
(`technical_body`, `structured_materials`, checklist clinico declarado). No debe
leer notas de QA, instrucciones del prompt, comentarios de correccion ni texto de
orquestacion.

## backlog_or_now

Integrarlos ahora como tests de estabilidad. Son pruebas sinteticas, pequenas y
conservadoras. No requieren source-pack legal ni decision comercial porque no
definen nuevos campos obligatorios para documentos reales; solo fijan los limites
de no ruido.

No promover nada a hard block despues de integrarlos. La promocion futura deberia
esperar inspeccion del diff real, revision humana de politica de trazabilidad y
fixtures adicionales con datos reales anonimizados o generados, nunca pacientes.

## recommendation

Crear `CLIN-P0-064` a `CLIN-P0-068` en el pack de fixtures sinteticos del
validator clinico y correr:

```bash
node -c scripts/qa/validate_clinical_p0_gates_v1.js
node scripts/qa/validate_clinical_p0_gates_v1.js
node scripts/qa/run_clinica_core_qa.js
```

Aceptar solo si los casos `064`, `065` y `068` no generan findings, `066` y
`067` generan `needs_review`, y todos conservan `mode=report_only`.

## confidence

Alta para el criterio de fixtures porque deriva directamente del contrato ya
aceptado y reduce falsos positivos previsibles. Media para rutas exactas y estado
de implementacion porque la app canonica no esta disponible en esta Mac y no se
inspecciono el validator real.

## attempted_routes

- Se hizo `git pull --rebase`.
- Se ejecuto `./scripts/personal_xh_check.sh` y se detecto el job asignado.
- Se reviso `jobs/20260527T235753-clinica-trazabilidad-materiales-frontier-fixtures-v2.md`.
- Se reviso `results/20260527T235024-clinica-trazabilidad-materiales-implementation-review-v1.result.md`.
- Se reviso `results/20260527T233900-clinica-next-p0-gates-prioritization-after-ayudantes-v1.result.md`.
- Se reviso `context/fronts/clinica.md`.
- No se uso Telegram, Gmail, Drive, Calendar, iCloud, Photos, adjuntos, datos de
  pacientes ni fuentes externas.

## risks_limits

- Este resultado no modifica el validator ni agrega los fixtures reales; entrega
  el pack y criterio para que el orquestador lo integre.
- No se inspecciono codigo de la app canonica ni se ejecutaron tests Node aqui.
- No se verifico normativa externa ni vigencia legal.
- No se tocaron plantillas, documentos reales, pacientes ni corpus medico-legal.
- La decision final queda en Codex orquestador.

## evidence_paths

- `jobs/20260527T235753-clinica-trazabilidad-materiales-frontier-fixtures-v2.md`
- `claims/20260527T235753-clinica-trazabilidad-materiales-frontier-fixtures-v2.json`
- `results/20260527T235753-clinica-trazabilidad-materiales-frontier-fixtures-v2.result.md`
- `results/20260527T235024-clinica-trazabilidad-materiales-implementation-review-v1.result.md`
- `results/20260527T233900-clinica-next-p0-gates-prioritization-after-ayudantes-v1.result.md`
- `context/fronts/clinica.md`
