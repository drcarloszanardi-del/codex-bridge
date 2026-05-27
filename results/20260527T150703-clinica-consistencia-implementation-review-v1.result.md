---
job_id: 20260527T150703-clinica-consistencia-implementation-review-v1
worker: personal-xh
status: completed
completed_at: 2026-05-27T15:14:00-03:00
front: CLINICA
no_external_actions: true
no_secrets: true
---

# Resultado - Clinica consistencia implementation review v1

## summary

Veredicto: **aceptar en observacion**.

Segun el orquestador, `consistencia_diagnostico_indicacion_procedimiento` fue
integrado localmente en modo detect-only/report-only dentro de
`validate_clinical_p0_gates_v1.js`, con fixtures `CLIN-DOC-CONSIST-005` a
`CLIN-DOC-CONSIST-014`, y paso `validate_clinical_p0_gates_v1` +
`run_clinica_core_qa` con warning esperado `core_only`. Ese resultado es
coherente con el contrato previo: compara solo datos explicitamente
estructurados, emite `needs_review`, no infiere nivel/lateralidad faltante, no
duplica historia minima y no toca plantillas finales.

No recomiendo revertir. El gate cubre una frontera P0 real: evitar que
diagnostico, indicacion, procedimiento, nivel, lado y estado del plan se
contradigan dentro de documentacion clinica interna. Debe seguir en observacion
porque todavia es una regla documental conservadora, no un criterio medico ni
legal para bloqueo.

## coverage_table

| Fuente | Estado | Uso |
| --- | --- | --- |
| `jobs/20260527T150703-clinica-consistencia-implementation-review-v1.md` | Revisada | Workorder, implementacion declarada, QA local y entregables. |
| `context/fronts/clinica.md` | Revisada | Canon CLINICA y lista de gates documentales. |
| `results/20260527T143446-clinica-consistencia-diagnostico-indicacion-procedimiento-plan-v1.result.md` | Revisada | Contrato previo, fixtures y guardrails. |
| `results/20260527T140548-clinica-historia-minima-implementation-review-v1.result.md` | Revisada | Frontera para no duplicar faltantes de historia minima. |
| `results/20260527T113720-clinica-diagnostico-separado-implementation-review-v1.result.md` | Revisada | Patron de aceptacion en observacion para gates detect-only. |
| `results/20260527T123551-clinica-datos-sensibles-implementation-review-v1.result.md` | Revisada | Secuencia P0 previa y criterio de report-only. |

## risks_p0_p1

| Pri | Riesgo | Tipo | Mitigacion |
| --- | --- | --- | --- |
| P0 | **Promocion accidental a hard block.** Una contradiccion aparente puede ser clinicamente justificable o depender de contexto operatorio. | Operativo/medico-legal | Mantener real documents en `needs_review`; `fail` solo para fixtures sinteticos si se usa como assertion interna. |
| P0 | **Correccion automatica de procedimiento, nivel o lateralidad.** El validator podria tentar a "arreglar" el documento. | Medico-legal | Findings solamente; recomendacion siempre "revisar coherencia", nunca proponer el procedimiento correcto. |
| P1 | **Familia quirurgica combinada.** Descompresion + artrodesis o discectomia + descompresion puede ser correcto aunque agregue familia extra. | Falso positivo | `needs_review`, no `fail`; fixture de combinacion justificada como pass/advisory. |
| P1 | **Indicacion amplia vs procedimiento especifico.** Una indicacion general puede admitir mas de una tecnica. | Falso positivo | Familias amplias y conservadoras; si no hay contradiccion obvia, `advisory` o pass. |
| P1 | **Antecedentes historicos comparados contra plan actual.** Cirugia previa o nivel viejo pueden parecer mismatch. | Falso positivo | Excluir segmentos `antecedentes`; conservar fixture historico como pass. |
| P1 | **Normalizacion de nivel/lateralidad.** `L4/5`, `L4-L5`, `L4 L5` o abreviaturas de lado pueden no normalizar igual. | Falso positivo/negativo | Fixture de equivalencias; comparar valores canonicos, no texto bruto. |
| P1 | **Plan pendiente con alternativa explicita.** "Posible microdiscectomia" o "a definir" no debe ser tratado como decision cerrada. | Falso positivo | Diferenciar procedimiento decidido de alternativa posible; `advisory` o pass si esta marcado como pendiente. |
| P1 | **Consentimiento con wording no tecnico.** Puede nombrar procedimiento en lenguaje amplio sin ser inconsistente. | Ruido documental | Mantener alcance conservador y report-only; no usar este gate para exigir wording legal. |

No veo P0 que obligue a ajustar o revertir con la evidencia disponible. El limite:
no inspeccione la app canonica ni el diff real desde el bridge; tomo como dato la
implementacion y QA local declarados por el orquestador.

## false_positives_expected

Esperaria falsos positivos en cuatro zonas:

| Zona | Ejemplo sintetico | Tratamiento recomendado |
| --- | --- | --- |
| Procedimientos combinados justificados | Indicacion de descompresion con artrodesis agregada por inestabilidad documentada. | `pass` o `advisory` si la justificacion esta en campos estructurados. |
| Plan en evolucion | Procedimiento mencionado como posibilidad mientras `plan_pending=true`. | No `needs_review` fuerte si hay marcador de posibilidad/pendiente. |
| Topografia historica | Antecedente L5-S1 y cuadro actual L4-L5. | Excluir antecedentes; no comparar contra plan actual. |
| Sinonimos/abreviaturas | `L4/5` vs `L4-L5`, derecho vs `D`, bilateral parcial. | Normalizar antes de comparar; si no se puede, `advisory`. |

## missing_fixtures

Los fixtures `005` a `014` alcanzan para aceptar en observacion. Antes de
cerrarlo como estable agregaria:

| Fixture | Tipo | Payload sintetico | Esperado |
| --- | --- | --- | --- |
| `CLIN-DOC-CONSIST-015-level-normalization-pass` | Negativo | `diagnosis.level=L4/5; procedure.level=L4-L5` | `pass`; evita mismatch por formato. |
| `CLIN-DOC-CONSIST-016-pending-alternative-pass` | Frontera | `plan_pending=true; procedure="posible microdiscectomia a definir"` | `pass` o `advisory`, no `needs_review` por procedimiento cerrado. |
| `CLIN-DOC-CONSIST-017-combined-procedure-justified-pass` | Negativo/frontera | `indication_family=decompression; procedure_families=[decompression,fusion]; justification=instability_present` | `pass` o `advisory`, no mismatch fuerte. |
| `CLIN-DOC-CONSIST-018-out-of-scope-public-summary-pass` | Negativo | `document_type=public_summary` con wording simplificado | `pass`; el gate no aplica a resumen publico/export minimizado. |
| `CLIN-DOC-CONSIST-019-cross-document-handoff-vs-part-review` | Positivo | Handoff prequirurgico L4-L5 derecha y draft parte L5-S1 izquierda del mismo caso sintetico. | `needs_review` con evidence paths a ambos documentos. |
| `CLIN-DOC-CONSIST-020-historia-minima-multiple-missing-suppressed` | Negativo/frontera | Diagnostico y plan ausentes; historia minima ya marca faltantes. | Un `advisory` de no evaluable o pass, no cadena de inconsistencias. |

## accept_adjust_revert

Decision: **aceptar en observacion**.

Condiciones:

```yaml
accept_observation:
  no_template_changes: true
  report_only_for_real_documents: true
  real_document_severity: needs_review
  no_autocomplete_or_correction: true
  no_infer_missing_level_or_laterality: true
  suppress_when_history_minima_missing_core_fields: true
  add_stability_fixtures:
    - CLIN-DOC-CONSIST-015-level-normalization-pass
    - CLIN-DOC-CONSIST-016-pending-alternative-pass
    - CLIN-DOC-CONSIST-017-combined-procedure-justified-pass
    - CLIN-DOC-CONSIST-018-out-of-scope-public-summary-pass
    - CLIN-DOC-CONSIST-019-cross-document-handoff-vs-part-review
    - CLIN-DOC-CONSIST-020-historia-minima-multiple-missing-suppressed
```

No conviene ajustar antes de observar salvo que los fixtures actuales impriman
texto clinico crudo en findings. Si eso ocurriera, el ajuste seria de salida:
`matched_text` estructurado y `local_context` minimo, no texto libre largo.

## next_p0_documental

El siguiente P0 documental recomendado es
**`consentimiento_especifico_no_generico`**, pero en dos pasos:

1. Workorder de plan/source-pack y fixtures sinteticos, sin tocar plantillas.
2. Solo despues, implementacion detect-only/report-only sobre consentimiento ya
   renderizado o campos estructurados, nunca hard block inicial.

Motivo:

- En el backlog CLINICA ya quedaron cubiertos diagnostico separado, datos
  sensibles, historia minima y consistencia diagnostico-indicacion-procedimiento.
- Consentimiento generico es el siguiente riesgo documental transversal.
- Requiere mas cuidado que los gates anteriores porque el wording obligatorio y
  los riesgos/alternativas no deben inventarse desde el validator.

Alcance inicial sugerido:

```yaml
gate_id: consentimiento_especifico_no_generico
mode: detect_only_report_only
initial_severity: needs_review
phase_1:
  - source_pack_versioned_or_internal_baseline
  - synthetic_fixtures_generic_vs_specific
  - no_template_mutation
checks_v1:
  - procedure_named_or_specific_family_present
  - level_or_region_present_when_applicable
  - laterality_present_when_applicable
  - generic_consent_language_detected
does_not_do:
  - invent_risk_list
  - rewrite_consent
  - validate legal sufficiency as hard gate
```

`trazabilidad_implantes_materiales` queda como siguiente candidato cuando el
flujo toque instrumentacion/materiales; para documentacion general, consentimiento
es mas transversal.

## recommendation

Mantener `consistencia_diagnostico_indicacion_procedimiento` aceptado en
observacion, sumar fixtures `CONSIST-015` a `CONSIST-020` antes de declararlo
estable, y abrir el proximo P0 para consentimiento especifico no generico en
fase de plan/source-pack. No tocar plantillas finales ni promover ningun gate a
hard block sin aprobacion explicita.

## confidence

Media-alta para aceptar en observacion, porque la implementacion declarada calza
con el contrato previo y QA local OK. Media para certificar el diff concreto,
porque desde el bridge no inspeccione la app canonica ni el JSON real de
fixtures. Media-baja para cualquier bloqueo medico-legal o criterio de
consentimiento sin source pack oficial/versionado y revision humana.

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
- Este resultado usa solo fixtures sinteticos y razonamiento documental.
- El gate no sustituye criterio medico ni legal; solo reporta contradicciones
  documentales obvias para revision.
- Cualquier fuente normativa o consentimiento hard gate requiere source pack,
  versionado, revision humana y aprobacion explicita.

## evidence_paths

- `jobs/20260527T150703-clinica-consistencia-implementation-review-v1.md`
- `claims/20260527T150703-clinica-consistencia-implementation-review-v1.json`
- `context/fronts/clinica.md`
- `results/20260527T143446-clinica-consistencia-diagnostico-indicacion-procedimiento-plan-v1.result.md`
- `results/20260527T140548-clinica-historia-minima-implementation-review-v1.result.md`
- `results/20260527T113720-clinica-diagnostico-separado-implementation-review-v1.result.md`
- `results/20260527T123551-clinica-datos-sensibles-implementation-review-v1.result.md`
