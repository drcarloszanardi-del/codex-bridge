---
job_id: 20260527T010224-clinica-corpus-gates-backlog-v2
worker: personal-xh
status: completed
completed_at: 2026-05-27T01:14:00-03:00
front: CLINICA
no_external_actions: true
no_secrets: true
---

# Resultado - Clinica corpus gates backlog v2

## summary honesto

El corpus medico-legal debe alimentar gates verificables, no solo notas. La
prioridad inicial debe ser normativa/documental: consentimiento informado,
historia clinica, privacidad/datos sensibles, consistencia diagnostico-indicacion
y trazabilidad del parte quirurgico. La jurisprudencia y doctrina entran despues
como refinamiento, siempre separadas de fuentes oficiales.

Evidencia: el resultado de corpus previo ya define taxonomia, metadatos y
conversion a gates. Inferencia: la app debe implementar primero gates
deterministicos de documentacion, porque reducen riesgo sin depender de criterio
legal fino. Opinion: no conviene integrar fallos amplios si aun no esta resuelta
la trazabilidad basica de plantillas.

## coverage_table

| Fuente | Estado | Uso |
| --- | --- | --- |
| `jobs/20260527T010224-clinica-corpus-gates-backlog-v2.md` | Revisada | Entregables y restricciones. |
| `context/fronts/clinica.md` | Revisada | Canon clinico, ruta app y regla de fixtures/gates. |
| `results/20260525T013125-corpus-jurisprudencia-leyes-gates-app-clinica.result.md` | Revisada | Taxonomia, metadatos y conversion a gates. |
| `results/20260525T122941-clinica-correcciones-a-fixtures-implementacion.result.md` | Revisada | Integracion de fixtures y gates clinicos. |

## gate_backlog

| Prioridad | Gate | Fuente requerida | Aplica a | Tipo |
| --- | --- | --- | --- | --- |
| P0 | Consentimiento especifico no generico | normativa oficial vigente | consentimiento | hard fail |
| P0 | Historia clinica minima completa | normativa oficial vigente | historia/parte | hard fail |
| P0 | Diagnostico separado de indicacion | correcciones Doctor + criterio documental | historia/consentimiento | hard fail |
| P0 | Consistencia diagnostico-indicacion-procedimiento | protocolo interno + QA medico | todas | hard fail/needs_review |
| P0 | Datos sensibles minimizados | normativa datos personales + frente clinica | exports/envios | hard fail |
| P1 | Riesgos especificos enumerados | normativa + plantilla validada | consentimiento | hard fail |
| P1 | Complicacion con manejo y estado final | normativa/documentacion + protocolo | parte quirurgico | needs_review |
| P1 | Implantes/materiales trazables | protocolo interno + documentacion tecnica | parte quirurgico | hard fail si falta |
| P2 | Jurisprudencia por tema | fuente oficial CIJ/JUBA/SAIJ | lenguaje/riesgo | advisory |

## official_source_requirements

Cada item del corpus debe registrar:

```yaml
source_id:
tipo: norma | fallo | doctrina | protocolo_interno
jurisdiccion:
organismo:
fecha:
estado: vigente | historico | dudoso | derogado_no_usar
tema:
criterio_util:
gate_derivado:
plantilla_afectada:
nivel_confianza:
requiere_revision_legal: true|false
source_path_or_url:
```

Regla: si la fuente no es oficial o no esta versionada, no puede crear hard gate.
Puede crear `advisory` o `needs_review`.

## template_impact

- Historia clinica: campos obligatorios, diagnostico puro, evolucion, indicacion
  separada, profesional/fecha/firma.
- Consentimiento: procedimiento, nivel/lado si aplica, riesgos especificos,
  alternativas razonables y ausencia de promesas.
- Parte quirurgico: tecnica, hallazgos, implantes, complicaciones, hemostasia,
  recuento, cierre y estado final.
- Export/envio: bloqueo de datos sensibles en canales externos no autorizados.

## qa_priority

1. Fixtures sinteticos P0 para consentimiento generico vs especifico.
2. Fixtures de historia clinica incompleta.
3. Fixtures diagnostico mezclado con indicacion.
4. Fixtures de contradiccion procedimiento/diagnostico.
5. Fixtures de datos sensibles en salida externa.
6. Fixtures de implantes/materiales sin trazabilidad.

## do_not_integrate_yet

- Fallos/jurisprudencia sin fuente oficial y metadatos completos.
- Doctrina convertida en hard gate universal.
- Reglas legales amplias que vuelvan inutil la plantilla clinica.
- Citas nominales de casos sin verificacion.
- Fuentes con estado dudoso, historico o derogado.

## risks / limits

- No se consultaron fuentes externas ni se verifico vigencia legal en vivo.
- Este backlog separa oficial/doctrina/inferencia, pero requiere revision legal
  antes de hard gates basados en normativa especifica.
- Demasiados hard gates pueden bloquear documentos correctos; usar `needs_review`
  cuando la regla dependa de contexto clinico.

## recommendation

Implementar primero P0 documental: consentimiento especifico, historia clinica
minima, diagnostico separado de indicacion, consistencia diagnostico-procedimiento
y privacidad. Dejar jurisprudencia para advisory hasta tener source pack oficial
con metadatos completos.

## confidence

Media-alta para el orden de backlog; media para hard gates legales hasta validar
fuentes oficiales vigentes.

## evidence_paths

- `jobs/20260527T010224-clinica-corpus-gates-backlog-v2.md`
- `context/fronts/clinica.md`
- `results/20260525T013125-corpus-jurisprudencia-leyes-gates-app-clinica.result.md`
- `results/20260525T122941-clinica-correcciones-a-fixtures-implementacion.result.md`
