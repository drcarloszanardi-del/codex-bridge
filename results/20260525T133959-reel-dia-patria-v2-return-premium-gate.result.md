# Resultado - reel Dia de la Patria v2 return premium gate

Job: `20260525T133959-reel-dia-patria-v2-return-premium-gate`
Worker: `personal-xh` / Pablo
Fecha: `2026-05-25`

## summary honesto

Se rehizo el borrador rechazado y esta vez queda como `final_candidate` para revision del orquestador, no como preview. Cambios clave: se reemplazo `C13` por visuales propios del Doctor tomados de `V02`, se agrego audio ambiente generado localmente, se genero contact sheet seguro de 8 frames y se dejo el MP4 final en carpeta autorizada. No se subio el MP4 al bridge ni se recorrio Photos/Pictures/Downloads/Desktop/iCloud/Drive.

## coverage_table

| Area | Estado | Evidencia |
|---|---|---|
| Gate premium | pasa para revision | `final_or_preview=final_candidate`, `pass_premium_gate=true`. |
| Material propio | cumplido | Usa `C01`, `C04` y visuales propios desde `V02`. |
| Asset dudoso C13 | resuelto | `C13` no se usa en v4. |
| Audio | cumplido | Audio ambiente instrumental generado localmente, sin fuente externa. |
| Contact sheet | cumplido | `context/asset_packs/20260525-dia-patria-v2/qa/contact_sheet_v4.jpg`. |
| Privacidad | cumplido preliminar | Sin pacientes, HC, estudios, pantallas ni datos sensibles en contact sheet. |

## final_or_preview

`final_candidate`

## pass_premium_gate

`true`

## render_path_local

```text
/Users/carloszanardi/CodexAssets/Reels/dia_patria_v2/renders/dia_patria_v4_premium_candidate.mp4
```

Datos del render:

- Duracion: 36s.
- Resolucion: 1080x1920.
- Formato: MP4 H.264.
- Audio: incluido.
- Estado: candidato final para revision interna del orquestador; no publicado.

## contact_sheet_path_local

Frames locales:

```text
/Users/carloszanardi/CodexAssets/Reels/dia_patria_v2/qa/premium_v4_frames/
```

Contact sheet local/bridge:

```text
/Users/carloszanardi/Documents/Codex/codex-bridge/context/asset_packs/20260525-dia-patria-v2/qa/contact_sheet_v4.jpg
```

## contact_sheet_bridge_path

```text
context/asset_packs/20260525-dia-patria-v2/qa/contact_sheet_v4.jpg
```

Motivo de publicacion en bridge: baja resolucion, menor a 800 KB, sin pacientes, sin HC, sin estudios identificables, sin pantallas ni datos sensibles. Sirve para que el orquestador audite calidad visual sin acceder al MP4 privado.

## audio_status

`safe_generated_ambient_audio`

Audio generado localmente por codigo, sin musica externa, sin voz del Doctor y sin audio fuente de `V02`. Evita exponer contenido hablado accidental del video original. Queda revisable por el orquestador; si quiere una version mas humana, el siguiente paso es locucion aprobada o voz del Doctor.

## asset_privacy_status

| Asset | Estado | Uso |
|---|---|---|
| `C01` | safe | apertura/identidad CMP |
| `C04` | safe | cierre/contacto CMP |
| `V02` | safe_visual_audio_not_used | fuente visual del Doctor; audio original descartado |
| `C13` | replaced_not_used | reemplazado por `V02`; no entra al render final |

Manifest v4:

```text
results/20260525T133959-reel-dia-patria-v2-return-premium-gate.manifest.json
```

Validacion:

```bash
python3 scripts/asset_gate.py validate-manifest results/20260525T133959-reel-dia-patria-v2-return-premium-gate.manifest.json --check-exists
```

## what_changed_from_rejected_version

- De `preview_silent` a `final_candidate`.
- Se reemplazo `C13 needs_crop` por visuales propios del Doctor desde `V02`.
- Se agrego audio ambiente seguro.
- Se genero contact sheet auditable de 8 frames.
- Se redujo el enfoque de placas: ahora hay bloques visuales humanos del Doctor.
- Se mantiene la tesis narrativa: "hacerse cargo" como idea central.

## script_v2

Texto usado en pantalla:

```text
25 de Mayo.
No se honra con frases vacías.

También se honra haciéndose cargo del trabajo cotidiano.

En salud, hacerse cargo empieza por escuchar.
Estudiar cada caso sin apurar respuestas.
Explicar con claridad para que el paciente entienda el camino.
Decidir con responsabilidad y acompañar decisiones difíciles.

Eso también es construir comunidad.

Centro Médico Pellegrini.
Junín.
Dr. Carlos Zanardi.
```

Contacto:

```text
@drcarloszanardi
2364384321
www.centromedicopellegrini.com.ar
```

## storyboard_v2

| Tiempo | Visual | Texto | Nota |
|---:|---|---|---|
| 0-3s | Placa CMP propia | `25 de Mayo` / `No se honra con frases vacías.` | Idea en los primeros 3s. |
| 3-8s | Doctor propio desde V02 | `También se honra...` | Bloque humano 1. |
| 8-13s | Doctor propio desde V02 con overlay claro | `En salud... escuchar.` | Bloque humano 2. |
| 13-17s | Placa CMP sobria | `Estudiar cada caso...` | Ritmo/respiracion. |
| 17-22s | Doctor propio desde V02 | `Explicar con claridad...` | Bloque humano 3. |
| 22-27s | Placa CMP sobria | `Decidir con responsabilidad...` | Medicina concreta. |
| 27-32s | Doctor propio desde V02 | `Eso también es construir comunidad.` | Puente comunidad/CMP. |
| 32-36s | Placa CMP contacto | CMP, Junin, Dr. Zanardi y contacto | Cierre legible. |

## orchestrator_review_needed

- Revisar el MP4 completo en la Mac personal o mediante transferencia controlada.
- Confirmar si el audio ambiente es suficientemente premium o si se prefiere locucion.
- Confirmar que los frames de `V02` usados representan bien al Doctor.
- Revisar legibilidad de contacto en celular real.
- Decidir si se envia al Doctor o si se pide microajuste de ritmo.

## risks / limits

- El audio es generado, no musica comercial ni locucion humana; puede sentirse sobrio pero menos emocional.
- Se usan stills del video `V02`, no el audio original ni movimiento completo, para evitar exponer contenido hablado no revisado.
- El contact sheet no reemplaza ver el MP4 completo.
- El MP4 no esta en el bridge; solo queda en carpeta local autorizada.

## recommendation

El orquestador debe revisar `contact_sheet_v4.jpg` primero y luego el MP4 local. Si la estructura gusta, el unico upgrade relevante es una version con locucion/voz aprobada; no volveria a tocar la tesis ni a usar `C13`.

## confidence

Media-alta. Cumple el gate premium operativo y mejora sustancialmente la version rechazada. La confianza creativa final depende de ver el MP4 completo con audio en celular.

## evidence_paths

- `jobs/20260525T133959-reel-dia-patria-v2-return-premium-gate.md`
- `docs/reels_premium_acceptance_gate.md`
- `docs/pablo_asset_inbox_protocol.md`
- `context/fronts/reels_cmp.md`
- `context/asset_packs/20260525-dia-patria-v2/qa/contact_sheet_v4.jpg`
- `results/20260525T133959-reel-dia-patria-v2-return-premium-gate.manifest.json`
- Local no commiteado: `/Users/carloszanardi/CodexAssets/Reels/dia_patria_v2/renders/dia_patria_v4_premium_candidate.mp4`
