---
id: 20260526T001920-clinica-corpus-gates-hardening-v3
job_id: 20260526T001920-clinica-corpus-gates-hardening-v3
created_at: 2026-05-26T00:23:04-03:00
created_by: personal-xh
worker: personal-xh
status: completed
no_external_actions: true
no_secrets: true
---

# Resultado - CLINICA corpus gates hardening v3

## summary

Paquete ejecutable para endurecer el siguiente bloque medico-legal de la app clinica sin tocar app real, web, documentos personales ni datos de pacientes. La decision central es separar dos canales: los gates clinicos criticos derivados de fixtures/correcciones ya pueden avanzar como detectores bloqueantes acotados; los gates medico-legales derivados de normativa, jurisprudencia o doctrina deben entrar por `corpus_item` y solo pasar a `gate_item` bloqueante cuando tengan fuente oficial, metadata completa y revision explicita.

La salida clinica final no debe llenarse de citas legales. El corpus debe traducirse a campos obligatorios, consistencia documental, alertas de consentimiento, privacidad y trazabilidad; no a texto largo juridico dentro de historia clinica, consentimiento o parte quirurgico.

## source_counts

| Fuente permitida | Estado | Uso |
|---|---:|---|
| `results/20260525T170711-clinica-corpus-official-gates-next-integration-v1.result.md` | Revisada | Priorizacion P0, separacion corpus/gates y cola oficial. |
| `results/20260525T224750-clinica-v2-gates-next-hardening-audit-v1.result.md` | Revisada | Estado de promocion hard/report_only y riesgos de falso positivo. |
| `results/20260525T221902-clinica-lumbar-regression-pack-from-prior-results-v1.result.md` | Revisada | Pack portable, cinco casos regression y reglas canonicas. |
| `results/20260525T184100-clinica-lumbar-v2-stress-artifacts-v1.result.md` | Revisada | Artifacts buenos/malos, readiness y traps. |
| `results/20260525T181000-clinica-lumbar-validator-detect-only-spec-v1.result.md` | Revisada | Contrato del validator, negaciones, orden y duplicados. |
| `results/20260525T153318-clinica-lumbar-inconsistency-gates-v2.result.md` | Revisada | Matriz LUM-GATE, gate rules y forbidden phrases. |
| `results/20260525T013125-corpus-jurisprudencia-leyes-gates-app-clinica.result.md` | Revisada | Taxonomia medico-legal y conversion corpus -> gate. |
| `results/20260525T021012-corpus-official-jurisprudence-candidate-queue-v2.result.md` | Revisada | Cola oficial separada por tipo de fuente. |
| `protocol.md` | Revisada | Contrato operativo del bridge y limites de seguridad. |

## official_source_basis

| Tipo de fuente | Uso permitido ahora | No hacer |
|---|---|---|
| `official_norm` | Crear `corpus_item` para Ley 26.529, Decreto 1089/2012, Ley 25.326, Ley 17.132 y normativa local ya en cola; activar gate solo con `review_status=approved_for_gate`. | No citar articulos ni texto legal no verificado en documentos clinicos. |
| `official_judiciary_full_text` / `official_judiciary_pdf` | Usar como `review_queue` con tribunal, fecha, jurisdiccion, hecho relevante, criterio util y limite del caso. | No convertir un fallo contextual en regla universal. |
| `official_saij_summary` | Usar como tamiz para decidir que fuente primaria revisar. | No hard gate desde resumen si falta texto/fuente primaria. |
| Doctrina tecnica curada | Mantener separada como criterio auxiliar y `requires_review=true`. | No mezclar doctrina con norma vigente. |
| Correccion del Doctor / fixture sintetico | Activar gates clinicos detect-only y luego hard fail si controles buenos/malos pasan. | No inventar hechos clinicos fuera de `explicit_input` o `approved_fixture_inference`. |

Regla de activacion recomendada:

```yaml
gate_activation_policy:
  hard_fail_allowed_if:
    - source_type in ["doctor_fixture", "approved_internal_clinical_fixture"]
    - or:
        source_type: "official_norm"
        source_status: "official"
        review_status: "approved_for_gate"
  report_only_if:
    - source_type in ["official_norm_pending_review", "official_judiciary_full_text", "official_judiciary_pdf", "official_saij_summary", "curated_doctrine"]
  blocked_if:
    - source_status in ["unknown", "unverified", "summary_only"]
    - review_status not in ["approved_for_gate", "approved_report_only"]
```

## P0_clinical_document_rules

1. Toda frase clinica debe poder trazarse a `explicit_input`, `approved_fixture_inference` o `template_required_field`.
2. Diagnostico, indicacion, procedimiento, consentimiento y parte quirurgico deben conservar consistencia de patologia, nivel, lateralidad, tecnica, implantes y eventos.
3. El diagnostico no debe contener conducta terapeutica ni indicacion.
4. Si falta topografia, subtipo, raiz, material o evento dural, la salida debe declarar ausencia de dato o pedir revision; no inferir.
5. El consentimiento debe ser especifico del procedimiento y del nivel cuando el corpus lo habilite: procedimiento, nivel, riesgos principales, alternativas y consistencia con HC/parte.
6. El parte quirurgico debe tener estructura minima: fecha/contexto, profesional, diagnostico, indicacion, tecnica, hallazgos, implantes/materiales si existen, complicaciones/eventos, hemostasia, recuento, cierre y firma/estado.
7. Complicacion o evento mencionado exige manejo, resolucion o estado final; si no se informa, queda `no informado` y `needs_review`.
8. Export/handoff debe minimizar datos sensibles y bloquear identificadores personales en contextos no clinicos.

## consent_gates

| Gate | Modo inicial | Condicion | Mensaje/impacto |
|---|---|---|---|
| `consentimiento_especifico_columna_v1` | `report_only` hasta corpus aprobado | Consentimiento sin procedimiento, nivel, riesgos especificos o alternativas. | `Consentimiento generico: falta procedimiento, nivel, riesgos principales o alternativas.` |
| `consent_matches_plan_v1` | `report_only` | Procedimiento, nivel o lateralidad no coinciden con HC/indicacion/parte. | `Consentimiento no coincide con plan documentado.` |
| `consent_no_generic_risk_phrase_v1` | `report_only` | Texto tipo `se explicaron riesgos` sin enumeracion util. | Pedir riesgos especificos del procedimiento, no cita legal. |
| `fusion_segment_no_laterality_in_consent` | `hard_fail_candidate` con controles buenos | `fijacion/artrodesis L4-L5 derecha` cuando la lateralidad pertenece al abordaje. | `La fusion es por segmento; mover lateralidad a abordaje/sintoma si corresponde.` |
| `consent_source_lock_v1` | `hard_fail` tecnico | Gate legal intenta bloquear sin `approved_for_gate`. | No activar gate normativo hasta revision. |

## surgical_report_gates

| Gate | Modo recomendado | Regla |
|---|---|---|
| `documento_minimo_parte_quirurgico_v1` | `report_only` inicial | Requerir campos minimos del parte antes de promover a hard. |
| `orden_hemostasia_recuento_cierre` | `hard_fail_ready` acotado | En seccion tecnica, hemostasia y recuento deben preceder cierre por planos/piel. |
| `sin_descompresion_directa_bloqueante` | `hard_fail_ready` | Si el input declara sin descompresion directa, fallan laminectomia, hemilaminectomia, flavectomia, recalibraje o liberacion directa afirmadas. |
| `extraforaminal_no_interlaminar` | `hard_fail_ready` | Hernia extraforaminal no puede renderizar abordaje interlaminar, flavectomia o hombro de raiz como eje principal. |
| `extraforaminal_root_table` | `hard_fail_ready_limited` | Solo niveles aprobados por fixture: L3-L4 -> L3, L4-L5 -> L4, L5-S1 -> L5. |
| `no_inventar_parche_dural` | `report_only` | Parche/refuerzo/sustituto dural solo si esta informado; robustecer sinonimos antes de bloquear. |
| `parche_dural_pre_cierre` | `hard_fail_ready_limited` | Si hay parche informado, debe aparecer antes del cierre. |
| `implantes_materiales_trazabilidad_basica` | `report_only` | Materiales una vez por entidad logica; no duplicar PLIF/TLIF/implantes por headings o resumen. |
| `complicacion_evento_manejo_estado_final` | `report_only` | Evento/complicacion exige manejo y estado final, sin inventar comunicacion ni evolucion. |

## clinical_history_gates

| Gate | Modo recomendado | Regla |
|---|---|---|
| `no_inventar_diagnostico_topografia` | `hard_fail_ready` | Si el input no informa topografia/subtipo/hallazgo, no agregar extraforaminal, posterolateral, secuestro, fragmento, raiz o hernia nueva. |
| `diagnostico_puro_sin_indicacion` | `report_only` inicial | Campo diagnostico no debe incluir `con indicacion de`, `requiere`, `se indica`, `instrumentacion` o conducta. |
| `preservar_subtipo_espondilolistesis` | `report_only` inicial | Si es degenerativa, no mezclar con istmica/pars/lisis. |
| `canal_estrecho_no_tautologico` | `report_only` | Evitar `canal estrecho con compromiso del canal`; es gate de calidad, no primer hard. |
| `historia_minima_fuente_trazable_v1` | `report_only` | Diagnostico, indicacion y antecedentes relevantes deben tener fuente estructurada o quedar como no informado. |
| `privacy_minimization_export_gate_v1` | `needs_more_evidence` | Bloquear identificadores en export/handoff cuando el batch de privacidad este revisado. |

## lumbar_specific_regression_cases

| Caso | Tipo | Debe fallar | Debe pasar |
|---|---|---|---|
| `LUM-HARD-001_extraforaminal_l45_der` | Parte/HC | `interlaminar`, `flavectomia`, `hombro de raiz`, `raiz L5 derecha`. | `extraforaminal`, `L4-L5`, `derecha`, `raiz L4 derecha`. |
| `LUM-HARD-002_sin_descompresion_directa` | Parte | Laminectomia, hemilaminectomia, flavectomia, recalibraje o liberacion directa afirmadas. | Negaciones claras: `no se realizo laminectomia`. |
| `LUM-HARD-003_orden_quirurgico` | Parte | Cierre/sutura/piel antes de hemostasia o recuento. | Hemostasia -> recuento -> cierre en seccion tecnica. |
| `LUM-REPORT-004_consentimiento_l45` | Consentimiento | Consentimiento generico o artrodesis L4-L5 lateralizada. | Procedimiento/nivel/riesgos/alternativas y lateralidad solo en abordaje si fue informada. |
| `LUM-REPORT-005_plif_materiales` | Parte | PLIF/TLIF duplicado o materiales reintroducidos sin input. | Titulo excluido, cuerpo narrativo con una mencion logica. |

## jurisprudence_to_template_impact

La jurisprudencia debe impactar en metadata, warnings y criterios de completitud, no en citas dentro del documento clinico. El flujo correcto es:

```text
fuente oficial -> corpus_item revisado -> gate_item con limite -> fixture sintetico -> validator/report_only -> hard fail si aplica
```

Impactos seguros:

| Tema | Impacto de plantilla/gate | Limite |
|---|---|---|
| Consentimiento informado | Exigir especificidad y evitar frases genericas. | No citar fallo ni articulo sin revision. |
| Historia clinica | Campos minimos, trazabilidad de cambios, coherencia temporal. | No convertir cada omision en mala praxis automatica. |
| Parte quirurgico | Tecnica, hallazgos, materiales, complicaciones, cierre y firma/estado. | Validar primero baseline real para evitar falsos positivos. |
| Datos personales | Minimizar identificadores en export/handoff. | Separar del batch lumbar tecnico. |
| Jurisprudencia provincial/nacional | `needs_review` con jurisdiccion, fecha, hecho y criterio. | No universalizar fallos. |

## tests_to_add

| id | Documento | Fixture sintetico | Resultado esperado |
|---|---|---|---|
| `CORPUS-BAD-001` | gate registry | `gate_item` legal sin `source_status=official` o sin `approved_for_gate`. | No puede ser hard fail. |
| `CONSENT-GOOD-001` | consentimiento | Fijacion/artrodesis L4-L5 con riesgos especificos y alternativas; abordaje derecho separado. | Pass/report_only sin lateralizar fusion. |
| `CONSENT-BAD-001` | consentimiento | `Consentimiento para cirugia lumbar con riesgos generales`, sin nivel/procedimiento. | Warning/fail report_only `consentimiento_especifico_columna_v1`. |
| `PARTE-BAD-001` | parte | Cierre de piel antes de recuento/hemostasia. | Hard fail `orden_hemostasia_recuento_cierre`. |
| `PARTE-BAD-002` | parte | Evento dural con parche despues del cierre. | Hard fail limitado si `dural_patch=yes`. |
| `HC-BAD-001` | historia | Diagnostico `espondilolistesis degenerativa con indicacion de fijacion`. | Report/fail `diagnostico_puro_sin_indicacion`. |
| `PRIV-BAD-001` | export/handoff | Texto con DNI, numero de HC o identificadores en salida no clinica. | Block/report segun batch privacidad aprobado. |
| `JURIS-BAD-001` | corpus | Fallo sin jurisdiccion, tribunal, fecha o hecho relevante. | No se convierte en gate activo. |

## do_not_integrate_without_review

- Articulos, citas, fallos, doctrina o frases legales no verificados.
- Jurisprudencia como hard gate universal.
- Consentimiento legal hard fail si el `corpus_item` todavia esta `needs_review`.
- Resumen SAIJ como fuente primaria.
- Texto legal largo dentro de HC/consentimiento/parte.
- Gates que reescriban automaticamente documentos clinicos sin mostrar spans y razon.
- Cualquier fixture con datos de pacientes o identificadores.

## implementation_order

1. Agregar/confirmar campos minimos de `corpus_item`: `source_type`, `source_status`, `jurisdiction`, `date`, `topic`, `criterion`, `derived_gate`, `review_status`, `requires_legal_review`, `evidence_path`.
2. Agregar politica de activacion: ningun gate derivado de corpus bloquea si no esta `approved_for_gate`.
3. Mantener hard fail clinico chico: `no_inventar_diagnostico_topografia`, `extraforaminal_no_interlaminar`, `extraforaminal_root_table` limitado, `sin_descompresion_directa_bloqueante`, `orden_hemostasia_recuento_cierre` limitado.
4. Correr consentimiento, parte minimo, privacidad, PLIF/materiales y jurisprudencia en `report_only`.
5. Agregar tests `CORPUS-BAD-001`, `CONSENT-*`, `PARTE-*`, `HC-BAD-001`, `JURIS-BAD-001`.
6. Guardar en cada failure: `gate_id`, `source_item_id`, `review_status`, `matched_text`, `context`, `section`, `severity`, `mode`.
7. Revisar falsos positivos con salidas reales antes de promover cualquier gate no critico.

## risks_limits

- No se navego web ni se verifico vigencia legal externa en este job.
- El paquete usa resultados previos del bridge; la revision juridica/medica final queda para el orquestador y el Doctor.
- Los ejemplos son sinteticos y no deben confundirse con documentos de pacientes.
- La app real no fue inspeccionada ni modificada desde Pablo.
- Los gates normativos pueden orientar validacion, pero no reemplazan criterio medico/legal.

## recommendation

Implementar primero el `gate_activation_policy` para impedir que cualquier fuente normativa o jurisprudencial pendiente se vuelva hard fail. En paralelo, conservar como hard fail solo el lote clinico critico ya estable y pasar consentimiento/documentacion minima/privacidad/jurisprudencia a `report_only` con spans y evidencia.

## confidence

Alta para el orden de implementacion y para separar hard gates clinicos de corpus medico-legal pendiente. Media para los gates de consentimiento, privacidad y parte minimo hasta que el orquestador los ejecute contra baseline real y corpus revisado.

## evidence_paths

- `jobs/20260526T001920-clinica-corpus-gates-hardening-v3.md`
- `results/20260525T170711-clinica-corpus-official-gates-next-integration-v1.result.md`
- `results/20260525T224750-clinica-v2-gates-next-hardening-audit-v1.result.md`
- `results/20260525T221902-clinica-lumbar-regression-pack-from-prior-results-v1.result.md`
- `results/20260525T184100-clinica-lumbar-v2-stress-artifacts-v1.result.md`
- `results/20260525T181000-clinica-lumbar-validator-detect-only-spec-v1.result.md`
- `results/20260525T153318-clinica-lumbar-inconsistency-gates-v2.result.md`
- `results/20260525T013125-corpus-jurisprudencia-leyes-gates-app-clinica.result.md`
- `results/20260525T021012-corpus-official-jurisprudence-candidate-queue-v2.result.md`
- `protocol.md`
