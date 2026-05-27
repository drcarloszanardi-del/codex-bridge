---
job_id: 20260527T004218-presentaciones-pilot-pack
worker: personal-xh
status: completed
completed_at: 2026-05-27T00:43:30-03:00
front: PRESENTACIONES
no_external_actions: true
no_secrets: true
---

# Resultado - Presentaciones pilot pack

## summary honesto

El pack piloto debe probar una cosa concreta: si podemos producir una
presentacion medica premium **editable**, trazable y visualmente revisada mejor
que el PPT artesanal. No conviene empezar pagando herramientas cerradas ni
generando slides vistosas sin fuente. El flujo correcto es: brief, source pack,
narrativa, storyboard, visual plan, PPTX editable, render QA y export.

Separacion pedida:

- Evidencia: el frente Presentaciones exige deck editable, QA visual y fuentes
  trazables.
- Inferencia: el primer piloto debe ser chico, 8-10 slides, para testear el
  sistema entero sin esconder errores bajo volumen.
- Opinion: un deck sobrio con fuentes y cero solapes vale mas que un deck
  espectacular pero no editable o sin citas.

No use acciones externas, no abri bibliotecas privadas, no toque credenciales y
no cree deck real porque el job pide pack operativo sin material especifico.

## coverage_table

| Fuente | Estado | Uso |
| --- | --- | --- |
| `jobs/20260527T004218-presentaciones-pilot-pack.md` | Revisada | Entregables, restricciones y criterio de terminado. |
| `context/fronts/presentaciones.md` | Revisada | Pipeline canonico, herramientas y gate. |
| `results/20260525T122120-presentaciones-ai-pilot-premium-v1.result.md` | Revisada | Pipeline, tool choices, brief template, folder structure y QA. |
| `results/20260525T112543-youtubers-auditoria-profunda-con-pack-obligatorio-v2.result.md` | Revisada | Separacion conversacion/artefacto, source packs y ruteo por modelo. |
| `results/20260526T064218-presentaciones-pilot-pack.result.md` | Revisada | Pack operativo previo y membership trigger. |

## pilot_pack

Piloto recomendado: deck medico premium de 8-10 slides sobre un tema no sensible,
por ejemplo `dolor lumbar: signos de alarma y cuando consultar`.

Entregables minimos:

- `brief.yaml`
- `source_manifest.json`
- `outline.md`
- `storyboard.md`
- `visual_direction.md`
- `assets_manifest.json`
- `deck.pptx`
- `render_contact_sheet.pdf` o `slides_png/`
- `qa_report.md`
- `source_traceability.md`
- `deck.pdf` solo si se pide export aparte

Definicion de terminado:

- PPTX editable abre sin errores.
- Texto sigue siendo texto editable, no capturas planas.
- Cada claim medico tiene fuente, cita o marca `doctor_experience`.
- Render/contact sheet revisado sin solapes, clipping ni texto fuera de margen.
- No hay datos sensibles ni notas internas visibles.

## brief_template

```yaml
presentation_brief:
  project_slug:
  title:
  owner: "Dr. Carlos Zanardi / Centro Medico Pellegrini"
  audience:
  duration_minutes:
  objective:
  decision_or_reaction_expected:
  clinical_context:
  must_include: []
  must_not_include: []
  tone: sobrio | academico | institucional | premium
  source_policy:
    claims_require_source: true
    doctor_experience_allowed: true
    unverified_claims_visible: false
  sources:
    - id:
      path_or_reference:
      status: official | paper | guideline | doctor_experience | draft | unverified
      allowed_for_slides: true
      citation_note:
  visual_direction:
    palette:
    typography:
    imagery_allowed:
    imagery_forbidden:
    generated_assets_allowed: decorative_only
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
- Titulo, cuerpo y cita legibles en proyector.
- Sin solapes, clipping, cajas fuera de margen ni iconos flotando.
- PPTX editable: texto como texto, graficos editables cuando sea razonable.
- Claims medicos trazables a fuente local, guideline, paper o experiencia del
  Doctor marcada como tal.
- Opinion/experiencia separada de evidencia bibliografica.
- Imagenes sin pacientes, HC, metadata sensible, nombres, fechas o interfaces
  clinicas identificables.
- Imagen generada solo decorativa o esquematica, nunca evidencia clinica.
- Notas internas fuera de slides visibles.
- Paleta, tipografia, margenes y componentes consistentes.
- Render/contact sheet revisado antes de entregar.

## membership_trigger

No pagar ni adoptar herramienta nueva por promesa visual. Activar prueba solo si
el piloto local ya existe y la herramienta se mide contra el mismo brief.

| Herramienta | Disparador valido | Hard stop |
| --- | --- | --- |
| NotebookLM | Hay 5+ fuentes y se necesita trazabilidad/citas. | No subir material sensible sin source pack sanitizado. |
| Claude/Opus | El outline necesita segunda lectura narrativa premium. | No reemplaza QA medico ni fuente. |
| Gemini/Nano Banana | Se requieren fondos, diagramas o variantes visuales no sensibles. | No usar anatomia generada como evidencia factual. |
| Gamma/Tome/Canva-like | Exporta PPTX realmente editable y supera render QA local. | Si no exporta editable, no sirve como flujo principal. |
| Stock/imagen/video pago | Falta un asset no sensible y hay decision del orquestador. | Worker no compra ni contacta. |

## risks / limits

- Este resultado define el pack; no certifica una herramienta externa ni crea
  una presentacion final.
- Capacidades/precios actuales no se verificaron por restriccion de no acciones
  externas.
- En medicina, un deck atractivo sin fuente puede aumentar riesgo, no calidad.
- El gate visual debe bloquear cualquier slide con datos sensibles o claims no
  trazables.

## recommendation

Proxima accion unica: ejecutar un piloto local de 8-10 slides con Codex +
Presentations usando tema no sensible, `brief.yaml`, `source_manifest.json`,
`deck.pptx` y render QA. Solo despues comparar herramientas externas. El primer
gate de bloqueo debe ser: **sin render QA o sin fuente para claims medicos, no se
entrega**.

## confidence

Alta para estructura, QA y criterios de fuente porque estan alineados con el
frente canonico y resultados previos. Media para decisiones de membresia hasta
probar herramientas con un caso real y material sanitizado.

## evidence_paths

- `jobs/20260527T004218-presentaciones-pilot-pack.md`
- `context/fronts/presentaciones.md`
- `results/20260525T122120-presentaciones-ai-pilot-premium-v1.result.md`
- `results/20260525T112543-youtubers-auditoria-profunda-con-pack-obligatorio-v2.result.md`
- `results/20260526T064218-presentaciones-pilot-pack.result.md`
