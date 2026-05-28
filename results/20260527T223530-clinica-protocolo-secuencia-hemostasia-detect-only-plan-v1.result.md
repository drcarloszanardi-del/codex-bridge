---
job_id: 20260527T223530-clinica-protocolo-secuencia-hemostasia-detect-only-plan-v1
worker: personal-xh
status: completed
completed_at: 2026-05-27T22:40:58-03:00
front: CLINICA
no_external_actions: true
no_secrets: true
---

# Resultado - Protocolo secuencia hemostasia detect-only plan v1

## summary

Plan detect-only/report-only para evitar un error medico-legal en partes
quirurgicos: mencionar `hemostasia` antes de narrar el acto tecnico principal
del procedimiento. No toque plantillas finales, documentos clinicos, pacientes,
credenciales ni fuentes externas.

La regla existente `orden_hemostasia_recuento_cierre` cubre que hemostasia y
recuento aparezcan antes del cierre. Este job pide otro guardrail: el acto
tecnico principal debe estar narrado antes de la primera hemostasia con sentido
de cierre/finalizacion. Propongo separarlo como
`secuencia_acto_principal_antes_hemostasia`, inicialmente solo `detect_only`.

## coverage_table

| Fuente local | Estado | Uso |
| --- | --- | --- |
| `jobs/20260527T223530-clinica-protocolo-secuencia-hemostasia-detect-only-plan-v1.md` | Revisada | Objetivo, restricciones y entregables. |
| `context/fronts/clinica.md` | Revisada | Ruta canonica, limites de no tocar plantillas y politica de gates/fixtures. |
| `results/20260525T084316-clinica-integration-checklist-route-guard-fixtures-v2.result.md` | Revisada | Gate previo de hemostasia/recuento antes de cierre. |
| `results/20260525T120000-clinica-fixtures-lumbares-v1.result.md` | Revisada | Fixtures lumbares y orden narrativo ya usado por bridge. |
| `results/20260525T153318-clinica-lumbar-inconsistency-gates-v2.result.md` | Revisada | Inconsistencias detect-only y estructura de severidades. |
| `results/20260525T181000-clinica-lumbar-validator-detect-only-spec-v1.result.md` | Revisada | Estilo de validador report-only para columna. |
| `results/20260525T221902-clinica-lumbar-regression-pack-from-prior-results-v1.result.md` | Revisada | Regression pack y gates asociados a cierre/hemostasia. |
| `results/20260525T224750-clinica-v2-gates-next-hardening-audit-v1.result.md` | Revisada | Hardening previo y riesgo de falsos positivos. |

## criterio_detect_only

Aplicar solo al cuerpo narrativo tecnico del `parte_quirurgico`. Excluir titulo,
diagnostico, indicacion, nombre del procedimiento, checklist, resumen final y
bloques administrativos. La segmentacion minima recomendada:

1. Preparacion, posicion, asepsia y campos.
2. Acceso o abordaje.
3. Acto tecnico principal del procedimiento.
4. Control/confirmacion tecnica o materiales, si corresponde.
5. Hemostasia.
6. Recuento.
7. Cierre.

La deteccion debe calcular posiciones de primera mencion afirmada para:
`acto_tecnico_principal`, `hemostasia`, `recuento` y `cierre`. El nuevo gate
solo observa `acto_tecnico_principal < hemostasia` cuando la hemostasia tiene
sentido de finalizacion o control posterior al acto.

## severidad

| Expected | Criterio |
| --- | --- |
| `pass` | El acto tecnico principal esta afirmado en el cuerpo narrativo antes de hemostasia; luego aparecen recuento/cierre en orden razonable. |
| `fail` | La primera hemostasia afirmada aparece antes de cualquier acto tecnico principal afirmado en el cuerpo tecnico, y luego se narra el acto principal. |
| `needs_review` | El acto principal solo aparece en titulo/diagnostico/procedimiento, el texto es demasiado escueto, hay multiples etapas, o la hemostasia puede referir a control local de acceso y no a cierre. |

## fixtures_sinteticos

| Procedimiento | Fixture sintetico | Expected |
| --- | --- | --- |
| Cifoplastia | "Paciente en decubito prono. Asepsia y campos. Acceso transpedicular L1 bajo radioscopia. Se introduce canula, se insufla balon y se realiza cementacion con PMMA con control radioscopico. Hemostasia. Recuento. Cierre." | `pass` |
| Cifoplastia | "Paciente en decubito prono. Asepsia y campos. Se realiza hemostasia. Luego se introduce canula transpedicular, se insufla balon y se cementa con PMMA." | `fail` |
| Cifoplastia | "Diagnostico: fractura L1. Procedimiento: cifoplastia. Hemostasia y cierre sin incidentes." | `needs_review` |
| Cifoplastia | "Hemostasia del trayecto. Luego se progresa canula y se insufla balon vertebral." | `fail` si es el primer acto narrado; `needs_review` si el texto demuestra sangrado de piel/acceso previo. |
| Hernia lumbar | "Abordaje lumbar posterior. Se expone espacio L4-L5, se realiza hemilaminotomia y flavectomia. Se identifica raiz, se reseca fragmento herniario y se libera receso. Hemostasia. Recuento. Cierre por planos." | `pass` |
| Hernia lumbar | "Abordaje lumbar posterior. Hemostasia cuidadosa. Luego se identifica raiz y se reseca fragmento herniario L4-L5." | `fail` |
| Hernia lumbar | "Se realiza procedimiento habitual de hernia lumbar. Hemostasia y cierre." | `needs_review` |
| Fijacion lumbar | "Abordaje posterior. Exposicion de elementos posteriores L4-S1. Colocacion de tornillos pediculares, barras y artrodesis posterolateral con injerto. Control radioscopico. Hemostasia. Recuento. Cierre." | `pass` |
| Fijacion lumbar | "Abordaje posterior. Hemostasia. Luego se colocan tornillos pediculares, barras e injerto posterolateral." | `fail` |
| Fijacion lumbar | "Se completa fijacion lumbar. Hemostasia, recuento y cierre." | `needs_review` por falta de narrativa tecnica verificable. |

## frases_fail

- `se realiza hemostasia. posteriormente se introduce/coloca/realiza/inicia`
- `hemostasia previa a la colocacion del balon`
- `hemostasia previa a la cementacion`
- `hemostasia previa a la reseccion del fragmento herniario`
- `hemostasia previa a la colocacion de tornillos/barras`
- `hemostasia y luego se cementa/descomprime/fija/reseca`
- `se efectua hemostasia. luego se identifica la raiz`
- `se efectua hemostasia. luego se colocan implantes`

Estas frases son `fail` solo si pertenecen al cuerpo tecnico y no a una
transcripcion negativa, hipotetica o administrativa.

## frases_needs_review

- `cifoplastia sin incidentes, hemostasia y cierre`
- `se realiza procedimiento habitual, hemostasia y cierre`
- `hemostasia durante el abordaje` sin detalle posterior suficiente
- `hemostasia del trayecto` antes de una etapa profunda, cuando puede ser
  sangrado local de acceso
- `tras completar el procedimiento, hemostasia` pero el procedimiento no fue
  narrado en el cuerpo tecnico
- `hemostasia` dentro de checklist, resumen, evolucion posoperatoria o plan
- multiples niveles o multiples procedimientos con hemostasia entre etapas

## recomendacion

Integrar en Codex principal como gate independiente y `report_only`:

1. Agregar un helper local de segmentacion del cuerpo tecnico del parte.
2. Definir lexicos por procedimiento para `acto_tecnico_principal`:
   - cifoplastia: `canula`, `trocar`, `balon`, `cementacion`, `PMMA`,
     `control radioscopico`.
   - hernia lumbar: `identifica raiz`, `flavectomia`, `discectomia`,
     `reseccion de fragmento`, `liberacion`, `foraminotomia`.
   - fijacion lumbar: `tornillos pediculares`, `barras`, `artrodesis`,
     `injerto`, `control radioscopico`.
3. Calcular primeras posiciones afirmadas en el cuerpo tecnico.
4. Reportar `fail` solo cuando `hemostasia` precede claramente al acto
   principal y el acto aparece despues.
5. Reportar `needs_review` para casos escuetos, multi-etapa o ambiguos.
6. Mantener separado de `orden_hemostasia_recuento_cierre`; ambos gates pueden
   correr juntos, pero no deben confundirse.
7. No modificar plantillas finales ni documentos reales sin baseline, ruta
   canonica y test focal aprobado.

Promocion sugerida: 7 a 14 dias como `detect_only`, revision manual de falsos
positivos, y recien despues evaluar hard-fail para frases de alta confianza.

## confidence

Media-alta para el criterio y los fixtures sinteticos porque deriva de gates
previos de columna y del incidente motivador. Media para integracion real: no se
audito ni modifico la app canonica y no se corrio validador contra historias o
partes reales.

## attempted_routes

- Se hizo `git pull --rebase` antes de procesar el job.
- Se ejecuto `./scripts/personal_xh_check.sh` y se detecto este job asignado a
  `personal-xh`.
- Se reviso `jobs/20260527T223530-clinica-protocolo-secuencia-hemostasia-detect-only-plan-v1.md`.
- Se busco contexto local con `rg` sobre `context/`, `jobs/` y `results/`.
- Se reviso `context/fronts/clinica.md`.
- No se uso Telegram, Gmail, Drive, Calendar, pacientes, credenciales, fuentes
  externas ni documentos clinicos reales.

## risks_limits

- Falso positivo por hemostasia de piel/subcutaneo durante el acceso antes del
  acto profundo. Debe ser `needs_review` salvo que el texto sea inequivoco.
- Procedimientos por etapas o multiples niveles pueden tener hemostasia legitima
  entre etapas. El scope debe ser por etapa si el texto lo permite.
- Checklists, resumenes y titulos no deben decidir el orden narrativo.
- Frases negativas o condicionales como "no se realiza hemostasia hasta
  finalizar" deben excluirse o ir a revision.
- OCR/dictado puede invertir conectores temporales; report-only reduce riesgo.
- Este resultado no certifica actualidad legal ni modifica corpus medico-legal;
  solo aporta regla operacional sintetica para QA documental.

## evidence_paths

- `jobs/20260527T223530-clinica-protocolo-secuencia-hemostasia-detect-only-plan-v1.md`
- `claims/20260527T223530-clinica-protocolo-secuencia-hemostasia-detect-only-plan-v1.json`
- `results/20260527T223530-clinica-protocolo-secuencia-hemostasia-detect-only-plan-v1.result.md`
- `context/fronts/clinica.md`
- `results/20260525T084316-clinica-integration-checklist-route-guard-fixtures-v2.result.md`
- `results/20260525T120000-clinica-fixtures-lumbares-v1.result.md`
- `results/20260525T153318-clinica-lumbar-inconsistency-gates-v2.result.md`
- `results/20260525T181000-clinica-lumbar-validator-detect-only-spec-v1.result.md`
- `results/20260525T221902-clinica-lumbar-regression-pack-from-prior-results-v1.result.md`
- `results/20260525T224750-clinica-v2-gates-next-hardening-audit-v1.result.md`
