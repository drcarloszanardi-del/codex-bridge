# Resultado - 20260526T005108-reel-cavernoma-premium-safe-derivatives-render-v1

## Summary

final_or_preview: `final_candidate`

pass_premium_gate: `false`

Se completo el pack seguro del reel de cavernoma intramedular y se dejo un primer candidato local renderizado para revision. El material usa solamente la carpeta autorizada `Reel Cavernoma ` y derivados anonimizados; no se commitearon originales medicos ni el MP4 final al bridge.

El render local existe en `/Users/carloszanardi/CodexAssets/Reels/reel_cavernoma/renders/cmp_reel_cavernoma_intramedular_v1.mp4`, dura 50.0 segundos, es vertical 1080x1920 y tiene 1 track de video sin audio agregado. No lo marco como premium-gate true porque todavia requiere revision humana/orquestador sobre cuatro assets sensibles y porque la version actual es un candidato sobrio de primera pasada, no la version final publicable.

## Source_Counts

- Carpeta fuente autorizada: `/Users/carloszanardi/Documents/Codex/codex-bridge/Reel Cavernoma `.
- Medios crudos inspeccionados: 7 archivos utiles; `.DS_Store` ignorado.
- Derivados locales seguros creados: 9 archivos en `/Users/carloszanardi/CodexAssets/Reels/reel_cavernoma/sanitized/`.
- Previews seguros para bridge: 9 archivos en `context/asset_packs/20260526-reel-cavernoma-safe/previews/`.
- Contact sheets para bridge: 2 (`contact_sheet.jpg` y `render_contact_sheet.jpg`).
- Render local: 1 MP4 seguro candidato, no commiteado al bridge.

## Coverage_Table

| asset_code | role | privacy_status | decision |
| --- | --- | --- | --- |
| `CAV-IMG-001` | preop | `needs_orchestrator_review` | Usable solo tras revisar texto fino de pantalla redacted. |
| `CAV-IMG-002` | preop | `passed` | Mejor imagen preoperatoria para el reel. |
| `CAV-IMG-003` | surgical/context | `passed` | Plano de quirofano sin rostros frontales visibles. |
| `CAV-IMG-004` | context | `needs_orchestrator_review` | Se redacted rostros/inset; recomiendo crop si se usa. |
| `CAV-IMG-005` | surgical piece | `needs_orchestrator_review` | No identifica paciente, pero es grafico/sensible. |
| `CAV-IMG-006` | monitoring | `passed` | Cabeceras/datos de monitor redacted. |
| `CAV-VID-001` | postop/control | `needs_orchestrator_review` | Solo poster redacted; video crudo no incluido. |
| `CAV-SLATE-001` | hook | `passed` | Placa institucional generada. |
| `CAV-SLATE-002` | closing | `passed` | Placa institucional generada. |

## Recommendation

Usar este render como candidato seguro de revision, no como version final automatica. Para pasar premium gate sugiero que el orquestador haga una segunda pasada con:

1. Revision visual de `CAV-IMG-001`, `CAV-IMG-004`, `CAV-IMG-005` y `CAV-VID-001`.
2. Decision editorial sobre si excluir `CAV-IMG-005` por sensibilidad grafica.
3. Ajuste fino de movimiento/ritmo para evitar que se perciba como slideshow.
4. Confirmacion de cierre institucional y datos publicos antes de publicar.

Si el orquestador aprueba privacidad, el archivo local puede servir como base de corte. Si no aprueba, el camino seguro es rehacer el render solo con `CAV-IMG-002`, `CAV-IMG-003`, `CAV-IMG-006` y las placas.

## Risks_Limits

- No se buscaron fotos fuera de la carpeta autorizada; no se uso Photos, Drive, Gmail, Telegram ni Downloads.
- No se commitearon originales crudos ni el MP4 del render al bridge.
- El render no tiene musica ni locucion; el Doctor agregara musica al publicar.
- `CAV-VID-001` quedo reducido a poster redacted; el video original requiere revision separada si se quiere incorporar movimiento real.
- El candidato conserva contacto institucional en el cierre; debe ser validado por el orquestador/Doctor antes de publicarse.
- La version actual es visualmente coherente y segura para revision, pero todavia no supera el gate premium por revision pendiente y movimiento limitado.

## Evidence_Paths

- Job: `jobs/20260526T005108-reel-cavernoma-premium-safe-derivatives-render-v1.md`
- Claim: `claims/20260526T005108-reel-cavernoma-premium-safe-derivatives-render-v1.json`
- Manifest QA bridge: `context/asset_packs/20260526-reel-cavernoma-safe/manifest.json`
- Contact sheet assets: `context/asset_packs/20260526-reel-cavernoma-safe/contact_sheet.jpg`
- Contact sheet render: `context/asset_packs/20260526-reel-cavernoma-safe/render_contact_sheet.jpg`
- Previews bridge: `context/asset_packs/20260526-reel-cavernoma-safe/previews/`
- Derivados locales seguros: `/Users/carloszanardi/CodexAssets/Reels/reel_cavernoma/sanitized/`
- Render local: `/Users/carloszanardi/CodexAssets/Reels/reel_cavernoma/renders/cmp_reel_cavernoma_intramedular_v1.mp4`
- Manifest de resultado: `results/20260526T005108-reel-cavernoma-premium-safe-derivatives-render-v1.manifest.json`

## Confidence

Media-alta. La sanitizacion y el render quedaron materialmente completos, con verificacion local de duracion/resolucion/tracks. Mantengo confianza no alta porque hay cuatro assets marcados para revision humana y porque el resultado editorial todavia necesita una segunda pasada para pasar premium gate.
