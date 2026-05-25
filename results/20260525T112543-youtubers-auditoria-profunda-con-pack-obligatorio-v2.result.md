# Resultado - youtubers-auditoria-profunda-con-pack-obligatorio-v2

Job: `20260525T112543-youtubers-auditoria-profunda-con-pack-obligatorio-v2`
Worker: `personal-xh` / Pablo
Fecha: `2026-05-25`
Paquete obligatorio: `context/youtube_content_packs/20260525-martell-maxmaxdata/`

## Summary honesto

Se reviso el paquete local versionado, sin fallback publico ni fuentes externas. La cobertura de archivo coincide con el piso del orquestador: 98 archivos. A nivel logico hay 8 videos de Dan Martell con VTT duplicado `en/en-orig`, 35 filas de inventario YouTube de Maxmaxdata, 29 videos Maxmaxdata con subtitulos SRT, 6 videos Maxmaxdata listados solo por metadata en JSONL, 1 JSON de Instagram/Reel, 6 reportes MD y 4 JSONL. Un JSONL de Dan (`agent_search`) esta vacio.

Conclusion operativa: el valor no esta en copiar el estilo de los youtubers. Esta en convertir sus mecanismos en sistema: brief fuerte, memoria versionada, agentes con herramientas, separacion conversacion/artefacto, ruteo de modelos, QA humano en temas medicos y loop de datos propios.

## source_counts

| Tipo | Efectivamente leido | Hallazgo |
|---|---:|---|
| Total archivos | 98 | Coincide con el piso esperado. |
| VTT Dan Martell | 16 | 8 videos logicos, cada uno con `en` y `en-orig`. |
| SRT Maxmaxdata | 71 | 29 videos con subtitulos, varias variantes por idioma/original. |
| JSONL total | 4 | Dan AI 120 filas, Dan channel 120 filas, Dan agent 0 filas, Maxmaxdata 35 filas. |
| JSON | 1 | Metadata de reel Instagram `DXqXdJ0DE1a`, 2:56, 67 palabras de descripcion. |
| MD | 6 | Reportes previos incluidos en el paquete. |
| Duracion inventariada Dan AI | 644.7 min | Metadata JSONL. |
| Duracion inventariada Dan channel | 1961.3 min | Metadata JSONL. |
| Duracion inventariada Maxmaxdata | 230.3 min | Metadata JSONL. |
| Tamano paquete | 5.0M | Verificado localmente. |

## coverage_table

### Inventarios, reportes y metadata

| Path | Estado | Contenido revisado |
|---|---|---|
| `danmartell_ai_search_flat_20260524.jsonl` | revisado | 120 filas de busqueda AI; inventario de titulos, duraciones y metadata para priorizar temas. |
| `danmartell_channel_flat_20260524.jsonl` | revisado | 120 filas del canal; confirma videos amplios sobre Claude, agentes, ChatGPT y herramientas. |
| `danmartell_agent_search_flat_20260524.jsonl` | no util | Archivo vacio, 0 filas; no aporta contenido. |
| `maxmaxdata/youtube_current_flat_80.jsonl` | revisado | 35 videos, 230.3 min; base para cubrir titulos, duraciones y faltantes de subtitulos. |
| `maxmaxdata/DXqXdJ0DE1a.info.json` | revisado | Reel/Instagram sobre 20 casos de uso de imagen IA, retratos/anuncios/mockups/comics; alto engagement, metadata no transcript. |
| `danmartell_ai_aplicado_zanardi_20260524.md` | revisado | AI Company OS, digital brain, RCCF, 10-80-10, camcorder method, agentes por funcion, data moat. |
| `danmartell_youtube_reformas_codex_telegram_20260524.md` | revisado | Reformas para Codex/Telegram: prompts, memoria, ruteo y agente operativo. |
| `martell_youtube_reformas_operativas_20260524.md` | revisado | Reformas operativas para bridge, orquestador, subagentes y outputs. |
| `maxmaxdata/cmp_brief_ia_visual_maxmaxdata_2026-05-25.md` | revisado | Brief para CMP: IA visual con criterio medico y control humano. |
| `maxmaxdata/maxmaxdata_analysis_2026-05-25.md` | revisado | Analisis Maxmaxdata: IA visual, datos, seguridad y criterio humano. |
| `maxmaxdata/maxmaxdata_content_audit_cmp_2026-05-25.md` | revisado | Auditoria Maxmaxdata para CMP/Codex; matriz de videos y aplicaciones. |

### Dan Martell VTT

| ID | Path(s) | Duracion aprox | Estado | Contenido |
|---|---|---:|---|---|
| `4JMH-4kKMC8` | `danmartell_expanded/How to Actually Use AI in 2026 [4JMH-4kKMC8].en*.vtt` | 11.4 min | revisado | Evitar consejo simplista tipo reemplazar equipo por agentes; usar IA para elevar trabajo real, con resultados medibles. |
| `7zPQV1BSH_k` | `danmartell_expanded/23 Ways to Use ChatGPT So Well it Feels Like Cheating [7zPQV1BSH_k].en*.vtt` | 16.6 min | revisado | Usos de ChatGPT: prompts maestros, memory vault, agente, espejo critico y automatizacion de tareas. |
| `D_YzcH0VsGY` | `danmartell_expanded/The most powerful AI Agent I've ever used in my life [D_YzcH0VsGY].en*.vtt` | 11.9 min | revisado | Agentes que actuan, no solo responden; browser/computer use, Make/Zapier/n8n y workflows ejecutables. |
| `FK5UNNBPbgM` | `danmartell_expanded/Give me 99 seconds and I'll make you DANGEROUSLY good with AI [FK5UNNBPbgM].en*.vtt` | 1.7 min | revisado | Prompt minimo util: rol, contexto, tarea y formato de salida. |
| `XRU-CjzYt_o` | `danmartell_expanded/Why I Switched From ChatGPT to Claude (without losing anything) [XRU-CjzYt_o].en*.vtt` | 16.1 min | revisado | Ruteo por herramienta: Claude/ChatGPT segun fortaleza, migracion sin perder contexto, no fanatismo de modelo. |
| `bkM-lYgAxh0` | `danmartell_expanded/These 6 ChatGPT Hacks Will Make You So Much Money It Feels Illegal [bkM-lYgAxh0].en*.vtt` | 15.4 min | revisado | Prompts de negocio, master prompts, stacks internos y uso de IA como herramienta de ejecucion comercial. |
| `np6CwvTYTAM` | `danmartell_expanded/I Tested 500+ AI Tools, These Will Make You Rich [np6CwvTYTAM].en*.vtt` | 22.7 min | revisado | Ranking de herramientas por ROI y uso; elegir por impacto operativo, no por novedad. |
| `wZeOwqmSw84` | `danmartell_expanded/Learn 97% of Claude in Under 16 Minutes [wZeOwqmSw84].en*.vtt` | 15.2 min | revisado | Claude Projects, Artifacts, Claude Code, skills, dispatch, computer use y dashboard/agent personal. |

### Maxmaxdata SRT revisados

| ID | Titulo | Variantes SRT | Duracion aprox | Estado | Contenido |
|---|---|---:|---:|---|---|
| `PNkqNILL3tQ` | Localizacion con IA | 2 | 2.0 min | revisado | Inferencia visual, localizacion y privacidad. |
| `fYcMU4ruw98` | Agente de IA controla webs | 2 | 3.0 min | revisado | Agente que entiende entorno y navega interfaces. |
| `j6j640m3UCg` | Ano 7 Maxmaxdata | 2 | 8.3 min | revisado | Constancia, empresa, comunicacion y contenido sostenido. |
| `MFlTEwnxn9I` | DeepSeek vs ChatGPT | 2 | 4.7 min | revisado | Comparacion de modelos, local/open code y tradeoffs. |
| `B23UGxrzvv4` | EITB / Distrito Euskadi | 2 | 16.8 min | revisado | Divulgacion IA, cambio cultural y adopcion empresarial. |
| `TWhDsRb_HgA` | 2024 redes 0 a +200k | 3 | 6.1 min | revisado | Calendario, volumen, consistencia y aprendizaje por publicacion. |
| `X-LHK4SJlbg` | Sora texto a video | 3 | 3.0 min | revisado | Video generativo como exploracion visual. |
| `3QwWD-c17BA` | Sora texto/imagen a video | 3 | 6.5 min | revisado | Prompt, remix, continuidad visual y limites. |
| `W90tNWrhlDI` | Test de Turing | 3 | 6.2 min | revisado | Transparencia, diferenciacion IA/persona y confianza. |
| `Cn4xzCOEn0E` | IA generativa sin deshumanizacion | 3 | 30.1 min | revisado | Criterio humano, desinformacion, innovacion responsable. |
| `Ql1MmxupOaY` | Onda Vasca / IA y datos | 3 | 4.9 min | revisado | Business intelligence y datos para decisiones. |
| `0Qb3Ypk7j6I` | Voz avanzada freestyle | 3 | 3.0 min | revisado | Interaccion por voz, creatividad y latencia. |
| `tJ9_xuMC7os` | Gemini Imagen 3 | 3 | 3.0 min | revisado | Generacion de imagenes, restricciones y calidad. |
| `kUYL_ckLHCg` | Mejorar imagenes con IA | 3 | 2.4 min | revisado | Iteracion visual, instrucciones y mejora de assets. |
| `NgzIwvHIGxw` | GPT 4o Canvas | 3 | 2.7 min | revisado | Separar conversacion de artefacto editable. |
| `shRt9kNvMlc` | Ahorrar tiempo con IA | 3 | 1.8 min | revisado | Convertir llamadas/pedidos en presupuesto o salida concreta. |
| `4_PaISVOW5U` | Preparar viaje a Roma | 3 | 2.8 min | revisado | Planificacion asistida con restricciones. |
| `vsZJXveBc8E` | IA viciada / reset | 3 | 2.9 min | revisado | Reset de contexto contaminado y recuperacion de control. |
| `yfL-_L_I8Mo` | IA no puede todo | 2 | 1.6 min | revisado | Evaluacion de imagen real/falsa y limites. |
| `7PVknGE0L18` | Imagen maxima calidad | 2 | 1.4 min | revisado | Tips de calidad visual. |
| `YBtFGxwdAno` | Bits a beats | 2 | 29.6 min | revisado | IA, creatividad, musica y contenido audiovisual. |
| `yO4a1Fie82U` | Tests psicotecnicos | 2 | 1.6 min | revisado | Entrenamiento con IA y ejercicios. |
| `YBuBQMI59gg` | IA en euskera | 2 | 9.6 min | revisado | Localizacion, idioma y accesibilidad. |
| `CMyVk6HF5ak` | Freestyle IA | 2 | 2.5 min | revisado | Voz/creatividad y restricciones de modelo. |
| `K31W7kLJRNU` | Secuestros de datos / IA | 2 | 42.4 min | revisado | Ciberseguridad, ransomware, datos de salud, digitalizacion real. |
| `mL6ieyaBJSo` | 5 aniversario | 2 | 1.2 min | revisado | Datos como base de negocio y comunicacion institucional. |
| `gixMLAqNvCY` | Big Data Company Bilbao | 2 | 1.4 min | revisado | Datos reducen incertidumbre. |
| `2uh9Jw-yZmI` | Xmas 2020 | 2 | 1.8 min | no util | Casi solo musica/licencia; no aporta metodo. |
| `77Q7TaMwcyE` | Comunicacion de insights | 2 | 0.8 min | no util | Casi solo musica/licencia; no aporta metodo. |

### Maxmaxdata JSONL sin SRT local

| ID | Titulo | Duracion | Estado | Contenido |
|---|---|---:|---|---|
| `64wmdNaNTzM` | Maxmaxdata en Radio Marca | 19.5 min | parcial | Inventario metadata sin subtitulo local; tema general de divulgacion/datos. |
| `K9ten-Fbarc` | Redneck Dashboard | 0.7 min | parcial | Metadata; dashboard/comunicacion visual de datos. |
| `FcivzYZyIDQ` | Sports trends pre/post covid19 | 1.4 min | parcial | Metadata; analitica comparativa y series temporales. |
| `lwhhBIRUrAg` | Infografia covid19 Spain | 1.8 min | parcial | Metadata; infografia y visualizacion de datos. |
| `IMjXdAAYll4` | 1st birthday | 1.1 min | parcial | Metadata institucional. |
| `Rg4zQURuvNE` | Xmas 2019 | 2.0 min | parcial | Metadata; no hay transcript en paquete. |

## exclusion_log

| Elemento | Decision | Motivo |
|---|---|---|
| `danmartell_agent_search_flat_20260524.jsonl` | excluir de contenido | Archivo vacio, 0 filas. |
| VTT duplicados `en/en-orig` | consolidar | Mismo video con variantes; se leyeron ambos y se reporta unidad logica. |
| SRT duplicados `es/es-orig/en` | consolidar | Se revisaron variantes; se reporta por video para no inflar hallazgos. |
| `2uh9Jw-yZmI` y `77Q7TaMwcyE` | no util | Subtitulos casi solo musica/licencia. |
| 6 Maxmaxdata JSONL sin SRT | parcial | Hay metadata local pero no transcript; no se inventa contenido. |
| URLs/metadata de descarga en JSON | no usar como fuente externa | El contrato exige paquete local, no navegacion ni fetch externo. |

## top ideas accionables con evidencia

1. Telegram debe ser un sistema operativo de trabajo, no una bandeja de chats. Evidencia: Martell insiste en master prompts, digital brain y agentes; Maxmaxdata muestra Canvas como separacion entre conversacion y artefacto. Accion: cada mensaje entrante debe convertirse en `brief.md`, `context_refs`, `decision_needed` y `artifact_target`.

2. Adoptar 10-80-10 como contrato de delegacion. Evidencia: los materiales de Martell se centran en dar direccion inicial fuerte, delegar ejecucion y reservar revision final humana. Accion: Doctor/orquestador define el 10 inicial, 5.3 hace el 80 de extraccion/transformacion, Pablo hace segunda mirada XH, Codex principal integra y decide.

3. Pasar de "modelo que responde" a agente con entorno y herramientas. Evidencia: Dan enfatiza agentes que actuan; Maxmaxdata muestra agentes que navegan webs. Accion: crear workorders con objetivo, herramienta permitida, carpeta permitida, criterio de terminado, evidencia requerida y riesgos.

4. Separar entrada, razonamiento, artefacto y entrega. Evidencia: Canvas y Artifacts aparecen como patron recurrente. Accion: Telegram Directo debe guardar album/audio/texto como input bruto; crear artifact draft; recien luego respuesta o commit.

5. Ruteo por modelo, no por marca. Evidencia: comparativas ChatGPT/Claude/Gemini/DeepSeek destacan fortalezas distintas. Accion: `5.3` para parser/OCR/extraccion/QA mecanico; `Pablo 5.5 XHT` para sintesis, estrategia y riesgo; Opus/Claude para artefactos largos/codigo con contexto; Gemini/Nano Banana para visual; principal para permisos y decision.

6. Construir memoria versionada propia. Evidencia: Martell apunta a memory vault/digital brain; Maxmaxdata insiste en datos como reduccion de incertidumbre. Accion: `context/fronts/*.md` con estado canonico por frente, actualizado por PR/commit, no por memoria informal.

7. Convertir correcciones del Doctor en fixtures. Evidencia: camcorder/SOP y mejora iterativa. Accion: cada correccion fuerte genera una regla testeable o checklist: "no pedir Drive si hay paquete local", "no responder sin evidence_paths", "no cerrar con no pude sin rutas alternativas".

8. IA visual sirve para storyboard y b-roll, no para verdad medica. Evidencia: Maxmaxdata explora Sora/Gemini/imagen, pero tambien recalca limites y criterio humano. Accion: CMP debe tener gate de anatomia/verdad clinica antes de publicar cualquier imagen generada.

9. El moat esta en datos propios medico-legales y operativos. Evidencia: Dan habla de sistemas internos y Maxmaxdata de datos/BI. Accion: corpus medico-legal, casos corregidos, respuestas validadas, comparables de inversiones y QA de reels deben volverse dataset interno versionado.

10. Reset de contexto contaminado es una funcion de producto. Evidencia: Maxmaxdata tiene video especifico sobre IA "viciada". Accion: Telegram Directo debe soportar `/reset_scope`, "ignorar hilo previo para esta tarea" y deteccion automatica de drift.

## applicability_matrix

| Idea | Frente aplicable | Modelo/herramienta | Riesgo | Proxima accion |
|---|---|---|---|---|
| Brief compiler | Telegram Directo | 5.3 + Codex principal | Responder con contexto incompleto | Implementar schema `brief/context/task/output/evidence`. |
| 10-80-10 | Todos | Orquestador + 5.3 + Pablo | Delegacion sin cierre humano | Agregar a template de jobs. |
| Agentic workflows | Inversiones/instrumental | Codex principal + browser permitido por job | Acciones externas no autorizadas | Workorders read-only con evidencia y sin contacto. |
| Canvas/Artifacts | Telegram, presentaciones, tesis | Claude/Opus o Codex artifact | Mezclar conversacion con resultado final | Guardar drafts en `artifacts/` antes de responder. |
| Ruteo por modelo | Bridge | Policy YAML | Usar XH para tareas baratas | Crear `docs/model_routing_policy.md`. |
| Memory vault | Bridge/context | Git + status/fronts | Memoria desactualizada | Crear `context/fronts/*.md` con owner y fecha. |
| Fixtures por correccion | Clinica/app | 5.3 + test runner | Repetir errores clinicos | Convertir correcciones en `fixtures/clinical/*.json`. |
| Visual truth gate | Reels/CMP | Gemini/Nano Banana + QA humano | Imagen medica falsa | Checklist antes de publicar: anatomia, claims, fuente, disclaimers. |
| Data moat | Tesis/app/inversiones | NotebookLM + corpus local | Mezclar fuentes no oficiales | Fuente con hash, origen, fecha y estado de validacion. |
| Reset scope | Telegram/router | Codex principal | Perder contexto util | Comando explicito y resumen de lo descartado. |

## execution_backlog

| Accion | Frente | Responsable sugerido | Modelo/herramienta | Input necesario | Criterio de terminado | Prioridad |
|---|---|---|---|---|---|---|
| Implementar `brief_compiler` para Telegram | Telegram | Codex principal | 5.3 + router | Mensaje/album/audio/topic | Crea brief con rol, contexto, tarea, output, evidencia antes de responder | P0 |
| Agregar contrato 10-80-10 a jobs | Bridge | Orquestador | Template jobs | `jobs/_template.md` | Cada job tiene 10 inicial, 80 delegado, 10 final | P0 |
| Crear `model_routing_policy.md` | Bridge | Pablo | GPT-5.5 XHT | Resultados previos + este informe | Tabla modelo/tarea/riesgo/costo aceptada por principal | P0 |
| Crear `context/fronts/*.md` | Todos | 5.3 | Git | Results existentes | Un archivo canonico por frente con estado, decisiones, proximas tareas | P0 |
| Hacer validator de resultados | Bridge | 5.3 | Python/script local | Contratos de jobs | Falla si falta coverage, evidence_paths, backlog o risks | P0 |
| Implementar media album buffer | Telegram/reels | Codex principal | Router + filesystem | Fotos/videos/notas del Doctor | No responde hasta procesar album completo o timeout | P1 |
| Crear visual truth gate CMP | Reels/CMP | Pablo + principal | Gemini/Nano Banana + checklist | Guion/storyboard/asset | Ningun reel medico pasa sin QA de anatomia y claim | P1 |
| Crear fixtures clinicos desde correcciones | App medico-legal | 5.3 | Test runner | Correcciones del Doctor | Cada correccion tiene test que falla antes y pasa despues | P1 |
| Protocolo NotebookLM source pack | Tesis | Pablo | NotebookLM + Git | PDFs/fuentes oficiales versionadas | Cada respuesta cita fuente local y estado de validez | P1 |
| Radar inversiones/instrumental con schema | Inversiones/instrumental | 5.3 + Pablo | Parser + XH | Candidatos y comparables | Scorecard con evidencia, riesgos, proxima accion no externa | P1 |
| Auditor automatico de paquetes YouTube | Bridge | 5.3 | Python | Carpeta `context/youtube_content_packs/*` | Genera counts, coverage table y exclusion_log automaticamente | P2 |
| Reset scope command | Telegram | Codex principal | Router | Mensaje `/reset_scope` | Hilo nuevo ignora contexto previo salvo fuentes fijadas | P2 |

## Que incorporar ahora

1. Template unico de workorder con `brief/context/task/output/evidence/risk/done`.
2. `context/fronts/` como memoria versionada por frente.
3. Validator de resultados para impedir informes vacios.
4. Politica de ruteo de modelos.
5. Buffer de albums/media antes de responder en Telegram.
6. Gate visual medico para reels CMP.
7. Regla de reset de contexto contaminado.

## Que probar en piloto

1. Piloto Telegram: tomar 10 mensajes reales del Doctor y convertirlos a briefs antes de ejecutar.
2. Piloto reels CMP: 3 piezas con guion, storyboard, visual gate y caption separados.
3. Piloto tesis: 1 mini-pack NotebookLM con fuentes versionadas y matriz de citas.
4. Piloto inversiones: 5 candidatos con scorecard y evidencia local.
5. Piloto app medico-legal: 5 correcciones del Doctor convertidas en fixtures.

## Que descartar

1. Copiar tono/estilo de youtuber como objetivo.
2. Pedir Drive/Gmail/OAuth si el job ya trae paquete local.
3. Usar imagen IA como prueba medica.
4. Reemplazar decision del Doctor por agente.
5. Ruteo por moda de modelo.
6. Responder en Telegram antes de consolidar album/contexto.
7. Informes sin paths, counts ni backlog verificable.

## 10 decisiones para el orquestador

1. Aprobar `brief_compiler` como paso obligatorio antes de responder Telegram.
2. Aprobar `context/fronts/` como memoria canonica por frente.
3. Aprobar que todo job importante tenga `coverage_table`, `exclusion_log` y `execution_backlog`.
4. Aprobar politica de modelo: 5.3 extraccion, Pablo segunda mirada, principal decision.
5. Aprobar gate visual CMP para toda imagen/anatomia/claim medico.
6. Aprobar fixture obligatorio para cada correccion clinica del Doctor.
7. Aprobar reset de scope en Telegram.
8. Aprobar que NotebookLM solo trabaje con source packs versionados cuando el frente sea tesis/corpus.
9. Aprobar que inversiones/instrumental sean read-only hasta autorizacion explicita de contacto/compra.
10. Aprobar auditor automatico de paquetes YouTube para no repetir trabajo manual de coverage.

## Que debe hacer 5.3

- Conteos, parsing, OCR, limpieza de subtitulos y deduplicacion.
- Construir coverage_table y source_counts automaticamente.
- Extraer snippets/temas por video sin decidir estrategia final.
- Validar contratos de salida y secret scan.
- Convertir correcciones en fixtures/checklists.
- Mantener `context/fronts/*.md` con cambios atomicos.

## Que debe hacer Pablo 5.5 XHT

- Sintesis profunda, segunda mirada y deteccion de riesgos.
- Traducir contenido externo a decisiones operativas del ecosistema Zanardi.
- Separar implementar ahora / piloto / investigar / descartar.
- Evaluar tradeoffs entre modelos y herramientas.
- Proponer arquitectura y backlog verificable.

## Que queda en Codex principal

- Decision final, prioridades y permisos.
- Integracion real en Telegram/router/app.
- Acciones externas, si el Doctor las autoriza explicitamente.
- Manejo de credenciales sin exponerlas al worker.
- Publicacion, contacto, compra o envio.
- Cierre final con el Doctor.

## Reformas concretas para Telegram

1. `InboxEvent`: cada mensaje, audio, imagen o album entra como evento crudo con topic y timestamp.
2. `BriefCompiler`: produce brief estructurado antes de invocar al agente.
3. `ContextBinder`: adjunta `context/fronts/<frente>.md`, ultimas decisiones y restricciones.
4. `MediaBuffer`: espera album completo o timeout antes de responder.
5. `ArtifactDraft`: crea salida intermedia separada de la conversacion.
6. `DecisionGate`: si hay duda de permisos, no ejecuta externo; deja propuesta local.
7. `ResetScope`: comando para limpiar contexto contaminado.
8. `ResultContract`: toda respuesta importante debe tener evidencia, riesgos y proxima accion.
9. `WorkerRouter`: decide 5.3/Pablo/principal segun tarea.
10. `DoctorCorrectionCapture`: cada reto/correccion del Doctor genera regla o test.

## Cambios para reels y presentaciones CMP

- Separar `guion`, `storyboard`, `asset_plan`, `caption`, `medical_claims`, `visual_truth_gate`.
- Usar Gemini/Nano Banana/Sora solo para storyboard, b-roll o exploracion visual.
- No usar IA visual para representar anatomia quirurgica como si fuera evidencia real.
- Incorporar checklist de anatomia, indicacion, contraindicacion, claim medico, tono y datos de contacto.
- Mantener banco de plantillas de reels exitosos con metricas: retencion, guardados, consultas, conversion.
- Para presentaciones: artifact editable primero, version final despues; no mezclar notas internas con slides.

## Cambios para tesis y corpus/app medico-legal

- Crear source packs versionados: fuente, hash, jurisdiccion, fecha, estado oficial/no oficial, resumen.
- NotebookLM solo con packs aprobados, no corpus mezclado informalmente.
- Cada respuesta medico-legal debe citar fuente local y nivel de confianza.
- App medico-legal debe tener route guard: no confundir busqueda, diagnostico, recomendacion y redaccion.
- Correcciones del Doctor se vuelven fixtures; ninguna mejora queda solo en chat.
- Para jurisprudencia/leyes: mantener exclusion_log de fuentes no oficiales o dudosas.

## Risks / limits

- No se uso fallback publico; por eso 6 videos Maxmaxdata sin SRT quedan parciales por metadata local.
- `danmartell_agent_search_flat_20260524.jsonl` esta vacio.
- VTT/SRT pueden contener errores automaticos de transcripcion/traduccion.
- No se verifico cada afirmacion contra video original online por regla del job.
- El JSON de Instagram contiene metadata y descripcion, no transcript completo.
- La sintesis de contenido largo esta basada en lectura local de captions/reportes y consolidacion por tema.

## recommendation

Implementar primero el paquete minimo: `brief_compiler`, `context/fronts`, `model_routing_policy`, `result_contract_validator` y `media_album_buffer`. Eso captura el 80% del valor observado en Martell/Maxmaxdata: mejor input, memoria propia, agentes con rol claro, salida verificable y criterio humano antes de accion externa.

Despues pilotear reels CMP y tesis con gates separados. No conviene empezar por mas herramientas visuales ni mas canales; conviene fortalecer el sistema de decision y evidencia.

## confidence

Alta para patrones operativos y arquitectura del bridge, porque la cobertura de archivos fue completa y los hallazgos convergen entre Dan, Maxmaxdata y reportes previos. Media para videos Maxmaxdata sin SRT local, porque solo hay metadata en el paquete.

## evidence_paths

- `context/youtube_content_packs/20260525-martell-maxmaxdata/`
- `context/youtube_content_packs/20260525-martell-maxmaxdata/danmartell_expanded/*.vtt`
- `context/youtube_content_packs/20260525-martell-maxmaxdata/danmartell_ai_search_flat_20260524.jsonl`
- `context/youtube_content_packs/20260525-martell-maxmaxdata/danmartell_channel_flat_20260524.jsonl`
- `context/youtube_content_packs/20260525-martell-maxmaxdata/danmartell_agent_search_flat_20260524.jsonl`
- `context/youtube_content_packs/20260525-martell-maxmaxdata/*.md`
- `context/youtube_content_packs/20260525-martell-maxmaxdata/maxmaxdata/youtube_current_flat_80.jsonl`
- `context/youtube_content_packs/20260525-martell-maxmaxdata/maxmaxdata/subtitles/*.srt`
- `context/youtube_content_packs/20260525-martell-maxmaxdata/maxmaxdata/DXqXdJ0DE1a.info.json`
- `context/youtube_content_packs/20260525-martell-maxmaxdata/maxmaxdata/*.md`
