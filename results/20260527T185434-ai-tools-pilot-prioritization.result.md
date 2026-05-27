---
job_id: 20260527T185434-ai-tools-pilot-prioritization
worker: personal-xh
status: completed
completed_at: 2026-05-27T18:55:44-03:00
front: CODEX-OPS
no_external_actions: true
no_secrets: true
---

# Resultado - Herramientas IA priorizacion de pilotos

## summary honesto

La decision sana no es comprar mas membresias: es correr tres pilotos medibles
con material no sensible y comparar contra el pipeline local. La matriz previa
ya separa funciones: Codex integra, 5.3 extrae y valida barato, Pablo revisa
riesgo, Presentations produce PPTX editable, NotebookLM organiza fuentes,
Claude/Opus mejora narrativa y Gemini/Nano Banana sirve para visuales no
sensibles.

Separacion pedida:

- Evidencia: `results/20260525T122119-ai-tools-apps-skills-models-deep-v1.result.md`
  recomienda herramienta por funcion y rechaza tool-hopping.
- Inferencia: los primeros pilotos deben atacar fallas reales del ecosistema:
  presentaciones editables, calidad Telegram y visuales CMP controlados.
- Opinion: pagar antes de medir contra un baseline local seria ruido caro.

No verifique precios ni capacidades actuales porque el job prohibe acciones
externas.

## coverage_table

| Fuente | Estado | Uso |
| --- | --- | --- |
| `jobs/20260527T185434-ai-tools-pilot-prioritization.md` | Revisada | Objetivo, secciones requeridas y restricciones. |
| `results/20260525T122119-ai-tools-apps-skills-models-deep-v1.result.md` | Revisada | Matriz de herramientas, modelos por funcion y reject hype log. |
| `context/youtube_content_packs/20260525-martell-maxmaxdata/` | Referenciada por auditoria local | Paquete fuente auditado previamente; principio de sistema y herramienta por funcion. |
| `results/20260525T112543-youtubers-auditoria-profunda-con-pack-obligatorio-v2.result.md` | Revisada indirectamente desde matriz | 10-80-10, source packs, ruteo por modelo y separacion conversacion/artefacto. |
| `results/20260527T005221-ai-tools-pilot-prioritization.result.md` | Revisada como antecedente | Priorizacion previa de pilotos y bloqueos de compra. |

## pilot_priority

| Prioridad | Piloto | Impacto | Privacidad | Costo | Esfuerzo | Decision |
| --- | --- | --- | --- | --- | --- | --- |
| P0 | Presentacion medica editable local | Alto: valida deck premium, PPTX editable y source QA. | Bajo si el tema es no sensible. | Cero extra si se usa Codex + Presentations. | Medio. | Ejecutar primero. |
| P0 | Telegram quality scorecard + ArtifactDraft | Alto: reduce respuestas con contexto incompleto, diffs crudos y entregas falsas. | Bajo: usa logs/resultados locales sanitizados. | Cero extra con 5.3/Codex. | Medio. | Ejecutar en observabilidad 7 dias. |
| P1 | Visual CMP abstracto con Gemini/Nano Banana | Medio-alto: mejora reels/decks sin tocar evidencia clinica. | Medio: solo assets no sensibles. | Solo si ya disponible o con autorizacion. | Medio. | Pilotear acotado con visual truth gate. |

No entran como primeros:

- Gamma/Tome/Canva-like hasta demostrar export PPTX editable y trazabilidad.
- Sora/video IA medico factual.
- Browser/computer-use con clicks externos.
- Automatizadores con cuentas reales.

## cost_privacy_matrix

| Herramienta | Costo incremental | Privacidad | Riesgo principal | Uso permitido ahora |
| --- | --- | --- | --- | --- |
| Codex + Presentations | Bajo/cero | Local/workspace | QA visual insuficiente si no se renderiza. | Si, baseline. |
| 5.3 | Bajo | Local/bridge | Cerrar sin criterio estrategico. | Si, extraccion, scorecards y validators. |
| Pablo XH | Alto relativo | Local/bridge | Usarlo para tareas mecanicas. | Si, segunda mirada y riesgo. |
| NotebookLM | Variable | Depende del source pack | Subir material sensible o no versionado. | Solo con pack sanitizado. |
| Claude/Opus | Variable | Depende del input | Material sensible fuera de control. | Solo narrativa sanitizada. |
| Gemini/Nano Banana | Variable | Visual/multimodal | Imagen medica falsa. | Solo fondos, esquemas y variantes no sensibles. |
| Gamma/Tome/Canva-like | Incierto | Externo | Lock-in, no editable, citas debiles. | No comprar aun. |
| Make/Zapier/n8n | Variable | Alto por credenciales | Acciones externas no autorizadas. | Disenar, no conectar. |

## success_metrics

Piloto 1, presentacion medica:

- 8-10 slides.
- PPTX editable abre sin errores.
- 0 solapes/clipping en render/contact sheet.
- 100% claims medicos con fuente, cita o `doctor_experience`.
- `qa_report.md` aprobado.

Piloto 2, Telegram scorecard + ArtifactDraft:

- 20 respuestas importantes evaluadas.
- 0 hard fails enviados: media sin buffer, diff crudo, entrega sin `message_id`,
  accion externa sin permiso o datos sensibles.
- Warnings clasificados sin bloquear respuestas simples.
- Al menos 3 fixtures/regresiones nuevos desde incidentes reales.

Piloto 3, visual CMP abstracto:

- 3 assets/fondos no sensibles.
- 0 datos de pacientes, 0 anatomia usada como evidencia.
- Telefono `2364384321`, Instagram `@drcarloszanardi` y web correctos si aparecen.
- Visual truth gate con decision `usar`, `ajustar` o `rechazar`.

## do_not_buy_yet

- Gamma/Tome/Canva-like: no hasta probar PPTX realmente editable y citas.
- Sora/video IA para medicina factual.
- Make/Zapier/n8n con credenciales reales.
- Browser/computer-use con posibilidad de contacto, compra o envio.
- Stock/video/music sin brief, licencia y aprobacion del orquestador.
- Cualquier herramienta que no deje evidencia local verificable.

## next_actions

1. Ejecutar piloto de presentacion local con tema no sensible y source manifest.
2. Implementar `scripts/qa/score_telegram_response.py` en modo observabilidad.
3. Crear 3 assets CMP abstractos y pasarlos por visual truth gate.
4. Comparar tiempo, calidad, privacidad y control contra baseline local.
5. Recién despues decidir si una membresia externa agrega valor real.

## risks / limits

- No se verificaron precios ni features actuales por restriccion de no acciones
  externas.
- Los costos reales dependen de cuentas, limites y terminos vigentes.
- Privacidad depende de usar material sanitizado; ningun piloto debe subir datos
  clinicos identificables.
- Las herramientas visuales no deben probar anatomia ni evidencia clinica.
- Ruta alternativa si no hay acceso a una herramienta externa: correr el piloto
  completo con Codex + Presentations + assets locales y dejar la comparativa para
  despues.

## recommendation

Ejecutar los pilotos en este orden: presentacion medica editable, Telegram
quality scorecard con ArtifactDraft, visual CMP abstracto. No comprar ni activar
membresias nuevas hasta que un piloto demuestre mejora medible en calidad,
tiempo o riesgo frente al pipeline local.

## confidence

Alta para el orden y los bloqueos por privacidad porque derivan de la matriz
local y del paquete auditado. Media para costos y capacidades comerciales no
verificados en vivo.

## evidence_paths

- `jobs/20260527T185434-ai-tools-pilot-prioritization.md`
- `results/20260525T122119-ai-tools-apps-skills-models-deep-v1.result.md`
- `results/20260525T112543-youtubers-auditoria-profunda-con-pack-obligatorio-v2.result.md`
- `results/20260527T005221-ai-tools-pilot-prioritization.result.md`
- `context/youtube_content_packs/20260525-martell-maxmaxdata/`
- `claims/20260527T185434-ai-tools-pilot-prioritization.json`
