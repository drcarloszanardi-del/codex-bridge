---
job_id: 20260526T233419-reels-lumbar-cinematic-v3-shotlist-and-gate-review
worker: personal-xh
status: completed
completed_at: 2026-05-26T23:55:10-03:00
front: REELS
no_external_actions: true
no_secrets: true
---

# Resultado - Reels lumbar cinematic v3 shotlist and gate review

## summary

Veredicto: **no aprobar el proxy v2 como final y no renderizar v3 con la misma
base sin pedir material real adicional**.

El proxy v2 mejora frente al reset anterior porque baja texto y ya intenta una
logica de RM -> tecnica -> cierre. Pero por contact sheet sigue debajo del gate
premium: depende demasiado del monitor de pared en quirofano, repite la misma
familia de planos, duplica el beat `Liberar la raiz`, y no demuestra por si solo
transiciones cinematicas ni audio final. La pieza todavia se siente mas como
registro tecnico proyectado en pantalla que como reel CMP premium.

La direccion v3 debe pasar de "mostrar una pantalla que muestra cirugia" a
"construir una decision clinica y tecnica con planos propios": RM anonima,
planificacion/mano/doctor, abordaje tubular real, gesto quirurgico corto y
cierre CMP legible.

No renderice, no use Telegram/Gmail/Drive/Calendar, no abri bibliotecas privadas
y no toque credenciales.

## coverage_table

| Fuente | Estado | Uso |
| --- | --- | --- |
| `jobs/20260526T233419-reels-lumbar-cinematic-v3-shotlist-and-gate-review.md` | Revisada | Pedido, entregables y restricciones. |
| `context/fronts/reels_cmp.md` | Revisada | Identidad CMP, contacto canonico y gate visual. |
| `docs/reels_premium_acceptance_gate.md` | Revisada | Hard stop, benchmark premium y criterios de rechazo. |
| `context/fronts/reels_cmp_cinematic_references_2026-05-26.md` | Revisada | Reglas de menos texto, mas imagen real y transiciones motivadas. |
| `results/20260526T230823-reels-cmp-low-text-transition-quality-reset-v1.result.md` | Revisada | Reset por rechazo: no salvar con mas placas/texto. |
| `context/asset_packs/20260526-lumbar-cinematic-v2-proxy/manifest.md` | Revisada | Estado del proxy v2 y evaluacion inicial del orquestador. |
| `context/asset_packs/20260526-lumbar-cinematic-v2-proxy/contact_sheet.jpg` | Revisada visualmente | Auditoria frame a frame por contacto sheet. |

## qa_verdict

```yaml
proxy_v2_gate: fail
publication_hold: true
pass_premium_gate: false
render_v3_now_with_same_visible_base: false
orchestrator_review_needed: true
doctor_send_ready: false
privacy_from_contact_sheet_only: no_identifiers_seen_but_requires_frame_review
audio_status: proxy_silent_or_not_audited
contact_sheet_status: useful_but_insufficient_for_motion_transitions_audio
```

Razones principales:

1. El reel depende de planos repetidos del monitor de pared, con poco control
   cinematografico del encuadre.
2. Hay poca variedad de bloques propios: falta Doctor, planificacion, mano,
   consultorio o contexto humano autorizado.
3. La mejor imagen es el close quirurgico de 15s, pero usado sin suficiente
   contexto puede verse grafico y no necesariamente educativo para publico.
4. `Liberar la raiz` aparece dos veces como beat, lo que reduce progresion.
5. El cierre CMP aparece correcto en intencion, pero desde el contact sheet
   conviene revisar legibilidad mobile de web, telefono e Instagram.
6. El contact sheet tiene 8 muestras; el gate pide evidencia mas granular
   cuando el candidato se acerca a publicacion.

## contact_sheet_findings

| Tiempo | Lectura | Gate |
| ---: | --- | --- |
| 1s | Monitor de pared con titulo `Descompresion lumbar`. Hook correcto en tema, pero visualmente institucional debil. | Rehacer hook. |
| 5s | RM anonima/recortada con `La causa`. Buen bloque de evidencia si no tiene datos. | Mantener, con movimiento sobrio. |
| 9s | Monitor de pared + `Abordaje tubular`. Mismo lenguaje visual que 1s. | No repetir como eje. |
| 15s | Close quirurgico + `Liberar la raiz`. Plano mas fuerte y mas propio. | Usar corto, con autorizacion y contexto. |
| 22s | Vuelve `Liberar la raiz` en monitor de pared. | Eliminar duplicacion. |
| 29s | Monitor de pared + `Precision`. Generico si no hay accion nueva. | Cambiar por detalle real o mano/instrumental. |
| 36s | Monitor de pared + `Control permanente`. Repite ambiente y composicion. | Necesita otro tipo de plano. |
| 42s | RM + tarjeta CMP/contacto. Cierre con marca, pero posible texto pequeno. | Revisar 540x960 y 4s estable. |

## shotlist_v3

Shotlist recomendado para un v3 de 44-52s. Si no existen estos planos en assets
propios/autorizados, pedirlos antes de renderizar.

| Tiempo | Funcion | Imagen | Texto maximo |
| --- | --- | --- | --- |
| 0-3s | Hook visual | Close quirurgico breve o RM anonima muy limpia, no monitor de pared. | `La raiz comprimida` |
| 3-7s | Causa | RM/placa anonima con foco en compresion, sin headers ni datos. | `La causa` |
| 7-12s | Criterio | Doctor, mano o esquema propio marcando nivel/objetivo en papel limpio. | `El plan` |
| 12-18s | Acceso | Abordaje tubular/instrumental real, encuadre cerrado y estable. | `Abordaje tubular` |
| 18-27s | Gesto tecnico | 1 o 2 closes quirurgicos maximo, sin gore innecesario. | `Liberar la raiz` |
| 27-34s | Seguridad | Monitoreo/control con plano diferente al wall-monitor repetido. | `Control permanente` |
| 34-42s | Confianza CMP | Doctor trabajando, consultorio, pasillo o detalle institucional limpio. | `Criterio y precision` |
| 42-50s | Cierre | Placa CMP sobria, logo/contacto grande, fondo real o neutro. | `Centro Medico Pellegrini` |

Regla editorial: cada bloque debe cambiar de informacion visual. Si dos planos
solo muestran el mismo monitor de pared con otro texto, el segundo queda afuera.

## transition_plan

| Paso | Transicion | Regla |
| --- | --- | --- |
| Hook -> RM | Corte directo o micro dissolve 6-8 frames por continuidad anatomica. | No flash, wipe ni zoom de plantilla. |
| RM -> plan | Match cut de linea/curva: zona marcada en RM hacia mano/esquema. | La mano o el gesto debe justificar el corte. |
| Plan -> abordaje | J-cut de voz o audio ambiente antes del plano tecnico. | No silencio entre bloques. |
| Abordaje -> liberar raiz | Match-on-action: instrumento/entrada -> close quirurgico. | Evitar saltar de monitor a monitor. |
| Liberar raiz -> control | L-cut: mantener audio/voz mientras cambia a monitoreo. | Usar plano nuevo, no otro wall-monitor igual. |
| Control -> CMP | Respiracion visual corta: consultorio/doctor antes de placa. | No cierre abrupto desde cirugia grafica a logo. |
| CMP -> final | Placa quieta 4s minimo. | Contacto sin animacion que reduzca legibilidad. |

## text_budget

Texto total recomendado en pantalla, excluyendo contacto: 18 palabras. No usar
subtitulos explicativos largos.

```text
La raiz comprimida
La causa
El plan
Abordaje tubular
Liberar la raiz
Control permanente
Criterio y precision
Centro Medico Pellegrini
```

Contacto final canonico:

```text
@drcarloszanardi
2364384321
www.centromedicopellegrini.com.ar
```

Restricciones de texto:

- No repetir `Liberar la raiz`.
- No usar frases de mas de una linea en mobile.
- No poner definiciones ni explicaciones como placas.
- Si falta voz, el texto no debe compensar con mas palabras; falta audio o falta
  material, no falta caption.

## asset_request_for_doctor

Pedido minimo para que v3 pueda entrar a gate premium:

```text
Para armar el reel lumbar con menos texto y mas imagen real, mandame por REELS:

1. Un video vertical de 10-15s tuyo en consultorio o quirofano limpio diciendo la idea central en una frase.
2. Un plano vertical de 6-10s de mano marcando en una RM anonima o dibujando columna/raiz en papel blanco.
3. Uno o dos planos verticales de 5-8s del abordaje/instrumental sin pacientes ni datos visibles.
4. Si esta autorizado, un close quirurgico corto y seguro para publico general.
5. Un plano de CMP/consultorio o del equipo trabajando sin pacientes, nombres, HC, fechas ni pantallas con datos.
6. Una nota de voz opcional con tus palabras exactas para la locucion.

No mandar pacientes identificables, historias clinicas, nombres, DNI, fechas,
interfaces de estudios con datos, ni pantallas con informacion privada.
```

Asset minimo si hay que destrabar rapido:

```text
1 video del Doctor + 1 plano de mano/esquema + 1 plano tecnico propio + cierre CMP.
```

## render_constraints

- No renderizar final si el material visible sigue siendo mayormente monitor de
  pared.
- No usar stock ni anatomia generada como evidencia clinica.
- No convertir el reel en slideshow de RM, fotos o placas con zoom.
- No usar el proxy v2 como final.
- No publicar sin audio decidido: voz, musica licenciada o version
  explicitamente silenciosa aprobada.
- No publicar sin contact sheet 10-12 frames y review de legibilidad a 540x960.
- No publicar si telefono, Instagram o web quedan por debajo de lectura mobile.
- No usar material quirurgico si falta autorizacion editorial/medico-legal.
- Mantener cierre CMP sobrio, estable y minimo 4s.

## risks_limits

- La auditoria se hizo sobre contact sheet, no sobre reproduccion de video; por
  eso no puedo certificar fluidez de transiciones, ritmo real ni audio.
- El proxy fue descrito como silenciado/no apto final, asi que audio sigue
  pendiente.
- En las muestras no vi pacientes ni datos identificables, pero una revision
  frame a frame del video completo sigue siendo obligatoria.
- El close quirurgico puede ser util y propio, pero tambien puede ser grafico;
  debe usarse corto, contextualizado y con autorizacion.
- Si los assets originales solo contienen el wall-monitor repetido, el v3 no
  deberia renderizarse: primero hay que pedir material.

## recommendation

Recomiendo **hold de publicacion y pedido de material antes de v3 final**. La
opcion correcta no es agregar mas texto ni repetir el monitor con transiciones:
es reconstruir el reel con 3-5 planos reales distintos y un cierre CMP legible.

Si el orquestador ya tiene ocultos en el pack los clips de Doctor, mano,
planificacion, instrumental y CMP, entonces puede renderizar v3 siguiendo este
shotlist. Si no los tiene, la siguiente accion es pedir el asset minimo al
Doctor y dejar el proxy v2 solo como evidencia de direccion, no como base final.

## confidence

Media-alta para el veredicto editorial por la evidencia del contact sheet y los
gates revisados. Media para privacidad/transiciones/audio porque requieren
video completo, no solo fotogramas.

## evidence_paths

- `jobs/20260526T233419-reels-lumbar-cinematic-v3-shotlist-and-gate-review.md`
- `context/fronts/reels_cmp.md`
- `docs/reels_premium_acceptance_gate.md`
- `context/fronts/reels_cmp_cinematic_references_2026-05-26.md`
- `results/20260526T230823-reels-cmp-low-text-transition-quality-reset-v1.result.md`
- `context/asset_packs/20260526-lumbar-cinematic-v2-proxy/manifest.md`
- `context/asset_packs/20260526-lumbar-cinematic-v2-proxy/contact_sheet.jpg`
