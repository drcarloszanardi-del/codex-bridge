# Resultado - AI tools apps skills models deep v1

Job: `20260525T122119-ai-tools-apps-skills-models-deep-v1`
Worker: `personal-xh` / Pablo
Fecha: `2026-05-25`

## summary honesto

La matriz accionable no recomienda comprar mas herramientas por novedad. Recomienda ordenar funciones: Codex para repo/automatizacion/orquestacion, 5.3 para extraccion barata, Pablo para segunda mirada XH, Claude/Opus para narrativa larga y artifacts, Gemini/Nano Banana para visuales, NotebookLM para fuentes trazables, y agentes/browser-use solo con permisos read-only. Del paquete youtubers se extrae un principio fuerte: herramienta por funcion, no por marca.

## source_counts

| Fuente | Archivos revisados | Uso |
|---|---:|---|
| `jobs/20260525T122119-ai-tools-apps-skills-models-deep-v1.md` | 1 | Preguntas CEO y contrato del job. |
| `results/20260525T112543-youtubers-auditoria-profunda-con-pack-obligatorio-v2.result.md` | 1 | Auditoria profunda del paquete Martell/Maxmaxdata. |
| `context/youtube_content_packs/20260525-martell-maxmaxdata/` | 98 | Paquete fuente ya auditado: VTT, SRT, JSONL, MD y metadata. |
| `context/fronts/presentaciones.md` | 1 | Estado canonico para herramientas de presentaciones. |
| `context/fronts/telegram.md` | 1 | Deuda activa: ArtifactDraft, ResultContract, ContextBinder. |
| `context/fronts/reels_cmp.md` | 1 | Gate visual y datos publicables CMP. |

## tool_matrix

| Herramienta / motor | Decision | Funcion donde gana | Frente | Riesgo | Piloto sugerido | Prioridad |
|---|---|---|---|---|---|---|
| Codex principal | adopt | Orquestacion, repo, scripts, bridge, integracion y decision final | Todos | Sobrecarga si hace todo | Mantener como router + integrador, no worker unico | P0 |
| `gpt-5.3-codex` | adopt | Extraccion, parsing, conteos, OCR, fixtures simples, QA mecanico | Bridge, clinica, radares | Cerrar sin criterio estrategico | Rutina diaria de barridos + validator | P0 |
| Pablo / `personal-xh` | adopt | Segunda mirada, sintesis profunda, arquitectura, riesgo, premium creative QA | Todos | Usarlo para healthchecks baratos | Solo jobs 10-80-10 con criterio alto | P0 |
| Claude/Opus | pilot | Narrativa larga, artifacts, reescritura, metodologia, documentos extensos | Presentaciones, tesis, docs | Subir material sensible fuera de control | 1 deck medico + 1 memo tesis con fuente sanitizada | P1 |
| Gemini/Nano Banana | pilot | Visuales, fondos, variaciones, analisis de imagen/video no sensible | Reels, presentaciones | Visual medico falso o con datos privados | 3 assets CMP abstractos + QA visual truth | P1 |
| NotebookLM | adopt/pilot | Q&A con source packs, tesis, corpus, citas trazables | Tesis, medico-legal | Mezclar fuentes no versionadas | 1 source pack de 10 PDFs/fuentes oficiales | P1 |
| Presentations plugin / PPTX editable | adopt | Construir deck editable verificable | Presentaciones | Deck lindo pero no editable si se usa otra herramienta | Pipeline local brief -> deck -> render QA | P0 |
| Make/Zapier/n8n | pilot later | Automatizar flujos repetibles entre apps | Telegram, ops | Acciones externas/credenciales | Solo diseño read-only; no conectar cuentas aun | P2 |
| Browser/computer-use agents | pilot guarded | Revisar interfaces, dashboards, fuentes publicas | Radares, QA | Clicks no autorizados | Modo read-only con whitelist por job | P2 |
| Sora/video IA | pilot limited | Storyboard/b-roll conceptual | Reels/presentaciones | Confundir visual generado con realidad clinica | Fondos abstractos y transiciones, no anatomia factual | P2 |
| DeepSeek/local/open models | investigate | Costo bajo, privacidad/local, comparacion tecnica | Ops/codigo | Calidad variable, compliance | Benchmark offline con tareas no sensibles | P3 |
| Gamma/Tome/Canva-like deck tools | investigate/reject for now | Velocidad visual | Presentaciones | Perder editabilidad/citas/control | No pagar hasta comparar con PPTX editable local | P3 |

## skills_to_build

| Skill | Que hace | Input | Output | Owner sugerido |
|---|---|---|---|---|
| `brief_compiler` | Convierte orden cruda en brief 10-80-10 | Telegram/job/manual | `brief.md` con rol/contexto/tarea/output/evidencia | 5.3 + principal |
| `artifact_draft` | Separa conversacion, borrador, asset plan y entrega | Brief + assets | Draft versionado antes de publicar/enviar | principal |
| `visual_truth_gate_cmp` | Revisa claims, anatomia, contacto y placeholders | Reel/storyboard/assets | Checklist pass/fail | Pablo + 5.3 |
| `result_contract_validator_plus` | Falla resultados sin evidencia/backlog/riesgos | Result markdown | OK/FAIL con faltantes | 5.3 |
| `youtube_pack_auditor` | Cuenta, deduplica y extrae coverage de paquetes | `context/youtube_content_packs/*` | coverage/source_counts/exclusion_log | 5.3 |
| `doctor_correction_capture` | Convierte correcciones del Doctor en fixtures | Correccion textual | Test/gate/checklist | Pablo define, 5.3 implementa |
| `presentation_brief_to_deck` | Pasa de brief a deck editable con QA visual | Brief + fuentes | PPTX/Google Slides editable | Codex + Presentations |
| `radar_anti_empty_validator` | Impide reportes vacios | Radar result | score/status | 5.3 |

## subagents_to_add_or_refine

| Subagente | Estado | Funcion | Trigger | No debe hacer |
|---|---|---|---|---|
| `Extractor 5.3` | existe/refinar | Limpia fuentes, tablas, OCR, dedup | Jobs con mucha materia prima | Decidir estrategia final |
| `Pablo XH` | existe | Segunda mirada, arquitectura, premium QA | Jobs complejos o idle queue | Acciones externas |
| `Visual QA CMP` | agregar | Revisa reels/presentaciones visuales | Antes de publicar/entregar | Inventar assets clinicos |
| `Clinical Gate Builder` | agregar/refinar | Convierte correcciones en fixtures | Correccion del Doctor | Crear criterio clinico nuevo |
| `Radar Scout 5.3` | agregar/refinar | Barridos y scorecards | Radares recurrentes | Cerrar vacio sin gate |
| `Presentation Producer` | agregar | Brief -> narrativa -> deck editable | Deck medico/tesis | Export final sin render QA |
| `Source Pack Librarian` | agregar | Prepara fuentes para NotebookLM/tesis | Tesis/corpus | Mezclar fuentes no oficiales |

## models_by_function

| Funcion | Motor primario | Segundo paso | Motivo |
|---|---|---|---|
| Repo/scripts/bridge | Codex principal | Pablo para review | Codex entiende workspace y puede commitear. |
| Extraccion masiva | 5.3 | Pablo si hay ambiguedad | Bajo costo y suficiente para parsing. |
| Sintesis estrategica | Pablo XH | Codex principal decide | Requiere criterio y riesgo. |
| Narrativa larga/deck/memo | Claude/Opus o Codex | Pablo review | Mejor para estructura extensa y claridad. |
| Visuales/fondos/imagen | Gemini/Nano Banana | Visual truth gate | Mejor funcion visual/multimodal. |
| Fuentes/citas | NotebookLM | Codex/Pablo interpretan | Grounding por source pack. |
| Browser/read-only | Browser/computer-use agent | Codex principal autoriza | Solo con whitelist y sin acciones externas. |

## presentation_tools_review

| Opcion | Decision | Uso |
|---|---|---|
| Codex + Presentations/PPTX local | adoptar | Base por editabilidad, control y QA render. |
| Claude/Opus para narrativa | pilot | Mejorar historia, estructura y lenguaje medico. |
| Gemini/Nano Banana para assets | pilot | Fondos, esquemas visuales no clinicos, variaciones. |
| NotebookLM | pilot/adopt | Decks con papers/fallos: fuente trazable. |
| Gamma/Tome/Canva-like | investigar mas | No pagar hasta demostrar PPTX editable, citas y export limpio. |
| Video AI | pilot limitado | Aperturas/fondos, no contenido medico factual. |

## pilot_plan

1. Presentacion medica: tomar un tema real, hacer source pack, brief, narrativa, deck editable y QA render.
2. Reels CMP: tres fondos/variantes visuales con datos correctos y visual truth gate.
3. Tesis: NotebookLM con 10 fuentes versionadas y matriz bibliografica.
4. Radares: 5.3 ejecuta barrido con anti-empty gate; Pablo solo revisa `needs_review`.
5. Clinica: 5 correcciones nuevas del Doctor pasan a fixtures antes de tocar plantilla.

## reject_hype_log

| Hype | Decision | Razon |
|---|---|---|
| "Reemplazar equipo por agentes" | reject | El paquete lo marca como mal consejo; mejorar equipo, no sustituir criterio. |
| "Una tool para todo" | reject | Ruteo por funcion supera fanatismo de modelo. |
| "Deck automatico no editable" | reject for now | El Doctor necesita deck editable y control medico. |
| "IA visual como evidencia medica" | reject | Alto riesgo medico/legal. |
| "Comprar membresias antes de piloto" | reject | Primero pilotos locales con material no sensible. |

## implementation_backlog

| Accion | Responsable | Criterio de terminado | Prioridad |
|---|---|---|---|
| Escribir `docs/model_routing_policy.md` | Pablo | Tabla funcion/modelo/riesgo aprobada | P0 |
| Implementar `artifact_draft` schema | Codex principal | Drafts versionados en 3 frentes | P0 |
| Crear piloto deck medico editable | principal + Pablo | PPTX renderizado sin solapes | P1 |
| Probar Gemini/Nano Banana con fondos CMP | principal | 3 fondos abstractos aprobados | P1 |
| Crear source pack NotebookLM tesis | 5.3 | 10 fuentes con hash y resumen | P1 |
| Benchmark Claude/Opus vs Codex para narrativa | Pablo | Comparativa 1 deck/1 memo | P2 |

## risks / limits

- No se navego ni se verificaron planes/precios actuales por prohibicion del job.
- La matriz inicial de Mac de trabajo `../docs/ai_tools_operating_matrix_youtubers_2026-05-25.md` no aparece en este repo; se uso equivalente: auditoria y contextos del bridge.
- Las decisiones de membresia requieren piloto real y aprobacion del orquestador.
- Herramientas visuales no deben tocar datos clinicos identificables.

## recommendation

Adoptar ahora: Codex principal, 5.3, Pablo, Presentations/PPTX local, NotebookLM con source packs. Pilotear: Claude/Opus para narrativa, Gemini/Nano Banana para assets, browser agents read-only. Rechazar por ahora: deck tools cerradas/no editables y cualquier membresia sin piloto medible.

## confidence

Alta para ruteo funcional y backlog, porque deriva de la auditoria local completa. Media para herramientas comerciales externas no verificadas en vivo.

## evidence_paths

- `jobs/20260525T122119-ai-tools-apps-skills-models-deep-v1.md`
- `results/20260525T112543-youtubers-auditoria-profunda-con-pack-obligatorio-v2.result.md`
- `context/youtube_content_packs/20260525-martell-maxmaxdata/`
- `context/fronts/presentaciones.md`
- `context/fronts/telegram.md`
- `context/fronts/reels_cmp.md`
