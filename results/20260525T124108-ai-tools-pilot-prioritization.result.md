# Resultado - AI tools pilot prioritization

Job: `20260525T124108-ai-tools-pilot-prioritization`
Worker: `personal-xh` / Pablo
Fecha: `2026-05-25`

## summary honesto

Los pilotos deben probar valor antes de membresias. La prioridad es: 1) deck medico editable con pipeline local, 2) visuales CMP no sensibles con Gemini/Nano Banana bajo QA, 3) source pack NotebookLM para tesis/corpus. Claude/Opus queda como comparativa de narrativa, no compra automatica. Herramientas de decks cerradas y automatizaciones tipo Make/Zapier/n8n no deben comprarse todavia.

## source_counts

| Fuente | Archivos revisados | Uso |
|---|---:|---|
| `jobs/20260525T124108-ai-tools-pilot-prioritization.md` | 1 | Contrato del job. |
| `results/20260525T122119-ai-tools-apps-skills-models-deep-v1.result.md` | 1 | Matriz de herramientas, skills y modelos. |
| `context/youtube_content_packs/20260525-martell-maxmaxdata/` | 98 | Paquete fuente ya auditado en profundidad. |
| `context/fronts/presentaciones.md` | 1 | Gate de deck editable y QA render. |
| `context/fronts/reels_cmp.md` | 1 | Gate visual CMP y datos publicables. |

## pilot_priority

| Prioridad | Piloto | Por que primero | Output esperado | Owner |
|---|---|---|---|---|
| P0 | Presentacion medica editable | Alto impacto, bajo riesgo, usa herramientas locales; valida si superamos PPT artesanal | PPTX editable + contact sheet + QA | Codex principal + Presentations + Pablo review |
| P1 | Visuales CMP abstractos | Mejora reels/presentaciones sin tocar datos sensibles | 3 fondos/variantes aprobadas por visual truth gate | Gemini/Nano Banana + Pablo QA |
| P1 | NotebookLM source pack | Tesis/corpus necesitan citas trazables y menos alucinacion | 10 fuentes versionadas + matriz bibliografica | 5.3 + NotebookLM + Pablo |
| P2 | Claude/Opus narrativa | Puede mejorar claridad, pero requiere material sanitizado | Comparativa outline vs Codex/Pablo | Orquestador |
| P3 | Browser/read-only agents | Util para radares pero mayor riesgo operacional | Prueba read-only con whitelist | Codex principal |

## cost_privacy_matrix

| Piloto | Costo incremental | Privacidad | Esfuerzo | Riesgo | Decision |
|---|---|---|---|---|---|
| Deck local editable | Bajo | Alto control local | Medio | Bajo | Hacer ya |
| Visuales CMP abstractos | Bajo/medio | Sin datos sensibles si se controla input | Bajo | Medio | Hacer con QA |
| NotebookLM source pack | Bajo/medio | Depende de fuentes; usar no sensibles/versionadas | Medio | Medio | Hacer con fuentes sanitizadas |
| Claude/Opus narrativa | Medio | Material debe estar sanitizado | Bajo | Medio | Comparar, no comprar por defecto |
| Gamma/Tome/Canva-like | Desconocido | Riesgo de subida/export cerrado | Medio | Alto | No comprar aun |
| Make/Zapier/n8n | Puede escalar | Credenciales/acciones externas | Alto | Alto | Postergar |

## success_metrics

| Piloto | Metrica de exito | Umbral |
|---|---|---|
| Deck medico | Editable, sin solapes, una idea por slide, fuentes trazables | 8-10 slides aprobadas sin rehacer estructura |
| Visuales CMP | No datos sensibles, no anatomia factual falsa, mejora estetica | 3 assets pasan QA y sirven en reel/deck |
| NotebookLM | Citas correctas, source pack limpio, matriz reutilizable | 10 fuentes con hash/estado/resumen y respuestas citadas |
| Claude/Opus | Mejora narrativa medible | Outline mejor que local en claridad sin perder fuentes |

## do_not_buy_yet

- Herramientas de deck cerradas que no exporten PPTX editable limpio.
- Automatizadores con credenciales o acciones externas.
- Video IA para anatomia o escenas medicas factuales.
- Membresias cuyo valor no supere el pipeline local en un piloto real.
- Cualquier tool que requiera subir datos clinicos identificables.

## next_actions

1. Codex principal crea job de piloto deck lumbar 8-10 slides.
2. 5.3 arma source pack minimo no sensible.
3. Presentations genera PPTX editable y contact sheet.
4. Pablo revisa narrativa/QA premium.
5. Orquestador decide si Claude/Opus o Gemini/Nano Banana aportan mejora real.

## risks / limits

- No se verificaron precios actuales por prohibicion de navegar/comprar.
- La privacidad depende del material que se suba a cada herramienta.
- El piloto debe usar material no sensible; nada de pacientes ni HC.
- El costo real solo se decide luego de comparar outputs.

## recommendation

Ejecutar primero el piloto de presentacion medica editable. Es el de mayor retorno y menor riesgo. En paralelo, probar visuales CMP abstractos solo con material no sensible. Postergar compras hasta que esos pilotos demuestren mejora contra Codex + Presentations local.

## confidence

Alta para la priorizacion relativa. Media para costos externos porque no se consultaron precios actuales.

## evidence_paths

- `jobs/20260525T124108-ai-tools-pilot-prioritization.md`
- `results/20260525T122119-ai-tools-apps-skills-models-deep-v1.result.md`
- `context/youtube_content_packs/20260525-martell-maxmaxdata/`
- `context/fronts/presentaciones.md`
- `context/fronts/reels_cmp.md`

