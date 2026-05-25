---
id: 20260525T170711-clinica-corpus-official-gates-next-integration-v1
job_id: 20260525T170711-clinica-corpus-official-gates-next-integration-v1
created_at: 2026-05-25T17:10:37-03:00
created_by: personal-xh
worker: personal-xh
status: completed
no_external_actions: true
no_secrets: true
---

# Resultado - CLINICA corpus oficial y gates críticos next integration v1

Job: `20260525T170711-clinica-corpus-official-gates-next-integration-v1`
Worker: `personal-xh` / Pablo
Fecha: `2026-05-25`

## summary

El próximo lote mínimo debe combinar dos líneas, sin mezclarlas: gates clínicos críticos ya derivados de correcciones del Doctor, y estructura de corpus oficial para que la app solo active reglas desde fuentes revisadas. La prioridad no es sumar jurisprudencia; es impedir documentos con hechos inventados, consentimiento genérico, diagnóstico contaminado con indicación, técnica quirúrgica incompatible y fallas de privacidad.

No se modificó la app real ni se usaron datos de pacientes. La recomendación es que Codex principal implemente primero un pack pequeño, verificable y bloqueante, con fixtures que fallen antes de tocar plantillas.

## source_counts

| Fuente | Archivos revisados | Uso |
|---|---:|---|
| `context/fronts/clinica.md` | 1 | Canon de app clínica, ruta real y regla de seguridad. |
| `results/20260525T013125-corpus-jurisprudencia-leyes-gates-app-clinica.result.md` | 1 | Taxonomía corpus -> gate y riesgos de alucinación. |
| `results/20260525T015134-corpus-medico-legal-schema-y-seed-oficial.result.md` | 1 | Schema `corpus_item`/`gate_item` y seed oficial inicial. |
| `results/20260525T021012-corpus-official-jurisprudence-candidate-queue-v2.result.md` | 1 | Cola de fuentes oficiales y reglas de uso. |
| `results/20260525T124545-clinica-corpus-gates-backlog-v2.result.md` | 1 | Backlog P0/P1 y separación hard gate vs needs_review. |
| `results/20260525T153318-clinica-lumbar-inconsistency-gates-v2.result.md` | 1 | Gates lumbares críticos, fixture matrix y plan de integración. |
| `decisions/corpus_official_candidate_queue_20260525.md` | 1 | Lista operativa de candidatos official_norm / judiciary / SAIJ. |

## coverage_table

| Frente | Estado | Decisión |
|---|---|---|
| Gates lumbares críticos | listos para integración mínima | Implementar primero por fixture y detector puro. |
| Corpus oficial | listo como cola/schema, no como texto clínico | Migrar `corpus_item` y activar solo `gate_item` revisados. |
| Jurisprudencia | no hard gate inicial | Usar como `needs_review` hasta metadata completa y revisión legal. |
| Plantillas clínicas | no tocar aún | Primero tests/gates; después ajustar generación. |
| Datos pacientes | excluidos | Solo fixtures sintéticos. |

## fuente_oficial_inferencia_recomendacion

| Tipo | Ejemplos | Uso permitido |
|---|---|---|
| Fuente oficial | Ley 26.529, Decreto 1089/2012, Ley 25.326, Ley 17.132, Ley PBA 14.494, JUBA/CIJ/Río Negro con texto oficial. | Alimentar `corpus_item` y, tras revisión, `gate_item`. |
| Inferencia operativa | "consentimiento debe incluir nivel/procedimiento/riesgos/alternativas"; "documento no debe inventar topografía". | Implementar como gate/fixture, no como cita legal en documento final. |
| Recomendación | Orden de integración, severidades, archivos a inspeccionar, batch mínimo. | Guía para Codex principal; no reemplaza revisión médica/legal. |

## top_10_integrations_ranked

| Rank | Integración | Tipo | Motivo | Primera verificación |
|---:|---|---|---|---|
| 1 | `no_inventar_diagnostico_topografia` | gate clínico crítico | Evita hechos clínicos no informados. | Fixture radiculopatía sin hernia no puede generar hernia/fragmento. |
| 2 | `sin_descompresion_directa_bloqueante` | gate quirúrgico crítico | Evita registrar laminectomía/flavectomía no realizadas. | Caso `sin descompresión directa` falla si aparece laminectomía. |
| 3 | `extraforaminal_no_interlaminar` + raíz aprobada | gate quirúrgico crítico | Corrige error anatómico/técnico de alto impacto. | L4-L5 extraforaminal derecha exige lógica foraminal/extraforaminal y raíz L4. |
| 4 | `diagnostico_puro_sin_indicacion` | gate documental high | Separa diagnóstico de conducta terapéutica. | Campo diagnóstico falla con `con indicación de`. |
| 5 | `segmento_fusion_sin_lateralidad` | gate consentimiento/parte high | Artrodesis/fijación es por nivel, no "derecha". | Consentimiento L4-L5 falla con `artrodesis L4-L5 derecha`. |
| 6 | `orden_hemostasia_recuento_cierre` | gate parte quirúrgico crítico | Evita secuencia quirúrgica ilógica. | Cierre antes de hemostasia/recuento falla. |
| 7 | `parche_dural_pre_cierre` + `no_inventar_parche_dural` | gate parte quirúrgico crítico | Evita inventar material/evento o ubicarlo tras cierre. | Parche sin input o posterior al cierre falla. |
| 8 | `consentimiento_especifico_columna_v1` | gate corpus oficial P0 | Bloquea consentimiento genérico. | Debe requerir procedimiento, nivel, riesgos principales y alternativas. |
| 9 | `documento_minimo_parte_quirurgico_v1` | gate corpus oficial P0 | Asegura estructura mínima de parte/HC. | Debe requerir fecha, profesional, diagnóstico, indicación, técnica, hallazgos, complicaciones/cierre/firma según baseline. |
| 10 | `privacy_minimization_export_gate_v1` | gate corpus oficial P0 | Evita datos sensibles en canales o export. | Handoff/export falla con pacientes, DNI, HC o estudios identificables. |

## critical_gates_first

Primer batch P0 recomendado:

```yaml
batch_p0_lumbar_and_documentation:
  - id: no_inventar_diagnostico_topografia
    severity: critical
    source: correccion_doctor_fixture
    scope: historia_clinica consent parte
  - id: sin_descompresion_directa_bloqueante
    severity: critical
    source: correccion_doctor_fixture
    scope: parte_quirurgico
  - id: extraforaminal_no_interlaminar
    severity: critical
    source: correccion_doctor_fixture
    scope: parte_quirurgico historia_clinica
  - id: orden_hemostasia_recuento_cierre
    severity: critical
    source: correccion_doctor_fixture
    scope: parte_quirurgico
  - id: consentimiento_especifico_columna_v1
    severity: critical
    source: official_norm_pending_review
    scope: consentimiento
  - id: privacy_minimization_export_gate_v1
    severity: critical
    source: official_norm_pending_review
    scope: handoff export prompt
```

Regla de activación: los cuatro gates clínicos pueden nacer de fixtures sintéticos del Doctor; los dos gates normativos deben tener `corpus_item` revisado antes de bloquear producción. Mientras tanto pueden correr en modo `warning/needs_review`.

## official_corpus_queue

| Prioridad | Fuente | Estado sugerido | Gate derivado | Acción |
|---|---|---|---|---|
| P0 | Ley 26.529 Derechos del Paciente | `official_norm -> needs_review -> approved_for_gate` | consentimiento específico, historia clínica completa | Crear `corpus_item` y revisar artículo/impacto antes de hard gate. |
| P0 | Decreto 1089/2012 | `official_norm -> needs_review` | detalle reglamentario CI/HC | Vincular como complemento de Ley 26.529. |
| P0 | Ley 25.326 Datos Personales | `official_norm -> needs_review` | privacidad/minimización en export/handoff | Gate de no exposición de datos sensibles. |
| P0 | Ley 17.132 Ejercicio medicina | `official_norm -> seed` | identificación profesional / responsabilidad documental | Mantener como soporte, no sobrelegalizar texto. |
| P0 | Ley PBA 14.494 + Decreto 1600/2024 | `official_norm -> seed` | HCE/trazabilidad local PBA | Gate administrativo si la app maneja HCE/export. |
| P1 | CCyC Ley 26.994 | `official_norm -> needs_review` | responsabilidad profesional/dano | No hard gate clínico inicial; usar como metadata. |
| P1 | JUBA idFallo 161074 | `official_judiciary_full_text -> review_queue` | CI como deber autónomo | Alerta `needs_review`, no regla universal. |
| P1 | JUBA idFallo 192025 | `official_judiciary_full_text -> review_queue` | HC con tiempos/controles/material | Alerta sobre completitud, con límite del caso. |
| P1 | CIJ sentencia SGU PDF | `official_judiciary_pdf -> copy_needed` | CI/riesgos posoperatorios | Requiere extracción segura antes de usar. |
| P2 | SAIJ dossier mala praxis | `official_saij_summary -> review_queue` | tamiz interno | No hard gate sin texto/fuente primaria aplicable. |

## app_files_to_inspect_by_orchestrator

En la app canónica `/Users/jarvis/.openclaw/workspace/clinica/app-clinica-medicolegal`, Codex principal debería inspeccionar primero:

```text
app/app.js
app/app.data.js
app/product.html
scripts/jarvis/clinical_document_handoff.js
scripts/qa/run_clinica_core_qa.js
scripts/qa/validate_20_pathology_scenarios.js
scripts/qa/validate_40_pathology_family_matrix.js
scripts/qa/validate_clinica_route_guard.js
scripts/qa/validate_clinical_inconsistency_audit.js
data/derived/clinical_test_cases/
data/corpus/
data/processed/legal_corpus/
```

Orden: localizar pipeline de generación/guardado, ubicar QA runner, agregar fixtures, agregar helpers puros, conectar gates, recién después tocar plantillas o prompts.

## fixture_pack_recommendation

Crear `data/derived/clinical_test_cases/lumbar_inconsistency_gates_v2.json` con 16 casos mínimos:

```yaml
fixtures:
  - LUM-GATE-001_extraforaminal_l45_der_no_interlaminar_root_l4
  - LUM-GATE-002_no_inventar_topografia_si_no_declarada
  - LUM-GATE-003_radiculopatia_sin_hernia_no_inventa_hernia
  - LUM-GATE-004_espondilolistesis_degenerativa_no_istmica
  - LUM-GATE-005_canal_estrecho_no_tautologico
  - LUM-GATE-006_diagnostico_puro_sin_indicacion
  - LUM-GATE-007_fijacion_artrodesis_l45_sin_lateralidad_segmento
  - LUM-GATE-008_sin_descompresion_directa_bloquea_laminectomia_flavectomia
  - LUM-GATE-009_con_descompresion_directa_respeta_input
  - LUM-GATE-010_plif_implantes_no_duplicados
  - LUM-GATE-011_parche_dural_pre_cierre
  - LUM-GATE-012_hemostasia_recuento_antes_de_cierre
  - LUM-GATE-013_no_duplicar_preparacion_inicial
  - LUM-GATE-014_topografia_foraminal_no_extraforaminal_si_no_se_dijo
  - LUM-GATE-015_plif_tlif_incompatible_sin_plan_combinado
  - LUM-GATE-016_consentimiento_hernia_lumbar_especifico
```

Cada fixture debe tener `input_axes`, `expected_present`, `forbidden_present`, `source_type`, `severity`, `gate_ids`, `doctor_correction_source` y `expected_message`.

## verification_plan

1. Crear fixtures y validator sin modificar generación.
2. Ejecutar validator contra textos sintéticos malos y verificar que falla.
3. Conectar al generador real en modo `report_only`.
4. Activar hard fail solo para gates con baja tasa de falso positivo.
5. Para corpus oficial, cargar `corpus_item` primero y exigir `source_status=official`, `review_status=approved_for_gate` antes de activar `gate_item`.
6. Correr QA focal:

```bash
node scripts/qa/validate_lumbar_inconsistency_gates_v2.js
node scripts/qa/run_clinica_core_qa.js
node scripts/qa/validate_clinica_route_guard.js
```

7. Revisar resultados con casos buenos y malos.
8. Documentar falsos positivos y ajustar negaciones/contexto.
9. Commit por capas: fixtures, helpers, gates, runner, plantilla/generador.
10. No liberar si falla cualquier `critical`.

## risks_limits

- No se verificó vigencia legal externa en este worker; las fuentes oficiales están listadas desde resultados previos y requieren revisión en work-mac.
- Jurisprudencia no debe transformarse en hard gate universal sin limitar hecho, tribunal, fecha y criterio.
- Regex literales pueden bloquear frases negadas; usar detección contextual.
- Un gate demasiado legalista puede empeorar el flujo clínico; la salida final no debe incluir citas legales ni lenguaje de abogado.
- La app real puede tener rutas diferentes; Codex principal debe inspeccionar baseline antes de editar.

## recommendation

Implementar primero el batch P0 de fixtures/gates clínicos y, en paralelo, crear el schema `corpus_item/gate_item` con seed oficial. No activar jurisprudencia como hard gate todavía. La primera victoria concreta debe ser que la app no pueda producir: hernia inventada, técnica extraforaminal mal abordada, descompresión directa negada pero documentada, diagnóstico con indicación mezclada, lateralidad incorrecta en artrodesis/fijación, ni cierre antes de hemostasia/recuento.

## confidence

Alta para priorización clínica y orden de implementación, porque deriva de correcciones directas y resultados previos del bridge. Media para activación legal exacta hasta revisión oficial/legal en la Mac de trabajo.

## evidence_paths

- `jobs/20260525T170711-clinica-corpus-official-gates-next-integration-v1.md`
- `context/fronts/clinica.md`
- `results/20260525T013125-corpus-jurisprudencia-leyes-gates-app-clinica.result.md`
- `results/20260525T015134-corpus-medico-legal-schema-y-seed-oficial.result.md`
- `results/20260525T021012-corpus-official-jurisprudence-candidate-queue-v2.result.md`
- `results/20260525T124545-clinica-corpus-gates-backlog-v2.result.md`
- `results/20260525T153318-clinica-lumbar-inconsistency-gates-v2.result.md`
- `decisions/corpus_official_candidate_queue_20260525.md`
