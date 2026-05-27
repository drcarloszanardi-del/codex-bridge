---
job_id: 20260527T113720-clinica-diagnostico-separado-implementation-review-v1
worker: personal-xh
status: completed
completed_at: 2026-05-27T11:41:00-03:00
front: CLINICA
no_external_actions: true
no_secrets: true
---

# Resultado - Clinica diagnostico separado implementation review v1

## summary

Veredicto: **aceptar en observacion con un ajuste chico de fixtures**.

Segun el orquestador, `diagnostico_separado_de_indicacion` ya fue integrado en
modo detect-only/report-only dentro de `validate_clinical_p0_gates_v1.js`, con
fixtures `CLIN-DOC-DX-005` a `CLIN-DOC-DX-010`, y paso
`validate_clinical_p0_gates_v1` + `run_clinica_core_qa` con warning esperado
`core_only`. Eso es aceptable para observacion: cubre los positivos principales,
la separacion correcta, la negacion local, antecedentes y el caso ambiguo de
`requiere correlacion`.

No recomiendo revertir. Si hay un ajuste antes de darlo por estable, seria
agregar dos fixtures de bajo costo: acentos (`Diagnóstico` / `indicación`) y
diagnostico estructurado sin heading renderizado. El riesgo principal restante
es falso negativo, no falso positivo.

## coverage_table

| Fuente | Estado | Uso |
| --- | --- | --- |
| `jobs/20260527T113720-clinica-diagnostico-separado-implementation-review-v1.md` | Revisada | Workorder, estado declarado y validaciones locales. |
| `context/fronts/clinica.md` | Revisada | Canon CLINICA y regla de fixtures/gates. |
| `results/20260527T110517-clinica-documental-p0-next-implementation-audit-v1.result.md` | Revisada | Decision previa de integrar este gate. |
| `results/20260527T070409-clinica-diagnostico-separado-implementation-pack-v1.result.md` | Revisada | Pack implementable, regex, severidades y falsos positivos. |
| `results/20260527T063553-clinica-next-documental-p0-gate-plan-v1.result.md` | Revisada | Contrato detect-only y fuente del candidato unico. |
| `results/20260527T010224-clinica-corpus-gates-backlog-v2.result.md` | Revisada | Backlog documental y siguiente P0 posible. |

## risks_p0_p1

| Pri | Riesgo | Tipo | Mitigacion |
| --- | --- | --- | --- |
| P1 | **Acentos y variantes de heading.** Si el matcher solo normaliza `diagnostico` y `indicacion` sin acentos, puede no detectar `Diagnóstico: ... con indicación de ...`. | Falso negativo | Normalizar acentos o agregar regex con `diagn[oó]stico` e `indicaci[oó]n`; fixture imprescindible. |
| P1 | **Validar solo `rendered_text` con heading.** Si la plantilla trae `source_fields.diagnosis` contaminado pero el render no usa heading `Diagnostico:`, el gate podria no disparar. | Falso negativo | Validar tambien `source_fields.diagnosis` como fuente primaria y reportar `evidence_path:"$.source_fields.diagnosis"`. |
| P1 | **`requiere` demasiado amplio.** `requiere correlacion`, `requiere control` o `requiere completar estudios` no son indicacion quirurgica. | Falso positivo | Mantener `CLIN-DOC-DX-010` como `needs_review`; `requiere` solo `fail` si esta cerca de cirugia/procedimiento/descompresion/artrodesis. |
| P1 | **Fuga de report-only a hard block real.** El gate debe fallar QA sintetico, pero no bloquear documentos reales en v1. | Operativo/legal | En salida real usar findings report-only y no modificar plantillas; QA core puede fallar solo por fixtures sinteticos esperados. |
| P2 | **Segmentacion insuficiente por secciones largas.** Texto con `Diagnostico` y `Plan` en el mismo parrafo puede mezclar ventanas. | Falso positivo/negativo | Cortar por headings conocidos y conservar `local_context`; si el corte es dudoso, `needs_review`. |
| P2 | **Sinonimos nuevos de plan terapeutico.** `se propone`, `se sugiere`, `a resolver quirurgicamente` pueden quedar fuera. | Falso negativo | No ampliar de golpe; sumar sinonimos solo con fixtures y revision del orquestador. |

No veo P0 conceptual con la evidencia disponible, porque la integracion declarada
sigue el modo detect-only/report-only y la suite local reportada paso. El limite:
no inspeccione la app canonica ni el diff real desde el bridge.

## additional_fixtures

Estos dos son los unicos que considero imprescindibles para robustecer antes de
cerrar como estable:

| Fixture | Tipo | Input sintetico | Render / campo sintetico | Esperado |
| --- | --- | --- | --- | --- |
| `CLIN-DOC-DX-011-accented-heading-and-marker` | Positivo | `diagnosis=hernia L4-L5; indication=microdiscectomia` | `Diagnóstico: hernia L4-L5 con indicación de microdiscectomía.` | `fail` |
| `CLIN-DOC-DX-012-source-field-contaminated` | Positivo | `source_fields.diagnosis="hernia L4-L5 con indicacion de microdiscectomia"; rendered_text="Resumen clinico sin heading diagnostico"` | Validar campo estructurado aunque render sea ambiguo. | `fail` o `needs_review` como minimo, nunca `pass` silencioso |

Fixtures utiles pero no bloqueantes para aceptar en observacion:

| Fixture | Esperado |
| --- | --- |
| `CLIN-DOC-DX-013-requires-control-review` con `Diagnostico: canal estrecho; requiere control evolutivo.` | `needs_review` o `pass`, no `fail`. |
| `CLIN-DOC-DX-014-plan-same-line-pass` con `Diagnostico: hernia L4-L5. Plan: evaluar cirugia.` | `pass`. |
| `CLIN-DOC-DX-015-suggested-surgery-review` con `Diagnostico: hernia; se sugiere eventual cirugia.` | `needs_review` hasta decidir si `se sugiere` entra como marcador. |

## accept_adjust_revert

Decision: **aceptar en observacion**.

Condiciones de observacion:

```yaml
accept_observation:
  no_template_changes: true
  report_only_for_real_documents: true
  synthetic_failures_allowed_to_fail_qa: true
  core_qa_ok: true
  add_two_fixture_patch:
    - accented_heading_and_marker
    - source_field_contaminated
```

No conviene revertir porque el set actual ya cubre los riesgos que originaron el
gate: mezcla afirmada de diagnostico e indicacion, separacion correcta, negacion,
antecedentes y ambiguedad. Tampoco conviene promover a bloqueo real todavia:
primero observar findings sobre documentos sinteticos/reales anonimizados y
calibrar.

## next_p0_documental

Si este gate queda aceptado en observacion, el siguiente P0 documental recomendado
es **`datos_sensibles_minimizados` para export/handoff**, tambien en
detect-only/report-only inicial.

Motivo:

- Tiene riesgo alto y transversal: nombres, DNI, telefono, domicilio, HC,
  estudios identificables o pantallas en exports/resumenes.
- Puede arrancar con fixtures sinteticos y reglas internas de minimizacion sin
  tocar plantillas clinicas finales.
- Es mas seguro como proximo paso que `consentimiento_especifico_no_generico` o
  `historia_clinica_minima_completa`, que requieren source pack oficial y
  calibracion legal/documental mas fina.

Alcance inicial sugerido:

```yaml
gate_id: datos_sensibles_minimizados
mode: detect_only_report_only
applies_to:
  - export
  - handoff
  - public_summary
  - texto_para_envio
synthetic_block_patterns:
  - DNI
  - telefono
  - domicilio
  - historia_clinica_id
  - nombre_apellido_sintetico
expected_output:
  - finding with matched_text redacted
  - evidence_path
  - recommendation: anonimizar_o_retirar_identificador
```

## recommendation

Proxima accion unica: **mantener
`diagnostico_separado_de_indicacion` aceptado en observacion y agregar los dos
fixtures `CLIN-DOC-DX-011` y `CLIN-DOC-DX-012` antes de considerarlo estable**.
Despues, abrir el siguiente workorder P0 para `datos_sensibles_minimizados` en
export/handoff report-only.

## confidence

Media-alta para aceptar en observacion, porque el estado declarado por el
orquestador coincide con el pack previo y QA local OK. Media para certificar la
implementacion concreta, porque desde el bridge no se inspecciono
`validate_clinical_p0_gates_v1.js` ni el JSON real de fixtures.

## attempted_routes

- Se hizo `git pull --rebase`.
- Se verifico la cola con `./scripts/personal_xh_check.sh`.
- Se reclamo el job con `python3 scripts/bridgectl.py claim`.
- Se reviso el workorder, el contexto canonico CLINICA y resultados previos del
  gate documental.
- No se abrio app real, Drive/iCloud/Photos/Gmail, Telegram, datos de pacientes
  ni ObraCash.

## risks_limits

- El resultado local `validate_clinical_p0_gates_v1 OK` y `run_clinica_core_qa OK`
  fue tomado como declaracion del orquestador; no se ejecuto contra la app real.
- Los fixtures propuestos son sinteticos; no requieren datos reales.
- Cualquier promocion a hard block real requiere otra revision con evidencia de
  documentos anonimizados y aprobacion explicita del orquestador/Doctor.

## evidence_paths

- `jobs/20260527T113720-clinica-diagnostico-separado-implementation-review-v1.md`
- `claims/20260527T113720-clinica-diagnostico-separado-implementation-review-v1.json`
- `context/fronts/clinica.md`
- `results/20260527T110517-clinica-documental-p0-next-implementation-audit-v1.result.md`
- `results/20260527T070409-clinica-diagnostico-separado-implementation-pack-v1.result.md`
- `results/20260527T063553-clinica-next-documental-p0-gate-plan-v1.result.md`
- `results/20260527T010224-clinica-corpus-gates-backlog-v2.result.md`
