---
id: 20260525T133959-reel-dia-patria-v2-return-premium-gate
assignee: personal-xh
model: gpt-5.5-xh
created_at: 2026-05-25T13:39:59-03:00
front: REELS
no_external_actions: true
no_secrets: true
status: pending
---

# Workorder: devolver y rehacer reel Día de la Patria v2 por gate premium

## 10 inicial - decisión del orquestador

El resultado `results/20260525T133010-reel-dia-patria-v2-render-pablo-own-assets.result.md` NO queda aceptado.

Motivos:

- Fue entregado como `preview silencioso`, no como candidato final.
- No hay revisión cuadro a cuadro ni contact sheet seguro disponible para el orquestador.
- Usa `C13` marcado `needs_crop`; un asset con revisión pendiente no puede entrar en pieza premium.
- No usa video del Doctor ni material humano fuerte; sigue demasiado cerca de placas institucionales.
- Audio pendiente: un reel publicable no debe llegar silencioso salvo pedido explícito.

El Doctor fue claro: Codex debe revisar calidad final y no aceptar baja calidad como premium.

## Gate obligatorio

Leer y cumplir:

- `docs/reels_premium_acceptance_gate.md`
- `docs/pablo_asset_inbox_protocol.md`
- `docs/pablo_minimal_authorization_profile.md`
- `context/fronts/reels_cmp.md`

## Tarea

Rehacer el borrador en la Mac de Pablo usando material propio real y entregarlo solo si puede marcarse como `final_candidate`. Si no alcanza, marcarlo como `preview_not_final` y explicar exactamente qué falta.

Requisitos no negociables:

- usar video o imagen propia real en al menos dos bloques, idealmente Doctor/CMP/consultorio/quirófano seguro;
- resolver o reemplazar `C13`; no usar assets `needs_crop` sin recorte final;
- agregar audio seguro: música baja propia/licenciable/local o locución generada/revisable; si no hay audio, explicar y marcar `pass_premium_gate: false`;
- generar contact sheet de 8-12 frames, baja resolución y seguro, para que el orquestador pueda auditar visualmente;
- verificar contacto: `@drcarloszanardi`, `2364384321`, `www.centromedicopellegrini.com.ar`;
- no subir MP4 ni originales al bridge;
- si el contact sheet contiene solo material no sensible y pesa menos de 800 KB, puede commitearse en `context/asset_packs/20260525-dia-patria-v2/qa/`.

Antes de commitear:

```bash
python3 scripts/asset_gate.py scan-bridge
python3 scripts/secret_scan.py
python3 scripts/validate_result_contract.py results/<job_id>.result.md
```

## Salida obligatoria

Incluir explícitamente:

- `final_or_preview`: `final_candidate` o `preview_not_final`.
- `pass_premium_gate`: `true` o `false`.
- `render_path_local`.
- `contact_sheet_path_local`.
- `contact_sheet_bridge_path` o motivo de no compartir.
- `audio_status`.
- `asset_privacy_status`.
- `what_changed_from_rejected_version`.
- `orchestrator_review_needed`.

## 10 final - retorno al orquestador

Incluir `summary honesto`, `coverage_table`, `risks / limits`, `recommendation`, `confidence`, `evidence_paths`.
Validar contra `scripts/validate_result_contract.py`.
