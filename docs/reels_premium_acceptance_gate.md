# Reels CMP Premium Acceptance Gate

Actualizado: 2026-05-25.

## Regla de CEO

Un reel no se acepta por estar renderizado. Codex orquestador debe rechazar cualquier pieza que sea visualmente correcta pero no transmita una idea clara, no use material propio real cuando fue pedido, sea solo placas genericas, o llegue como preview incompleto.

## No pasa

- Pieza silenciosa si se pidio reel publicable.
- "Preview" presentado como entrega.
- Solo placas/texto sin video o imagenes propias cuando el Doctor pidio material nuestro.
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
