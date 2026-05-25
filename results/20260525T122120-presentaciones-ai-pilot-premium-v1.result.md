# Resultado - presentaciones AI pilot premium v1

Job: `20260525T122120-presentaciones-ai-pilot-premium-v1`
Worker: `personal-xh` / Pablo
Fecha: `2026-05-25`

## summary honesto

El piloto recomendado no reemplaza PPT por una herramienta magica. Reemplaza el proceso artesanal desordenado por una cadena controlada: brief estrategico, source pack, narrativa, storyboard, assets, deck editable, render QA y export. La entrega final debe seguir siendo PPTX/Google Slides editable salvo pedido distinto del Doctor.

## coverage_table

| Fuente | Estado | Uso |
|---|---|---|
| `jobs/20260525T122120-presentaciones-ai-pilot-premium-v1.md` | revisado | Objetivo y restricciones del piloto. |
| `context/fronts/presentaciones.md` | revisado | Estado canonico y gate de presentaciones. |
| `results/20260525T015500-mejoras-tesis-presentaciones-reels-cmp.result.md` | revisado | Pipeline previo de presentaciones/reels/tesis. |
| `results/20260525T112543-youtubers-auditoria-profunda-con-pack-obligatorio-v2.result.md` | revisado | Separacion conversacion/artefacto y ruteo por modelo. |
| `context/youtube_content_packs/20260525-martell-maxmaxdata/` | revisado por resultado previo | Base conceptual de tools/modelos/visual. |

## presentation_pipeline

1. `intake`: objetivo, audiencia, duracion, decision esperada, material disponible.
2. `source_pack`: papers/fallos/videos/imagenes autorizadas con origen y estado.
3. `narrative_pass`: tesis del deck, arco argumental, secciones, tono.
4. `storyboard`: slide por slide con una idea dominante.
5. `visual_plan`: diagramas, fondos, imagenes, tablas, iconos y assets.
6. `deck_editable`: crear PPTX/Google Slides editable con Presentations/Codex.
7. `render_qa`: exportar/contact sheet y revisar solapes, jerarquia, legibilidad.
8. `medical_source_qa`: claims medicos con fuente o marca de opinion/experiencia.
9. `final_export`: PPTX editable + PDF/video solo si se pide.

## tool_choices

| Paso | Herramienta primaria | Alternativa | Decision |
|---|---|---|---|
| Brief | Codex principal | 5.3 para limpiar input | Adoptar local. |
| Source pack | NotebookLM + Git | 5.3 extractor | Adoptar para decks con fuentes. |
| Narrativa | Claude/Opus o Pablo | Codex principal | Pilotear comparativa. |
| Storyboard | Pablo + Codex | Claude/Opus | Adoptar. |
| Visuales | Gemini/Nano Banana | Codex assets simples | Pilotear con assets no sensibles. |
| Deck editable | Codex + Presentations | PowerPoint manual | Adoptar. |
| QA render | Presentations/render + checklist | Capturas manuales | Adoptar obligatorio. |
| Herramientas tipo Gamma/Tome/Canva | Ninguna por defecto | Investigar | No pagar sin piloto de editabilidad. |

## brief_template

```yaml
presentation_brief:
  title:
  audience:
  duration_minutes:
  decision_or_reaction_expected:
  clinical_context:
  must_include:
  must_not_include:
  sources:
    - path_or_reference:
      status: official | paper | doctor_experience | draft | unverified
  visual_tone: sobrio | academico | premium | institucional
  output:
    editable: pptx | google_slides
    export: pdf | none
  qa_required:
    - render_contact_sheet
    - no_overlap
    - source_traceability
    - sensitive_data_anonymized
```

## folder_structure

```text
presentations/<project_slug>/
  00_brief/brief.yaml
  01_sources/source_manifest.json
  02_narrative/outline.md
  03_storyboard/storyboard.md
  04_assets/
    approved/
    generated/
    rejected/
  05_deck/<project_slug>.pptx
  06_render/contact_sheet.pdf
  07_qa/qa_report.md
  08_exports/
```

## qa_checklist

- Una idea por slide.
- Texto visible en proyector y celular.
- Sin solapamientos ni clipping en render.
- Citas o fuente local para claims medicos.
- Opinion/experiencia del Doctor separada de evidencia.
- Imagenes sin datos de pacientes ni metadata sensible.
- Fondos generados no representan anatomia como evidencia.
- Estilo consistente: titulos, tipografia, paleta, margenes.
- Notas internas fuera de slides visibles.
- Entrega final editable.

## pilot_candidate

Piloto recomendado: deck medico de 8-10 slides sobre `dolor lumbar / hernia discal / signos de alarma / cuando consultar`, porque permite probar contenido medico, visuales sobrios, fuente trazable y tono de CMP sin usar datos sensibles.

Entregables del piloto:

- `brief.yaml`
- `source_manifest.json`
- `outline.md`
- `storyboard.md`
- `deck.pptx`
- `contact_sheet.pdf`
- `qa_report.md`

## membership_decision

| Membresia/herramienta | Decision |
|---|---|
| NotebookLM | Usar si ya esta disponible; no subir fuentes sensibles sin criterio. |
| Claude/Opus | Pilotear narrativa con material sanitizado antes de pagar mas. |
| Gemini/Nano Banana | Pilotear assets abstractos/fondos; no anatomia factual. |
| Gamma/Tome/Canva-like | No pagar ahora. Primero exigir export editable, citas y control visual. |
| Stock/video/music | No comprar desde worker; orquestador decide si piloto lo justifica. |

## risks / limits

- No se creo deck real porque el job pide diseño de piloto y no trae material especifico.
- Sin rubrica local `docs/rubricas/presentaciones_ai_rubrica.md` en bridge; se usa gate de `context/fronts/presentaciones.md`.
- Si se usa herramienta externa cerrada puede perderse editabilidad o trazabilidad.
- Para decks medicos, imagenes generadas deben ser decorativas o esquematicas, no prueba clinica.

## recommendation

Ejecutar un piloto local primero con Codex + Presentations: 8-10 slides, fuente trazable, render QA y PPTX editable. Solo despues comparar con Claude/Opus para narrativa y Gemini/Nano Banana para visuales. No pagar herramienta de decks hasta que supere al pipeline local en calidad, editabilidad y trazabilidad.

## confidence

Alta para el pipeline y QA. Media para decision de herramientas externas porque no se verificaron precios/capacidades actuales por regla del job.

## evidence_paths

- `jobs/20260525T122120-presentaciones-ai-pilot-premium-v1.md`
- `context/fronts/presentaciones.md`
- `results/20260525T015500-mejoras-tesis-presentaciones-reels-cmp.result.md`
- `results/20260525T112543-youtubers-auditoria-profunda-con-pack-obligatorio-v2.result.md`
- `context/youtube_content_packs/20260525-martell-maxmaxdata/`
