---
id: 20260526T005616-reel-cavernoma-render-safe-motion-v2
created_at: 2026-05-26T00:56:16-03:00
created_by: orchestrator
assignee: personal-xh
front: REELS
model: gpt-5.5
reasoning_effort: high
status: queued
priority: high
no_external_actions: true
no_secrets: true
asset_policy: authorized_folder_only_safe_derivatives_only
---

# Reel cavernoma intramedular - render seguro con movimiento real

## Contexto

Gracias por completar el handoff seguro en:

`context/asset_packs/20260526-cavernoma-intramedular/`

El contact sheet ya permite avanzar. Ahora falta una pieza que no sea una simple suma de fotos. El Doctor pidio un reel premium/cinematografico de 40 a 60 segundos para publicar manana, con material propio, sin musica agregada por nosotros.

## Objetivo

Producir, en tu Mac local, un primer candidato visual premium usando solo la carpeta autorizada y derivados seguros. El objetivo es sumar movimiento real cuando sea seguro, especialmente del video de control postoperatorio, sin exponer datos identificables.

## Material autorizado

Solo usar:

- Carpeta original autorizada: `/Users/carloszanardi/Documents/Codex/codex-bridge/Reel Cavernoma `
- Trabajo local autorizado: `/Users/carloszanardi/CodexAssets/Reels/reel_cavernoma/`
- Pack seguro ya generado: `context/asset_packs/20260526-cavernoma-intramedular/`

No abrir Fotos, iCloud, Drive, Gmail, Telegram, Downloads, Desktop, Pictures ni bibliotecas completas.

## Render esperado

Crear localmente:

`/Users/carloszanardi/CodexAssets/Reels/reel_cavernoma/renders/cmp_reel_cavernoma_intramedular_v2.mp4`

Duracion objetivo: 45-55 s.
Formato: 1080x1920 vertical.
Audio: silencioso o sin pista musical. No agregar musica.

Si el MP4 final no puede subirse seguro, crear un proxy liviano seguro o al menos un contact sheet del render:

`context/asset_packs/20260526-cavernoma-intramedular/render_contact_sheet_v2.jpg`

## Uso de assets

Usar preferentemente:

- `CAV-IMG-002`: imagen preoperatoria principal.
- `CAV-IMG-003`: escena quirurgica/equipo, si se mantiene sin identificadores.
- `CAV-IMG-006`: monitoreo intraoperatorio, recortado si hay datos visibles.
- `CAV-VID-001`: extraer 3-6 segundos seguros del video postoperatorio crudo solo si se puede anonimizar rostro/audio/metadata. Si no, usar poster seguro.

Evitar en v2:

- `CAV-IMG-005` pieza quirurgica, salvo que sea imprescindible y quede presentado con sobriedad. Es sensible para publico general.
- `CAV-IMG-004` si las redacciones visibles arruinan el look premium; usar solo con crop limpio.

## Narrativa visual

Titulo: `Cavernoma intramedular`
Idea central: patologia desafiante donde el diagnostico, la planificacion, el monitoreo y el seguimiento importan tanto como el acto tecnico.

Texto breve en pantalla:

1. `Hay lesiones en las que un milimetro importa.`
2. `Diagnostico preciso. Planificacion fina.`
3. `Microcirugia con monitoreo neurofisiologico.`
4. `Cuidar funcion tambien es parte del tratamiento.`
5. `Control, seguimiento y prudencia.`
6. Cierre: `Centro Medico Pellegrini` + `@drcarloszanardi` + `2364384321` + `www.centromedicopellegrini.com.ar`

Evitar:

- Prometer cura, recuperacion o ausencia de secuelas.
- Tono triunfalista.
- Efectos de shock o sensacionalismo.
- Frases genericas como "tecnologia de punta".
- Placas largas o texto que tape la imagen.

## Estetica

- Inspirarse en el ultimo reel aprobado por el Doctor: cinematografico, sobrio, con material real.
- Movimiento: pans lentos, zoom controlado, transiciones suaves, parallax si se puede.
- Logo CMP integrado, no invasivo.
- Paleta CMP clara: azul Pellegrini, cian suave, blanco/papel.
- Contacto solo al cierre.

## Gate de aceptacion

Aplicar `docs/reels_premium_acceptance_gate.md`.

No marcar `pass_premium_gate: true` si:

- no hay evidencia visual;
- es solo una suma de fotos;
- quedan datos identificables;
- el texto es generico;
- el cierre tiene telefono incorrecto;
- no hay contact sheet del render.

## Entregable en results

Crear:

- `results/20260526T005616-reel-cavernoma-render-safe-motion-v2.result.md`
- `results/20260526T005616-reel-cavernoma-render-safe-motion-v2.manifest.json`

Incluir:

- `final_or_preview`
- `pass_premium_gate`
- `render_path_local`
- `render_contact_sheet_bridge_path`
- duracion/resolucion/fps
- assets usados/rechazados
- privacidad: passed/rejected/needs_review por asset
- si se extrajo clip del video postoperatorio: indicar si audio fue removido y rostro/datos fueron anonimizados
- proxima accion necesaria del orquestador

Si una autorizacion de macOS bloquea el video crudo, no pedir acceso amplio. Usar las imagenes seguras y dejar constancia del bloqueo puntual.
