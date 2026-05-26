# Resultado - 20260526T005616-reel-cavernoma-render-safe-motion-v2

## Summary

final_or_preview: `final_candidate`

pass_premium_gate: `true`

Se genero un candidato visual v2 local, vertical y seguro, con movimiento real en el tramo de control postoperatorio. El MP4 no se subio al bridge: quedo solo en la Mac, en `/Users/carloszanardi/CodexAssets/Reels/reel_cavernoma/renders/cmp_reel_cavernoma_intramedular_v2.mp4`. El bridge recibe un contact sheet seguro para revision en `context/asset_packs/20260526-cavernoma-intramedular/render_contact_sheet_v2.jpg`.

El render dura 46.0 segundos, 1080x1920, 24 fps, 1 track de video y 0 tracks de audio. No se agrego musica. El clip postoperatorio crudo se uso solamente como crop inferior de marcha/andador, sin rostro, sin audio y sin metadata exportada al bridge.

## Source_Counts

- Carpeta fuente autorizada usada: `/Users/carloszanardi/Documents/Codex/codex-bridge/Reel Cavernoma `.
- Trabajo local autorizado usado: `/Users/carloszanardi/CodexAssets/Reels/reel_cavernoma/`.
- Derivados seguros usados: 5 (`CAV-SLATE-001`, `CAV-IMG-002`, `CAV-IMG-003`, `CAV-IMG-006`, `CAV-SLATE-002`).
- Clip postoperatorio crudo usado: 1 tramo visual convertido a crop inferior anonimo, sin audio.
- Assets evitados en v2: 2 (`CAV-IMG-004`, `CAV-IMG-005`).
- Render local creado: 1 MP4, 26 MB aprox., no commiteado.
- Contact sheet bridge creado: 1 JPG, 8 frames.

## Coverage_Table

| asset_code | uso en v2 | privacy_status | decision |
| --- | --- | --- | --- |
| `CAV-SLATE-001` | hook | `passed` | Placa segura de apertura. |
| `CAV-IMG-002` | imagen preoperatoria principal | `passed` | Usada con pan/zoom lento y texto breve. |
| `CAV-IMG-003` | escena quirurgica/equipo | `passed` | Usada dos veces con movimiento para continuidad visual. |
| `CAV-IMG-006` | monitoreo intraoperatorio | `passed` | Usada como evidencia de monitoreo, sin datos identificables legibles. |
| `CAV-VID-001` | control postoperatorio | `passed_after_crop` | Se extrajo movimiento real solo de piernas/andador; audio removido; rostro excluido. |
| `CAV-SLATE-002` | cierre CMP | `passed` | Cierre institucional sin musica. |
| `CAV-IMG-004` | no usado | `rejected_for_v2` | Redacciones visibles/crop poco premium. |
| `CAV-IMG-005` | no usado | `rejected_for_v2` | Pieza quirurgica grafica; no necesaria para publico general. |

## Recommendation

Usar `cmp_reel_cavernoma_intramedular_v2.mp4` como candidato principal para revision final del Doctor/orquestador. La v2 mejora la v1 porque incorpora movimiento real seguro del control postoperatorio y evita la pieza quirurgica grafica.

Antes de publicar, el orquestador deberia hacer una revision visual completa del MP4 local y confirmar que el cierre institucional conserva telefono, usuario y web correctos. Si se quiere un acabado aun mas premium, la proxima pasada deberia ajustar microtransiciones y agregar la musica elegida por el Doctor al momento de publicar.

## Risks_Limits

- El MP4 local no fue commiteado porque deriva de material clinico y pesa 26 MB; solo se commiteo el contact sheet seguro.
- El video postoperatorio original contiene rostro y audio, pero el render v2 usa un crop inferior y genera salida sin audio tracks.
- La revision del contact sheet no reemplaza una pasada humana completa sobre el MP4 antes de publicacion.
- No se abrieron Fotos, iCloud, Drive, Gmail, Telegram, Downloads, Desktop, Pictures ni bibliotecas completas.
- No se prometen resultados clinicos, cura ni ausencia de secuelas.

## Evidence_Paths

- Job: `jobs/20260526T005616-reel-cavernoma-render-safe-motion-v2.md`
- Claim: `claims/20260526T005616-reel-cavernoma-render-safe-motion-v2.json`
- Render local: `/Users/carloszanardi/CodexAssets/Reels/reel_cavernoma/renders/cmp_reel_cavernoma_intramedular_v2.mp4`
- Contact sheet bridge: `context/asset_packs/20260526-cavernoma-intramedular/render_contact_sheet_v2.jpg`
- Pack seguro previo: `context/asset_packs/20260526-reel-cavernoma-safe/manifest.json`
- Resultado manifest: `results/20260526T005616-reel-cavernoma-render-safe-motion-v2.manifest.json`
- Validacion tecnica local: duracion 46.0s, resolucion 1080x1920, fps 24.0, video_tracks 1, audio_tracks 0.

## Confidence

Alta para el cumplimiento tecnico y de privacidad del candidato v2. Media-alta para el gate editorial premium, porque el contact sheet muestra una pieza sobria y segura, pero la decision final de publicacion debe quedar en revision humana del MP4 completo.
