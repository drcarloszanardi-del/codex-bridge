# Tool routing policy

## regla principal

La herramienta no otorga autoridad. La autoridad la define el orquestador y las politicas del repo.

## matriz

| Herramienta | Uso | Datos permitidos | Salida permitida | No usar para | Escalamiento |
|---|---|---|---|---|---|
| Codex orquestador | mando, integracion, acciones | contexto completo autorizado | decisiones y ejecucion | tareas rutinarias masivas | decision final |
| personal-xh | auditoria, diseno, QA, propuestas | jobs/context empaquetado | results/decisions/scripts repo | canales externos, credenciales | orquestador integra |
| subagentes 5.3 | clasificar, resumir, buscar | no sensible o sanitizado | borradores/indices | decisiones criticas | subir a orquestador/XH |
| 5.4 | redaccion y razonamiento intermedio | sanitizado | propuestas | decisiones medico-legales finales | subir a XH/orquestador |
| Opus/Claude | segunda lectura textual | extractos sanitizados | opinion comparativa | credenciales/pacientes reales | orquestador decide |
| Gemini | contexto largo, multimodal | material no sensible | resumen/vision/storyboard | datos identificables | aprobacion para externos |
| NotebookLM | corpus curado | fuentes cerradas | mapas y citas internas | corpus no verificado | revision humana |
| Nano Banana | imagen/creativo | assets no sensibles | imagenes/propuestas | diagnostico o datos reales | QA antes publicar |
| Ollama/local | clasificacion local | no sensible o local permitido | etiquetas/resumen | razonamiento legal alto | escalar si duda |
| HeyGen | video/avatar | guiones aprobados | borrador visual | publicar directo | aprobacion humana |
| Blender/UE/FreeCAD | 3D/visualizacion | objetos/proyectos no sensibles | renders/modelos | urgencias clinicas | proyecto especifico |

## no-usos globales

- No credenciales.
- No datos de pacientes reales salvo empaquetado seguro y permiso explicito.
- No compras, reservas, publicaciones ni contactos sin aprobacion.
- No ObraCash contenido operativo.
