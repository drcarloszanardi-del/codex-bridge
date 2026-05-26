# Resultado - 20260526T064839-clinica-corpus-gates-backlog-v2

## summary honesto

Este backlog convierte los resultados previos de corpus medico-legal y correcciones clinicas en gates verificables para historia clinica, consentimiento informado y parte quirurgico. La prioridad no es sumar texto legal, sino bloquear documentos incompletos, contradictorios o con hechos clinicos inventados.

**Evidencia:** los resultados previos ya definen taxonomia de fuentes, metadatos minimos, gates documentales y correcciones lumbares criticas.

**Inferencia:** conviene activar primero gates derivados de normativa/documentacion y protocolos internos del Doctor, porque son mas estables y testeables que jurisprudencia amplia.

**Opinion:** la jurisprudencia debe entrar como cola revisada y trazable; no como regla universal automatica hasta tener fuente oficial, estado vigente y revision legal/clinica.

## coverage_table

| Fuente | Cobertura usada | Limite |
| --- | --- | --- |
| `context/fronts/clinica.md` | Estado canonico: toda HC/CI/parte debe pasar por ruta canonica, manifiesto valido y QA medico-legal. | No contiene reglas detalladas por plantilla. |
| `results/20260525T013125-corpus-jurisprudencia-leyes-gates-app-clinica.result.md` | Taxonomia, metadatos, conversion de fuentes a gates y riesgos de alucinacion. | No verifica fuentes oficiales externas ni vigencia legal. |
| `results/20260525T122941-clinica-correcciones-a-fixtures-implementacion.result.md` | Orden de integracion: fixtures, helpers, gates deterministicos, QA runner; foco lumbar/extraforaminal. | No inspecciona la app real ni modifica plantillas. |

## gate_backlog

| Prioridad | Gate | Plantillas afectadas | Evidencia / criterio | Proxima accion |
| --- | --- | --- | --- | --- |
| P0 | Consentimiento especifico de procedimiento | Consentimiento informado | Bloquear CI generico sin procedimiento, nivel, lado, alternativas y riesgos principales. | Crear fixture `ci_specificity_min_fields` con casos positivos/negativos. |
| P0 | Separacion diagnostico / indicacion | Historia clinica, parte quirurgico | No escribir diagnostico mezclado con conducta terapeutica o indicacion agregada. | Gate de texto contextual antes de render/guardado. |
| P0 | Campos minimos de parte quirurgico | Parte quirurgico | Exigir fecha, profesional, diagnostico, indicacion, tecnica, hallazgos, complicaciones, cierre y firma. | Schema validator por seccion obligatoria. |
| P0 | Consistencia documental cruzada | Historia clinica, consentimiento, parte quirurgico | Diagnostico, indicacion, procedimiento, tecnica y consentimiento no pueden contradecirse. | Matriz `document_consistency_gate_v1`. |
| P0 | No invencion de hechos quirurgicos | Parte quirurgico, historia clinica | Correcciones del Doctor: no agregar laminectomia, descompresion directa, parche dural, raiz/nivel/lateralidad no informados. | Activar fixtures lumbares criticos como release blockers. |
| P0 | Datos sensibles y minimizacion | Todas | Prohibir canales externos y exigir anonimizar/minimizar datos en corpus y QA. | Gate de salida: sin datos identificables ni referencias externas. |
| P1 | Complicacion documentada completa | Parte quirurgico, evolucion | Si aparece complicacion, debe incluir manejo, estado final y comunicacion si aplica. | Validator condicional por presencia de complicacion. |
| P1 | Trazabilidad de implantes/material | Parte quirurgico | Si hay osteosintesis/interbody, exigir nivel, tipo de implante y control. | Gate condicional por material/implante detectado. |
| P1 | Metadatos completos de fuente | Corpus, review queue | Cada `corpus_item` debe tener fuente, tipo, jurisdiccion, organismo, fecha, estado, tema, criterio y nivel de confianza. | Schema `corpus_item` obligatorio. |
| P1 | Separacion oficial/doctrina/inferencia | Corpus, gate registry | No mezclar norma, fallo, doctrina, protocolo interno e inferencia del sistema. | Campo `source_class` y `gate_origin` obligatorio. |
| P2 | Legibilidad clinica sin sobrelegalizar | Todas | Evitar plantillas inutiles por exceso de texto legal. | Score de longitud/claridad como warning, no blocker. |
| P2 | Duplicados y tautologias | Todas | Evitar repeticiones como posicion/proteccion/hemostasia duplicada. | QA de estilo como `warning` hasta calibrar. |

## official_source_requirements

Estados permitidos antes de transformar una fuente en gate:

| Estado | Puede bloquear release | Requisitos |
| --- | --- | --- |
| `official_verified` | Si | Fuente oficial localmente documentada, jurisdiccion/organismo/fecha/estado completos, criterio traducido a regla testeable. |
| `internal_protocol` | Si, para conducta/documentacion propia | Protocolo o correccion del Doctor con alcance clinico claro, fixtures sinteticos y trazabilidad. |
| `doctrine_review` | No | Doctrina separada de ley/fallo, con revision pendiente y uso solo como warning o comentario editorial. |
| `unverified_do_not_gate` | No | Fuente sin path oficial, sin vigencia, sin jurisdiccion o sin criterio verificable. |

Metadatos obligatorios por item: `source_id`, `tipo`, `jurisdiccion`, `tribunal_organismo`, `fecha`, `estado`, `tema`, `hecho_relevante`, `criterio_util`, `gate_derivado`, `plantilla_afectada`, `nivel_confianza`, `requiere_revision_legal`.

Regla de proteccion: ningun fallo o doctrina debe convertirse en gate universal si falta fuente oficial, vigencia, jurisdiccion o revision legal. En ese caso entra a cola `review_queue`, no a `active_gate`.

## template_impact

| Plantilla / area | Impacto propuesto | Tipo de cambio |
| --- | --- | --- |
| Historia clinica | Validar que diagnostico, indicacion y antecedentes no agreguen hechos no informados; exigir trazabilidad de fuente/caso. | P0 gate antes de guardar. |
| Consentimiento informado | Exigir procedimiento especifico, nivel/lado cuando aplique, alternativas razonables y riesgos principales enumerados. | P0 gate y fixture de consentimiento. |
| Parte quirurgico | Exigir campos minimos, consistencia anatomica, secuencia quirurgica compatible y manejo de complicaciones/material. | P0/P1 gates deterministicos. |
| Corpus medico-legal | Separar `official_verified`, `internal_protocol`, `doctrine_review` y `unverified_do_not_gate`. | Schema + review queue. |
| QA runner | Incluir fixtures criticos como release blockers; warnings de estilo separados de blockers. | Runner con exit code no cero para P0. |

## qa_priority

1. `validate_corpus_item_schema`: falla si falta metadata oficial o separacion fuente/doctrina/inferencia.
2. `validate_ci_specificity_min_fields`: falla si CI no identifica procedimiento, nivel/lado cuando aplica, alternativas y riesgos principales.
3. `validate_clinical_document_minimum_fields`: falla si parte quirurgico no contiene campos esenciales.
4. `validate_document_consistency_gate`: falla si diagnostico, indicacion, procedimiento, tecnica y consentimiento se contradicen.
5. `validate_lumbar_doctor_corrections_v1`: falla ante hechos quirurgicos inventados o raiz/nivel/lateralidad incorrectos.
6. `validate_sensitive_data_minimization`: falla si el corpus/QA expone datos sensibles o propone envio externo.
7. `validate_complication_and_implant_conditionals`: empieza como warning P1 y sube a blocker cuando tenga fixtures suficientes.

Comandos esperados una vez implementados por Codex principal en la app real: `scripts/qa/run_clinica_core_qa.js`, `scripts/qa/validate_clinica_route_guard.js`, `scripts/qa/validate_lumbar_doctor_corrections_v1.js` y validator de schema para corpus/gates.

## do_not_integrate_yet

- Fallos sin fuente oficial, estado vigente, jurisdiccion o fecha.
- Doctrina transformada en regla universal sin revision legal.
- Criterios provinciales/nacionales mezclados como si fueran equivalentes.
- Texto legal largo que degrade la utilidad clinica de la plantilla.
- Gates que agreguen diagnosticos, indicaciones, abordajes o secuencias no informadas por el Doctor.
- Datos identificables de pacientes en fixtures, corpus, resultados o QA.
- Automatizaciones que manden documentos por canales externos.
- Cambios directos sobre plantillas sin baseline canonico y test focal.

## risks_limits

- No se consultaron fuentes externas ni se verifico vigencia legal actualizada; este backlog prioriza reglas desde evidencia local ya producida.
- Los paths exactos de implementacion dependen de inspeccionar la app canonica `/Users/jarvis/.openclaw/workspace/clinica/app-clinica-medicolegal`.
- Algunos gates requieren regex contextual para distinguir una tecnica afirmada de una tecnica negada.
- La jurisprudencia puede orientar redaccion, pero sin revision no debe bloquear ni generar obligaciones universales.
- El primer release debe ser chico: schema + P0 documentales + fixtures lumbares criticos.

## recommendation

Codex principal deberia implementar primero el schema de `corpus_item/gate_item` y los P0 documentales: consentimiento especifico, campos minimos de parte, consistencia cruzada, no invencion de hechos quirurgicos y datos sensibles. La cola jurisprudencial queda separada como `review_queue` hasta tener fuente oficial y revision. Para bajar riesgo, integrar en commits separados: schema, fixtures, gates, runner.

## confidence

Media-alta para la priorizacion y el orden de QA, porque deriva de resultados locales consistentes. Media para convertir fuentes legales especificas en gates productivos hasta verificar vigencia oficial y revisar con criterio legal/clinico.

## evidence_paths

- `jobs/20260526T064839-clinica-corpus-gates-backlog-v2.md`
- `context/fronts/clinica.md`
- `results/20260525T013125-corpus-jurisprudencia-leyes-gates-app-clinica.result.md`
- `results/20260525T122941-clinica-correcciones-a-fixtures-implementacion.result.md`
