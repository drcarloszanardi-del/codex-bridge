---
job_id: 20260527T063553-clinica-next-documental-p0-gate-plan-v1
worker: personal-xh
status: completed
completed_at: 2026-05-27T06:40:30-03:00
front: CLINICA
no_external_actions: true
no_secrets: true
---

# Resultado - Clinica next documental P0 gate plan v1

## summary

Gate candidato unico: **`diagnostico_separado_de_indicacion`** en modo
detect-only/report-only. Es el mejor siguiente P0 documental porque no depende
de inventar normativa externa: deriva de reglas internas ya documentadas en
CLINICA y del backlog previo, y protege una frontera medico-legal concreta:
separar el hecho diagnostico del plan terapeutico.

Evidencia: `context/fronts/clinica.md` lista "diagnostico separado de
indicacion" entre corpus a gates, y
`results/20260527T010224-clinica-corpus-gates-backlog-v2.result.md` lo marca
P0 para historia/consentimiento. Inferencia: despues de los gates clinicos de
topografia, descompresion y extraforaminal, conviene un gate documental que
controle estructura de documentos sin bloquear por criterios legales amplios.
Opinion: dejar consentimiento generico como segundo candidato, pero no primero,
hasta tener source pack oficial/versionado.

## coverage_table

| Fuente | Estado | Uso |
| --- | --- | --- |
| `jobs/20260527T063553-clinica-next-documental-p0-gate-plan-v1.md` | Revisada | Workorder, limites y entregables. |
| `context/fronts/clinica.md` | Revisada | Canon CLINICA, ruta canonica y corpus a gates. |
| `results/20260527T030306-clinica-documental-p0-gates-detect-only-plan-v1.result.md` | Revisada | Plan documental P0, contrato base y fixtures previos. |
| `results/20260527T010224-clinica-corpus-gates-backlog-v2.result.md` | Revisada | Backlog P0 documental y frontera de fuentes oficiales. |

## findings

| Prioridad | Gate | Decision | Evidencia | Riesgo si se implementa mal |
| --- | --- | --- | --- | --- |
| P0 | `diagnostico_separado_de_indicacion` | Candidato unico recomendado. | Figura como P0 en el backlog y como gate documental en el frente CLINICA. | Falso positivo si marca frases historicas, negadas o secciones de plan como diagnostico. |
| P0/P1 | `consentimiento_especifico_no_generico` | Top 2, no recomendado como siguiente unico. | Tambien es P0 en backlog, pero requiere fuente oficial antes de hard gate legal real. | Inventar requisito legal o bloquear consentimientos correctos por wording. |

## detect_only_contract_json

Input minimo:

```json
{
  "case_id": "SYN-DOC-DX-001",
  "document_type": "historia_clinica|consentimiento|parte_quirurgico",
  "source_fields": {
    "diagnosis": "hernia discal L4-L5 derecha",
    "indication": "microdiscectomia L4-L5 derecha",
    "procedure": "microdiscectomia L4-L5 derecha",
    "level": "L4-L5",
    "laterality": "derecha"
  },
  "rendered_text": "Diagnostico: hernia discal L4-L5 derecha con indicacion de microdiscectomia.",
  "metadata": {
    "template_id": "synthetic_template_v1",
    "gate_policy_version": "documental_p0_gates_v1",
    "mode": "detect_only"
  }
}
```

Output esperado:

```json
{
  "case_id": "SYN-DOC-DX-001",
  "ok": false,
  "mode": "detect_only",
  "summary": {
    "fail": 1,
    "needs_review": 0,
    "advisory": 0
  },
  "findings": [
    {
      "gate_id": "diagnostico_separado_de_indicacion",
      "status": "fail",
      "severity": "fail",
      "document_type": "historia_clinica",
      "evidence_path": "$.rendered_text",
      "matched_text": "Diagnostico: hernia discal L4-L5 derecha con indicacion de microdiscectomia.",
      "local_context": "Diagnostico: hernia discal L4-L5 derecha con indicacion de microdiscectomia.",
      "source_boundary": "internal_documental_rule",
      "reason": "El campo diagnostico mezcla diagnostico con indicacion terapeutica.",
      "recommendation": "Separar Diagnostico e Indicacion en secciones distintas."
    }
  ]
}
```

Reglas iniciales:

| Regla | Resultado |
| --- | --- |
| Activar solo en seccion/campo `diagnostico` o encabezado equivalente. | Evita revisar todo el texto como si fuera diagnostico. |
| Fallar si el diagnostico contiene verbos/frases de indicacion: `se indica`, `con indicacion de`, `requiere`, `se programa`, `candidato a`, `tratamiento quirurgico`. | `fail` QA-only. |
| Pasar si diagnostico e indicacion estan en secciones separadas. | `pass`. |
| Si la frase aparece negada o como antecedente historico, no fallar; devolver `pass` o `needs_review` segun contexto. | Control de falsos positivos. |
| Si el documento no tiene seccion diagnostico identificable, reportar `needs_review`, no `fail`. | Evita hard fail por parseo incompleto. |

## fixtures

| Fixture | Tipo | Input sintetico | Render sintetico | Esperado | Razon |
| --- | --- | --- | --- | --- | --- |
| `CLIN-DOC-DX-005-indication-in-diagnosis` | Positivo | `document_type=historia_clinica; diagnosis=hernia L4-L5; indication=microdiscectomia` | `Diagnostico: hernia L4-L5 derecha con indicacion de microdiscectomia.` | `fail` | Mezcla diagnostico e indicacion en el mismo campo. |
| `CLIN-DOC-DX-006-requires-surgery-in-diagnosis` | Positivo | `document_type=consentimiento; diagnosis=canal estrecho; indication=descompresion` | `Diagnostico: canal estrecho lumbar que requiere descompresion quirurgica.` | `fail` | `requiere` convierte diagnostico en indicacion. |
| `CLIN-DOC-DX-007-separated-pass` | Negativo | `diagnosis=hernia L4-L5; indication=microdiscectomia` | `Diagnostico: hernia L4-L5 derecha. Indicacion: microdiscectomia L4-L5 derecha.` | `pass` | Las secciones estan separadas. |
| `CLIN-DOC-DX-008-negated-pass` | Negativo | `diagnosis=hernia L4-L5; indication=null` | `Diagnostico: hernia L4-L5 derecha. No se consigna indicacion dentro del diagnostico.` | `pass` | Menciona indicacion en forma negada y metadocumental. |

## medico_legal_risks

| Riesgo | Manejo detect-only |
| --- | --- |
| Documento ambiguo: el diagnostico parece justificar tratamiento sin separar hecho y plan. | Reportar con span y pedir revision/separacion. |
| Bloqueo excesivo de documentos correctos. | En fase inicial, `fail` solo rompe QA sintetico; en documentos reales se emite reporte. |
| Confundir criterio medico con criterio legal. | Declarar `source_boundary=internal_documental_rule`; no citar normativa no verificada. |
| Plantilla con secciones no estandar. | Si no se detecta seccion diagnostico, `needs_review` y no `fail`. |
| Consentimiento con lenguaje juridico amplio. | No activar este gate sobre todo el consentimiento; solo sobre diagnostico/campo equivalente. |

## false_positive_controls

- Segmentacion por encabezados: `Diagnostico`, `Indicacion`, `Procedimiento`,
  `Plan`, `Antecedentes`.
- Ventana local: solo evaluar frases dentro del segmento diagnostico.
- Negacion local: no disparar por "no se consigna indicacion dentro del
  diagnostico".
- Historial/antecedentes: frases como "se habia indicado previamente" fuera de
  diagnostico deben ser `needs_review` o `pass`.
- Sinonimos calibrados: empezar con lista corta y ampliar solo con fixtures.

## qa_commands

Comandos sugeridos en la app canonica, cuando el orquestador cree el workorder
de implementacion:

```bash
node -c scripts/qa/validate_documental_p0_gates_v1.js
node scripts/qa/validate_documental_p0_gates_v1.js --fixture data/derived/clinical_test_cases/documental_p0_gates_v1.json --gate diagnostico_separado_de_indicacion
node -c scripts/qa/validate_clinical_p0_gates_v1.js
node scripts/qa/validate_clinical_p0_gates_v1.js
node scripts/qa/run_clinica_core_qa.js
```

Validaciones bridge de este resultado:

```bash
python3 scripts/validate_result_contract.py results/20260527T063553-clinica-next-documental-p0-gate-plan-v1.result.md
git diff --check
python3 scripts/secret_scan.py
```

## attempted_routes

- Se hizo `git pull --rebase`.
- Se reclamo el job con `python3 scripts/bridgectl.py claim`.
- Se reviso `jobs/20260527T063553-clinica-next-documental-p0-gate-plan-v1.md`.
- Se revisaron las tres fuentes minimas pedidas por el workorder.
- Se busco contexto adicional local con `rg` sin abrir ObraCash, Drive, iCloud,
  Gmail, Photos, Downloads ni acciones externas.
- No se inspecciono la app canonica real ni se tocaron plantillas finales.

## risks_limits

- Este resultado es plan/contrato, no implementacion sobre la app real.
- No verifica normativa vigente; por eso el gate se declara regla documental
  interna y detect-only/report-only.
- La severidad `fail` aplica a QA sintetico inicial; en documentos reales debe
  reportar hasta calibracion y aprobacion explicita.
- Los sinonimos de indicacion terapeutica deben crecer por fixtures, no por
  intuicion amplia.

## recommendation

Proxima accion unica: crear un workorder de implementacion para
`diagnostico_separado_de_indicacion` dentro de
`documental_p0_gates_v1`, agregando los cuatro fixtures anteriores y un
validator detect-only que emita JSON auditable. No tocar plantillas finales y no
promover a bloqueo real hasta pasar QA core y revision del orquestador.

## confidence

Media-alta. La recomendacion deriva directamente de las fuentes locales pedidas
y evita apoyarse en normativa no verificada. La confianza baja a media para
rutas exactas y nombres finales hasta que el orquestador inspeccione la app
canonica.

## evidence_paths

- `jobs/20260527T063553-clinica-next-documental-p0-gate-plan-v1.md`
- `context/fronts/clinica.md`
- `results/20260527T030306-clinica-documental-p0-gates-detect-only-plan-v1.result.md`
- `results/20260527T010224-clinica-corpus-gates-backlog-v2.result.md`
- `claims/20260527T063553-clinica-next-documental-p0-gate-plan-v1.json`
