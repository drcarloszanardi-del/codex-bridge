# Resultado - presentaciones pilot pack

Job: `20260525T123025-presentaciones-pilot-pack`
Worker: `personal-xh` / Pablo
Fecha: `2026-05-25`

## summary honesto

El pack piloto debe producir una presentacion medica premium editable sin depender de membresias nuevas. La prueba real debe medir si el pipeline supera PPT artesanal en narrativa, visual, trazabilidad y QA. No se debe comprar ni subir material privado; primero se arma un pack local con brief, fuentes sanitizadas, storyboard, PPTX editable y render QA.

## source_counts

| Fuente | Archivos revisados | Uso |
|---|---:|---|
| `jobs/20260525T123025-presentaciones-pilot-pack.md` | 1 | Contrato del pack piloto. |
| `context/fronts/presentaciones.md` | 1 | Estado canonico y gate. |
| `results/20260525T122120-presentaciones-ai-pilot-premium-v1.result.md` | 1 | Pipeline, tool choices, brief, folder structure. |
| `results/20260525T112543-youtubers-auditoria-profunda-con-pack-obligatorio-v2.result.md` | 1 | Ruteo de modelos y separacion artefacto/entrega. |

## pilot_pack

Tema sugerido: `Dolor lumbar: signos de alarma, hernia discal y cuando consultar`.

Entregables:

- `brief.yaml`
- `source_manifest.json`
- `outline.md`
- `storyboard.md`
- `visual_direction.md`
- `deck.pptx`
- `contact_sheet.pdf`
- `qa_report.md`

Medicion de exito:

- Deck editable.
- 8-10 slides.
- Una idea por slide.
- Claims medicos trazables o marcados como experiencia/opinion.
- Render sin solapes.
- Tiempo de produccion menor al artesanal.
- Aprobacion del Doctor sin rehacer estructura desde cero.

## brief_template

```yaml
title: "Dolor lumbar: signos de alarma y cuando consultar"
audience: "pacientes / comunidad / charla breve"
duration_minutes: 8
decision_or_reaction_expected: "educar y orientar consulta prudente"
tone: "sobrio, claro, medico, cercano"
must_include:
  - signos de alarma
  - que es una hernia discal en lenguaje simple
  - cuando consultar
  - limites: no diagnosticar por presentacion
must_not_include:
  - promesas de curacion
  - imagenes de pacientes
  - datos clinicos identificables
sources:
  - path_or_reference: ""
    status: official|paper|doctor_experience|draft|unverified
output:
  editable: pptx
  export: pdf
qa_required:
  - render_contact_sheet
  - source_traceability
  - no_sensitive_data
  - no_overlap
```

## folder_structure

```text
presentations/dolor-lumbar-pilot/
  00_brief/brief.yaml
  01_sources/source_manifest.json
  02_narrative/outline.md
  03_storyboard/storyboard.md
  04_visual/visual_direction.md
  05_assets/approved/
  05_assets/generated/
  05_assets/rejected/
  06_deck/dolor-lumbar-pilot.pptx
  07_render/contact_sheet.pdf
  08_qa/qa_report.md
  09_exports/dolor-lumbar-pilot.pdf
```

## qa_checklist

- PPTX editable abre sin errores.
- Contact sheet revisado.
- Sin texto cortado, solapado o ilegible.
- Cada slide tiene una idea dominante.
- Claims medicos con fuente o etiqueta `experiencia clinica del Doctor`.
- No hay datos de pacientes.
- Visuales generados no simulan evidencia clinica.
- Paleta sobria, consistente y profesional.
- El cierre tiene CTA prudente, no venta agresiva.
- Notas internas no aparecen en slides visibles.

## membership_trigger

No pagar herramienta nueva salvo que el piloto local falle en una de estas areas y una herramienta externa demuestre mejora:

| Trigger | Prueba requerida |
|---|---|
| Narrativa floja | Claude/Opus mejora outline con mismo brief y fuentes sanitizadas. |
| Visual pobre | Gemini/Nano Banana produce assets abstractos aprobados por QA. |
| Deck lento | Tool externa exporta PPTX editable limpio y mantiene citas. |
| QA manual excesivo | Herramienta genera render/contact sheet o detecta solapes mejor. |

Si una herramienta no exporta PPTX editable, no sirve como flujo principal.

## risks / limits

- No se creo deck real porque falta tema final/fuentes autorizadas.
- La eleccion de membresias requiere prueba con material no sensible.
- Un deck visualmente lindo pero no editable o sin fuentes no cumple.
- Para contenido medico, la fuente importa mas que la estetica.

## recommendation

Hacer un piloto local de 8-10 slides con tema lumbar. Despues comparar solo dos mejoras: Claude/Opus para narrativa y Gemini/Nano Banana para visuales. Mantener Codex + Presentations como base hasta que otra herramienta demuestre export editable, trazabilidad y mejor QA.

## confidence

Alta para pack, brief, carpetas y QA. Media para trigger de membresias hasta correr piloto real.

## evidence_paths

- `jobs/20260525T123025-presentaciones-pilot-pack.md`
- `context/fronts/presentaciones.md`
- `results/20260525T122120-presentaciones-ai-pilot-premium-v1.result.md`
- `results/20260525T112543-youtubers-auditoria-profunda-con-pack-obligatorio-v2.result.md`

