## summary_honesto

Pack implementable para el proximo ciclo clinico P0 `evento_complicacion_manejo_estado_final`, en modo `detect-only/report-only`, enfocado en parte quirurgico: evento dural/LCR/parche dural y sangrado relevante.

No encontre un gate equivalente completo en el bridge. Si existen piezas parciales previas: `no_inventar_parche_dural`, `parche_dural_pre_cierre`, consistencia cuando aparece parche sin evento, y una mencion conceptual `complicacion_evento_manejo_estado_final` como `report_only`. La brecha es que no hay pack cerrado para verificar, en un mismo gate, evento afirmado + manejo + estado final, ni reparacion/parche dural sin evento/source claro.

La app canonica declarada `/Users/jarvis/.openclaw/workspace/clinica/app-clinica-medicolegal` no esta disponible en esta Mac, asi que no propongo patch aplicado. El entregable queda como pack seguro para que Codex orquestador lo implemente en la Mac de trabajo.

## coverage_table

| Fuente / ruta | Estado | Uso |
|---|---|---|
| `jobs/20260528T021145-clinica-evento-complicacion-manejo-detect-only-pack-v1.md` | Revisada | Workorder y contrato del ciclo. |
| `results/20260528T015145-clinica-next-p0-gates-prioritization-safe-pack-v1.result.md` | Revisada | Candidato recomendado y fixtures base 069-072. |
| `results/20260527T183421-clinica-correcciones-a-fixtures-implementacion.result.md` | Revisada | Antecedente `LUM-DOC-013`: parche/refuerzo dural solo si indicado y en secuencia. |
| `results/20260527T223530-clinica-protocolo-secuencia-hemostasia-detect-only-plan-v1.result.md` | Revisada | Segmentacion del cuerpo tecnico y exclusions de headings/checklists. |
| `results/20260527T230844-clinica-hemostasia-secuencia-postfixture-review-v2.result.md` | Revisada | Politica report-only y `technical_body` como fuente primaria. |
| `results/20260528T000957-clinica-trazabilidad-frontier-implementation-review-v1.result.md` | Revisada | Modelo de cierre en observacion sin hard block. |
| `results/20260525T153318-clinica-lumbar-inconsistency-gates-v2.result.md` | Revisada | Reglas parciales `no_inventar_parche_dural` y `parche_dural_pre_cierre`. |
| `/Users/jarvis/.openclaw/workspace/clinica/app-clinica-medicolegal` | Ausente en esta Mac | Limite: no se inspecciono codigo real ni fixtures reales. |

## equivalent_gate_check

No duplicar: si en la app canonica ya existe `evento_complicacion_manejo_estado_final` o `complicacion_evento_manejo_estado_final`, el orquestador deberia agregar solo los fixtures y brechas de frontera de este pack.

Brechas encontradas en resultados previos:

- `no_inventar_parche_dural`: cubre parche inventado cuando no fue informado, pero no cubre manejo/estado final de un evento dural afirmado.
- `parche_dural_pre_cierre`: cubre orden relativo parche/cierre, pero no valida si hay evento/source ni resultado final.
- `consistencia_diagnostico_indicacion_procedimiento`: puede marcar parche sin evento como contradiccion, pero no es un gate especifico de complicaciones.
- `complicacion_evento_manejo_estado_final`: aparece como regla conceptual `report_only`, no como pack de fixtures cerrado.

Conclusion: implementar como gate nuevo solo si no existe en app. Si existe, integrar este pack como regression/frontier fixtures.

## fixture_pack_sintetico

Formato sugerido para `data/derived/clinical_test_cases/clinical_p0_gates_v1.json` o fixture documental equivalente:

```json
[
  {
    "id": "CLIN-P0-069-dural-event-without-management-review",
    "gate_id": "evento_complicacion_manejo_estado_final",
    "mode": "report_only",
    "document_type": "parte_quirurgico",
    "procedure_family": "columna_lumbar",
    "technical_body": "Durante la exposicion se constata salida de LCR. Se continua el procedimiento y se realiza cierre por planos.",
    "excluded_sections": {},
    "expected_status": "needs_review",
    "expected_missing": ["management", "final_status"],
    "expected_reason": "evento dural afirmado sin manejo especifico ni estado final"
  },
  {
    "id": "CLIN-P0-070-no-dural-event-pass",
    "gate_id": "evento_complicacion_manejo_estado_final",
    "mode": "report_only",
    "document_type": "parte_quirurgico",
    "procedure_family": "columna_lumbar",
    "technical_body": "No se constata durotomia ni salida de LCR. Hemostasia, recuento y cierre.",
    "expected_status": "pass",
    "expected_reason": "negacion local de evento dural"
  },
  {
    "id": "CLIN-P0-071-patch-without-event-review",
    "gate_id": "evento_complicacion_manejo_estado_final",
    "mode": "report_only",
    "document_type": "parte_quirurgico",
    "procedure_family": "columna_lumbar",
    "technical_body": "Se coloca parche dural y se realiza cierre, sin otra descripcion.",
    "expected_status": "needs_review",
    "expected_missing": ["source_event", "final_status"],
    "expected_reason": "reparacion/parche dural sin evento o source claro"
  },
  {
    "id": "CLIN-P0-072-dural-event-managed-pass",
    "gate_id": "evento_complicacion_manejo_estado_final",
    "mode": "report_only",
    "document_type": "parte_quirurgico",
    "procedure_family": "columna_lumbar",
    "technical_body": "Se constata pequena apertura dural, se repara con sutura y parche, sin fuga al control final. Hemostasia, recuento y cierre.",
    "expected_status": "pass",
    "expected_reason": "evento, manejo y estado final presentes"
  }
]
```

Fixtures frontera recomendados para una segunda mini-pasada si el orquestador quiere mas estabilidad:

| Fixture | Input sintetico | Esperado | Motivo |
|---|---|---|---|
| `CLIN-P0-075-consent-risk-lcr-ignored-pass` | `document_type=consentimiento; text="riesgo de LCR o durotomia"` | `pass` | Riesgo hipotetico no es evento ocurrido. |
| `CLIN-P0-076-checklist-dural-risk-ignored-pass` | `checklist="riesgo: LCR"; technical_body="sin incidentes"` | `pass` | Checklist/riesgo no alimenta evento. |
| `CLIN-P0-077-relevant-bleeding-without-management-review` | `technical_body="Se constata sangrado relevante. Cierre por planos."` | `needs_review` | Sangrado relevante afirmado sin manejo/estado final. |
| `CLIN-P0-078-bleeding-managed-pass` | `technical_body="Se constata sangrado epidural, se controla con hemostaticos, sin sangrado activo al cierre."` | `pass` | Evento + manejo + estado final. |

## lexicon_inicial

Eventos/complicaciones durales afirmativas:

- `durotomia`
- `apertura dural`
- `lesion dural`
- `desgarro dural`
- `salida de LCR`
- `fuga de LCR`
- `perdida de LCR`
- `liquido cefalorraquideo`
- `brecha dural`

Manejo/reparacion dural:

- `sutura dural`
- `reparacion dural`
- `cierre dural`
- `parche dural`
- `refuerzo dural`
- `sellante dural`
- `sustituto dural`
- `plastía dural` / `plastia dural`

Estado final/control:

- `sin fuga`
- `sin salida de LCR`
- `prueba de Valsalva negativa`
- `control final sin fuga`
- `sin perdida persistente`
- `sin deficit neurologico agregado`
- `sin sangrado activo`

Sangrado relevante:

- `sangrado relevante`
- `sangrado abundante`
- `sangrado epidural`
- `lesion vascular`
- `hemorragia`
- `sangrado persistente`
- `requiere hemostatico`
- `requiere transfusion`

## negaciones_locales_y_exclusiones

Negaciones locales que deben producir `pass` o excluir el evento si estan en la misma oracion/ventana cercana:

- `sin durotomia`
- `no se constata durotomia`
- `sin salida de LCR`
- `no se observa salida de LCR`
- `sin perdida de LCR`
- `no fue necesario parche dural`
- `no se coloca parche dural`
- `sin complicaciones`
- `sin sangrado activo`
- `sin sangrado relevante`

Secciones excluidas para evitar falsos positivos:

- consentimiento informado;
- riesgos hipoteticos/preoperatorios;
- diagnostico;
- indicacion;
- titulo/procedimiento codificado;
- checklist administrativo;
- resumen final no tecnico;
- notas QA/orquestacion;
- instrucciones del prompt;
- antecedentes/historia previa si no son evento intraoperatorio.

Fuente admitida inicial: `technical_body` / `cuerpo_tecnico` y, si ya existe en la app, campos estructurados de eventos intraoperatorios aprobados. No leer expediente bruto ni texto no seleccionado para el parte.

## expected_result_contract

Salida JSON sugerida:

```json
{
  "gate_id": "evento_complicacion_manejo_estado_final",
  "mode": "report_only",
  "status": "needs_review",
  "document_type": "parte_quirurgico",
  "event_family": "dural_event",
  "event_detected": true,
  "management_detected": false,
  "final_status_detected": false,
  "missing_fields": ["management", "final_status"],
  "evidence_path": "$.technical_body",
  "source_boundary": "technical_body",
  "recommendation": "revisar manejo y estado final del evento/complicacion antes de cerrar el parte"
}
```

Reglas:

- `needs_review`: evento afirmado sin manejo o sin estado final; reparacion/parche sin evento/source claro; sangrado relevante sin manejo/estado final.
- `pass`: evento negado; no hay evento; evento con manejo y control final; riesgos hipoteticos solo en consentimiento/checklist.
- No usar `hard_fail` en documentos reales.
- No reescribir ni completar el parte automaticamente.
- No sugerir que ocurrio una complicacion: si falta evidencia, escribir `needs_review`.

## files_to_inspect_or_patch

Rutas probables en la app canonica de trabajo:

```text
data/derived/clinical_test_cases/clinical_p0_gates_v1.json
data/derived/clinical_test_cases/documental_p0_gates_v1.json
scripts/qa/validate_clinical_p0_gates_v1.js
scripts/qa/validate_documental_p0_gates_v1.js
scripts/qa/run_clinica_core_qa.js
```

Busquedas sugeridas antes de implementar:

```bash
rg -n "evento_complicacion|complicacion_evento|durotomia|LCR|parche dural|technical_body|cuerpo_tecnico" .
rg -n "trazabilidad_implantes_materiales|hemostasia_secuencia|consistencia_diagnostico" scripts data
```

Si ya existe helper de segmentacion/exclusion para `hemostasia_secuencia`, reutilizarlo para `technical_body` y secciones excluidas. Ese es el path mas seguro.

## patch_propuesto

No aplique patch porque la app canonica no esta presente en esta Mac. Patch minimo conceptual:

1. Agregar fixtures `CLIN-P0-069` a `CLIN-P0-072` al JSON de fixtures clinicos/documentales.
2. Agregar gate `evento_complicacion_manejo_estado_final` al validator existente, reutilizando helpers de:
   - normalizacion;
   - segmentacion `technical_body`;
   - negacion local;
   - exclusion de checklist/resumen/consentimiento.
3. Conectar el gate al runner core solo como `report_only`.
4. Agregar assertion de que todos los findings tengan `mode=report_only`.

Es seguro porque no toca plantillas, no lee documentos reales, no modifica output clinico y solo agrega deteccion/fixtures sinteticos.

## test_commands

Focal:

```bash
node -c scripts/qa/validate_clinical_p0_gates_v1.js
node scripts/qa/validate_clinical_p0_gates_v1.js --gate evento_complicacion_manejo_estado_final
```

Si el validator documental separado existe:

```bash
node -c scripts/qa/validate_documental_p0_gates_v1.js
node scripts/qa/validate_documental_p0_gates_v1.js --gate evento_complicacion_manejo_estado_final
```

Regresion:

```bash
node scripts/qa/run_clinica_core_qa.js
```

Acceptance:

- `CLIN-P0-069` => `needs_review`
- `CLIN-P0-070` => `pass`
- `CLIN-P0-071` => `needs_review`
- `CLIN-P0-072` => `pass`
- todos los findings del gate tienen `mode=report_only`
- ningun test toca plantillas ni documentos reales

## false_positive_risks

| Riesgo | Mitigacion |
|---|---|
| Consentimiento enumera riesgo de LCR y el gate lo interpreta como evento ocurrido. | Excluir `document_type=consentimiento` y seccion de riesgos hipoteticos. |
| Checklist o titulo menciona "parche dural" como opcion, no como acto realizado. | Analizar solo `technical_body` / cuerpo tecnico admitido. |
| Negacion local incompleta dispara con `sin durotomia`. | Fixture `CLIN-P0-070` obligatorio y ventana de negacion por oracion. |
| Parche dural usado como refuerzo planificado sobre zona expuesta sin complicacion. | `needs_review`, no `fail`, hasta tener source/evento estructurado. |
| Sangrado menor normal del abordaje se trata como complicacion. | Lexicon de sangrado debe exigir relevancia: abundante, persistente, vascular, requiere manejo especifico. |
| Durotomia manejada correctamente pero sin frase exacta de estado final. | `needs_review`; no inferir estado final. Agregar sinonimos despues de observacion. |

## recommendation

Implementar el pack como proximo ciclo detect-only/report-only, preferentemente reutilizando el helper de `hemostasia_secuencia` para leer solo `technical_body` y excluir secciones no tecnicas. Si aparece un gate equivalente en la app canonica, no crear otro: agregar estos fixtures y assertions como frontera/regresion.

No promover a hard block. No corregir el parte. No inventar evento, manejo ni estado final. La siguiente revision deberia auditar el diff real y confirmar que `069/071` generan `needs_review`, `070/072` pasan, y el core QA conserva los gates previos.

## confidence

Media-alta para el pack de fixtures y criterio porque deriva del P0 priorizado y de gates previos de hemostasia/trazabilidad. Media para nombres exactos de archivos y helpers porque la app canonica no esta disponible en esta Mac. Baja para cualquier bloqueo real o severidad productiva sin observacion, aprobacion humana y revision medico-legal.

## attempted_routes

- Se sincronizo el bridge con `git pull --rebase origin main`.
- Se ejecuto `./scripts/personal_xh_check.sh` y se detecto este job.
- Se reviso el job actual y los resultados previos indicados por el orquestador.
- Se busco equivalencia con `rg` en `jobs/`, `results/` y `context/`.
- Se verifico la ruta canonica declarada de app con `test -d`; no esta disponible en esta Mac.
- No se leyeron historias clinicas reales, adjuntos, Drive, iCloud, Photos, Gmail, Telegram ni datos personales.
- No se tocaron plantillas finales, validadores operativos ni app real.

## risks_limits

- Este resultado no implementa codigo; entrega pack y contrato para Codex orquestador.
- La auditoria de equivalencia en app real queda pendiente hasta trabajar en la Mac con la app canonica.
- Las reglas deben observarse en `report_only` antes de cualquier promocion.
- No se verifico normativa externa ni se pretende cerrar criterio medico-legal productivo.
- Si falta evidencia en un documento real, el resultado correcto es `needs_review`, no afirmacion clinica.

## evidence_paths

- `jobs/20260528T021145-clinica-evento-complicacion-manejo-detect-only-pack-v1.md`
- `claims/20260528T021145-clinica-evento-complicacion-manejo-detect-only-pack-v1.json`
- `results/20260528T021145-clinica-evento-complicacion-manejo-detect-only-pack-v1.result.md`
- `results/20260528T015145-clinica-next-p0-gates-prioritization-safe-pack-v1.result.md`
- `results/20260527T183421-clinica-correcciones-a-fixtures-implementacion.result.md`
- `results/20260527T223530-clinica-protocolo-secuencia-hemostasia-detect-only-plan-v1.result.md`
- `results/20260527T230844-clinica-hemostasia-secuencia-postfixture-review-v2.result.md`
- `results/20260528T000957-clinica-trazabilidad-frontier-implementation-review-v1.result.md`
- `results/20260525T153318-clinica-lumbar-inconsistency-gates-v2.result.md`
- `/Users/jarvis/.openclaw/workspace/clinica/app-clinica-medicolegal`

## draft_para_topic_clinica

Pack listo para `evento_complicacion_manejo_estado_final`: fixtures 069-072, lexicon dural/LCR/parche/sangrado, negaciones locales y exclusiones para consentimiento/riesgos/checklists. No hay gate equivalente completo en bridge; hay piezas parciales de parche dural y secuencia, asi que en app real conviene primero buscar equivalencia y, si existe, sumar estos fixtures como frontera. Todo queda report-only: 069/071 `needs_review`, 070/072 `pass`.
