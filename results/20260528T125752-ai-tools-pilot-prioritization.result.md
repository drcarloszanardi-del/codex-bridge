---
job_id: 20260528T125752-ai-tools-pilot-prioritization
worker: personal-xh
status: completed
completed_at: 2026-05-28T12:59:48-03:00
front: CODEX-OPS
no_external_actions: true
no_secrets: true
---

# Resultado - AI tools pilot prioritization

## summary honesto

Priorizar herramientas por marca sigue siendo una trampa. El orden util para el ecosistema Zanardi es priorizar pilotos que prueben una funcion concreta con material local, no pagar membresias por promesa. Los tres pilotos recomendados son: presentacion medica editable con fuentes, reels CMP con gate visual, y source pack NotebookLM/tesis o medico-legal con trazabilidad. Todo lo demas queda como investigacion o comparativa posterior.

## coverage_table

| Requisito | Estado | Evidencia |
|---|---|---|
| `pilot_priority` | cubierto | Matriz previa de herramientas, frentes de presentaciones/reels/telegram y paquete Martell/Maxmaxdata. |
| `cost_privacy_matrix` | cubierto | Ruteo por funcion y restricciones de no datos sensibles/no acciones externas. |
| `success_metrics` | cubierto | Gates medibles por piloto: editabilidad, QA visual, trazabilidad, tiempo y rechazo de output vacio. |
| `do_not_buy_yet` | cubierto | Hype log previo y regla de piloto local antes de membresia. |
| `next_actions` | cubierto | Secuencia implementable para Codex principal sin compras ni cuentas externas. |

## evidencia

- `results/20260525T122119-ai-tools-apps-skills-models-deep-v1.result.md` ya separa Codex, 5.3, Pablo, Claude/Opus, Gemini/Nano Banana, NotebookLM, Presentations y agentes browser por funcion.
- `context/youtube_content_packs/20260525-martell-maxmaxdata/` contiene 27 archivos locales revisables en este repo, incluyendo transcripciones, JSONL, auditorias y material Maxmaxdata.
- `context/fronts/presentaciones.md` exige deck editable, pipeline objetivo/narrativa/storyboard/visuales/deck/QA/export y render sin solapes.
- `context/fronts/reels_cmp.md` exige contacto CMP correcto, visual truth gate, assets propios y separacion de guion/storyboard/assets/caption/QA.
- `context/fronts/telegram.md` marca deuda activa de ResultContract y ArtifactDraft, y confirma que entrega enviada requiere `ok=true` y `message_id` real.

## inferencia

- El primer filtro debe ser privacidad: ningun piloto debe necesitar pacientes, credenciales ni cuentas externas.
- El segundo filtro debe ser posibilidad de medir exito en 1-2 dias.
- El tercer filtro debe ser reutilizacion: si el piloto deja template, validator o checklist, vale mas que una demo vistosa.

## opinion

El mejor gasto ahora no es una membresia; es una bateria chica de pruebas que fuerce a cada herramienta a competir contra el flujo local. Si no mejora control, trazabilidad o velocidad sin romper privacidad, no merece entrar.

## pilot_priority

| Prioridad | Piloto | Herramientas candidatas | Por que primero | Output minimo |
|---:|---|---|---|---|
| P1 | Deck medico editable con fuentes | Codex + Presentations, 5.3, Pablo, opcional Claude/Opus, opcional NotebookLM | Alto valor profesional, riesgo controlable si usa tema no sensible y fuentes locales. | `brief.yaml`, `source_manifest.json`, `deck.pptx`, `render_contact_sheet.pdf`, `qa_report.md`. |
| P2 | Reels CMP visual truth gate | Codex, 5.3, Pablo, opcional Gemini/Nano Banana para fondos no clinicos | Impacta presencia publica diaria y evita errores de contacto/anatomia/placeholder. | `guion.md`, `storyboard.md`, `assets_manifest.json`, `visual_truth_gate.md`, `caption.md`. |
| P3 | Source pack trazable para tesis/medico-legal | 5.3, NotebookLM, Pablo | Reduce alucinacion y mejora decisiones con fuentes versionadas. | `source_manifest.json`, hashes/rutas, matriz de claims, exclusion log, `qa_traceability.md`. |

Pilotos descartados para esta tanda:

- Agents/browser-use sobre sitios vivos: utiles pero requieren permisos read-only y whitelist.
- Gamma/Tome/Canva-like: no hasta demostrar PPTX editable y citas limpias.
- Video IA/Sora: solo despues de resolver visual truth gate; no para anatomia factual.
- Automatizacion Make/Zapier/n8n: no antes de tener eventos, permisos y secretos resueltos.

## cost_privacy_matrix

| Opcion | Costo esperado | Privacidad | Esfuerzo | Decision |
|---|---:|---|---:|---|
| Codex + scripts locales | bajo/ya disponible | alto control local | medio | Adoptar como base. |
| 5.3 barato para extraccion/QA | bajo | alto si opera sobre repo local | bajo | Adoptar en validators y conteos. |
| Pablo XH | costo alto relativo | alto si solo lee bridge | bajo/medio | Usar para criterio, no para checks mecanicos. |
| Presentations/PPTX local | bajo/ya disponible | alto | medio | Base para deck. |
| NotebookLM | medio | medio, requiere source packs sanitizados | medio | Pilotear solo con fuentes no sensibles. |
| Claude/Opus | medio/alto | medio, depende de material | bajo | Pilotear narrativa con material sanitizado. |
| Gemini/Nano Banana | medio | medio, no subir datos sensibles | bajo | Pilotear assets no clinicos/fondos. |
| Gamma/Tome/Canva-like | medio | variable | bajo | No comprar todavia. |
| Browser/computer-use agents | variable | bajo/medio si navega fuera | alto | Pilotear luego read-only. |
| Make/Zapier/n8n | variable | bajo si toca credenciales | alto | Postergar. |

## success_metrics

| Piloto | Metricas de exito | Hard stop |
|---|---|---|
| Deck medico | `PPTX` editable, render/contact sheet sin solapes, 100% claims medicos trazados, tiempo total medido, notas internas ausentes. | Si no hay fuente o render QA, no se entrega. |
| Reels CMP | Contacto correcto `2364384321`, IG `@drcarloszanardi`, web correcta, sin placeholders, sin anatomia falsa, assets manifest completo. | Si falta material propio para el tema, no reemplazar con stock generico. |
| Source pack | Todas las fuentes con ruta, tipo, estado, hash si aplica, claim map y exclusion log; separa evidencia/opinion. | Si la fuente no es verificable o esta mezclada, queda fuera. |

Metricas transversales:

- Tiempo hasta primer borrador.
- Numero de correcciones humanas evitables.
- Numero de fallas detectadas por QA antes de entrega.
- Porcentaje de output reutilizable como template.
- Costo incremental cero o aprobado explicitamente.

## do_not_buy_yet

- No comprar deck tools cerradas si no exportan `PPTX` editable con fuentes/citas rastreables.
- No comprar visual/video IA para reemplazar material medico real.
- No conectar Make/Zapier/n8n a cuentas antes de tener politica de secretos, permisos y logs.
- No usar browser agents para acciones externas; solo read-only con whitelist por job.
- No adoptar una suite "todo en uno" si obliga a perder trazabilidad, artefactos locales o QA.

## next_actions

1. Codex principal crea carpeta local de piloto de presentaciones con `brief.yaml`, `source_manifest.json`, `outline.md`, `storyboard.md`, `deck.pptx`, `render_contact_sheet.pdf` y `qa_report.md`.
2. Ejecutar el mismo tema con flujo local primero; recien despues comparar una herramienta externa sobre el mismo brief.
3. Crear `visual_truth_gate.md` para el proximo reel CMP y aplicarlo antes de cualquier render/publicacion.
4. Armar un source pack chico de 10 fuentes no sensibles para NotebookLM o equivalente, con manifest y exclusion log.
5. Registrar costo, tiempo, fallas y decision `adopt/pilot/reject` en una tabla unica de herramientas.

## risks / limits

- No se verificaron precios ni features actuales porque el job prohibe acciones externas.
- La privacidad puede degradarse si alguien sube material clinico real sin sanitizar.
- Un piloto lindo pero no editable o no trazable no cuenta como exito.
- Si no hay tiempo para tres pilotos, hacer solo el deck medico: concentra fuente, narrativa, visual y QA.
- Ruta alternativa: si no se puede usar herramienta externa, el flujo local igual produce entregables validables.

## recommendation

Ejecutar primero el deck medico editable, porque obliga a probar lo mas importante: fuente, narrativa, assets, editabilidad y QA. En paralelo, preparar el gate de reels CMP como checklist local. No comprar membresias hasta que al menos uno de esos pilotos tenga medicion de tiempo, fallas y calidad.

## confidence

Alta para priorizacion y criterios porque deriva de resultados y frentes locales. Media para costo/herramientas comerciales porque no se consultaron planes actuales.

## evidence_paths

- `jobs/20260528T125752-ai-tools-pilot-prioritization.md`
- `results/20260525T122119-ai-tools-apps-skills-models-deep-v1.result.md`
- `context/youtube_content_packs/20260525-martell-maxmaxdata/`
- `context/fronts/presentaciones.md`
- `context/fronts/reels_cmp.md`
- `context/fronts/telegram.md`
