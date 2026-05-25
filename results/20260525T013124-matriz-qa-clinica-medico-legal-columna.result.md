---
id: 20260525T013124-matriz-qa-clinica-medico-legal-columna
job_id: 20260525T013124-matriz-qa-clinica-medico-legal-columna
created_at: 2026-05-25T01:36:58-03:00
created_by: personal-xh
status: completed
no_external_actions: true
no_secrets: true
---

# matriz qa clinica medico legal columna result

## summary

La matriz debe funcionar como gates medico-legales antes de emitir diagnosticos, partes quirurgicos, consentimientos o piezas publicas. El principio rector: no inventar hallazgos, no mezclar diagnostico con indicacion, y no describir pasos quirurgicos que contradicen la tecnica declarada.

## matriz qa propuesta

| Escenario | Error que debe detectar | Gate verificable | Pruebas sinteticas | Riesgo |
|---|---|---|---|---|
| Diagnostico lumbar | Mezcla diagnostico con indicacion quirurgica | Campo `diagnostico` no puede contener verbos de conducta: operar, indicar, resolver, artrodesar | "Hernia L4-L5. Se indica microdiscectomia" debe fallar en diagnostico | Alto |
| Hernia no especificada | Inventar posterolateral si el input no lo dijo | No inferir topografia ausente; exigir `topografia_desconocida` o aclaracion | Input: "hernia L5-S1" no debe generar "posterolateral" | Alto |
| Hernia extraforaminal | Usar abordaje interlaminar/hemilaminotomia/flavectomia como secuencia principal | Si `topografia=extraforaminal`, bloquear tecnica interlaminar como principal salvo justificacion explicita | "extraforaminal L4-L5 derecha" + "flavectomia" debe alertar | Alto |
| Fijacion L4-L5 | Poner lateralidad derecha en artrodesis/fijacion bilateral | Artrodesis/fijacion de nivel no lleva lateralidad salvo componente unilateral explicitado | "artrodesis L4-L5 derecha" debe fallar | Alto |
| Fijacion sin descompresion directa | Describir laminectomia, flavectomia o liberacion radicular | Si `descompresion_directa=false`, prohibir esos pasos salvo campo de excepcion | "TLIF sin descompresion directa" + "laminectomia" debe fallar | Alto |
| Parte quirurgico | Hemostasia/recuento despues del cierre | Orden canonico: hemostasia y recuento antes de cierre por planos | Parte con cierre antes de recuento debe alertar | Medio/Alto |
| Durotomia/parche | Duplicar parche dural o reparacion | Un solo bloque de manejo dural, con lateralidad/nivel si aplica | Dos menciones de "parche dural" deben alertar | Alto |
| PLIF/TLIF | Duplicar tecnica o mezclar procedimientos incompatibles | Un solo procedimiento principal por nivel salvo plan combinado explicito | "PLIF L4-L5" repetido o PLIF+TLIF sin motivo debe alertar | Alto |
| Consentimiento | Riesgos genericos sin riesgos especificos de columna | Consentimiento debe incluir riesgos neurologicos, infeccion, sangrado, dural, dolor persistente, reoperacion, material si aplica | Consentimiento sin lesion neurologica debe fallar | Alto |
| Pieza publica CMP | Telefono CMP incorrecto | Campo telefono publico debe ser exactamente `2364384321` | Cualquier otro telefono en pieza publica debe alertar | Medio |

## reglas/gates transversales

- Gate de no invencion: todo hallazgo anatomico debe mapear a una frase fuente o campo estructurado.
- Gate de separacion semantica: diagnostico, indicacion, tecnica, consentimiento y pieza publica son secciones con vocabulario permitido distinto.
- Gate de consistencia anatomica: nivel, lado, topografia, procedimiento y abordaje deben ser compatibles.
- Gate de orden quirurgico: preparacion, exposicion, gesto principal, hemostasia, recuento y cierre deben respetar secuencia.
- Gate de duplicados: detectar repeticion de procedimiento, implante, parche dural, PLIF/TLIF, complicacion y cierre.
- Gate de excepcion explicita: si se permite una aparente contradiccion, debe quedar marcada como `excepcion_justificada` con razon.

## recommendation

Implementar primero gates deterministas de alto riesgo: no invencion de topografia, extraforaminal vs abordaje interlaminar, fijacion sin lateralidad, sin descompresion directa, y orden hemostasia/recuento/cierre. Despues agregar evaluador LLM como segunda lectura, no como unica barrera.

## confidence

Alta para diseno de QA. Requiere validacion clinica final del Dr. Zanardi antes de uso real.

## evidence_paths

- `jobs/20260525T013124-matriz-qa-clinica-medico-legal-columna.md`
