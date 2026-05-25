---
id: 20260525T184100-clinica-lumbar-v2-stress-artifacts-v1
job_id: 20260525T184100-clinica-lumbar-v2-stress-artifacts-v1
created_at: 2026-05-25T18:45:08-03:00
created_by: personal-xh
worker: personal-xh
status: completed
no_external_actions: true
no_secrets: true
---

# Resultado - CLINICA lumbar v2 stress artifacts v1

## summary

Segunda capa de estres para el validator lumbar v2: textos sinteticos buenos y malos mas realistas para medir falsos positivos y falsos negativos. No hay pacientes, no hay datos reales y no se modifica la app real.

La recomendacion es correr estos artifacts en `report_only` primero y promover a hard fail solo los gates critical con comportamiento estable: no inventar topografia, no describir descompresion directa negada, extraforaminal no interlaminar, parche antes de cierre y hemostasia/recuento antes de cierre.

## coverage_table

| Fuente permitida | Estado | Uso |
|---|---:|---|
| `results/20260525T181000-clinica-lumbar-validator-detect-only-spec-v1.result.md` | Revisada | Contrato, normalizacion, negaciones, orden y duplicados. |
| `results/20260525T173726-clinica-lumbar-fixture-pack-draft-v2.result.md` | Revisada | Fixtures LUM-GATE-001 a 016. |
| `results/20260525T153318-clinica-lumbar-inconsistency-gates-v2.result.md` | Revisada | Gates clinicos y matriz de errores graves. |
| `context/fronts/clinica.md` | Revisada | Regla de no tocar app real y convertir correcciones en gates. |

## stress_artifacts_good

Artifacts buenos: deben pasar o, si el gate esta en modo corpus/revision, producir solo `warning=none`.

| id | fixture_ref | texto sintetico bueno | gates esperados |
|---|---|---|---|
| `GOOD-LUM-001` | `LUM-GATE-001` | `Parte: hernia discal extraforaminal L4-L5 derecha. Se realiza abordaje extraforaminal derecho orientado a la raiz L4 derecha, sin descripcion de abordaje interlaminar.` | pass `extraforaminal_no_interlaminar`, pass `extraforaminal_root_table` |
| `GOOD-LUM-002` | `LUM-GATE-002` | `Historia clinica: hernia discal L4-L5 derecha. No se informa topografia foraminal, extraforaminal ni posterolateral en la documentacion recibida.` | pass `no_inventar_diagnostico_topografia` por negaciones |
| `GOOD-LUM-003` | `LUM-GATE-004` | `Diagnostico: espondilolistesis degenerativa L4-L5 con estenosis asociada. No se consignan datos de lisis ni pars.` | pass `preservar_subtipo_espondilolistesis` |
| `GOOD-LUM-004` | `LUM-GATE-007` | `Consentimiento: fijacion instrumentada y artrodesis L4-L5. Se aclara abordaje derecho para maniobras de acceso, sin lateralizar el segmento fusionado.` | pass `segmento_fusion_sin_lateralidad` |
| `GOOD-LUM-005` | `LUM-GATE-008` | `Parte: fijacion instrumentada y artrodesis L4-L5. No se realizo laminectomia, hemilaminectomia, flavectomia ni liberacion radicular directa.` | pass `sin_descompresion_directa_bloqueante` por negacion |
| `GOOD-LUM-006` | `LUM-GATE-010` | `Parte: se realiza PLIF L4-L5 con dos cajas intersomaticas y sustituto oseo. Luego se completa fijacion con tornillos y barras.` | pass duplicados/materiales |
| `GOOD-LUM-007` | `LUM-GATE-011` | `Parte: se coloca refuerzo dural sobre zona expuesta. Se verifica hemostasia, recuento correcto y luego cierre por planos y piel.` | pass `parche_dural_pre_cierre`, pass `orden_hemostasia_recuento_cierre` |
| `GOOD-LUM-008` | `LUM-GATE-013` | `Parte: paciente en decubito prono, proteccion ocular y acolchado de prominencias. Se realiza antisepsia y campo esteril. Al cierre se deja constancia de hemostasia y recuento.` | pass `no_duplicar_preparacion_inicial` |

## stress_artifacts_bad

Artifacts malos: deben fallar con los gates indicados.

| id | fixture_ref | texto sintetico malo | gates esperados |
|---|---|---|---|
| `BAD-LUM-001` | `LUM-GATE-001` | `Parte: hernia extraforaminal L4-L5 derecha. Se realiza abordaje interlaminar con flavectomia, liberando raiz L5 derecha.` | fail `extraforaminal_no_interlaminar`, fail `extraforaminal_root_table` |
| `BAD-LUM-002` | `LUM-GATE-002` | `Historia clinica: hernia L4-L5 derecha posterolateral/extraforaminal, aunque la imagen no especifica topografia.` | fail `no_inventar_diagnostico_topografia` |
| `BAD-LUM-003` | `LUM-GATE-003` | `Historia: radiculopatia L5 derecha por hernia discal extruida con secuestro, sin informe de imagen disponible.` | fail `no_inventar_diagnostico_topografia` |
| `BAD-LUM-004` | `LUM-GATE-004` | `Diagnostico: espondilolistesis degenerativa o istmica L4-L5, probable pars.` | fail `preservar_subtipo_espondilolistesis` |
| `BAD-LUM-005` | `LUM-GATE-006` | `Diagnostico: espondilolistesis degenerativa L4-L5 con indicacion de fijacion instrumentada.` | fail `diagnostico_puro_sin_indicacion` |
| `BAD-LUM-006` | `LUM-GATE-007` | `Consentimiento para fijacion L4-L5 derecha y artrodesis L4-L5 derecha.` | fail `segmento_fusion_sin_lateralidad` |
| `BAD-LUM-007` | `LUM-GATE-008` | `Parte: aunque el plan era sin descompresion directa, se realiza hemilaminectomia y flavectomia amplia.` | fail `sin_descompresion_directa_bloqueante` por afirmacion posterior |
| `BAD-LUM-008` | `LUM-GATE-010` | `Parte: PLIF L4-L5 con caja. Se completa PLIF L4-L5 y luego se describe TLIF L4-L5 sin plan combinado.` | fail `tecnica_implantes_no_duplicados`, fail `tecnica_incompatible` |
| `BAD-LUM-009` | `LUM-GATE-011` | `Parte: se realiza cierre por planos y piel. Posteriormente se coloca parche dural.` | fail `parche_dural_pre_cierre` |
| `BAD-LUM-010` | `LUM-GATE-012` | `Parte: cierre de piel. Luego se verifica hemostasia y recuento de gasas.` | fail `orden_hemostasia_recuento_cierre` |
| `BAD-LUM-011` | `LUM-GATE-013` | `Parte: decubito prono con proteccion ocular. Tras exposicion, nuevamente se coloca en decubito prono y se reitera proteccion ocular.` | fail `no_duplicar_preparacion_inicial` |
| `BAD-LUM-012` | `LUM-GATE-016` | `Consentimiento generico para cirugia lumbar, sin nivel, riesgos especificos ni alternativas.` | fail/report_only `consentimiento_especifico_columna_v1` |

## expected_gate_outcomes

| artifact | expected_ok | failures | mode |
|---|---:|---|---|
| `GOOD-LUM-001` a `GOOD-LUM-008` | true | none | hard/pass |
| `BAD-LUM-001` | false | `extraforaminal_no_interlaminar`, `extraforaminal_root_table` | hard |
| `BAD-LUM-002`, `BAD-LUM-003` | false | `no_inventar_diagnostico_topografia` | hard |
| `BAD-LUM-004` | false | `preservar_subtipo_espondilolistesis` | hard |
| `BAD-LUM-005` | false | `diagnostico_puro_sin_indicacion` | hard after low false positive |
| `BAD-LUM-006` | false | `segmento_fusion_sin_lateralidad` | hard after low false positive |
| `BAD-LUM-007` | false | `sin_descompresion_directa_bloqueante` | hard |
| `BAD-LUM-008` | false | `tecnica_implantes_no_duplicados`, `tecnica_incompatible` | report_only then hard |
| `BAD-LUM-009`, `BAD-LUM-010` | false | order gates | hard |
| `BAD-LUM-011` | false | `no_duplicar_preparacion_inicial` | report_only |
| `BAD-LUM-012` | false | `consentimiento_especifico_columna_v1` | report_only until corpus approved |

## false_positive_traps

| Trap | Texto | Resultado correcto |
|---|---|---|
| Negacion fuerte | `No se realizo laminectomia ni flavectomia.` | No fallar por tokens prohibidos. |
| Negacion de topografia | `No se informa hernia extraforaminal.` | No fallar por `extraforaminal`. |
| Titulo repetido | `PLIF L4-L5` como titulo y luego `se realiza PLIF L4-L5` una vez. | No contar como duplicado si se excluyen headings. |
| Checklist interno | `proteccion ocular` aparece en checklist no renderizado y texto final. | Validar solo texto final o excluir seccion interna. |
| Resumen posterior | `Resumen: se realizo hemostasia y cierre` despues del cierre narrativo correcto. | No usar resumen como secuencia quirurgica principal. |
| Lateralidad de abordaje | `abordaje derecho para artrodesis L4-L5` | No fallar; lateralidad no esta pegada al segmento fusionado. |

## false_negative_traps

| Trap | Texto | Mitigacion |
|---|---|---|
| Afirmacion despues de negacion | `Sin descompresion directa planificada. Se realiza hemilaminectomia.` | Verbo afirmativo cercano gana sobre negacion lejana. |
| Sinonimo material | `sustituto oseo` / `injerto oseo` duplicado | Normalizar sinonimos de material. |
| Orden invertido con frases largas | `Tras cierre de piel, y luego de completar curacion, se verifica recuento.` | Comparar posiciones y regex ventana amplia. |
| Topografia camuflada | `lateral foraminal externo` como pseudo-extraforaminal | Report_only si no esta en diccionario; ampliar vocabulario con revision. |
| PLIF/TLIF en abreviaturas con puntos | `P.L.I.F.` y `T.L.I.F.` | Normalizar abreviaturas con puntos. |
| Consentimiento generico con palabras sueltas | Dice `riesgos` y `alternativas` pero sin nivel/procedimiento. | Requerir campos minimos completos, no solo palabras. |

## recommended_artifact_mode_contract

```json
{
  "artifact_id": "BAD-LUM-001",
  "fixture_ref": "LUM-GATE-001",
  "mode": "bad_should_fail",
  "document_type": "parte_quirurgico",
  "text": "synthetic text only",
  "expected_failures": ["extraforaminal_no_interlaminar"],
  "expected_warnings": [],
  "hard_fail_eligible": true,
  "notes": "No patient data"
}
```

Modos:

| mode | Uso |
|---|---|
| `good_should_pass` | Control de falso positivo. |
| `bad_should_fail` | Control de falso negativo. |
| `ambiguous_report_only` | Caso util pero no apto para hard fail todavia. |

## hard_fail_readiness_score

| Gate | Score | Estado |
|---|---:|---|
| `no_inventar_diagnostico_topografia` | 9/10 | Hard fail listo si negaciones pasan. |
| `sin_descompresion_directa_bloqueante` | 9/10 | Hard fail listo si afirmacion posterior a negacion falla. |
| `extraforaminal_no_interlaminar` | 8/10 | Hard fail listo con scope a extraforaminal documentada. |
| `extraforaminal_root_table` | 7/10 | Hard fail solo para niveles aprobados. |
| `orden_hemostasia_recuento_cierre` | 8/10 | Hard fail si se limita a tecnica quirurgica. |
| `parche_dural_pre_cierre` | 8/10 | Hard fail si hay `dural_patch=yes`. |
| `segmento_fusion_sin_lateralidad` | 7/10 | Hard fail tras validar abordaje lateral permitido. |
| `tecnica_implantes_no_duplicados` | 6/10 | Report_only primero por riesgo de titulos/listas. |
| `no_duplicar_preparacion_inicial` | 5/10 | Report_only; es calidad, no riesgo critico. |
| `consentimiento_especifico_columna_v1` | 5/10 | Report_only hasta corpus aprobado. |

## next_actions_for_orchestrator

1. Crear archivo de stress artifacts sinteticos junto al fixture pack o dentro del test del validator.
2. Ejecutar todos los `GOOD-*` y exigir cero failures hard.
3. Ejecutar todos los `BAD-*` y exigir failures exactos.
4. Separar `report_only` de `hard_fail_eligible`.
5. Guardar spans/contexto de cada match para auditar falsos positivos.
6. Promover hard fail solo los gates con score 8/10 o superior.
7. Mantener corpus legal/consentimiento como warning hasta revision oficial.

## recommendation

La proxima accion concreta es agregar `GOOD-LUM-005`, `BAD-LUM-007`, `BAD-LUM-009` y `BAD-LUM-010` como smoke tests obligatorios: cubren negacion, afirmacion posterior, parche despues de cierre y cierre antes de recuento/hemostasia.

## risks_limits

- Stress artifacts son sinteticos y no reemplazan revision clinica humana.
- Un texto quirurgico real puede tener secciones resumen que confundan orden; validar solo seccion tecnica.
- El validator no debe reescribir documentos, solo reportar.
- No se inspecciono ni modifico app real.

## confidence

Alta para artifacts de negacion, orden y topografia. Media para duplicados/materiales y consentimiento hasta ver salidas reales del generador y corpus aprobado.

## evidence_paths

- `jobs/20260525T184100-clinica-lumbar-v2-stress-artifacts-v1.md`
- `results/20260525T181000-clinica-lumbar-validator-detect-only-spec-v1.result.md`
- `results/20260525T173726-clinica-lumbar-fixture-pack-draft-v2.result.md`
- `results/20260525T153318-clinica-lumbar-inconsistency-gates-v2.result.md`
- `context/fronts/clinica.md`
