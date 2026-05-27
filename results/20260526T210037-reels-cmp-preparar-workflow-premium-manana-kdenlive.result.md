---
job_id: 20260526T210037-reels-cmp-preparar-workflow-premium-manana-kdenlive
worker: personal-xh
status: completed
completed_at: 2026-05-26T21:06:11-03:00
front: REELS
no_external_actions: true
no_secrets: true
---

# Resultado - REELS CMP preparar workflow premium manana Kdenlive

## summary

Veredicto: **workflow listo como checklist operativo, pero el setup local citado
no esta confirmado en esta Mac**.

El job dice que `Kdenlive 25.04` quedo instalado en
`/Applications/kdenlive.app`, y que el proyecto/inbox viven en rutas de
`/Users/jarvis/...`. En esta Mac esas rutas no existen: no hay
`/Applications/kdenlive.app`, no aparece una app Kdenlive/DaVinci en
`/Applications`, y tampoco existe `/Users/jarvis`. Por eso no se puede validar
el proyecto base real ni abrir Kdenlive desde esta maquina.

La salida util es un checklist de arranque para el orquestador: cuando el
material llegue, no editar hasta tener raiz local autorizada, proyecto real,
manifest de assets, storyboard de 1 frase, y gate visual con contact sheet. El
piso editorial debe ser el reel 25 de Mayo: idea clara, video real propio,
ritmo, audio, contacto CMP y evidencia visual.

## coverage_table

| Fuente / chequeo | Estado | Decision |
| --- | --- | --- |
| `jobs/20260526T210037-reels-cmp-preparar-workflow-premium-manana-kdenlive.md` | Revisado | Se toma como alcance y restricciones. |
| `/Applications/kdenlive.app` | No existe en esta Mac | No se puede verificar Kdenlive 25.04 ni abrir proyecto. |
| `/Applications` con `kdenlive`, `DaVinci`, `Resolve`, `Blackmagic` | Sin matches | No hay editor premium confirmado por app instalada. |
| `/Users/jarvis/.openclaw/workspace/reels-studio/projects/2026-05-27-daily-reel` | No existe | No tocar ni asumir proyecto base ausente. |
| `/Users/jarvis/.openclaw/workspace/reels-studio/inbox/REELS/2026-05-27-daily-reel` | No existe | No hay material local autorizado visible. |
| `docs/reels_premium_acceptance_gate.md` | Revisado | Gate CEO y daily reel gate. |
| `context/fronts/reels_cmp.md` | Revisado | Contacto CMP y reglas visuales canonicas. |
| `docs/pablo_asset_inbox_protocol.md` | Revisado | No acceder a Fotos/iCloud/Drive/Downloads ni carpetas amplias. |
| `results/20260525T133959-reel-dia-patria-v2-return-premium-gate.result.md` | Revisado | Benchmark 25 de Mayo aprobado. |

## findings

### Riesgos de calidad

1. **Falsa seguridad de setup.** Si el orquestador cree que Kdenlive ya esta
   disponible en esta Mac, puede mandar trabajo que Pablo no puede abrir. Hay
   que corregir la ruta/app real antes de prometer edicion.

2. **Riesgo de slideshow.** Si llega solo foto o placa, el daily reel falla el
   gate: minimo dos bloques de video propio/autorizado o material real que
   sostenga una historia.

3. **Riesgo de "preview como final".** El gate exige `final_candidate` solo con
   contact sheet, frame QA, audio definido y contacto correcto.

4. **Riesgo de privacidad.** Estudios, pantallas, reflejos, carpetas, nombres y
   caras no autorizadas deben revisarse cuadro a cuadro antes de exportar.

5. **Riesgo editorial.** Si no se puede decir en una frase que transmite el
   reel, el reel falla aunque este bien renderizado.

## recommendation

### Workflow operativo cuando llegue material

1. **Confirmar raiz autorizada.** Usar una carpeta tipo
   `/Users/carloszanardi/CodexAssetInbox/REELS/2026-05-27-daily-reel` o
   `/Users/carloszanardi/CodexAssets/Reels/2026-05-27-daily-reel`. No usar
   Fotos, iCloud, Drive, Downloads ni Desktop.

2. **Crear o recibir manifest.** Debe listar cada asset, origen, permiso,
   sensibilidad y uso recomendado. Antes de editar:

```bash
python3 scripts/asset_gate.py validate-manifest <manifest.json> --check-exists
```

3. **Brief de una frase.** Ejemplo: `No se opera una imagen; se evalua una
   persona con sintomas, examen y contexto`.

4. **Storyboard 25-40s.**
   - 0-3s: hook/conflicto.
   - 3-10s: video real del Doctor o material propio.
   - 10-25s: medicina concreta en 2-3 beats.
   - 25-34s: comunidad/CMP o aprendizaje para paciente.
   - 34-40s: cierre con `@drcarloszanardi`, `2364384321`,
     `www.centromedicopellegrini.com.ar`.

5. **Proyecto Kdenlive recomendado.** Si Kdenlive queda instalado, crear:

```text
2026-05-27-daily-reel/
  00_brief/
    brief.md
  01_assets_originals_local_not_git/
  02_assets_safe_derivatives/
  03_storyboard/
    storyboard.md
  04_edit/
    kdenlive/
      2026-05-27-daily-reel.kdenlive
      proxies/
  05_audio/
  06_subtitles/
  07_exports/
    preview/
    final_candidate/
  08_qa/
    contact_sheet/
    frame_checks/
    gate_report.md
  manifest.json
```

6. **Configuracion de timeline.**
   - Formato: vertical `1080x1920`.
   - Duracion objetivo: `25-40s`.
   - Ritmo: cambios visuales cada `2-5s`.
   - Subtitulos: maximo 1-2 lineas, alto contraste, margen seguro.
   - Audio: voz real/locucion/musica segura; no final silencioso salvo pedido.

7. **QA minimo antes de exportar.**
   - Contact sheet 8-12 frames.
   - Preview 540x960 para lectura en celular.
   - Verificacion de contacto.
   - Verificacion de privacidad cuadro a cuadro.
   - Confirmar que hay al menos dos bloques de material propio real.
   - Confirmar `publication_hold=false` solo si el gate pasa completo.

### Mantener el piso del reel 25 de Mayo

- Abrir con una idea, no con logo.
- Usar material real del Doctor/CMP, no placas genericas.
- Evitar texto largo: que el video cuente y el texto ancle.
- Cerrar con marca/contacto limpio, no con flyer.
- Si el material no alcanza, pedir material nuevo en vez de bajar calidad.

## attempted_routes

- Se reviso la app declarada `/Applications/kdenlive.app`.
- Se busco Kdenlive/DaVinci/Resolve/Blackmagic en `/Applications`.
- Se verificaron las rutas de proyecto e inbox indicadas en `/Users/jarvis/...`.
- Se usaron gates/documentos locales del bridge como fuente de verdad.
- No se accedio a Fotos/iCloud/Drive/Downloads, no se enviaron mensajes
  externos y no se creo ningun asset.

## risks/limits

- Este resultado no confirma instalacion de Kdenlive; reporta que la ruta
  indicada no existe en esta Mac.
- No hay material del Doctor visible en una ruta autorizada para este job.
- La estructura propuesta debe aplicarse cuando exista carpeta autorizada real.
- Si el orquestador necesita Kdenlive en esta Mac, debe abrir un job separado de
  instalacion/verificacion o corregir la ruta exacta de la app.

## confidence

**high** para el checklist/gate y **medium** para el estado del setup, porque se
verificaron las rutas locales declaradas y no existen en esta Mac. No se puede
asegurar si Kdenlive esta instalado en otra computadora o bajo otra ruta no
autorizada por el job.

## evidence_paths

- `jobs/20260526T210037-reels-cmp-preparar-workflow-premium-manana-kdenlive.md`
- `claims/20260526T210037-reels-cmp-preparar-workflow-premium-manana-kdenlive.json`
- `docs/reels_premium_acceptance_gate.md`
- `context/fronts/reels_cmp.md`
- `docs/pablo_asset_inbox_protocol.md`
- `results/20260525T133959-reel-dia-patria-v2-return-premium-gate.result.md`
- Ruta ausente: `/Applications/kdenlive.app`
- Ruta ausente: `/Users/jarvis/.openclaw/workspace/reels-studio/projects/2026-05-27-daily-reel`
- Ruta ausente: `/Users/jarvis/.openclaw/workspace/reels-studio/inbox/REELS/2026-05-27-daily-reel`
