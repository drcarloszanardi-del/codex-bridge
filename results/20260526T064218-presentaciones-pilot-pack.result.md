# Resultado - 20260526T064218-presentaciones-pilot-pack

## summary honesto

Se define un pack piloto operativo para una presentacion medica premium, centrado en producir un PPTX/Google Slides editable con fuentes trazables y QA visual. No se creo deck real porque el job pide definicion del pack y no trae tema/material especifico.

**Evidencia:** el frente Presentaciones fija pipeline `objetivo -> narrativa -> storyboard -> visuales -> deck editable -> QA visual -> export`. El piloto previo recomienda PPTX editable, source pack, narrative pass, storyboard, render QA y medical source QA.

**Inferencia:** el pack debe impedir dos fallas: decks visualmente lindos pero no editables, y slides con claims medicos sin fuente/cita.

**Opinion:** la primera prueba debe ser un deck medico simple de 8-10 slides, no una clase enorme; el objetivo es probar el sistema, no ganar por volumen.

## coverage_table

| fuente | uso | limite |
| --- | --- | --- |
| `context/fronts/presentaciones.md` | Estado canonico, herramientas y gates. | No contiene proyecto concreto. |
| `results/20260525T122120-presentaciones-ai-pilot-premium-v1.result.md` | Pipeline, brief, folder structure, QA y decision de herramientas. | No creo deck real. |
| `results/20260525T112543-youtubers-auditoria-profunda-con-pack-obligatorio-v2.result.md` | Separacion conversacion/artefacto, ruteo por modelo y source packs versionados. | No debe copiar estilo de youtuber. |

## pilot_pack

Piloto recomendado: presentacion medica premium de 8-10 slides sobre un tema no sensible, por ejemplo `dolor lumbar: signos de alarma y cuando consultar`.

Entregables:

- `brief.yaml`
- `source_manifest.json`
- `outline.md`
- `storyboard.md`
- `visual_plan.md`
- `assets_manifest.json`
- `deck.pptx`
- `render_contact_sheet.pdf` o PNGs renderizados
- `qa_report.md`
- `exports/deck.pdf` solo si se pide

Definicion de terminado: PPTX editable, render QA revisado, claims medicos trazables, sin datos sensibles y sin notas internas visibles.

## brief_template

```yaml
presentation_brief:
  title:
  owner: "Dr. Carlos Zanardi / CMP"
  audience:
  duration_minutes:
  objective:
  decision_or_reaction_expected:
  clinical_context:
  must_include: []
  must_not_include: []
  tone: sobrio | academico | institucional | premium
  sources:
    - id:
      path_or_reference:
      status: official | paper | guideline | doctor_experience | draft | unverified
      allowed_for_slides: true
  visual_direction:
    palette:
    typography:
    imagery_allowed:
    imagery_forbidden:
  output:
    editable: pptx
    optional_export: pdf | none
  qa_required:
    - render_contact_sheet
    - no_overlap
    - source_traceability
    - sensitive_data_anonymized
    - editable_deck
```

## folder_structure

```text
presentations/<project_slug>/
  00_brief/
    brief.yaml
  01_sources/
    source_manifest.json
    files/
  02_narrative/
    outline.md
    speaker_notes.md
  03_storyboard/
    storyboard.md
    slide_table.csv
  04_visual_plan/
    visual_direction.md
    image_prompts.md
  05_assets/
    approved/
    generated/
    rejected/
    assets_manifest.json
  06_deck/
    <project_slug>.pptx
  07_render/
    contact_sheet.pdf
    slides_png/
  08_qa/
    qa_report.md
    source_traceability.md
  09_exports/
    <project_slug>.pdf
```

## qa_checklist

- Una idea dominante por slide.
- Titulo y jerarquia legibles en proyector y notebook.
- Sin texto solapado, clipping, cajas fuera de margen ni iconos flotando.
- PPTX editable: texto como texto, no capturas planas salvo imagenes.
- Fuentes/citas trazables para cada claim medico.
- Opinion/experiencia del Doctor separada de evidencia bibliografica.
- Datos sensibles anonimizados.
- Imagen generada solo decorativa/esquematica, no evidencia clinica factual.
- Notas internas fuera de slides visibles.
- Paleta y tipografia consistentes.
- Render/contact sheet revisado antes de entregar.

## membership_trigger

No pagar ni adoptar herramienta nueva solo por promesa visual. Activar prueba de membresia si cumple todo:

| herramienta | disparador valido |
| --- | --- |
| NotebookLM | Hay 5+ fuentes/papers y se necesita trazabilidad de citas. |
| Claude/Opus | El outline necesita segunda lectura narrativa premium o claridad metodologica. |
| Gemini/Nano Banana | Se requieren fondos/diagramas/variantes visuales no sensibles. |
| Gamma/Tome/Canva-like | Solo si exporta PPTX realmente editable, respeta citas y supera al pipeline local en QA. |

Regla: primero piloto local con Codex + Presentations; despues comparar herramientas externas con el mismo brief y la misma rubrica.

## risks_limits

- Sin tema/material especifico, esto es pack operativo, no deck final.
- Las capacidades/precios actuales de herramientas externas no fueron verificados por regla del job.
- En medicina, un deck atractivo sin trazabilidad es peor que un deck sobrio y correcto.
- IA visual no debe representar anatomia o resultados clinicos como prueba.

## recommendation

Ejecutar un piloto local de 8-10 slides con PPTX editable, source manifest y render QA. Solo despues decidir si conviene pagar o incorporar herramientas externas. El primer gate que debe bloquear entrega es: sin render QA o sin fuente para claims medicos, no se entrega.

## confidence

Alta para estructura, QA y criterios de fuente; media para decision de herramientas externas hasta probarlas con un caso real.

## evidence_paths

- `jobs/20260526T064218-presentaciones-pilot-pack.md`
- `context/fronts/presentaciones.md`
- `results/20260525T122120-presentaciones-ai-pilot-premium-v1.result.md`
- `results/20260525T112543-youtubers-auditoria-profunda-con-pack-obligatorio-v2.result.md`
