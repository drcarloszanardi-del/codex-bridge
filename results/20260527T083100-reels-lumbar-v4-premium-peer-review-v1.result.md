---
job_id: 20260527T083100-reels-lumbar-v4-premium-peer-review-v1
worker: personal-xh
status: completed
completed_at: 2026-05-27T08:36:00-03:00
front: REELS
no_external_actions: true
no_secrets: true
---

# Resultado - Reels lumbar v4 premium peer review v1

## summary

verdict: **hold_for_v5**.

El v4 mejora claramente contra v2/v3: arranca con video real quirurgico, usa RM
breve, baja texto y el cierre CMP ya esta presente. Como revision interna de
direccion editorial, sirve para mostrar que el camino correcto es menos placa y
mas medicina real. Pero no lo consideraria aceptable como pieza premium final:
la contact sheet todavia se apoya demasiado en la misma familia visual
quirurgica/monitor, repite informacion y no introduce presencia humana, mano,
consultorio ni instrumental limpio fuera de pantalla.

Dictamen limitado a contact sheet: no vi el video completo ni audio, asi que no
certifico ritmo real, transiciones ni legibilidad final cuadro a cuadro. La
proxima accion concreta es pedir un asset minimo corto al Doctor para v5, no
seguir puliendo la misma base.

## coverage_table

| Fuente | Estado | Uso |
| --- | --- | --- |
| `jobs/20260527T083100-reels-lumbar-v4-premium-peer-review-v1.md` | Revisada | Workorder y criterios. |
| `context/asset_packs/20260527-lumbar-v4-premium-review/manifest.md` | Revisada | Contexto editorial declarado por orquestador. |
| `context/asset_packs/20260527-lumbar-v4-premium-review/contact_sheet.jpg` | Revisada visualmente | Evidencia frame a frame disponible. |
| `docs/reels_premium_acceptance_gate.md` | Revisada | Gate premium CMP y hard stops. |
| `context/fronts/reels_cmp.md` | Revisada | Contacto canonico y criterio CMP. |
| `results/20260526T233419-reels-lumbar-cinematic-v3-shotlist-and-gate-review.result.md` | Revisada | Rechazo v2/v3 y pedido de assets. |
| `results/20260526T230823-reels-cmp-low-text-transition-quality-reset-v1.result.md` | Revisada | Reset: menos texto, mas video real, no salvar con placas. |

## findings

| Severidad | Hallazgo | Evidencia contact sheet | Recomendacion |
| --- | --- | --- | --- |
| OK | El arranque ya no parece placa: abre con video real quirurgico. | 1s muestra close quirurgico, no logo ni slide. | Mantener hook real, pero hacerlo mas comprensible y menos crudo con contexto inmediato. |
| OK | RM mas sobria y breve. | 4s y 8s muestran RM anonima/recortada con texto corto `Hernia lumbar` / `La causa`. | Mantener, revisar que no haya headers/datos en video completo. |
| P1 | La pieza sigue sin bloque humano o CMP real antes del cierre. | No aparecen Doctor, mano, consultorio, instrumental limpio, pasillo o equipo; solo RM, cirugia y monitor. | Pedir 1 video Doctor/consultorio y 1 plano mano/esquema para v5. |
| P1 | Repeticion visual quirurgica y monitor sigue pesando demasiado. | 1s, 16s, 22s y 28s son closes quirurgicos muy similares; 12s, 34s y 37s vuelven al monitor de pared. | Reducir a 1-2 planos quirurgicos y reemplazar el resto por planificacion/doctor/CMP real. |
| P1 | El bloque `Control` todavia se siente como monitor grabado. | 34s y 37s repiten monitor de quirofano con pared y equipo secundario. | Si no hay plano alternativo de control/monitoreo, cortar esa idea o pedir asset especifico. |
| P2 | Cierre CMP existe pero debe pasar prueba mobile. | 40s muestra tarjeta CMP con `@drcarloszanardi`, telefono y web; se lee en contact sheet, pero el texto inferior es pequeno. | Asegurar 4s estables y preview 540x960; aumentar telefono/web si hace falta. |

## verdict

```yaml
verdict: hold_for_v5
accept_for_internal_review: true
accept_for_publication_or_doctor_final: false
pass_premium_gate: false
publication_hold: true
privacy_from_contact_sheet_only: no_identifiers_seen_but_video_full_review_required
audio_status: not_audited
contact_sheet_status: sufficient_for_editorial_hold_not_final_approval
```

## top_3_v5_changes

1. **Agregar presencia humana o decision clinica antes de la tecnica.** Un plano
   de Doctor a camara, mano dibujando o RM en papel/tablet limpio haria que el
   reel pase de "cirugia en pantalla" a "criterio medico".
2. **Reducir repeticion de quirurgico/monitor.** Dejar un close fuerte de
   descompresion y un plano tecnico breve; reemplazar 22s/28s/34s/37s por
   planificacion, instrumental limpio o CMP real.
3. **Rehacer cierre mobile-first.** Mantener CMP, pero contacto grande, 4s
   quietos y sin fade que achique la lectura. Validar `2364384321`,
   `@drcarloszanardi` y `www.centromedicopellegrini.com.ar` en 540x960.

## asset_request_minimo

Pedido corto y accionable para el Doctor, sin pedir biblioteca completa:

```text
Para subir el reel lumbar a nivel premium, mandame por REELS solo esto:

1. Un video vertical tuyo de 8-12s en consultorio diciendo una frase central sobre la hernia lumbar o la decision quirurgica.
2. Un plano vertical de 6-8s de mano marcando una RM anonima o dibujando columna/raiz en papel blanco.
3. Un plano vertical de 5-8s de instrumental/abordaje tubular limpio, sin pacientes ni datos visibles.
4. Un plano corto de CMP/consultorio/pasillo o equipo trabajando, sin pacientes, nombres, HC, fechas ni pantallas con datos.

Si hay poco tiempo: 1 video tuyo + 1 mano/esquema + 1 plano CMP limpio.
```

## recommendation

Recomendacion unica: **mantener v4 como revision interna y abrir v5 con asset
request minimo**. No lo rechazaria como avance, porque corrige parte del camino
v2/v3. Pero no lo aceptaria como final premium ni seguiria renderizando sobre
la misma base visible sin sumar Doctor/mano/CMP real.

## attempted_routes

- Se hizo `git pull --rebase`.
- Se inspeccionaron jobs asignados con `./scripts/personal_xh_check.sh`.
- Se reclamo el job con `python3 scripts/bridgectl.py claim`.
- Se reviso el workorder, manifest, gate premium, frente REELS/CMP y resultados
  previos indicados.
- Se reviso visualmente `contact_sheet.jpg`.
- No se envio Telegram/Gmail/Drive/Calendar ni se abrieron bibliotecas privadas.
- No se tocaron credenciales ni secretos.

## risks_limits

- Sin MP4 completo no puedo evaluar fluidez de transiciones, audio, timing exacto
  ni privacidad cuadro a cuadro.
- La contact sheet no prueba legibilidad mobile final; solo sugiere que el
  cierre existe y necesita prueba 540x960.
- El material quirurgico parece seguro en la muestra, pero requiere aprobacion
  editorial/medico-legal y revision completa antes de cualquier publicacion.

## confidence

Media-alta para el veredicto editorial por contact sheet y comparacion con los
gates previos. Media para audio, ritmo y privacidad porque requieren el video
completo.

## evidence_paths

- `jobs/20260527T083100-reels-lumbar-v4-premium-peer-review-v1.md`
- `context/asset_packs/20260527-lumbar-v4-premium-review/manifest.md`
- `context/asset_packs/20260527-lumbar-v4-premium-review/contact_sheet.jpg`
- `docs/reels_premium_acceptance_gate.md`
- `context/fronts/reels_cmp.md`
- `results/20260526T233419-reels-lumbar-cinematic-v3-shotlist-and-gate-review.result.md`
- `results/20260526T230823-reels-cmp-low-text-transition-quality-reset-v1.result.md`
- `claims/20260527T083100-reels-lumbar-v4-premium-peer-review-v1.json`
