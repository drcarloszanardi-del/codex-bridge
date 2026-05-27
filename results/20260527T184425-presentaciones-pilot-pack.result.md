---
job_id: 20260527T184425-presentaciones-pilot-pack
worker: personal-xh
status: completed
completed_at: 2026-05-27T18:45:32-03:00
front: PRESENTACIONES
no_external_actions: true
no_secrets: true
---

# Resultado - Presentaciones IA pack piloto operativo

## summary honesto

El pack piloto viable para una presentacion medica premium no es "usar IA para
hacer slides lindas". Es un contrato operativo: brief cerrado, source pack
trazable, narrativa, storyboard, direccion visual, PPTX editable, render QA y
gate medico antes de entregar. El deck final debe seguir siendo editable y
auditable; la IA sirve para acelerar el proceso y subir el estandar, no para
saltear fuentes ni revision humana.

Separacion pedida:

- Evidencia: `context/fronts/presentaciones.md` exige PPTX/Google Slides editable,
  pipeline por etapas, QA visual y fuentes/citas trazables.
- Inferencia: el piloto debe ser chico, 8-10 slides, porque ahi se ve si el
  sistema sostiene editabilidad, trazabilidad y estetica sin esconder fallas.
- Opinion: conviene medir cualquier membresia o herramienta externa contra este
  pack local; si no supera editabilidad, citas y render QA, no merece entrar al
  flujo principal.

No use acciones externas, no abri Gmail/Drive/Telegram/Calendar, no toque
credenciales y no cree una presentacion real porque el job pide el pack operativo
sin material medico especifico.

## coverage_table

| Fuente | Estado | Uso |
| --- | --- | --- |
| `jobs/20260527T184425-presentaciones-pilot-pack.md` | Revisada | Objetivo, restricciones, entregables y criterio de terminado. |
| `context/fronts/presentaciones.md` | Revisada | Estado canonico, pipeline, herramientas y gate de presentaciones. |
| `results/20260525T122120-presentaciones-ai-pilot-premium-v1.result.md` | Revisada | Pipeline base, template de brief, folder structure y QA inicial. |
| `results/20260525T112543-youtubers-auditoria-profunda-con-pack-obligatorio-v2.result.md` | Revisada | 10-80-10, separacion conversacion/artefacto, source packs, ruteo por modelo y gate visual medico. |
| `results/20260527T004218-presentaciones-pilot-pack.result.md` | Revisada como antecedente local | Pack operativo previo para evitar regresion y afinar disparadores de membresia. |

## pilot_pack

Objetivo del piloto: producir una presentacion medica premium de 8-10 slides,
editable y trazable, sobre un tema no sensible. Tema sugerido: `dolor lumbar:
signos de alarma y cuando consultar`. Evita pacientes reales, permite probar
claims medicos y no exige imagenes clinicas identificables.

Entregables minimos:

| Entregable | Proposito | Gate |
| --- | --- | --- |
| `brief.yaml` | Alinear audiencia, objetivo, tono, restricciones y output. | No avanzar si falta audiencia, duracion u objetivo. |
| `source_manifest.json` | Listar fuentes, estado y uso permitido. | Cada claim medico debe mapear a fuente o `doctor_experience`. |
| `outline.md` | Narrativa y secciones. | Una tesis clara y arco logico. |
| `storyboard.md` | Slide por slide, una idea dominante por slide. | Ninguna slide mezcla dos mensajes principales. |
| `visual_direction.md` | Paleta, tipografia, imagenes permitidas/prohibidas. | IA visual solo decorativa o esquematica, no evidencia clinica. |
| `assets_manifest.json` | Origen, licencia/estado y uso de cada asset. | Sin pacientes, metadatos sensibles ni imagenes dudosas. |
| `deck.pptx` | Entrega editable. | Texto como texto; no capturas planas como sustituto del deck. |
| `render_contact_sheet.pdf` o `slides_png/` | QA visual real. | Bloquea si hay solapes, clipping o texto ilegible. |
| `qa_report.md` | Cierre de QA y riesgos residuales. | Debe incluir fuente, visual, editabilidad y datos sensibles. |
| `source_traceability.md` | Mapa claim -> fuente -> slide. | Bloquea claims no trazables. |

Definicion de terminado:

- PPTX abre sin errores y mantiene elementos editables.
- Render/contact sheet revisado.
- Sin solapamientos, clipping, texto fuera de margen ni notas internas visibles.
- Claims medicos trazables a fuente local, guideline, paper o experiencia del
  Doctor marcada como tal.
- Datos sensibles anonimizados o ausentes.
- Estilo consistente con audiencia medica premium.

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
- Titulo y cuerpo legibles en proyector y en captura reducida.
- Sin solapes, clipping, cajas fuera de margen ni elementos flotantes.
- PPTX editable: texto como texto; graficos editables cuando sea razonable.
- Cada claim medico tiene fuente, cita o marca `doctor_experience`.
- Opinion/experiencia separada de evidencia bibliografica.
- Imagenes sin pacientes, historias clinicas, nombres, fechas, interfaces
  identificables o metadata sensible.
- Imagen generada solo decorativa o esquematica, nunca evidencia clinica.
- Paleta, tipografia, margenes y componentes consistentes.
- Notas internas fuera de slides visibles.
- Render/contact sheet revisado antes de entregar.
- `source_traceability.md` revisado contra el deck final.

## membership_trigger

Regla: no comprar ni adoptar herramienta nueva por promesa visual. Primero se
ejecuta el piloto local; despues cada herramienta compite contra el mismo brief,
source pack y QA.

| Herramienta/membresia | Disparador valido | Hard stop |
| --- | --- | --- |
| NotebookLM | Hay varias fuentes y se necesita trazabilidad/citas. | No subir material sensible sin source pack sanitizado. |
| Claude/Opus | El outline necesita segunda lectura narrativa premium. | No reemplaza QA medico ni source traceability. |
| Gemini/Nano Banana | Se necesitan fondos, variantes visuales o esquemas no sensibles. | No usar anatomia generada como evidencia factual. |
| Gamma/Tome/Canva-like | Exporta PPTX realmente editable y supera render QA local. | Si no exporta editable, no sirve como flujo principal. |
| Stock/imagen/video pago | Falta un asset no sensible y el orquestador autoriza. | El worker no compra ni contacta. |

Decision sugerida: activar comparativa externa solo cuando exista un
`deck.pptx` local con `qa_report.md` y `source_traceability.md`; si la herramienta
no mejora tiempo/calidad sin perder control, queda descartada.

## risks / limits

- Este resultado define el pack operativo; no certifica ninguna herramienta
  externa ni crea una presentacion final.
- No se verificaron precios, features actuales ni terminos de herramientas por
  restriccion de no acciones externas.
- En medicina, un deck atractivo sin fuente puede subir el riesgo operativo.
- El punto mas fragil es la trazabilidad slide por slide: si queda manual, se
  puede degradar con cambios de ultima hora.
- Ruta alternativa si falta fuente: mantener el claim fuera del deck o marcarlo
  como `doctor_experience`; no inventar bibliografia.
- Ruta alternativa si falla el render: entregar solo outline/storyboard y dejar
  el PPTX como no aprobado hasta corregir.

## recommendation

Proxima accion unica: que Codex principal ejecute un piloto local de 8-10 slides
con el tema no sensible sugerido, usando `brief.yaml`, `source_manifest.json`,
`deck.pptx`, `render_contact_sheet.pdf` y `qa_report.md`. El gate que debe
bloquear entrega es: sin render QA o sin fuente para claims medicos, no se
entrega.

## confidence

Alta para estructura, QA y criterios de fuente porque salen del frente canonico
y de resultados previos. Media para decisiones de membresia porque requieren
prueba real con herramienta actual y material sanitizado.

## evidence_paths

- `jobs/20260527T184425-presentaciones-pilot-pack.md`
- `context/fronts/presentaciones.md`
- `results/20260525T122120-presentaciones-ai-pilot-premium-v1.result.md`
- `results/20260525T112543-youtubers-auditoria-profunda-con-pack-obligatorio-v2.result.md`
- `results/20260527T004218-presentaciones-pilot-pack.result.md`
- `claims/20260527T184425-presentaciones-pilot-pack.json`
