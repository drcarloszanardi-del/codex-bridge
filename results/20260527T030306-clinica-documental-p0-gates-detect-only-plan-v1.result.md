---
job_id: 20260527T030306-clinica-documental-p0-gates-detect-only-plan-v1
worker: personal-xh
status: completed
completed_at: 2026-05-27T03:15:00-03:00
front: CLINICA
no_external_actions: true
no_secrets: true
---

# Resultado - Clinica documental P0 gates detect-only plan v1

## summary

Plan implementable, detect-only/report-only, para convertir el backlog
documental de CLINICA en gates P0 sin tocar plantillas finales ni inventar
normativa. La prioridad es auditar si los documentos tienen campos minimos,
trazabilidad y coherencia clinico-documental; la promocion a hard gate legal
queda condicionada a fuentes oficiales vigentes y revision legal.

Evidencia: el frente CLINICA ya fija corpus a gates y separa fuentes oficiales
de jurisprudencia/doctrina. Inferencia: el primer patch debe ser un runner puro
con fixtures sinteticos y salida JSON auditable. Opinion: conviene empezar por
cinco gates estrechos, porque reducen riesgo sin bloquear por criterio legal
amplio.

## coverage_table

| Fuente | Estado | Uso |
| --- | --- | --- |
| `jobs/20260527T030306-clinica-documental-p0-gates-detect-only-plan-v1.md` | Revisada | Workorder, entregables y limites. |
| `context/fronts/clinica.md` | Revisada | Canon, ruta probable de app y corpus a gates. |
| `results/20260527T010224-clinica-corpus-gates-backlog-v2.result.md` | Revisada | Backlog documental P0 y frontera de fuentes oficiales. |
| `results/20260527T003215-clinica-correcciones-a-fixtures-implementacion.result.md` | Revisada | Secuencia de implementacion y archivos probables. |
| `results/20260526T145636-clinica-p0-extraforaminal-no-interlaminar-plan-v1.result.md` | Revisada | Contrato detect-only, severidades y fixtures de frontera. |

## p0_gate_scope

| Orden | Gate P0 | Aplica a | Severidad inicial | Razon |
| --- | --- | --- | --- | --- |
| 1 | `consentimiento_especifico_no_generico` | consentimiento | `needs_review` o `fail` en fixture QA | Evita consentimientos vacios/genericos. |
| 2 | `historia_clinica_minima_completa` | historia clinica | `needs_review` | Detecta documentos incompletos antes de render final. |
| 3 | `diagnostico_separado_de_indicacion` | historia, consentimiento | `fail` en QA sintetico | Regla documental interna ya derivada de correcciones del Doctor. |
| 4 | `consistencia_diagnostico_indicacion_procedimiento` | historia, consentimiento, parte | `needs_review` | Evita contradicciones entre ejes del caso. |
| 5 | `datos_sensibles_minimizados` | export/envio/texto final | `fail` en QA si hay identificadores sinteticos prohibidos | Reduce riesgo de exponer datos no necesarios. |

No incluyo jurisprudencia/doctrina como P0 activo: queda `advisory` hasta tener
fuente oficial, metadatos completos y revision legal.

## detect_only_contract

### Input JSON

```json
{
  "case_id": "SYN-CLIN-DOC-001",
  "document_type": "historia_clinica|consentimiento|parte_quirurgico|export",
  "source_fields": {
    "diagnosis": "hernia lumbar L4-L5",
    "indication": "microdiscectomia",
    "procedure": "microdiscectomia L4-L5 derecha",
    "laterality": "derecha",
    "level": "L4-L5",
    "risks": ["infeccion", "sangrado"],
    "alternatives": ["tratamiento medico"],
    "implants": [],
    "patient_identifiers_allowed": false
  },
  "rendered_text": "texto final sintetico a validar",
  "metadata": {
    "template_id": "synthetic_template_v1",
    "source_policy_version": "internal_doc_gates_v1"
  }
}
```

### Output JSON

```json
{
  "case_id": "SYN-CLIN-DOC-001",
  "ok": false,
  "findings": [
    {
      "gate_id": "diagnostico_separado_de_indicacion",
      "severity": "fail",
      "status": "fail",
      "matched_text": "hernia L4-L5 con indicacion de cirugia",
      "local_context": "Diagnostico: hernia L4-L5 con indicacion de cirugia",
      "evidence_path": "$.rendered_text",
      "source_boundary": "internal_documental_rule",
      "message": "El diagnostico mezcla indicacion terapeutica."
    }
  ]
}
```

Severidades:

| Severidad | Uso |
| --- | --- |
| `fail` | Solo para QA sintetico o reglas internas estrechas con condicion clara. En produccion inicial puede impedir merge del fixture, no necesariamente bloquear documento real. |
| `needs_review` | Falta campo, contradiccion posible o regla legal/documental que requiere contexto clinico o fuente oficial. |
| `advisory` | Jurisprudencia, doctrina, estilo o mejora que no debe frenar generacion. |

## fixtures

Todos los fixtures son sinteticos, sin pacientes reales, sin nombres reales y sin
fechas reales. "Positivo" significa que el gate debe disparar; "negativo"
significa control que debe pasar.

| Gate | Fixture | Tipo | Input sintetico | Output sintetico | Esperado |
| --- | --- | --- | --- | --- | --- |
| consentimiento_especifico_no_generico | `CLIN-DOC-CONS-001-generic-procedure` | positivo | `procedure=microdiscectomia L4-L5 derecha; risks=[infeccion,sangrado]; alternatives=[tratamiento medico]` | `Autorizo el procedimiento que el medico considere necesario.` | `needs_review` |
| consentimiento_especifico_no_generico | `CLIN-DOC-CONS-002-missing-risks` | positivo | `procedure=artrodesis L4-L5; risks=[]` | `Acepto la artrodesis L4-L5 sin detalle de riesgos especificos.` | `needs_review` |
| consentimiento_especifico_no_generico | `CLIN-DOC-CONS-003-specific-pass` | negativo | `procedure=microdiscectomia L4-L5 derecha; risks=[infeccion,sangrado,lesion neural]; alternatives=[tratamiento medico]` | `Consentimiento para microdiscectomia L4-L5 derecha, con riesgos y alternativas enumerados.` | `pass` |
| consentimiento_especifico_no_generico | `CLIN-DOC-CONS-004-negated-generic-pass` | negativo | `procedure=cirugia especifica; risks=[infeccion]` | `No se usa consentimiento generico; se consigna procedimiento y riesgos especificos.` | `pass` |
| historia_clinica_minima_completa | `CLIN-DOC-HC-001-no-diagnosis` | positivo | `diagnosis=null; indication=cirugia` | `Historia clinica: se indica cirugia. Diagnostico no consignado.` | `needs_review` |
| historia_clinica_minima_completa | `CLIN-DOC-HC-002-no-date-professional` | positivo | `diagnosis=canal estrecho; professional=null; date=null` | `Historia clinica de canal estrecho sin profesional ni fecha.` | `needs_review` |
| historia_clinica_minima_completa | `CLIN-DOC-HC-003-complete-pass` | negativo | `diagnosis=hernia L4-L5; symptoms=radiculalgia; exam=deficit leve; plan=cirugia; professional=synthetic_doctor; date=synthetic_date` | `Historia con diagnostico, sintomas, examen, indicacion, profesional y fecha sintetica.` | `pass` |
| historia_clinica_minima_completa | `CLIN-DOC-HC-004-not-applicable-export` | negativo | `document_type=export; diagnosis=null` | `Export resumido sin pretension de historia clinica completa.` | `pass` |
| diagnostico_separado_de_indicacion | `CLIN-DOC-DX-001-indication-in-dx` | positivo | `diagnosis=hernia L4-L5; indication=microdiscectomia` | `Diagnostico: hernia L4-L5 con indicacion de microdiscectomia.` | `fail` |
| diagnostico_separado_de_indicacion | `CLIN-DOC-DX-002-treatment-in-dx` | positivo | `diagnosis=canal estrecho; indication=descompresion` | `Diagnostico: canal estrecho que requiere descompresion quirurgica.` | `fail` |
| diagnostico_separado_de_indicacion | `CLIN-DOC-DX-003-separated-pass` | negativo | `diagnosis=hernia L4-L5; indication=microdiscectomia` | `Diagnostico: hernia L4-L5. Indicacion: microdiscectomia.` | `pass` |
| diagnostico_separado_de_indicacion | `CLIN-DOC-DX-004-negated-pass` | negativo | `diagnosis=hernia L4-L5` | `Diagnostico: hernia L4-L5. No se consigna indicacion dentro del diagnostico.` | `pass` |
| consistencia_diagnostico_indicacion_procedimiento | `CLIN-DOC-CONSIST-001-level-mismatch` | positivo | `diagnosis=hernia L4-L5 derecha; procedure=microdiscectomia L5-S1 izquierda` | `Se diagnostica L4-L5 derecha y se programa L5-S1 izquierda.` | `needs_review` |
| consistencia_diagnostico_indicacion_procedimiento | `CLIN-DOC-CONSIST-002-procedure-contradiction` | positivo | `diagnosis=estenosis; indication=artrodesis; procedure=parche dural` | `Parte final centrado en parche dural sin evento dural informado.` | `needs_review` |
| consistencia_diagnostico_indicacion_procedimiento | `CLIN-DOC-CONSIST-003-consistent-pass` | negativo | `diagnosis=hernia L4-L5 derecha; indication=microdiscectomia; procedure=microdiscectomia L4-L5 derecha` | `Diagnostico, indicacion y procedimiento coinciden en nivel y lado.` | `pass` |
| consistencia_diagnostico_indicacion_procedimiento | `CLIN-DOC-CONSIST-004-unknown-safe-pass` | negativo | `diagnosis=hernia lumbar; level=null; procedure=microdiscectomia lumbar` | `Sin nivel informado; el documento mantiene nivel no especificado y pide revision.` | `pass` |
| datos_sensibles_minimizados | `CLIN-DOC-PRIV-001-phone-in-export` | positivo | `document_type=export; patient_identifiers_allowed=false` | `Paciente SYN-NOMBRE, telefono 1111111111, DNI 99999999.` | `fail` |
| datos_sensibles_minimizados | `CLIN-DOC-PRIV-002-address-in-export` | positivo | `document_type=export; patient_identifiers_allowed=false` | `Domicilio sintetico completo incluido en export publico.` | `fail` |
| datos_sensibles_minimizados | `CLIN-DOC-PRIV-003-minimized-pass` | negativo | `document_type=export; patient_identifiers_allowed=false` | `Caso sintetico sin nombre, DNI, telefono ni domicilio.` | `pass` |
| datos_sensibles_minimizados | `CLIN-DOC-PRIV-004-internal-allowed-review` | negativo | `document_type=historia_clinica; patient_identifiers_allowed=true` | `Identificador interno sintetico permitido en historia clinica no exportada.` | `pass` |

## files_to_inspect

Rutas probables de la app real, sin acceder desde este job:

```text
/Users/jarvis/.openclaw/workspace/clinica/app-clinica-medicolegal
data/derived/clinical_test_cases/clinical_p0_gates_v1.json
data/derived/clinical_test_cases/documental_p0_gates_v1.json
scripts/qa/validate_clinical_p0_gates_v1.js
scripts/qa/validate_documental_p0_gates_v1.js
scripts/qa/run_clinica_core_qa.js
scripts/jarvis/clinical_document_handoff.js
app/app.js
app/product.html
```

Comandos `rg` sugeridos para localizar equivalentes:

```bash
rg -n "clinical_p0|p0_gates|lumbar|documental|consentimiento|historia|parte_quirurgico" /Users/jarvis/.openclaw/workspace/clinica/app-clinica-medicolegal
rg -n "rendered_text|document_type|diagnosis|indication|procedure|consent" /Users/jarvis/.openclaw/workspace/clinica/app-clinica-medicolegal
rg -n "run_clinica_core_qa|validate_clinical|route_guard|handoff" /Users/jarvis/.openclaw/workspace/clinica/app-clinica-medicolegal/scripts
```

## implementation_sequence

1. Commit 1 - datos sinteticos: agregar `documental_p0_gates_v1.json` con los
   fixtures anteriores, sin tocar plantillas.
2. Commit 2 - helper puro: agregar normalizacion, segmentacion, negacion local y
   extractores de campos a un modulo QA.
3. Commit 3 - validator detect-only: implementar los cinco gates con salida JSON
   `findings[]`, sin reescribir documentos.
4. Commit 4 - core QA: conectar el runner al QA clinico existente; fallar solo
   en fixtures `fail`, reportar `needs_review` y `advisory`.
5. Commit 5 - calibracion: agregar casos frontera de falsos positivos y dejar
   metricas de conteo por gate.
6. Recien despues, y en otro workorder, evaluar si algun gate pasa de QA-only a
   bloqueo de documento real.

## legal_source_boundary

| Gate | Regla documental interna ahora | Requiere fuente oficial antes de hard gate real |
| --- | --- | --- |
| `consentimiento_especifico_no_generico` | Detectar procedimiento/riesgos/alternativas ausentes o texto generico. | Si, para definir obligatoriedad legal exacta, jurisdiccion y texto minimo. |
| `historia_clinica_minima_completa` | Reportar ausencia de diagnostico, evolucion, profesional, fecha o firma sintetica. | Si, para convertir campos minimos en bloqueo medico-legal universal. |
| `diagnostico_separado_de_indicacion` | Regla interna fuerte: no mezclar hecho diagnostico con plan terapeutico. | No para QA interno; si antes de presentarlo como exigencia legal. |
| `consistencia_diagnostico_indicacion_procedimiento` | Regla clinico-documental interna: marcar contradicciones entre campos. | Depende del caso; hard gate amplio requiere revision medico-legal. |
| `datos_sensibles_minimizados` | Bloquear identificadores sinteticos en exports no autorizados. | Si, para mapa legal fino de datos personales; no para QA de minimizacion interna. |

Jurisprudencia y doctrina: solo `advisory` hasta fuente oficial, metadatos
completos, vigencia y revision legal. Ningun fallo no verificado debe crear
hard gate.

## qa_commands

Focal, despues de implementar:

```bash
node -c scripts/qa/validate_documental_p0_gates_v1.js
node scripts/qa/validate_documental_p0_gates_v1.js --fixture data/derived/clinical_test_cases/documental_p0_gates_v1.json
```

Core QA clinico:

```bash
node -c scripts/qa/validate_clinical_p0_gates_v1.js
node scripts/qa/validate_clinical_p0_gates_v1.js
node scripts/qa/run_clinica_core_qa.js
```

Bridge/result QA usado en este job:

```bash
python3 scripts/validate_result_contract.py results/20260527T030306-clinica-documental-p0-gates-detect-only-plan-v1.result.md
git diff --check
python3 scripts/secret_scan.py
```

## attempted_routes

- Se hizo `git pull --rebase`.
- Se reclamo el job con `python3 scripts/bridgectl.py claim`.
- Se reviso `jobs/20260527T030306-clinica-documental-p0-gates-detect-only-plan-v1.md`.
- Se revisaron las fuentes listadas en `coverage_table`.
- No se abrio Drive, iCloud, Gmail, Photos, Downloads, Telegram real, ObraCash
  ni bibliotecas privadas.
- No se inspecciono la app canonica real; este entregable es plan/contrato para
  el orquestador.

## risks_limits

- Falsos positivos: texto generico negado, menciones historicas o campos
  ausentes por documento no aplicable. Mitigacion: activar por `document_type`,
  usar negacion local y devolver `needs_review`.
- Falsos negativos: plantillas que esconden campos en frases largas o sinonimos
  no cubiertos. Mitigacion: fixtures frontera y `matched_text/local_context`.
- Contexto clinico: consistencia diagnostico-procedimiento puede necesitar
  criterio medico; no convertir contradicciones ambiguas en `fail` inicial.
- Bloqueo excesivo: al principio `needs_review` debe informar, no frenar
  documentos reales.
- Legal: sin fuente oficial vigente, las reglas legales quedan como auditoria o
  advisory; no como hard gate universal.

## recommendation

Proxima accion unica para el orquestador: crear un workorder de implementacion
para `data/derived/clinical_test_cases/documental_p0_gates_v1.json` y
`scripts/qa/validate_documental_p0_gates_v1.js`, con los cinco gates de este
resultado en modo detect-only/report-only y sin tocar plantillas finales.

## confidence

Media-alta para el alcance, contrato y secuencia porque deriva de los resultados
CLINICA previos y del frente canonico. Media para rutas exactas hasta que el
orquestador inspeccione la app real. Media-baja para cualquier hard gate legal
sin source pack oficial y revision legal.

## evidence_paths

- `jobs/20260527T030306-clinica-documental-p0-gates-detect-only-plan-v1.md`
- `context/fronts/clinica.md`
- `results/20260527T010224-clinica-corpus-gates-backlog-v2.result.md`
- `results/20260527T003215-clinica-correcciones-a-fixtures-implementacion.result.md`
- `results/20260526T145636-clinica-p0-extraforaminal-no-interlaminar-plan-v1.result.md`
