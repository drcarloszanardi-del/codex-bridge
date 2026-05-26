# Resultado - 20260526T064631-ai-tools-pilot-prioritization

## summary honesto

Se priorizan tres pilotos reales antes de comprar membresias o adoptar mas herramientas. No se verificaron precios actuales ni se hicieron acciones externas. La regla es simple: herramienta por funcion, piloto medible, material no sensible y decision posterior.

**Evidencia:** la matriz previa recomienda adoptar Codex/5.3/Pablo/Presentations, pilotear Claude/Opus, Gemini/Nano Banana y NotebookLM, y no comprar deck tools cerradas sin probar editabilidad.

**Inferencia:** los mejores pilotos son los que atraviesan frentes activos y reducen errores reales: presentaciones editables, source packs con citas y visuales CMP no sensibles.

**Opinion:** el peor gasto ahora seria pagar herramientas de deck/visual antes de saber si superan el pipeline local con QA.

## coverage_table

| fuente | uso | limite |
| --- | --- | --- |
| `results/20260525T122119-ai-tools-apps-skills-models-deep-v1.result.md` | Tool matrix, skills, pilots y reject hype log. | No verifica precios/capacidades actuales. |
| `context/youtube_content_packs/20260525-martell-maxmaxdata/` | Evidencia ya auditada: herramienta por funcion, artifacts, datos propios, visual con criterio. | No se reaudito archivo por archivo en este job. |

## pilot_priority

| prioridad | piloto | por que primero | salida medible |
| ---: | --- | --- | --- |
| 1 | Presentacion medica editable local | Alto impacto, bajo riesgo, usa stack ya disponible. | PPTX 8-10 slides + render QA + source traceability. |
| 2 | NotebookLM/source pack tesis o medico-legal | Mejora trazabilidad y reduce citas flojas. | 10 fuentes versionadas + matriz de claims/citas + QA. |
| 3 | Visual CMP con Gemini/Nano Banana en material no sensible | Reels/presentaciones necesitan assets premium, pero con truth gate. | 3 fondos/variantes no clinicas + QA visual + decision usar/no usar. |

No priorizar ahora: Gamma/Tome/Canva-like, Sora/video IA, Make/Zapier/n8n, browser agents con acciones. Van despues de resolver editabilidad, fuentes y privacidad.

## cost_privacy_matrix

| herramienta | costo antes de piloto | privacidad | esfuerzo | decision |
| --- | --- | --- | --- | --- |
| Codex + Presentations | bajo si ya disponible | local/controlado | medio | usar ya |
| NotebookLM | bajo/medio segun disponibilidad | requiere source pack sanitizado | medio | pilotear/adoptar con fuentes no sensibles |
| Claude/Opus | medio | no subir sensibles | bajo/medio | pilotear narrativa sanitizada |
| Gemini/Nano Banana | medio | usar no sensible/abstracto | medio | pilotear visual CMP |
| Gamma/Tome/Canva-like | incierto | riesgo de lock-in y editabilidad | bajo | no comprar aun |
| Make/Zapier/n8n | medio | credenciales/acciones externas | alto | postergar |
| Browser agents | bajo/medio | riesgo clicks/estado | alto | solo read-only futuro |

## success_metrics

- Presentaciones: PPTX editable, 0 solapes en render, 100% claims medicos con fuente o marca de opinion, entrega reproducible en carpeta.
- NotebookLM/source pack: 10 fuentes con origen/fecha/hash, matriz de claims, citas trazables, cero fuentes sensibles no autorizadas.
- Visual CMP: 3 assets utiles, 0 logos falsos, 0 anatomia factual generada, contacto CMP correcto, aprobado/rechazado por QA visual.
- Decision de membresia: se paga solo si mejora calidad/tiempo al menos 30% sin perder trazabilidad/editabilidad.

## do_not_buy_yet

- Deck tools que no exporten PPTX editable real.
- Stock/video/music sin pieza concreta aprobada.
- Automatizadores con credenciales o acciones externas.
- Browser/computer-use agents sin whitelist read-only.
- Modelos nuevos por hype sin benchmark contra una tarea del ecosistema Zanardi.

## next_actions

1. Ejecutar piloto de presentacion medica editable con carpeta `presentations/<slug>/`.
2. Preparar source pack NotebookLM con material no sensible y versionado.
3. Generar 3 visuales CMP abstractos/no clinicos y pasarlos por visual truth gate.
4. Registrar tiempo, calidad, retrabajo y riesgos por piloto.
5. Decidir membresias solo con evidencia comparativa.

## risks_limits

- Sin precios actuales, la matriz no decide compra; decide orden de prueba.
- Herramientas externas no deben recibir datos sensibles ni material clinico identificable.
- Un piloto exitoso en visual no habilita usar IA como evidencia medica.

## recommendation

Empezar por presentaciones editables y source packs. Dejar herramientas visuales como tercer piloto acotado. No comprar deck tools cerradas ni automatizadores hasta tener un caso que el pipeline local no pueda resolver.

## confidence

Alta para priorizacion relativa; media para costo real por falta de verificacion externa.

## evidence_paths

- `jobs/20260526T064631-ai-tools-pilot-prioritization.md`
- `results/20260525T122119-ai-tools-apps-skills-models-deep-v1.result.md`
- `context/youtube_content_packs/20260525-martell-maxmaxdata/`
