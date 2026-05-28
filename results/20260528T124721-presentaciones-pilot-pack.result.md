---
job_id: 20260528T124721-presentaciones-pilot-pack
worker: personal-xh
status: completed
completed_at: 2026-05-28T12:47:48-03:00
front: PRESENTACIONES
no_external_actions: true
no_secrets: true
---

# Resultado - Presentaciones IA pack piloto operativo

## summary honesto

Se definio un pack piloto operativo para producir una presentacion medica premium editable, trazable y verificable. No se creo un deck real porque el job pide el pack operativo y no trae material medico especifico. La regla central se mantiene: la IA acelera narrativa, storyboard, assets y QA, pero la entrega confiable sigue siendo `PPTX` o Google Slides editable con render revisado y fuentes rastreables.

## coverage_table

| Seccion pedida | Estado | Evidencia usada |
|---|---|---|
| `pilot_pack` | cubierto | Pipeline canonico y resultados previos de presentaciones. |
| `brief_template` | cubierto | Template premium previo, ajustado a presentacion medica. |
| `folder_structure` | cubierto | Estructura operativa con brief, fuentes, storyboard, deck, render, QA y exports. |
| `qa_checklist` | cubierto | Gate canonico: render/contact sheet, no solapes, fuentes y datos sensibles. |
| `membership_trigger` | cubierto | Reglas para probar herramientas externas solo contra piloto local. |

## evidencia

- `context/fronts/presentaciones.md` fija entrega preferida como `PPTX`/Google Slides editable y pipeline: objetivo, narrativa, storyboard, visuales, deck editable, QA visual y export.
- `results/20260525T122120-presentaciones-ai-pilot-premium-v1.result.md` ya define brief, source pack, narrativa, storyboard, visual plan, deck editable, render QA y export.
- `results/20260525T112543-youtubers-auditoria-profunda-con-pack-obligatorio-v2.result.md` refuerza separacion entre conversacion, artefacto, source pack, modelo/herramienta y QA humano en temas medicos.
- Antecedentes de `presentaciones-pilot-pack` coinciden en no pagar herramientas cerradas antes de probar editabilidad, trazabilidad y render QA.

## inferencia

- El primer piloto debe ser chico, de 8-10 slides, porque permite detectar fallas de fuentes, layout, editabilidad y QA sin ocultarlas bajo volumen.
- El tema ideal debe ser medico pero no sensible, por ejemplo `dolor lumbar: signos de alarma y cuando consultar`.
- La herramienta externa solo merece entrar si mejora calidad/tiempo sin romper editabilidad, fuentes ni revision visual.

## opinion

La mejora importante no es que una IA "haga slides"; es que cada presentacion nazca con brief, fuentes, storyboard y QA, asi el Doctor no tenga que rescatar un PPT lindo pero clinicamente flojo o imposible de editar.

## pilot_pack

Piloto recomendado: deck medico premium de 8-10 slides sobre `Dolor lumbar: signos de alarma y cuando consultar`, sin pacientes reales ni datos sensibles.

### Entregables minimos

| Entregable | Proposito | Gate |
|---|---|---|
| `brief.yaml` | Define objetivo, audiencia, duracion, decision esperada y restricciones. | No avanzar si falta objetivo, audiencia o duracion. |
| `source_manifest.json` | Lista fuentes, estado y uso permitido. | Cada claim medico debe mapear a fuente o `doctor_experience`. |
| `outline.md` | Estructura narrativa y tesis del deck. | Debe tener arco claro y no mezclar objetivos. |
| `storyboard.md` | Slide por slide, una idea dominante. | Ninguna slide con dos mensajes principales. |
| `visual_direction.md` | Paleta, tipografia, imagenes permitidas/prohibidas. | Imagen generada solo decorativa o esquematica. |
| `assets_manifest.json` | Origen, licencia/estado y uso de cada asset. | Sin pacientes, metadatos sensibles ni assets dudosos. |
| `deck.pptx` | Entrega editable principal. | Texto editable; no capturas planas como deck. |
| `render_contact_sheet.pdf` o `slides_png/` | QA visual real. | Bloquea solapes, clipping y texto ilegible. |
| `qa_report.md` | Cierre de QA visual, medico y operativo. | Debe listar riesgos residuales. |
| `source_traceability.md` | Mapa slide/claim/fuente. | Bloquea claims no trazables. |

### Definicion de terminado

- `deck.pptx` abre sin errores y mantiene elementos editables.
- Render/contact sheet revisado.
- Sin solapamientos, clipping, cajas fuera de margen ni notas internas visibles.
- Cada claim medico tiene fuente local, guideline/paper o marca `doctor_experience`.
- Datos sensibles ausentes o anonimizados.
- Estilo visual consistente con audiencia y tono medico premium.

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
  narrative:
    main_thesis:
    sections:
      - name:
        message:
        expected_slide_count:
  visual_direction:
    palette:
    typography:
    imagery_allowed:
    imagery_forbidden:
    generated_assets_allowed: decorative_or_schematic_only
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
  04_visual_direction/
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
- Titulo, cuerpo, cita y pie legibles en proyector y en captura reducida.
- Sin solapes, clipping, texto fuera de margen, iconos flotando ni layouts rotos.
- `PPTX` editable: texto como texto; tablas/graficos editables cuando sea razonable.
- Claims medicos trazables a fuente local, guideline, paper o experiencia del Doctor marcada como tal.
- Opinion/experiencia separada de evidencia bibliografica.
- Imagenes sin pacientes, historias clinicas, nombres, fechas, interfaces identificables ni metadata sensible.
- Imagen generada solo decorativa o esquematica, nunca evidencia clinica factual.
- Paleta, tipografia, margenes y componentes consistentes.
- Notas internas fuera de slides visibles.
- Render/contact sheet revisado antes de entregar.
- `source_traceability.md` revisado contra el deck final.

## membership_trigger

Regla: no pagar ni adoptar herramienta nueva por promesa visual. Primero se ejecuta el piloto local; despues cada herramienta compite contra el mismo brief, source pack y QA.

| Herramienta/membresia | Disparador valido | Hard stop |
|---|---|---|
| NotebookLM | Hay varias fuentes y se necesita trazabilidad/citas. | No subir material sensible sin source pack sanitizado. |
| Claude/Opus | El outline necesita segunda lectura narrativa premium. | No reemplaza QA medico ni `source_traceability.md`. |
| Gemini/Nano Banana | Se necesitan fondos, variantes visuales o esquemas no sensibles. | No usar anatomia generada como evidencia factual. |
| Gamma/Tome/Canva-like | Exporta `PPTX` realmente editable y supera render QA local. | Si no exporta editable, no sirve como flujo principal. |
| Stock/imagen/video pago | Falta un asset no sensible y el orquestador autoriza. | El worker no compra ni contacta. |

Decision sugerida: activar comparativa externa solo cuando exista un `deck.pptx` local con `qa_report.md` y `source_traceability.md`; si la herramienta no mejora tiempo/calidad sin perder control, queda descartada.

## risks_limits

- Este resultado define el pack operativo; no certifica ninguna herramienta externa ni crea una presentacion final.
- No se verificaron precios, features actuales ni terminos de herramientas por restriccion de no acciones externas.
- En medicina, un deck atractivo sin fuente puede aumentar riesgo, no calidad.
- La trazabilidad slide por slide puede degradarse con ediciones de ultimo momento si no se revalida despues del render.
- Ruta alternativa si falta fuente: quitar el claim o marcarlo como `doctor_experience`; no inventar bibliografia.
- Ruta alternativa si falla el render: entregar solo outline/storyboard y dejar el `PPTX` como no aprobado hasta corregir.

## recommendation

Proxima accion unica: que Codex principal ejecute un piloto local de 8-10 slides con tema no sensible, usando `brief.yaml`, `source_manifest.json`, `deck.pptx`, `render_contact_sheet.pdf` y `qa_report.md`. El gate de bloqueo debe ser: sin render QA o sin fuente para claims medicos, no se entrega.

## confidence

Alta para estructura, QA y criterios de fuente porque salen del frente canonico y de resultados previos. Media para decisiones de membresia porque requieren prueba real con herramienta actual y material sanitizado.

## evidence_paths

- `jobs/20260528T124721-presentaciones-pilot-pack.md`
- `context/fronts/presentaciones.md`
- `results/20260525T122120-presentaciones-ai-pilot-premium-v1.result.md`
- `results/20260525T112543-youtubers-auditoria-profunda-con-pack-obligatorio-v2.result.md`
- `results/20260527T184425-presentaciones-pilot-pack.result.md`
