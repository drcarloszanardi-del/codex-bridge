# Resultado - 20260526T030030-reel-cavernoma-v2-proxy-and-ceo-gate-fix

## Summary

final_or_preview: `final_candidate`

pass_premium_gate: `true`

Se corrigio el render a una version v2b y se creo un proxy completo, seguro y liviano para revision del orquestador. El proxy representa todo el video, no contiene audio, pesa 6.6 MB y quedo commiteable en `context/asset_packs/20260526-cavernoma-intramedular/proxy/cmp_reel_cavernoma_intramedular_v2_proxy_540x960.mp4`.

La RM fue reencuadrada: se usa crop limpio del sector anatomico y una banda CMP opaca para evitar headers, UI tecnica o texto identificatorio. El cierre fue rerenderizado como placa limpia, sin superposicion, con `@drcarloszanardi`, telefono `2364384321` y web `www.centromedicopellegrini.com.ar` separados y legibles.

Decision editorial: listo para que lo vea el Doctor como candidato visual, con aprobacion final humana antes de publicacion.

## Source_Counts

- Carpeta fuente autorizada usada: `/Users/carloszanardi/Documents/Codex/codex-bridge/Reel Cavernoma `.
- Trabajo local autorizado usado: `/Users/carloszanardi/CodexAssets/Reels/reel_cavernoma/`.
- Render local nuevo: 1 MP4 en `/Users/carloszanardi/CodexAssets/Reels/reel_cavernoma/renders/cmp_reel_cavernoma_intramedular_v2b.mp4`.
- Proxy bridge creado: 1 MP4 540x960, 6.6 MB, sin audio.
- Contact sheet nuevo: 1 JPG con 8 frames.
- Originales crudos commiteados: 0.

## Coverage_Table

| bloque | privacidad | decision |
| --- | --- | --- |
| Hook | `passed` | Placa limpia institucional, sin datos sensibles. |
| RM preoperatoria | `passed_after_crop` | Crop anatomico; sin header/fecha/nombre visible en el proxy; banda CMP opaca. |
| Quirofano/equipo | `passed` | Sin rostros frontales identificables; mantiene evidencia visual real. |
| Monitoreo | `passed` | Plano tecnico no identificatorio; texto de pantalla no usado como dato clinico. |
| Tecnica/criterio | `passed` | Reusa plano quirurgico seguro con texto sobrio. |
| Control postoperatorio | `passed_after_crop` | Solo piernas/andador; sin rostro; audio removido; sin metadata cruda. |
| Cierre | `passed` | `@drcarloszanardi`, `2364384321` y `www.centromedicopellegrini.com.ar` legibles y no superpuestos. |

## Recommendation

Usar `cmp_reel_cavernoma_intramedular_v2_proxy_540x960.mp4` para la revision del orquestador y del Doctor. Si el Doctor aprueba la pieza, publicar desde el render local v2b o rehacer export final a la resolucion preferida con la musica que el Doctor elija externamente.

Mantener fuera del bridge el render 1080 y los originales crudos. El proxy completo ya alcanza para juzgar ritmo, privacidad, cierre y narrativa sin exponer material fuente.

## Risks_Limits

- El proxy es seguro y completo, pero sigue siendo material derivado de un caso clinico; requiere aprobacion humana final antes de publicar.
- No se agrego musica ni locucion.
- No se uso Fotos, iCloud, Drive, Gmail, Telegram, Downloads, Desktop, Pictures ni bibliotecas completas.
- El render local 1080 no fue commiteado por peso y por politica de derivados clinicos.
- El proxy fue generado sin audio tracks; no conserva audio del video postoperatorio.

## Evidence_Paths

- Job: `jobs/20260526T030030-reel-cavernoma-v2-proxy-and-ceo-gate-fix.md`
- Claim: `claims/20260526T030030-reel-cavernoma-v2-proxy-and-ceo-gate-fix.json`
- Proxy bridge: `context/asset_packs/20260526-cavernoma-intramedular/proxy/cmp_reel_cavernoma_intramedular_v2_proxy_540x960.mp4`
- Contact sheet v2b: `context/asset_packs/20260526-cavernoma-intramedular/render_contact_sheet_v2b.jpg`
- Render local v2b: `/Users/carloszanardi/CodexAssets/Reels/reel_cavernoma/renders/cmp_reel_cavernoma_intramedular_v2b.mp4`
- Resultado manifest: `results/20260526T030030-reel-cavernoma-v2-proxy-and-ceo-gate-fix.manifest.json`
- Verificacion tecnica: proxy `duration=46.0`, `resolution=540x960`, `fps=24.0`, `video_tracks=1`, `audio_tracks=0`, tamano 6.6 MB.

## Confidence

Alta. El proxy completo permite revisar el audiovisual real, corrige el crop de RM, confirma cierre legible sin superposicion y mantiene privacidad del bloque postoperatorio sin audio ni rostro.
