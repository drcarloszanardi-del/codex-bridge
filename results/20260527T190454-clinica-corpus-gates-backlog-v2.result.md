---
job_id: 20260527T190454-clinica-corpus-gates-backlog-v2
worker: personal-xh
status: completed
completed_at: 2026-05-27T19:20:23-03:00
front: CLINICA
no_external_actions: true
no_secrets: true
---

# Resultado - Clinica corpus medico-legal gates backlog v2

## summary honesto

El corpus medico-legal debe convertirse en gates verificables, pero no todo
corpus puede bloquear documentos. La prioridad segura es documental y clinica:
historia clinica minima, consentimiento especifico, diagnostico separado de
indicacion, consistencia diagnostico-indicacion-procedimiento, datos sensibles e
implantes/materiales. Jurisprudencia y doctrina deben quedar como `advisory` o
`needs_review` hasta tener fuente oficial, metadatos completos y revision legal.

Separacion pedida:

- Evidencia oficial/local: `context/fronts/clinica.md` define la regla de
  convertir correcciones en fixtures/gates y separar busqueda de corpus, cola de
  revision y gate activo.
- Inferencia: los gates P0 deben ser deterministas y documentales antes de
  integrar fallos amplios.
- Opinion: el peor error ahora seria transformar doctrina o jurisprudencia no
  verificada en hard fail y romper documentos clinicos correctos.

No toque la app canonica, no use pacientes, no consulte fuentes externas y no
modifique plantillas.

## coverage_table

| Fuente | Estado | Uso |
| --- | --- | --- |
| `jobs/20260527T190454-clinica-corpus-gates-backlog-v2.md` | Revisada | Objetivo, restricciones y secciones requeridas. |
| `context/fronts/clinica.md` | Revisada | Canon clinico, ruta app, corpus a gates y regla de seguridad. |
| `results/20260525T013125-corpus-jurisprudencia-leyes-gates-app-clinica.result.md` | Revisada | Taxonomia de fuentes, metadatos y conversion a gates. |
| `results/20260525T122941-clinica-correcciones-a-fixtures-implementacion.result.md` | Revisada | Orden seguro: fixtures, helpers, gates y runner QA. |
| `results/20260527T010224-clinica-corpus-gates-backlog-v2.result.md` | Revisada como fuente operativa | Backlog previo y separacion oficial/advisory. |

## gate_backlog

| Prioridad | Gate | Base | Aplica a | Severidad inicial | Fuente/estado requerido |
| --- | --- | --- | --- | --- | --- |
| P0 | Historia clinica minima completa | Oficial + canon local | historia clinica, parte | `hard_fail` si faltan campos estructurales | Normativa oficial vigente + schema local. |
| P0 | Consentimiento especifico no generico | Oficial | consentimiento | `hard_fail` | Fuente oficial versionada; plantilla validada. |
| P0 | Diagnostico separado de indicacion | Correcciones Doctor + canon documental | historia, consentimiento | `hard_fail` para mezcla clara; `needs_review` si ambiguo | Protocolo interno/fixtures sinteticos. |
| P0 | Consistencia diagnostico-indicacion-procedimiento | Correcciones Doctor + QA medico | todos | `hard_fail` para contradiccion explicita; `needs_review` para contexto incompleto | Fixtures sinteticos + revision clinica. |
| P0 | Datos sensibles minimizados | Oficial + canon local | export/envio, documentos | `hard_fail` | Normativa datos personales + politica local. |
| P1 | Riesgos especificos enumerados | Oficial | consentimiento | `hard_fail` si queda generico; `needs_review` si faltan detalles clinicos | Fuente oficial + lista por procedimiento. |
| P1 | Implantes/materiales trazables | Protocolo interno + documentacion tecnica | parte quirurgico | `hard_fail` si se menciona implante sin nivel/tipo; `needs_review` si no aplica | Protocolo interno revisado. |
| P1 | Complicacion con manejo y estado final | Documental + protocolo interno | parte quirurgico | `needs_review` inicial | Requiere contexto clinico; no hard fail automatico al inicio. |
| P2 | Jurisprudencia por tema | Oficial solo si verificada | lenguaje/riesgo | `advisory` | CIJ/CSJN, JUBA/SCBA, SAIJ u oficial equivalente con metadatos. |
| P2 | Doctrina tecnica curada | Doctrina | checklist/alerta | `advisory` | Nunca hard gate sin revision legal y clinica. |

Primera tanda recomendada: implementar solo P0 documentales y clinicos con
fixtures sinteticos. Dejar P1/P2 en `report_only` hasta calibrar falsos positivos.

## official_source_requirements

Todo item del corpus debe entrar con metadata minima antes de derivar gates:

```yaml
source_id:
source_type: norma | fallo | doctrina | protocolo_interno
source_status: oficial | interno | doctrina | no_verificado
jurisdiccion:
organismo_o_tribunal:
fecha:
vigencia: vigente | historico | dudoso | derogado_no_usar
tema:
criterio_util:
gate_derivado:
plantilla_afectada:
evidence_path:
review_status: pendiente | revisado_clinico | revisado_legal | aprobado_para_gate
requires_legal_review: true | false
allowed_gate_level: none | advisory | report_only | needs_review | hard_fail
```

Reglas de activacion:

- Fuente oficial vigente + revision legal/clinica suficiente: puede proponer
  `hard_fail` si el control es documental y determinista.
- Protocolo interno o correccion del Doctor: puede crear fixture/gate clinico
  si no inventa normativa.
- Jurisprudencia verificada: inicia como `advisory` o `report_only`; sube solo
  tras revision legal.
- Doctrina: nunca crea hard gate universal por si sola.
- Fuente dudosa, historica, sin path o sin metadata: `none` o `blocked_if`.

## template_impact

| Documento | Impacto permitido ahora | No tocar todavia |
| --- | --- | --- |
| Historia clinica | Campos minimos, diagnostico puro, indicacion separada, fecha/profesional/firma, datos sensibles minimizados. | Reescritura amplia de estilo o doctrina legal en cuerpo clinico. |
| Consentimiento | Procedimiento especifico, nivel/lado si aplica, riesgos especificos, alternativas, ausencia de promesas. | Listados legales extensos no validados por procedimiento. |
| Parte quirurgico | Diagnostico, indicacion, tecnica, hallazgos, implantes/materiales, complicaciones, hemostasia/recuento/cierre. | Hard fail por complicacion ausente sin saber si hubo complicacion real. |
| Export/envio | Deteccion de nombres, DNI, historia clinica, estudios identificables y canales externos no autorizados. | Envio automatico externo o sanitizacion destructiva del documento canonico. |
| Corpus | `corpus_item` y `gate_item` con metadata y estado de revision. | Mezclar fuentes oficiales, doctrina e inferencia en una unica categoria. |

## qa_priority

1. Fixture P0: consentimiento generico vs consentimiento especifico con
   procedimiento/nivel/lado/riesgos.
2. Fixture P0: historia clinica incompleta sin diagnostico o sin indicacion
   separada.
3. Fixture P0: diagnostico contaminado con frase de conducta terapeutica.
4. Fixture P0: procedimiento incompatible con diagnostico o topografia.
5. Fixture P0: datos sensibles en salida/export no autorizado.
6. Fixture P1: implante/material mencionado sin nivel/tipo/trazabilidad.
7. Fixture P1: complicacion mencionada sin manejo/estado final, en
   `needs_review`.
8. Fixture P2: fuente jurisprudencial sin metadatos intenta crear hard gate; debe
   fallar como `advisory_only`.

Comandos sugeridos para Codex principal en la app canonica:

```bash
rg -n "corpus|gate|consentimiento|historia|parte|implante|datos sensibles" /Users/jarvis/.openclaw/workspace/clinica/app-clinica-medicolegal
rg -n "clinical_test_cases|fixtures|validate_.*gates|run_clinica_core_qa" /Users/jarvis/.openclaw/workspace/clinica/app-clinica-medicolegal
node scripts/qa/run_clinica_core_qa.js
```

## do_not_integrate_yet

- Fallos sin fuente oficial, metadatos completos y revision legal.
- Doctrina convertida en hard gate.
- Citas nominales de casos sin verificacion.
- Reglas legales amplias que vuelvan inutil la plantilla clinica.
- Fuentes historicas, dudosas o derogadas.
- Hard fail de complicaciones sin conocer si hubo complicacion real.
- Cambios de plantilla clinica sin baseline y test focal.
- Datos reales de pacientes en fixtures, corpus o resultados.

## risks / limits

- No se verifico vigencia legal en vivo por restriccion de no acciones externas.
- El backlog es accionable, pero los hard gates basados en normativa requieren
  source pack oficial y revision legal antes de uso productivo.
- Demasiados hard fails pueden bloquear documentos correctos; usar
  `needs_review` donde haya contexto clinico.
- La ubicacion exacta de archivos depende de la app canonica; este worker no la
  inspecciono ni la modifico.
- Ruta alternativa si falta fuente oficial: mantener el item como `advisory` o
  `report_only` y crear fixture que demuestre la necesidad sin bloquear.

## recommendation

Codex principal deberia implementar primero una `gate_activation_policy` y el
schema `corpus_item/gate_item`, luego conectar tres P0 detectables con fixtures:
historia clinica minima, consentimiento especifico y diagnostico separado de
indicacion. Jurisprudencia y doctrina deben quedar en `advisory/report_only`
hasta tener fuente oficial versionada, metadatos completos y revision legal.

## confidence

Media-alta para el orden de backlog y QA porque coincide con el frente canonico
y resultados previos. Media para severidades legales hasta validar fuentes
oficiales vigentes y revisar falsos positivos en la app real.

## evidence_paths

- `jobs/20260527T190454-clinica-corpus-gates-backlog-v2.md`
- `context/fronts/clinica.md`
- `results/20260525T013125-corpus-jurisprudencia-leyes-gates-app-clinica.result.md`
- `results/20260525T122941-clinica-correcciones-a-fixtures-implementacion.result.md`
- `results/20260527T010224-clinica-corpus-gates-backlog-v2.result.md`
- `claims/20260527T190454-clinica-corpus-gates-backlog-v2.json`
