# Reels CMP Premium Acceptance Gate

Actualizado: 2026-05-26.

## Regla de CEO

Un reel no se acepta por estar renderizado. Codex orquestador debe rechazar cualquier pieza que sea visualmente correcta pero no transmita una idea clara, no use material propio real cuando fue pedido, sea solo placas genericas, o llegue como preview incompleto.

El piso minimo de calidad para CMP es el reel del 25 de Mayo 2026 sobre creatividad argentina/trabajo real. Toda pieza nueva debe igualar o superar ese benchmark en narrativa, ritmo, seleccion visual, calidad cinematografica, integracion de marca y cierre institucional. Si no lo supera, no se envia.

## No pasa

- Pieza silenciosa si se pidio reel publicable.
- "Preview" presentado como entrega.
- Rehacer sobre una base que el Doctor ya rechazo por calidad editorial, salvo que el pedido sea explicitamente "rescatala" o "retocala".
- Reel medico desafiante sin direccion editorial escrita antes del render: concepto, emocion, secuencia visual, assets propios/seguros y razon de cada plano.
- Reel institucional o medico por debajo del benchmark 25 de Mayo 2026.
- Solo placas/texto sin video o imagenes propias cuando el Doctor pidio material nuestro.
- Suma de fotos con zoom/pan si no construye una historia visual reconocible.
- Contact sheet donde los planos humanos se vean oscuros, lavados, mal recortados o con texto diminuto.
- Cierre que parezca aviso de WhatsApp/folleto de baja calidad en lugar de pieza institucional premium.
- Asset marcado `needs_crop`, `safe_candidate` o `needs_review` sin recorte/revision resuelta.
- Contacto incorrecto o ilegible.
- Falta de QA cuadro a cuadro/contact sheet.
- Texto generico que podria pertenecer a cualquier clinica.
- No mostrar el archivo final o una evidencia visual suficiente para auditarlo.

## Debe pasar todo

1. **Contenido**: idea central clara en los primeros 3 segundos.
2. **Progresion**: tesis -> medicina concreta -> comunidad/CMP -> cierre.
3. **Material propio**: minimo dos bloques visuales reales propios/autorizados, no solo placas.
4. **Ritmo**: 25-40 segundos, sin pausas muertas ni texto excesivo.
5. **Audio**: musica segura, locucion o decision explicita justificada. No entregar silencioso salvo pedido.
6. **Privacidad**: sin pacientes, HC, estudios identificables, pantallas, nombres, DNI o datos.
7. **Visual**: sin solapamientos, sin marcas de agua, sin texto placeholder, legible en celular.
8. **Contacto**: `@drcarloszanardi`, `2364384321`, `www.centromedicopellegrini.com.ar`.
9. **Evidencia**: contact sheet seguro con 8-12 frames y datos tecnicos del MP4.
10. **Aprobacion**: Codex orquestador lo revisa antes de enviarlo al Doctor.
11. **Evidencia audiovisual**: si el bridge no puede transportar el MP4 final, Pablo debe entregar proxy seguro o contact sheet suficiente para juzgar ritmo, encuadre y cierre. Un contact sheet pobre falla aunque el manifiesto tecnico pase.
12. **Juicio editorial**: Codex debe poder decir en una frase que transmite el reel y por que esos planos representan la patologia/caso; si esa frase suena generica, el reel falla.
13. **Caso clinico complejo**: cavernoma, columna, neurocirugia o procedimientos de alto impacto requieren material propio/sanitizado o referencias medicas reales de calidad; no usar anatomia generica ni stock que parezca desconectado del caso.

## Hard stop tras rechazo del Doctor

Si el Doctor califica una pieza como mala o no publicable:

- Marcar el proyecto `rejected_by_doctor_editorial_quality`.
- No enviar otra version basada en la misma estructura.
- Hacer nueva direccion editorial desde cero antes de renderizar.
- Revisar contact sheet/video completo con criterio editorial, no solo privacidad/tecnica.
- Si no hay material propio suficiente, pedir el asset minimo o proponer una pieza institucional alternativa sin simular caso clinico.

## Historias CMP

Las historias institucionales o asociadas al Centro Medico Pellegrini no se aprueban como simples placas personales. Deben tener plantilla CMP reconocible, logo visible, texto legible en celular, contacto exacto y evidencia visual auditable.

Falla si:

- falta logo o marca CMP cuando el pedido es institucional;
- el texto requiere zoom para leerse en telefono;
- el telefono, web o IG estan ausentes, incorrectos o demasiado chicos;
- la foto del regalo/caso ocupa la pieza sin una idea narrativa clara;
- no hay JPG/PNG final ni preview/contact sheet para revisar.

Salida minima para historias:

- `story_paths`
- `preview_540x960_paths`
- `text_blocks`
- `contact_fields`
- `template_present: true/false`
- `mobile_legibility: pass/fail`
- `orchestrator_review_needed: true`

## Salida minima de Pablo

Pablo debe devolver:

- `final_or_preview`: `final_candidate` o `preview_not_final`.
- `pass_premium_gate`: `true` solo si cumple todos los puntos.
- `render_path_local`.
- `contact_sheet_path_local`.
- `contact_sheet_bridge_path` si es seguro y menor a 800 KB.
- `audio_status`.
- `asset_privacy_status`.
- `orchestrator_review_needed`.

Si no puede mostrar evidencia visual segura, debe marcar `pass_premium_gate: false`.
