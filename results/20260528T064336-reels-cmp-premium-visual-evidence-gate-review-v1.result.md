---
job_id: 20260528T064336-reels-cmp-premium-visual-evidence-gate-review-v1
worker: personal-xh
status: completed
completed_at: 2026-05-28T06:49:35-03:00
front: REELS
no_external_actions: true
no_secrets: true
---

# Resultado - REELS CMP premium visual evidence gate review v1

## summary

Revision declarativa y de bajo riesgo del gate premium para REELS CMP.

Recomendacion central: implementar un **guard local simple** y dejar el checklist
manual solo como reporte/observacion. Los incidentes recientes son P0 cuando una
pieza silenciosa se presenta como final, cuando el montaje afirma elementos no
verificados, cuando se mezclan materiales de otro reel, o cuando un envio se
marca entregado sin `ok=true` y `message_id` real.

No se uso Telegram, Gmail, Drive, Calendar, iCloud, Photos, adjuntos reales ni
servicios externos.

## coverage_table

| Fuente | Estado | Uso |
| --- | --- | --- |
| `jobs/20260528T064336-reels-cmp-premium-visual-evidence-gate-review-v1.md` | Revisada | Workorder y alcance permitido. |
| `docs/reels_premium_acceptance_gate.md` | Revisada | Criterio canonico premium CMP y salida minima de Pablo. |
| `context/fronts/reels_cmp.md` | Revisada | Datos CMP correctos y gate visual canonico. |
| `context/fronts/telegram.md` | Revisada | Regla canonica de entrega: `ok=true` y `message_id` real. |
| `results/20260528T062330-telegram-direct-visual-evidence-guard-review-v1.result.md` | Revisada | Cierre declarativo del guard de evidencia visual. |
| `results/20260525T133959-reel-dia-patria-v2-return-premium-gate.result.md` | Revisada | Ejemplo de correccion: preview silencioso -> final candidate con audio/evidencia. |

## evidencia_verificada

- El gate premium vigente declara que no pasa una pieza silenciosa si se pidio
  reel publicable, ni un preview presentado como entrega.
- El gate premium vigente exige evidencia visual suficiente: contact sheet seguro
  con 8-12 frames, datos tecnicos del MP4 y revision del orquestador antes de
  enviar.
- El gate visual de REELS CMP exige verificar que las imagenes medicas
  representen realmente el tema, no usar anatomia generada como evidencia
  clinica, quitar marcas de agua/placeholder y separar guion, storyboard, assets,
  caption y QA.
- La salida minima de Pablo ya contiene campos que permiten automatizar el
  bloqueo: `final_or_preview`, `pass_premium_gate`, `audio_status`,
  `asset_privacy_status`, `contact_sheet_path_local`,
  `contact_sheet_bridge_path` y `orchestrator_review_needed`.
- El frente Telegram establece que una entrega confirmada requiere `ok=true` y
  `message_id` real; una cola/outbox no equivale a enviado.
- El resultado visual previo de Telegram Directo propone que todo claim visual
  relevante este respaldado por adjunto, `media_id`, frame, OCR o transcripcion.

## inferencias

- Infiero que el mismo criterio de evidencia visual de Telegram Directo debe
  aplicarse antes de aceptar un reel CMP como premium, porque ambos riesgos
  comparten la misma falla: una afirmacion visual sin respaldo inspeccionable.
- Infiero que el checklist manual reduce errores de criterio, pero no bloquea
  de forma confiable los P0 repetibles. Por eso conviene una validacion local
  deterministica para campos minimos y una revision humana para gusto editorial.
- Infiero que `material_set_id` o un identificador equivalente debe ser
  obligatorio para evitar arrastre de assets entre reels, incluso si el operador
  trabaja en la misma carpeta local.

## premium_checklist_minimo

| Check | Bloquea | Condicion de pase |
| --- | --- | --- |
| `preview_silencioso` | Preview o pieza silenciosa presentada como final. | `final_or_preview=final_candidate`, `audio_status` no silencioso, o decision silenciosa explicitamente pedida y justificada. |
| `visual_claim_without_evidence` | Claim visual no respaldado por material fuente. | Cada claim del guion/caption/storyboard mapea a `media_id`, `frame_id`, OCR, transcripcion o `asset_manifest_id`; si no hay evidencia, se omite o marca no verificado. |
| `wrong_material_set` | Mezcla de assets de reels distintos o contexto viejo. | Cada asset pertenece al mismo `material_set_id` del job actual; reutilizacion solo si el job lo autoriza explicitamente. |
| `missing_delivery_receipt_message_id` | "Entregado/enviado" sin recibo real. | Solo se declara entrega con `ok=true`, `message_id` real y topic/reply target esperado. |
| `insufficient_visual_evidence` | Pieza imposible de auditar. | Contact sheet seguro de 8-12 frames, datos tecnicos, ruta local del candidato final y `orchestrator_review_needed=true`. |
| `asset_state_not_resolved` | Uso de material marcado dudoso. | Ningun asset con `needs_crop`, `safe_candidate` o `needs_review` sin resolucion documentada. |
| `cmp_contact_mismatch` | Contacto CMP incorrecto o ilegible. | Cierre con `@drcarloszanardi`, `2364384321` y `www.centromedicopellegrini.com.ar`, legibles en celular. |

## risks_p0_p1_p2

| Pri | Riesgo | Clasificacion operativa | Mitigacion |
| --- | --- | --- | --- |
| P0 | `preview_silencioso` como entrega premium. | Falsa aceptacion del producto final y perdida directa de confianza. | Hard fail si no hay audio o permiso explicito de silencio. |
| P0 | `visual_claim_without_evidence`. | Invencion visual o medica; puede afirmar elementos que el montaje no muestra. | Mapeo obligatorio claim -> evidencia. |
| P0 | `wrong_material_set`. | Contaminacion entre reels, tema equivocado o uso de material no autorizado para ese job. | `material_set_id` obligatorio y reset de contexto por job. |
| P0 | `missing_delivery_receipt_message_id`. | Declarar enviado sin prueba tecnica, o enviar al topic equivocado. | Gate de `ok=true`, `message_id` y topic/reply target. |
| P1 | Asset visual con recorte, privacidad o legibilidad sin resolver. | Puede degradar calidad o exponer informacion no deseada. | Bloquear estados `needs_*` hasta resolucion. |
| P1 | Pieza tecnicamente valida pero editorialmente pobre. | No cumple benchmark CMP aunque pase privacidad/tecnica. | Revision humana del MP4/contact sheet antes de publicar. |
| P1 | Datos CMP correctos pero ilegibles en celular. | La pieza no sirve como cierre institucional. | QA en 1080x1920 y preview 540x960. |
| P2 | Timing, transiciones o copy mejorables sin riesgo factual. | Pulido editorial. | Ajuste posterior si no afecta publicacion ni verdad visual. |

## fixtures_sinteticos

1. `premium_gate_blocks_silent_preview_without_explicit_silent_approval`
   - Input sintetico: `final_or_preview=preview_not_final`, `audio_status=silent`,
     sin `silent_requested_by_doctor`.
   - Esperado: `pass_premium_gate=false`, razon `preview_silencioso`.

2. `premium_gate_rejects_visual_claim_without_evidence_id`
   - Input sintetico: caption dice "se ve microscopio y neuroimagen" pero el
     storyboard no declara `media_id`, `frame_id`, OCR ni transcripcion para ese
     claim.
   - Esperado: hard fail `visual_claim_without_evidence`.

3. `premium_gate_rejects_cross_reel_material_set_mismatch`
   - Input sintetico: job actual `material_set_id=reel_consulta_columna_20260528`
     y un asset declara `material_set_id=dia_patria_20260525`.
   - Esperado: hard fail `wrong_material_set`.

4. `premium_gate_requires_delivery_message_id_and_topic_match`
   - Input sintetico: envio con `queued=true`, `ok` ausente o `message_id=null`,
     o topic diferente del esperado.
   - Esperado: no se permite declarar "entregado"; razon
     `missing_delivery_receipt_message_id`.

5. `premium_gate_rejects_unresolved_asset_and_missing_contact_sheet`
   - Input sintetico: asset con `needs_crop=true` y sin contact sheet auditable.
   - Esperado: hard fail `asset_state_not_resolved` e
     `insufficient_visual_evidence`.

## recommendation

Implementar un guard local simple como requisito de aceptacion para REELS CMP.
Debe validar campos estructurados antes de que una pieza pueda llamarse
`final_candidate`, `premium`, `publicable` o `delivered`.

El checklist manual queda util para observacion editorial, pero no como unica
defensa. Los P0 deben fallar automaticamente; el juicio humano debe concentrarse
en si la pieza supera el benchmark CMP, no en recordar condiciones repetibles.

## confidence

Alta para recomendar guard local simple: las reglas ya existen en el bridge y el
alcance del job es declarativo. Media para especificar nombres finales de campos,
porque la implementacion real puede usar nombres distintos a `material_set_id` o
`frame_id`; el contrato puede mapearlos sin cambiar el criterio.

## attempted_routes

- Se hizo `git pull --rebase origin main`.
- Se ejecuto `./scripts/personal_xh_check.sh` y se detecto el job asignado.
- Se reviso el workorder actual.
- Se revisaron documentos canonicos de REELS CMP y Telegram.
- Se revisaron resultados previos de gate premium y evidencia visual.
- No se abrieron ni usaron bibliotecas, adjuntos reales, multimedia privado,
  Telegram, Gmail, Drive, Calendar, iCloud, Photos ni servicios externos.

## risks_limits

- Resultado declarativo: no modifica archivos operativos ni ejecuta suites de la
  app real.
- No certifica renders, MP4, audio, miniaturas ni material multimedia.
- No decide publicacion; la decision final queda en Codex orquestador.
- El guard propuesto debe adaptarse a los nombres de campos reales del pipeline
  si difieren de los nombres usados aqui.

## evidence_paths

- `jobs/20260528T064336-reels-cmp-premium-visual-evidence-gate-review-v1.md`
- `docs/reels_premium_acceptance_gate.md`
- `context/fronts/reels_cmp.md`
- `context/fronts/telegram.md`
- `results/20260528T062330-telegram-direct-visual-evidence-guard-review-v1.result.md`
- `results/20260525T133959-reel-dia-patria-v2-return-premium-gate.result.md`
