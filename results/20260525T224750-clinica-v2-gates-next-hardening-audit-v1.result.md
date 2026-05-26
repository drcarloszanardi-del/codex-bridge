---
id: 20260525T224750-clinica-v2-gates-next-hardening-audit-v1
job_id: 20260525T224750-clinica-v2-gates-next-hardening-audit-v1
created_at: 2026-05-25T22:51:26-03:00
created_by: personal-xh
worker: personal-xh
status: completed
no_external_actions: true
no_secrets: true
---

# Resultado - CLINICA v2 gates next hardening audit

## summary

Segunda pasada XH sobre el pack `lumbar_inconsistency_gates_v2` ya validado por el orquestador. La base esta bien encaminada: los gates critical de topografia inventada, extraforaminal, raiz L4, descompresion directa negada y orden hemostasia/recuento/cierre son los primeros candidatos a hard fail.

La recomendacion es no promover todo junto. Promover solo gates con controles buenos/malos robustos, dejar consentimiento especifico, duplicados/materiales y preparacion inicial en `report_only`, y agregar controles que ataquen falsos positivos por negacion, headings, resumenes y lateralidad de abordaje.

## source_counts

| Fuente permitida | Estado | Uso |
|---|---:|---|
| `results/20260525T221902-clinica-lumbar-regression-pack-from-prior-results-v1.result.md` | Revisada | Pack portable, reglas canonicas y cinco casos principales. |
| `results/20260525T181000-clinica-lumbar-validator-detect-only-spec-v1.result.md` | Revisada | Contrato, negaciones, orden, duplicados y false positive risks. |
| `results/20260525T184100-clinica-lumbar-v2-stress-artifacts-v1.result.md` | Revisada | Buenos/malos sinteticos, readiness score y traps. |
| `results/20260525T153318-clinica-lumbar-inconsistency-gates-v2.result.md` | Revisada | 16 fixtures, gate rules y forbidden phrases. |
| `results/20260525T170711-clinica-corpus-official-gates-next-integration-v1.result.md` | Revisada | Priorizacion P0 y cautela con corpus normativo. |
| `context/fronts/clinica.md` y `protocol.md` | Revisadas | Canon CLINICA y reglas del bridge. |

## already_covered

| Area | Cobertura actual | Estado |
|---|---|---|
| Extraforaminal L4-L5 derecha | Bloquea interlaminar, flavectomia, hombro de raiz y raiz L5; exige raiz L4 en fixture aprobado. | Fuerte. |
| No inventar topografia | Bloquea posterolateral, extraforaminal, fragmento o secuestro cuando no estan en input. | Fuerte si negacion pasa. |
| Sin descompresion directa | Bloquea laminectomia, hemilaminectomia, flavectomia, recalibraje y liberacion directa afirmadas. | Fuerte. |
| Orden quirurgico | Evalua hemostasia y recuento antes de cierre, y parche antes de cierre si existe. | Fuerte si se limita a seccion tecnica. |
| Segmento de fusion sin lateralidad | Bloquea `fijacion/artrodesis L4-L5 derecha`; permite lateralidad de abordaje. | Bueno, requiere mas controles buenos. |
| Diagnostico puro | Separa diagnostico de indicacion o conducta. | Bueno. |
| Consentimiento especifico | Requiere nivel, procedimiento, riesgos y alternativas. | Mantener report_only. |
| PLIF/materiales/duplicados | Cuenta tecnica y materiales evitando headings. | Mantener report_only. |

## residual_false_negative_risks

| Riesgo | Ejemplo sintetico malo que podria escapar | Control recomendado |
|---|---|---|
| Sinonimos no normalizados de descompresion | `se reseca ligamento amarillo`, `se amplia receso lateral`, `foraminotomia directa` en caso sin descompresion. | Ampliar diccionario `descompresion_directa` y agregar BAD especifico. |
| Orden quirurgico camuflado | `Luego de suturar piel se constata recuento correcto` sin palabra `cierre`. | Agregar sinonimos de cierre: sutura, piel, planos, agrafes. |
| PLIF/TLIF con puntuacion | `P.L.I.F.` o `T.L.I.F.` no detectados. | Normalizar abreviaturas con puntos antes de conteo. |
| Topografia inventada indirecta | `foraminal externa`, `lateral extremo`, `extracanalar` como pseudo extraforaminal. | Primero warning con spans, luego diccionario revisado. |
| Raiz incorrecta por frase larga | `se libera L5` lejos de `extraforaminal L4-L5`. | Buscar raiz en ventana de tecnica y hallazgos, no solo junto al diagnostico. |
| Evento dural inventado por sinonimo | `sellado dural`, `sustituto dural`, `refuerzo de duramadre`. | Unificar sinonimos durales. |

## residual_false_positive_risks

| Riesgo | Ejemplo sintetico bueno que no debe fallar | Mitigacion |
|---|---|---|
| Negacion fuerte | `No se realizo laminectomia ni flavectomia.` | Negation window y verbo afirmativo cercano. |
| Afirmacion historica no realizada | `Se discutio laminectomia, pero no se realizo.` | Distinguir plan/discusion de acto realizado. |
| Heading repetido | Titulo `PLIF L4-L5` y cuerpo `se realiza PLIF L4-L5`. | Excluir headings y contar cuerpo narrativo. |
| Resumen posterior | Tecnica correcta, luego `resumen: hemostasia, recuento y cierre`. | Evaluar solo seccion tecnica principal. |
| Lateralidad de abordaje | `abordaje derecho para artrodesis L4-L5`. | Fallar solo lateralidad pegada al segmento fusionado. |
| Consentimiento con sinonimos | `opciones no quirurgicas` en vez de `alternativas`. | Report_only hasta mapear sinonimos reales. |
| Parche negado | `No se utilizo parche dural.` | Negacion debe bloquear failure de parche. |

## good_control_texts_needed

| id sugerido | Gate protegido | Texto sintetico bueno minimo | Resultado esperado |
|---|---|---|---|
| `GOOD-HARD-001` | `sin_descompresion_directa_bloqueante` | `Parte: fijacion y artrodesis L4-L5. Se discutio laminectomia, pero no se realizo laminectomia, flavectomia ni liberacion directa.` | Pass. |
| `GOOD-HARD-002` | `extraforaminal_no_interlaminar` | `Parte: hernia extraforaminal L4-L5 derecha. Abordaje extraforaminal derecho a raiz L4 derecha, sin abordaje interlaminar.` | Pass. |
| `GOOD-HARD-003` | `orden_hemostasia_recuento_cierre` | `Tecnica: hemostasia completa. Recuento correcto. Cierre por planos y piel. Resumen: cierre sin incidentes.` | Pass. |
| `GOOD-HARD-004` | `segmento_fusion_sin_lateralidad` | `Consentimiento: artrodesis L4-L5 por abordaje derecho. El segmento fusionado es L4-L5.` | Pass. |
| `GOOD-REPORT-001` | `tecnica_implantes_no_duplicados` | `Titulo: PLIF L4-L5. Cuerpo: se realiza PLIF L4-L5 con dos cajas y sustituto oseo.` | Pass en report_only. |
| `GOOD-REPORT-002` | `no_inventar_parche_dural` | `No se utilizo parche dural ni refuerzo dural.` | Pass. |

## bad_control_texts_needed

| id sugerido | Gate atacado | Texto sintetico malo minimo | Resultado esperado |
|---|---|---|---|
| `BAD-HARD-001` | `sin_descompresion_directa_bloqueante` | `Parte: sin descompresion directa planificada. Se realiza reseccion de ligamento amarillo y foraminotomia directa.` | Fail. |
| `BAD-HARD-002` | `extraforaminal_root_table` | `Hernia extraforaminal L4-L5 derecha. Se libera raiz L5 derecha como raiz principal.` | Fail. |
| `BAD-HARD-003` | `orden_hemostasia_recuento_cierre` | `Se sutura piel. Luego se constata recuento instrumental y hemostasia.` | Fail. |
| `BAD-HARD-004` | `no_inventar_diagnostico_topografia` | `Input sin topografia. Salida: hernia extracanalar/extraforaminal con secuestro.` | Fail o warning si `extracanalar` aun no esta aprobado. |
| `BAD-REPORT-001` | `tecnica_implantes_no_duplicados` | `P.L.I.F. L4-L5 con cajas. Luego se completa PLIF y se agrega T.L.I.F. sin plan combinado.` | Fail report_only. |
| `BAD-REPORT-002` | `consentimiento_especifico_columna_v1` | `Consentimiento para cirugia lumbar con riesgos generales, sin nivel ni procedimiento.` | Warning/report_only. |

## promotion_readiness

| Gate | Estado | Motivo |
|---|---|---|
| `no_inventar_diagnostico_topografia` | `hard_fail_ready` | Critical, bajo falso positivo si respeta negaciones y no falla frases `no se informa`. |
| `extraforaminal_no_interlaminar` | `hard_fail_ready` | Critical y scope claro a extraforaminal documentada. |
| `extraforaminal_root_table` | `hard_fail_ready` limitado | Promover solo para niveles aprobados por fixture: L3-L4, L4-L5, L5-S1. |
| `sin_descompresion_directa_bloqueante` | `hard_fail_ready` | Critical, con controles de negacion y afirmacion posterior. |
| `orden_hemostasia_recuento_cierre` | `hard_fail_ready` limitado | Promover si opera sobre seccion tecnica, no resumen ni checklist. |
| `parche_dural_pre_cierre` | `hard_fail_ready` limitado | Promover solo si `dural_patch=yes`; si no hay evidencia, usar gate separado. |
| `no_inventar_parche_dural` | `report_only` | Requiere mas sinonimos y negaciones antes de bloquear. |
| `diagnostico_puro_sin_indicacion` | `report_only` inicialmente | High, pero puede colisionar con labels o campos mal segmentados. |
| `preservar_subtipo_espondilolistesis` | `report_only` inicialmente | Bueno, pero requiere input estructurado de subtipo. |
| `segmento_fusion_sin_lateralidad` | `report_only` inicialmente | Promover tras buenos de lateralidad de abordaje. |
| `canal_estrecho_no_tautologico` | `report_only` | Calidad/redaccion; no bloquear produccion todavia. |
| `tecnica_implantes_no_duplicados` | `report_only` | Alto riesgo por headings, listas, resumen y materiales repetidos legitimamente. |
| `tecnica_incompatible` | `needs_more_evidence` | Puede ser hard luego, pero necesita control de `combined_plan=true`. |
| `no_duplicar_preparacion_inicial` | `needs_more_evidence` | Calidad, susceptible a checklist interno. |
| `consentimiento_especifico_columna_v1` | `needs_more_evidence` | No promover hasta corpus oficial revisado y sinonimos reales. |
| `privacy_minimization_export_gate_v1` | `needs_more_evidence` | No forma parte del pack lumbar tecnico; tratar en batch separado. |

## next_orchestrator_actions

1. Agregar primero los seis controles `GOOD-HARD-*` y `BAD-HARD-*` arriba, sin tocar plantillas.
2. Separar runner en tres modos: `hard_fail_candidate`, `report_only`, `needs_more_evidence`.
3. Para cada failure guardar `gate_id`, `matched_text`, `context`, `section`, `is_negated` y `source_fixture_id`.
4. Promover a hard fail solo: `no_inventar_diagnostico_topografia`, `extraforaminal_no_interlaminar`, `extraforaminal_root_table` limitado, `sin_descompresion_directa_bloqueante`, `orden_hemostasia_recuento_cierre` limitado.
5. Mantener `consentimiento_especifico_columna_v1`, `tecnica_implantes_no_duplicados`, `tecnica_incompatible`, `no_duplicar_preparacion_inicial` y `canal_estrecho_no_tautologico` en report_only hasta ver salidas reales.
6. Ejecutar QA en orden: validator lumbar, controles buenos/malos, core QA, route guard.
7. Recién despues de cero falsos positivos en buenos, ajustar prompts o plantillas con commit separado.

## risks/limits

- No se inspecciono la app real ni sus archivos locales; este analisis parte solo de resultados previos permitidos.
- Los textos buenos/malos propuestos son sinteticos y no representan documentos clinicos finales.
- La promocion a hard fail debe depender de salidas reales del runner en la Mac de trabajo.
- Consentimiento, duplicados/materiales y preparacion inicial siguen con riesgo de falso positivo por sinonimos, headings, listas y corpus no revisado.
- Ningun gate debe reescribir contenido automaticamente: primero detectar, reportar spans y dejar decision al orquestador.

## recommendation

Promover solo un lote chico de hard fail: `no_inventar_diagnostico_topografia`, `extraforaminal_no_interlaminar`, `extraforaminal_root_table` limitado, `sin_descompresion_directa_bloqueante` y `orden_hemostasia_recuento_cierre` limitado a seccion tecnica. Todo lo demas debe correr `report_only` hasta sumar controles buenos/malos y evidencia del generador real.

## confidence

Alta para priorizar los gates critical y para los controles de negacion, extraforaminal y orden quirurgico. Media para lateralidad de fusion, PLIF/materiales y consentimiento, porque esos gates dependen mucho de secciones, headings, sinonimos y corpus revisado.

## evidence_paths

- `jobs/20260525T224750-clinica-v2-gates-next-hardening-audit-v1.md`
- `results/20260525T221902-clinica-lumbar-regression-pack-from-prior-results-v1.result.md`
- `results/20260525T181000-clinica-lumbar-validator-detect-only-spec-v1.result.md`
- `results/20260525T184100-clinica-lumbar-v2-stress-artifacts-v1.result.md`
- `results/20260525T153318-clinica-lumbar-inconsistency-gates-v2.result.md`
- `results/20260525T170711-clinica-corpus-official-gates-next-integration-v1.result.md`
- `context/fronts/clinica.md`
- `protocol.md`
