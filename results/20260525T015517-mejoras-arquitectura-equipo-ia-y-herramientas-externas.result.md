---
id: 20260525T015517-mejoras-arquitectura-equipo-ia-y-herramientas-externas
job_id: 20260525T015517-mejoras-arquitectura-equipo-ia-y-herramientas-externas
created_at: 2026-05-25T01:59:19-03:00
created_by: personal-xh
status: completed
no_external_actions: true
no_secrets: true
---

# mejoras arquitectura equipo ia y herramientas externas result

## summary

Usar herramientas por rol, no por entusiasmo. Codex orquestador decide; `personal-xh` audita y produce profundidad; modelos baratos clasifican; herramientas externas solo con contexto empaquetado y sin secretos.

## matrix

| Herramienta | Uso recomendado | Frentes | Costo/riesgo | Escalamiento |
|---|---|---|---|---|
| Codex orquestador | mando, contexto global, acciones | todos | alto valor | siempre para decision final |
| personal-xh | auditoria profunda, QA, arquitectura | clinica, corpus, ops | bajo riesgo si bridge | workorders empaquetados |
| subagentes 5.3 | clasificacion, scraping, resumen | rutina | bajo costo | no decisiones |
| 5.4 | borradores intermedios | tesis, presentaciones | medio | si 5.3 no alcanza |
| Opus/Claude | segunda opinion redaccional/argumental | tesis, medico-legal | costo/privacidad | solo contexto sanitizado |
| Gemini | contexto largo, video/imagenes | presentaciones, reels | privacidad | sin datos sensibles |
| NotebookLM | corpus cerrado, tesis, docs | tesis/corpus | riesgo de fuente | solo fuentes curadas |
| Nano Banana | imagenes/creativos | reels/CMP | marca/calidad | no datos clinicos reales |
| Ollama/local | clasificacion no sensible | mail, bridge, logs | capacidad limitada | rutina |
| HeyGen | avatar/video | reels/presentaciones | reputacion/imagen | aprobacion antes publicar |
| Blender/UE/FreeCAD | visualizacion/3D | presentaciones/educacion | tiempo | proyectos especificos |

## protocols

- Context pack minimo: objetivo, restricciones, fuente, decision esperada.
- No pasar credenciales ni datos sensibles a herramientas externas.
- Toda salida externa vuelve como propuesta, no como accion final.
- Para contenido publico: QA medico + QA datos publicos + aprobacion humana.

## recommendation

Crear `TOOL_ROUTING.md`: matriz oficial de que modelo/herramienta puede tocar cada frente, con permisos y salidas permitidas.

## confidence

Alta.

## evidence_paths

- `context/frentes_activos_resumen_20260525.md`
- `AUTHORITY_POLICY.md`
- `protocol.md`
