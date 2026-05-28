---
id: 20260528T013026-viajes-costa-mujeres-direct-flight-price-validation-v2
created_at: 2026-05-28T01:30:26-03:00
created_by: orchestrator
assignee: personal-xh
front: VIAJES
model: gpt-5.5-xh
reasoning_effort: xhigh
status: queued
no_external_actions: true
no_secrets: true
---

# viajes-costa-mujeres-direct-flight-price-validation-v2

## Objetivo

Pablo, hacer una segunda pasada acotada sobre Costa Mujeres para validar el punto mas importante que quedo abierto: si conviene Aerolineas directo saliendo jueves 16/07/2026 de noche o viernes 17/07/2026 temprano, y regresando 24/07 o 25/07, frente a Copa via Panama.

## Contexto

El informe base ya fue entregado al topic VIAJES por el orquestador:

- Catalonia Grand Costa Mujeres + Copa estimado: USD 8.765 + tasa ambiental.
- RIU Dunamar + Copa estimado: USD 8.625.
- RIU Palace + Copa estimado: USD 10.095.
- La duda abierta es si Aerolineas directo permite ganar mas playa real con una diferencia razonable de precio.

## Alcance permitido

- Investigar solo fuentes publicas: Aerolineas Argentinas, Copa, buscadores publicos como referencia secundaria, y sitios oficiales de hoteles si hace falta confirmar noche extra/early check-in.
- No comprar, reservar, iniciar hold, pagar, usar credenciales ni contactar terceros.
- No enviar Telegram real ni mails.
- No usar Gmail, Drive, iCloud, Photos ni datos sensibles.

## Entregable esperado

1. Comparar 3 escenarios:
   - Copa EZE-CUN 17/07 ida + 24/07 vuelta.
   - Aerolineas directo saliendo 16/07 noche o 17/07 y volviendo 24/07.
   - Aerolineas directo agregando regreso 25/07 o noche extra si mejora playa/costo.
2. Para cada escenario: horarios, escalas, duracion, precio por pasajero y total 5 pax si figura, moneda, equipaje visible, fuente/URL y timestamp.
3. Impacto en dias completos de playa y necesidad de early check-in/noche extra.
4. Recomendacion corta: mantener Copa, subir a Aerolineas directo, o pedir cotizacion humana.
5. Borrador listo para topic VIAJES, con lenguaje prudente y sin decir reserva.

## Reglas

- No cerrar con "no pude"; si una web falla, intentar ruta alternativa y documentar limite exacto.
- No enviar mensajes externos.
- No tocar secretos ni credenciales.
- Tratar precios como dinamicos y no garantizados.
- La decision final queda en Codex orquestador.
