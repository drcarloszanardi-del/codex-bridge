---
job_id: 20260527T233900-clinica-next-p0-gates-prioritization-after-ayudantes-v1
worker: personal-xh
status: completed
completed_at: 2026-05-27T23:39:36-03:00
front: CLINICA
no_external_actions: true
no_secrets: true
---

# Resultado - Clinica next P0 gates prioritization after ayudantes v1

## summary

Recomendacion: **integrar ahora, en detect-only/report-only, el gate
`trazabilidad_implantes_materiales`** para partes quirurgicos.

Despues de cerrar en observacion los gates de topografia, descompresion,
extraforaminal, secuencia hemostasia y ayudantes, el siguiente mayor impacto con
menor riesgo de falso positivo es trazabilidad de materiales/implantes cuando
el propio parte o la familia quirurgica declara uso de material. Es acotado,
deterministico, no necesita inventar normativa ni tocar plantillas, y cubre un
riesgo medico-legal fuerte en columna: tornillos, barras, PMMA/cemento, injertos,
separadores, cajas u otro material mencionado sin tipo/nivel/lado/cantidad o sin
referencia minima.

No promover a hard block. La primera integracion debe reportar findings y fallar
solo fixtures sinteticos. Si falta dato humano o fuente tecnica, el resultado es
`needs_review`, no autocorreccion.

## coverage_table

| Fuente | Estado | Uso |
| --- | --- | --- |
| `jobs/20260527T233900-clinica-next-p0-gates-prioritization-after-ayudantes-v1.md` | Revisada | Objetivo, candidatos, restricciones y entregables. |
| `context/fronts/clinica.md` | Revisada | Backlog corpus a gates y regla de no tocar plantillas. |
| `results/20260527T010224-clinica-corpus-gates-backlog-v2.result.md` | Revisada | Priorizacion P0/P1 y trazabilidad de parte quirurgico. |
| `results/20260527T190454-clinica-corpus-gates-backlog-v2.result.md` | Revisada | Backlog actualizado, P1 implantes/materiales y limites legales. |
| `results/20260527T153504-clinica-consentimiento-especifico-source-pack-plan-v1.result.md` | Revisada | Estado consentimiento: importante, pero source-pack/humano antes de activacion amplia. |
| `results/20260527T160545-clinica-consentimiento-source-pack-draft-review-v1.result.md` | Revisada | Draft aceptado; validator real todavia requiere fronteras y revision. |
| `results/20260527T120441-clinica-datos-sensibles-minimizados-p0-plan-v1.result.md` | Revisada | Privacidad/export: alto valor, pero ya tiene plan/flujo previo. |
| `results/20260527T133621-clinica-historia-clinica-minima-p0-plan-v1.result.md` | Revisada | Historia minima: alto valor, mas amplio y mas ruidoso si ya no esta observado. |

## ranking_candidatos

| Rank | Gate | Decision | Justificacion breve |
| --- | --- | --- | --- |
| 1 | `trazabilidad_implantes_materiales` | **Integrar ahora report-only** | Mayor valor incremental tras gates quirurgicos: aplica solo si hay implante/material o procedimiento material-dependiente; falsos positivos controlables con `when_applicable`; no inventa contenido clinico. |
| 2 | `consentimiento_especifico_no_generico` | Dejar listo, pedir dato humano/source-pack antes de activar amplio | P0 medico-legal muy alto, pero alto riesgo si se exigen riesgos/alternativas/wording sin source-pack oficial o baseline humano. |
| 3 | `historia_clinica_minima_completa` | Mantener/retomar solo si no esta ya observado | P0 basico y transversal, pero mas ruidoso por tipo documental, notas parciales y campos pendientes. Si ya esta observado, el lugar 3 pasa a mantenimiento de `datos_sensibles_minimizados` en exports. |

Nota operacional: diagnostico separado, consistencia, datos sensibles e historia
minima ya tienen resultados previos de plan/review en este bridge. Si el
orquestador confirma que alguno no esta realmente activo en la app canonica, ese
gate debe volver al ranking antes de consentimiento.

## contrato_gate_recomendado

```yaml
gate_id: trazabilidad_implantes_materiales
mode: detect_only_report_only
source_boundary: internal_surgical_traceability_rule
initial_real_document_severity: needs_review
synthetic_fixture_assertions: allowed
real_document_blocking: false
applies_to:
  document_type:
    - parte_quirurgico
    - protocolo_quirurgico
  procedure_families:
    - fijacion_lumbar
    - artrodesis
    - instrumentacion
    - cifoplastia
    - cementoplastia
    - injerto_oseo
inputs_minimos:
  - document_type
  - procedure_family
  - surgical_body_or_structured_materials
  - levels_or_region_when_applicable
  - materials_or_implants_mentions
does_not_do:
  - infer_missing_implant_from_procedure_without_review
  - invent_brand_lot_batch_model
  - edit_template_or_part
  - validate_vendor_or_regulatory_status
```

## condiciones_status

| Status | Condicion |
| --- | --- |
| `fail` | Fixture sintetico o documento de prueba declara/usa material implantable y falta trazabilidad minima obligatoria en el payload estructurado. |
| `needs_review` | Documento real menciona material/implante pero faltan tipo, cantidad, nivel/lado, o la aplicabilidad no es segura. Tambien si procedimiento sugiere material pero el texto no lo menciona. |
| `pass` | No aplica por familia/procedimiento, o el material esta trazado con tipo/familia, cantidad, nivel/region/lado cuando corresponde, y referencia interna minima. |

Trazabilidad minima v1:

- `material_family`: tornillo, barra, caja/cage, cemento/PMMA, injerto, separador, parche/material dural u otro.
- `quantity` cuando sea contable.
- `level_or_region` si aplica a columna.
- `laterality` cuando aplique.
- `model_or_ref`/`lot_or_batch` solo como `needs_review` si el flujo local aun no lo captura; no hard fail inicial.
- `evidence_path` exacto al campo o segmento.

## campos_evidencia_obligatorios

```json
{
  "gate_id": "trazabilidad_implantes_materiales",
  "mode": "report_only",
  "status": "needs_review",
  "document_type": "parte_quirurgico",
  "procedure_family": "fijacion_lumbar",
  "material_family": "tornillos_pediculares",
  "missing_fields": ["quantity", "level_or_region"],
  "evidence_path": "$.parte_quirurgico.materiales[0]",
  "expected": "material implantable con tipo, cantidad y nivel/region cuando aplica",
  "observed": "material mencionado sin trazabilidad minima",
  "recommendation": "revisar trazabilidad de implantes/materiales antes de cerrar el parte"
}
```

No guardar texto clinico largo. `observed` debe ser marcador estructurado, no
copiar parrafos del parte.

## fixtures_sinteticos_minimos

| Fixture | Tipo | Payload sintetico | Esperado |
| --- | --- | --- | --- |
| `CLIN-P0-054-fixation-implants-missing-trace-review` | Positivo | `procedure_family=fijacion_lumbar; text="se colocan tornillos y barras"; materials=[]` | `needs_review` por material mencionado sin trazabilidad estructurada. |
| `CLIN-P0-055-fixation-implants-structured-pass` | Negativo | `materials=[{family:tornillo_pedicular, qty:4, levels:L4-L5, ref:REF_SYN},{family:barra, qty:2, levels:L4-L5}]` | `pass`. |
| `CLIN-P0-056-kyphoplasty-pmma-missing-volume-review` | Positivo | `procedure_family=cifoplastia; text="cementacion con PMMA"; materials=[{family:PMMA, ref:null, volume:null}]` | `needs_review` por PMMA sin ref/volumen si el flujo lo requiere. |
| `CLIN-P0-057-kyphoplasty-pmma-structured-pass` | Negativo | `materials=[{family:PMMA, ref:REF_SYN, volume:VOL_SYN, level:L1}]` | `pass`. |
| `CLIN-P0-058-discectomy-no-implant-pass` | Negativo | `procedure_family=hernia_lumbar; no material mention; materials=[]` | `pass`, no exigir implante donde no aplica. |
| `CLIN-P0-059-implant-mentioned-in-summary-only-review` | Frontera | Titulo/resumen dice "instrumentacion" pero cuerpo no describe materiales. | `needs_review`, no `fail`. |
| `CLIN-P0-060-dural-patch-mentioned-without-material-review` | Positivo/frontera | `text="se coloca parche dural"; materials=[]` | `needs_review`, coordinado con gate de evento dural. |
| `CLIN-P0-061-negated-implant-pass` | Negativo | `text="no se colocan implantes ni material de osteosintesis"` | `pass`. |
| `CLIN-P0-062-graft-mentioned-missing-source-review` | Positivo | `text="se coloca injerto oseo"; materials=[{family:injerto, source:null}]` | `needs_review`. |
| `CLIN-P0-063-materials-in-checklist-not-body-review` | Frontera | Checklist marca implante, cuerpo tecnico no lo narra. | `needs_review` por discrepancia de trazabilidad. |

## falsos_positivos_previsibles

| Riesgo | Mitigacion |
| --- | --- |
| Procedimiento puede ser no instrumentado aunque pertenezca a familia amplia. | No fallar por familia sola; exigir mencion de material o campo estructurado incompleto para `needs_review`. |
| Material descartable/no implantable se confunde con implante. | V1 solo aplica a materiales implantables o trazables declarados; descartables quedan fuera salvo politica interna. |
| PMMA/cemento con datos en proveedor externo no capturado. | `needs_review` inicial; no hard fail por lote/modelo faltante hasta tener flujo. |
| Injerto autologo no requiere los mismos campos que implante comercial. | `material_family` decide campos requeridos; autologo puede requerir origen/sitio, no lote. |
| Checklist y cuerpo tecnico discrepan. | Reportar discrepancia como `needs_review`; no corregir el parte. |
| Texto negado "no se colocan implantes" dispara por palabra implante. | Fixture de negacion obligatorio. |

## decision

**Integrar ahora** `trazabilidad_implantes_materiales` como report-only.

No pediria dato humano antes de v1: alcanza con fixtures sinteticos y reglas
conservadoras. Si luego se quiere exigir lote/modelo/ref comercial como bloqueo
real, ahi si hace falta definir politica humana y source-pack tecnico.

`consentimiento_especifico_no_generico` queda como siguiente P0 grande, pero no
lo activaria antes de estabilizar source-pack/versionado. `historia_clinica`
queda como candidato de retoma solo si no esta realmente activo en observacion.

## recommendation

Abrir workorder de implementacion para `trazabilidad_implantes_materiales` en
`scripts/qa/validate_clinical_p0_gates_v1.js` o el validator documental clinico
existente, con fixtures `CLIN-P0-054` a `CLIN-P0-063`, sin tocar plantillas y
con salida `needs_review` para documentos reales.

QA minimo esperado:

```bash
node -c scripts/qa/validate_clinical_p0_gates_v1.js
node scripts/qa/validate_clinical_p0_gates_v1.js --gate trazabilidad_implantes_materiales
node scripts/qa/run_clinica_core_qa.js
```

## confidence

Media-alta para la priorizacion y contrato v1 porque deriva del backlog CLINICA,
de los gates quirurgicos ya observados y de una regla documental acotada. Media
para rutas exactas y severidad final porque no se inspecciono la app canonica en
esta Mac. Baja para cualquier hard block legal/regulatorio sin source-pack
tecnico, revision humana y aprobacion explicita.

## attempted_routes

- Se hizo `git pull --rebase`.
- Se ejecuto `./scripts/personal_xh_check.sh` y se detecto el job asignado.
- Se reviso `jobs/20260527T233900-clinica-next-p0-gates-prioritization-after-ayudantes-v1.md`.
- Se reviso `context/fronts/clinica.md`.
- Se revisaron resultados previos de backlog/corpus, consentimiento, datos
  sensibles e historia clinica minima.
- Se intento inspeccionar `/Users/jarvis/.openclaw/workspace/clinica/app-clinica-medicolegal`, pero la ruta no existe en esta Mac.
- No se uso Telegram, Gmail, Drive, Calendar, iCloud, Photos, adjuntos, datos de
  pacientes ni fuentes externas.

## risks_limits

- No se verifico la app canonica real ni sus archivos modificados.
- No se verifico normativa externa ni vigencia legal.
- El ranking asume que los gates documentales previos reportados por el bridge
  estan ya en observacion o listos para observacion; si no lo estan, hay que
  reordenar con datos sensibles/historia minima antes de trazabilidad.
- Este resultado no modifica plantillas, documentos reales ni corpus medico-legal.

## evidence_paths

- `jobs/20260527T233900-clinica-next-p0-gates-prioritization-after-ayudantes-v1.md`
- `claims/20260527T233900-clinica-next-p0-gates-prioritization-after-ayudantes-v1.json`
- `results/20260527T233900-clinica-next-p0-gates-prioritization-after-ayudantes-v1.result.md`
- `context/fronts/clinica.md`
- `results/20260527T010224-clinica-corpus-gates-backlog-v2.result.md`
- `results/20260527T190454-clinica-corpus-gates-backlog-v2.result.md`
- `results/20260527T153504-clinica-consentimiento-especifico-source-pack-plan-v1.result.md`
- `results/20260527T160545-clinica-consentimiento-source-pack-draft-review-v1.result.md`
- `results/20260527T120441-clinica-datos-sensibles-minimizados-p0-plan-v1.result.md`
- `results/20260527T133621-clinica-historia-clinica-minima-p0-plan-v1.result.md`
