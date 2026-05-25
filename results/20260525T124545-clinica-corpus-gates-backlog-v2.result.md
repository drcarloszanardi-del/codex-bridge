# Resultado - clinica corpus gates backlog v2

Job: `20260525T124545-clinica-corpus-gates-backlog-v2`
Worker: `personal-xh` / Pablo
Fecha: `2026-05-25`

## summary honesto

El backlog debe convertir el corpus medico-legal en gates verificables, pero con una separacion estricta: normativa oficial y correcciones directas del Doctor pueden alimentar gates duros; jurisprudencia, doctrina e inferencias deben entrar primero como alertas `needs_review` hasta tener fuente, metadata y revision legal. La prioridad inmediata es impedir documentos clinicos con hechos inventados, consentimiento generico o inconsistencias entre diagnostico, indicacion, tecnica y parte quirurgico.

## source_counts

| Fuente | Archivos revisados | Uso |
|---|---:|---|
| `context/fronts/clinica.md` | 1 | Canon clinico y regla de convertir correcciones en gates. |
| `results/20260525T013125-corpus-jurisprudencia-leyes-gates-app-clinica.result.md` | 1 | Taxonomia de fuentes, metadata y conversion corpus -> gate. |
| `results/20260525T122941-clinica-correcciones-a-fixtures-implementacion.result.md` | 1 | Orden de implementacion, fixtures y gates lumbares criticos. |

## gate_backlog

| Prioridad | Gate | Tipo de fuente aceptable | Plantilla afectada | Accion sugerida |
|---|---|---|---|---|
| P0 | Consentimiento especifico por procedimiento, nivel, lado, riesgos principales y alternativas razonables | Normativa oficial revisada | Consentimiento | Bloquear consentimiento generico o sin identificacion anatomica suficiente. |
| P0 | Parte quirurgico con fecha, profesional, diagnostico, indicacion, tecnica, hallazgos, complicaciones, cierre y firma | Normativa oficial revisada + baseline app | Parte quirurgico / HC | Validar campos minimos antes de render o guardado. |
| P0 | Consistencia diagnostico, indicacion, procedimiento, tecnica y consentimiento | Correccion Doctor + corpus | HC, consentimiento, parte | Bloquear contradicciones y hechos no derivados del input. |
| P0 | Privacidad: no datos sensibles en canales externos; minimizacion y anonimizacion | Normativa oficial revisada | Handoff / export | Bloquear exportaciones o prompts con pacientes identificables. |
| P1 | Complicacion documentada con manejo, estado final y comunicacion cuando aplique | Corpus medico-legal, requiere revision | Parte quirurgico | Alerta `needs_review` hasta fuente oficial o criterio interno aprobado. |
| P1 | Implantes/materiales con nivel, tipo, trazabilidad y control | Criterio clinico + documentacion | Parte quirurgico | Gate de completitud, no de decision clinica. |
| P1 | Diagnostico puro separado de indicacion o conducta | Correccion Doctor | HC / resumen | Fixture y regex contextual para no contaminar diagnostico. |
| P1 | No inventar tecnica, topografia, abordaje, raiz o lateralidad | Correccion Doctor + fixtures | Generador clinico | Gate critico con fixtures sinteticos. |
| P2 | Jurisprudencia amplia y doctrina | Fuente oficial completa + revision | Alertas / backlog | No usar como hard gate todavia. |

## official_source_requirements

Un hard gate medico-legal solo debe activarse si el item tiene:

- `source_id`, tipo, jurisdiccion, organismo o tribunal, fecha y estado.
- Texto o referencia oficial verificable, no resumen suelto.
- Campo `plantilla_afectada` y `gate_derivado`.
- `nivel_confianza` y `requiere_revision_legal`.
- Si es jurisprudencia: tribunal, fecha, link/fuente oficial, criterio limitado al hecho del caso y prohibicion de universalizar sin revision.
- Si es doctrina: solo `needs_review`; no hard gate.
- Si es criterio interno del Doctor: marcar como `protocolo interno` y convertir a fixture sintetico antes de tocar plantilla.

## template_impact

| Superficie | Impacto | Implementacion segura |
|---|---|---|
| Historia clinica | Evita diagnosticos contaminados, indicaciones agregadas y contradicciones | Validadores previos a render, fixtures por patologia. |
| Consentimiento | Evita formularios genericos sin procedimiento/nivel/lado/riesgos | Schema minimo + lista de faltantes accionable. |
| Parte quirurgico | Evita tecnica incompatible, secuencia incorrecta o complicacion sin manejo | Gates deterministicos y QA runner. |
| Handoff/export | Evita datos sensibles y perdida de trazabilidad | Gate de privacidad y manifest. |
| Corpus admin | Evita mezcla de oficial/doctrina/inferencia | Cola separada: `official`, `review`, `inference`. |

## qa_priority

1. P0: fixtures criticos del Doctor, consentimiento especifico, consistencia documental y privacidad.
2. P1: completitud de parte quirurgico, complicaciones, implantes y trazabilidad.
3. P2: jurisprudencia/doctrina como alertas revisables, sin bloquear generacion clinica hasta validacion.

El primer batch implementable debe ser chico: consentimiento especifico, consistencia diagnostico/procedimiento y el caso extraforaminal L4-L5 derecha sin interlaminar ni raiz incorrecta.

## do_not_integrate_yet

- Fallos sin fuente oficial completa, fecha, tribunal y estado.
- Doctrina transformada en regla universal.
- Inferencias medico-legales que sobrelegalicen plantillas y vuelvan inutil el flujo clinico.
- Reglas derivadas de un caso aislado sin limite contextual.
- Campos nuevos sin utilidad de QA o sin punto claro en la plantilla.
- Validadores que penalicen una frase negada como si afirmara el hecho.

## risks / limits

- No se verificaron fuentes legales externas en este worker; el resultado ordena backlog, no certifica vigencia legal.
- Un gate demasiado amplio puede bloquear documentacion correcta por falsos positivos.
- La jurisprudencia debe ser refinamiento, no base inicial del sistema.
- La app real esta en otra Mac; este resultado no inspecciona ni modifica su codigo.

## recommendation

Codex principal debe implementar primero un `corpus_item`/`gate_item` con separacion oficial/revision/inferencia y, en paralelo, un primer pack P0 de fixtures y gates deterministicos. No integrar jurisprudencia amplia como hard gate hasta completar metadata y revision.

## confidence

Alta para prioridades P0 y orden de implementacion. Media para cualquier regla legal especifica hasta verificar fuentes oficiales vigentes.

## evidence_paths

- `jobs/20260525T124545-clinica-corpus-gates-backlog-v2.md`
- `context/fronts/clinica.md`
- `results/20260525T013125-corpus-jurisprudencia-leyes-gates-app-clinica.result.md`
- `results/20260525T122941-clinica-correcciones-a-fixtures-implementacion.result.md`
