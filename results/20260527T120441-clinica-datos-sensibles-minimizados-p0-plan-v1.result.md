---
job_id: 20260527T120441-clinica-datos-sensibles-minimizados-p0-plan-v1
worker: personal-xh
status: completed
completed_at: 2026-05-27T12:10:00-03:00
front: CLINICA
no_external_actions: true
no_secrets: true
---

# Resultado - Clinica datos sensibles minimizados P0 plan v1

## summary

Recomendacion: **integrar ahora como gate detect-only/report-only estrecho**:
`datos_sensibles_minimizados` para `export`, `handoff`, `public_summary` y
`texto_para_envio`.

El objetivo de v1 no es hacer cumplimiento legal completo ni inspeccionar
historias clinicas internas. Es detectar identificadores obvios que no deberian
salir en textos de circulacion externa o semi-externa: DNI/documento, telefono,
email, domicilio, nombre completo del paciente, fecha de nacimiento, historia
clinica/id de afiliado y metadatos de estudios identificables. Todo hallazgo
debe reportar evidencia redacted, nunca imprimir el dato sensible completo.

Con la evidencia local, este es el siguiente P0 correcto despues de
`diagnostico_separado_de_indicacion`: tiene alto valor, puede probarse solo con
fixtures sinteticos y no exige tocar plantillas finales ni datos reales.

## coverage_table

| Fuente | Estado | Uso |
| --- | --- | --- |
| `jobs/20260527T120441-clinica-datos-sensibles-minimizados-p0-plan-v1.md` | Revisada | Workorder, limites y entregable esperado. |
| `context/fronts/clinica.md` | Revisada | Canon CLINICA y backlog corpus a gates. |
| `results/20260527T010224-clinica-corpus-gates-backlog-v2.result.md` | Revisada | Priorizacion P0 y frontera de privacidad/export. |
| `results/20260527T030306-clinica-documental-p0-gates-detect-only-plan-v1.result.md` | Revisada | Contrato base detect-only/report-only. |
| `results/20260527T063553-clinica-next-documental-p0-gate-plan-v1.result.md` | Revisada | Secuencia documental P0 y control de falsos positivos. |
| `results/20260527T110517-clinica-documental-p0-next-implementation-audit-v1.result.md` | Revisada | Decision de integrar primero diagnostico separado. |
| `results/20260527T113720-clinica-diagnostico-separado-implementation-review-v1.result.md` | Revisada | Aceptacion en observacion y candidato siguiente. |

## alcance_detect_only_report_only

```yaml
gate_id: datos_sensibles_minimizados
mode: detect_only_report_only
source_boundary: internal_privacy_minimization_rule
initial_effect:
  synthetic_fixture_fail: true
  real_document_blocking: false
  report_findings_to_orchestrator: true
applies_to:
  document_type:
    - export
    - handoff
    - public_summary
    - texto_para_envio
  payload_paths:
    - $.rendered_text
    - $.export_payload.text
    - $.messages[*].body
    - $.attachments[*].caption
does_not_apply_to:
  - historia_clinica_interna_with_identifiers_allowed
  - consentimiento_interno_with_identifiers_allowed
  - parte_quirurgico_interno_with_identifiers_allowed
  - source_case_raw_fields_not_selected_for_export
```

Regla de frontera: si un dato sensible existe en el caso fuente pero no esta en
el texto/payload exportado, v1 no debe fallar. El gate mira la salida o el
payload de handoff, no el expediente bruto entero.

## patrones_p0_v1

Patrones permitidos para v1, todos con match redacted:

| Categoria | Disparo estrecho | Ejemplo seguro de `matched_text` redacted | Severidad |
| --- | --- | --- | --- |
| Documento/DNI/CUIL/pasaporte | Etiqueta `dni`, `documento`, `cuil`, `pasaporte` cerca de una secuencia alfanumerica. | `DNI <ID:DNI:8_DIGITS>` | `fail` |
| Telefono/WhatsApp | Etiqueta `telefono`, `tel`, `whatsapp`, `celular` o numero con formato telefonico en salida no autorizada. | `telefono <PHONE:10_DIGITS>` | `fail` |
| Email personal | Patron email en export/handoff no autorizado. | `<EMAIL:REDACTED>` | `fail` |
| Domicilio/direccion | Etiqueta `domicilio`, `direccion`, `calle`, `altura`, `piso`, `depto` con valor concreto. | `domicilio <ADDRESS:REDACTED>` | `fail` |
| Nombre completo de paciente | Campo estructurado `patient_name` exportado o texto con etiqueta `paciente:` + dos tokens de nombre. | `Paciente <PATIENT_NAME:REDACTED>` | `fail` o `needs_review` si solo hay heuristica textual. |
| Fecha de nacimiento/edad identificante | Etiqueta `fecha de nacimiento`, `nac.`, `fn`, `dob`. No marcar fechas quirurgicas. | `fecha de nacimiento <DATE:REDACTED>` | `fail` |
| Historia clinica / id interno | Etiqueta `historia clinica`, `HC`, `nro afiliado`, `id paciente`, `accession`. | `HC <MEDICAL_RECORD_ID:REDACTED>` | `fail` |
| Obra social / afiliado | Etiqueta `obra social` + numero afiliado, plan o credencial. | `afiliado <MEMBERSHIP_ID:REDACTED>` | `fail` |
| Metadatos de estudio identificables | `study_id`, `accession_number`, `DICOM PatientID` en payload exportado. | `accession <STUDY_ID:REDACTED>` | `fail` |

No incluir en v1:

- Toponimos amplios como ciudad/provincia si no identifican al paciente.
- Edad sola, salvo que este combinada con nombre/documento u otro identificador.
- Fechas clinicas necesarias, si no son fecha de nacimiento ni identificador.
- Diagnostico, nivel/lado, tecnica o riesgo medico cuando no identifican a la
  persona.

## contrato_output_redacted

El validator debe emitir JSON auditable sin filtrar el dato sensible completo:

```json
{
  "case_id": "SYN-PRIV-001",
  "ok": false,
  "mode": "detect_only",
  "summary": {
    "fail": 1,
    "needs_review": 0,
    "advisory": 0
  },
  "findings": [
    {
      "gate_id": "datos_sensibles_minimizados",
      "status": "fail",
      "severity": "fail",
      "document_type": "public_summary",
      "category": "dni",
      "evidence_path": "$.rendered_text",
      "matched_text": "DNI <ID:DNI:8_DIGITS>",
      "local_context": "Paciente <PATIENT_NAME:REDACTED>, DNI <ID:DNI:8_DIGITS>, ...",
      "redaction_applied": true,
      "raw_match_available": false,
      "source_boundary": "internal_privacy_minimization_rule",
      "recommendation": "Retirar o anonimizar DNI antes de exportar."
    }
  ]
}
```

Reglas obligatorias:

- `matched_text` y `local_context` son redacted por defecto; no agregar un campo
  paralelo con raw text.
- `evidence_path` debe apuntar al path exacto del payload exportado, no solo al
  documento completo.
- `recommendation` debe ser accionable y no repetir el identificador.
- Si una regla textual esta insegura, usar `needs_review` con redaccion, no
  `fail` amplio.
- Si el texto ya contiene placeholders como `<DNI_REDACTED>` o
  `[telefono omitido]`, debe pasar.

## fixtures_sinteticos_minimos

| Fixture | Tipo | Input sintetico | Salida/payload sintetico | Esperado |
| --- | --- | --- | --- | --- |
| `CLIN-DOC-PRIV-005-dni-in-public-summary` | Positivo | `document_type=public_summary; patient_identifiers_allowed=false` | `Paciente SYN-NOMBRE, DNI 99112233, diagnostico hernia L4-L5.` | `fail`, redacted como `<PATIENT_NAME>` y `<ID:DNI:8_DIGITS>`. |
| `CLIN-DOC-PRIV-006-phone-whatsapp-in-handoff` | Positivo | `document_type=handoff; patient_identifiers_allowed=false` | `Contactar por WhatsApp 1111111111 para coordinar.` | `fail`, redacted como `<PHONE:10_DIGITS>`. |
| `CLIN-DOC-PRIV-007-address-in-export` | Positivo | `document_type=export; patient_identifiers_allowed=false` | `Domicilio sintetico Calle Falsa 123 Piso 4.` | `fail`, redacted como `<ADDRESS:REDACTED>`. |
| `CLIN-DOC-PRIV-008-email-in-texto-envio` | Positivo | `document_type=texto_para_envio; patient_identifiers_allowed=false` | `Enviar copia a paciente@example.invalid.` | `fail`, redacted como `<EMAIL:REDACTED>`. |
| `CLIN-DOC-PRIV-009-hc-and-affiliate-id` | Positivo | `document_type=handoff; patient_identifiers_allowed=false` | `HC SYN-000123, afiliado OS-SYN-999.` | `fail`, redacted como `<MEDICAL_RECORD_ID>` y `<MEMBERSHIP_ID>`. |
| `CLIN-DOC-PRIV-010-birth-date-in-summary` | Positivo | `document_type=public_summary; patient_identifiers_allowed=false` | `Fecha de nacimiento 01/02/1970.` | `fail`, redacted como `<DATE:REDACTED>`. |
| `CLIN-DOC-PRIV-011-minimized-pass` | Negativo | `document_type=public_summary; patient_identifiers_allowed=false` | `Paciente anonimizado, diagnostico hernia L4-L5, plan quirurgico a revisar.` | `pass`. |
| `CLIN-DOC-PRIV-012-redacted-token-pass` | Negativo | `document_type=export; patient_identifiers_allowed=false` | `DNI <DNI_REDACTED>, telefono [omitido].` | `pass`. |
| `CLIN-DOC-PRIV-013-internal-identifiers-allowed-pass` | Negativo | `document_type=historia_clinica; patient_identifiers_allowed=true` | `Identificador interno sintetico permitido en documento interno.` | `pass`, fuera de alcance v1. |
| `CLIN-DOC-PRIV-014-negated-mention-pass` | Negativo | `document_type=public_summary; patient_identifiers_allowed=false` | `No se incluye DNI, telefono, email ni domicilio.` | `pass`. |
| `CLIN-DOC-PRIV-015-age-and-clinical-date-pass` | Negativo | `document_type=handoff; patient_identifiers_allowed=false` | `Varon de 45 anos; control posoperatorio el dia sintetico informado.` | `pass` o `advisory`, no `fail`. |
| `CLIN-DOC-PRIV-016-name-heuristic-review` | Frontera | `document_type=public_summary; patient_identifiers_allowed=false` | `Paciente Juan Perez sintetico con cuadro lumbar.` | `needs_review` si no viene de campo estructurado; `fail` si proviene de `export_payload.patient_name`. |

## reglas_de_redaccion

| Campo | Regla |
| --- | --- |
| `matched_text` | Debe contener solo categoria y placeholder. Ej.: `telefono <PHONE:10_DIGITS>`. |
| `local_context` | Maximo una ventana corta, con todos los identificadores reemplazados. |
| `evidence_path` | JSONPath exacto: `$.rendered_text`, `$.messages[0].body`, `$.export_payload.patient_name`. |
| `recommendation` | Frase generica: "Retirar o anonimizar [categoria] antes de exportar." |
| `category` | Una de `dni`, `phone`, `email`, `address`, `patient_name`, `birth_date`, `medical_record_id`, `membership_id`, `study_id`. |
| `source_boundary` | Siempre `internal_privacy_minimization_rule` en v1. |
| `raw_match_available` | `false`. Evita que consumidores guarden el dato sin querer. |

Si el orquestador necesita debug local, que sea por conteos y categorias, no por
texto crudo persistido en resultados.

## riesgos_p0_p1

| Pri | Riesgo | Tipo | Mitigacion |
| --- | --- | --- | --- |
| P0 | Fuga por output de QA: el validator detecta un dato sensible y lo imprime crudo. | Fuga de datos | Redactar antes de construir findings; tests que fallen si `matched_text` contiene digitos largos, email o direccion completa. |
| P0 | Gate analiza expediente bruto y reporta identificadores internos necesarios. | Falso positivo y fuga | Evaluar solo payload exportado/seleccionado; excluir `source_case_raw_fields_not_selected_for_export`. |
| P0 | Report-only se transforma en hard block real sin calibracion. | Operativo/legal | En v1 solo falla fixtures sinteticos y reporta documentos reales. |
| P1 | Heuristica de nombres marca medicos, instituciones o procedimientos capitalizados. | Falso positivo | `patient_name` es `fail` solo si proviene de campo estructurado; heuristica textual es `needs_review`. |
| P1 | Numeros clinicos se confunden con DNI o telefono. | Falso positivo | Requerir etiqueta cercana para DNI/telefono salvo patron telefonico muy evidente. |
| P1 | Fechas quirurgicas o de control se marcan como fecha de nacimiento. | Falso positivo | Fallar solo con etiqueta de nacimiento/DOB/FN. |
| P1 | Placeholders redacted se vuelven a marcar como datos. | Falso positivo | Whitelist de `<...REDACTED>`, `[omitido]`, `anonimizado`. |
| P1 | Identificadores en adjuntos/captions quedan fuera. | Falso negativo | Incluir `attachments[*].caption` en v1; dejar binarios fuera hasta otro workorder. |

## decision

**Integrar ahora** como plan de implementacion local, con estas condiciones:

1. Solo fixtures sinteticos; ningun dato real.
2. Validator puro y report-only; no toca plantillas finales.
3. Redaccion previa a persistir findings.
4. QA focal debe probar que no se filtran digitos/email/direccion crudos.
5. `patient_name` textual queda `needs_review` salvo campo estructurado.
6. No abrir ni procesar Drive/iCloud/Photos/Gmail/Telegram/datos de pacientes.

No hace falta pedir material humano para v1: los patrones iniciales se cubren
con datos sinteticos. Si luego se quiere promocionar a bloqueo real, ahi si se
necesita revision humana con ejemplos anonimizados y politica legal/versionada.

## recommendation

Proxima accion unica: crear workorder de implementacion en la app canonica para
`datos_sensibles_minimizados`, agregando fixtures `CLIN-DOC-PRIV-005` a
`CLIN-DOC-PRIV-016`, validator detect-only/report-only y tests especificos de
redaccion que fallen si el JSON de findings contiene DNI/telefono/email/domicilio
crudos.

## attempted_routes

- Se hizo `git pull --rebase`.
- Se ejecuto `./scripts/personal_xh_check.sh` y se detecto el job asignado.
- Se reclamo el job con claim local bajo `claims/`.
- Se reviso el workorder, `context/fronts/clinica.md` y resultados CLINICA
  previos de backlog/documental P0.
- No se abrio app real, Drive/iCloud/Photos/Gmail, Telegram, datos de pacientes
  ni ObraCash.

## risks_limits

- Este entregable es plan/contrato desde el bridge; no valida el diff real de la
  app canonica.
- No verifica normativa externa vigente; por eso v1 queda como regla interna de
  minimizacion y report-only.
- La deteccion de nombres por texto libre es deliberadamente conservadora para
  evitar falsos positivos.
- Los adjuntos binarios, imagenes, PDFs y capturas quedan fuera de v1 salvo
  captions/texto asociado; requieren otro gate.

## confidence

Alta para el alcance v1 y el contrato redacted, porque deriva del backlog P0
local y de la secuencia ya aceptada para gates documentales. Media para rutas
exactas de implementacion hasta que el orquestador inspeccione la app canonica.
Media-baja para cualquier promocion a hard block legal sin source pack oficial,
revision humana y QA con material anonimo controlado.

## evidence_paths

- `jobs/20260527T120441-clinica-datos-sensibles-minimizados-p0-plan-v1.md`
- `claims/20260527T120441-clinica-datos-sensibles-minimizados-p0-plan-v1.json`
- `context/fronts/clinica.md`
- `results/20260527T010224-clinica-corpus-gates-backlog-v2.result.md`
- `results/20260527T030306-clinica-documental-p0-gates-detect-only-plan-v1.result.md`
- `results/20260527T063553-clinica-next-documental-p0-gate-plan-v1.result.md`
- `results/20260527T110517-clinica-documental-p0-next-implementation-audit-v1.result.md`
- `results/20260527T113720-clinica-diagnostico-separado-implementation-review-v1.result.md`
