---
id: 20260526T233419-reels-lumbar-cinematic-v3-shotlist-and-gate-review
created_at: 2026-05-26T23:34:19-03:00
created_by: orchestrator
assignee: personal-xh
front: REELS
model: gpt-5.5-xh
reasoning_effort: xhigh
status: queued
no_external_actions: true
no_secrets: true
---

# Reels CMP lumbar cinematic v3 - shotlist y gate review

## 10 inicial - direccion del orquestador

El Doctor rechazo el reel lumbar por baja calidad, transiciones pobres y demasiado texto descriptivo.
Tambien indico que el piso minimo debe ser el reel cinematografico del 25 de Mayo y que no acepta
slideshow, frases genericas ni placas explicativas. No renderizar, no enviar Telegram y no abrir bibliotecas
privadas.

Contexto minimo:

- `context/fronts/reels_cmp.md`
- `docs/reels_premium_acceptance_gate.md`
- `context/fronts/reels_cmp_cinematic_references_2026-05-26.md`
- `results/20260526T230823-reels-cmp-low-text-transition-quality-reset-v1.result.md`
- `context/asset_packs/20260526-lumbar-cinematic-v2-proxy/manifest.md`
- `context/asset_packs/20260526-lumbar-cinematic-v2-proxy/contact_sheet.jpg`

Objetivo: auditar el proxy v2 solo por contact sheet y convertir el feedback en una direccion v3 concreta,
con menos texto y mas video real. El resultado debe ser implementable por Codex principal sin improvisar.

## 80 delegado - trabajo de Pablo

Entregar:

- `qa_verdict`: aceptar/rechazar proxy v2 y por que, usando el gate premium.
- `shotlist_v3`: lista de planos necesarios y orden exacto 40-55s.
- `transition_plan`: transiciones por continuidad visual, accion o audio; prohibir wipes/zoom repetido.
- `text_budget`: maximo de palabras por beat y texto final exacto permitido en pantalla.
- `asset_request_for_doctor`: pedido minimo de material propio si el v2 no alcanza.
- `render_constraints`: que no debe hacer el orquestador al renderizar.
- `risks_limits`: privacidad, material insuficiente y puntos que exigen revision humana.
- `recommendation`: si conviene renderizar v3 con lo existente o pedir material antes.

Reglas:

- No usar stock ni material externo como sustituto de evidencia clinica.
- No abrir Fotos/iCloud/Drive/Gmail/Downloads ni bibliotecas privadas.
- No proponer frases epicas ni motivacionales.
- No cerrar con "no pude" sin rutas alternativas, limite exacto y proxima accion.

## 10 final - retorno al orquestador

El resultado debe incluir summary honesto, evidencia usada, decision concreta y un proximo paso unico.
Validar contra `scripts/validate_result_contract.py` antes de marcarlo completado.
