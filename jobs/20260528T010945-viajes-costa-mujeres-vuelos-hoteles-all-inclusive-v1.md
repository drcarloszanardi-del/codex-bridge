---
id: 20260528T010945-viajes-costa-mujeres-vuelos-hoteles-all-inclusive-v1
created_at: 2026-05-28T01:09:45-03:00
created_by: orchestrator
assignee: personal-xh
front: VIAJES
model: gpt-5.5-xh
reasoning_effort: xhigh
status: queued
no_external_actions: true
no_secrets: true
---

# viajes-costa-mujeres-vuelos-hoteles-all-inclusive-v1

## Objetivo

Pablo, preparar una cotizacion comparativa para Costa Mujeres / Cancun all inclusive, priorizando que los vuelos encajen para maximizar dias completos de playa.

Pedido del Doctor desde Telegram Directo:

- Costa Mujeres.
- Hoteles all inclusive en linea RIU o Barcelo, o calidad equivalente.
- Dos habitaciones.
- Incluir vuelos e itinerario completo.
- Revisar aerolineas directo, no solo agregadores.
- Buscar seteos de menor costo en dolares/pesos.
- Entregar informe para el topic VIAJES.

## Supuestos de trabajo

- Usar como fecha objetivo base 17 a 24 de julio de 2026, salvo que encuentres evidencia local reciente de otra fecha para Costa Mujeres.
- Usar grupo familiar de 5 personas como supuesto operativo: 4 adultos + 1 menor de 10, coherente con el corte Bayahibe reciente. Si una fuente exige edades exactas, marcarlo como dato a confirmar, no inventarlo.
- Usar Buenos Aires como origen probable y comparar EZE/AEP cuando aplique. Si no se puede confirmar origen, declarar el supuesto.

## Alcance permitido

- Usar fuentes publicas web y sitios oficiales de aerolineas/hoteles/agencias para investigacion.
- No comprar, reservar, pagar, iniciar holds, usar credenciales ni contactar terceros.
- No usar Gmail, Drive, iCloud, Photos ni datos sensibles.
- No enviar Telegram real; entregar resultado en `results/` para que el orquestador decida.

## Entregable esperado

1. Tabla corta de 3 a 5 paquetes/caminos viables:
   - hotel/resort,
   - fechas,
   - configuracion de habitaciones,
   - vuelos sugeridos con aerolinea, escalas, horarios, equipaje si figura,
   - noches reales y dias completos de playa estimados,
   - precio total y moneda,
   - fuente/URL y timestamp de consulta.
2. Mejor opcion recomendada y por que.
3. Opciones de seteo para bajar costo:
   - mover salida/llegada +/- 1 o 2 dias,
   - cambiar aeropuerto,
   - separar hotel/vuelo vs paquete,
   - comparar dos habitaciones vs familiar/conectada.
4. Riesgos y datos a confirmar antes de avanzar.
5. Borrador breve listo para reportar al topic VIAJES, sin afirmar reserva ni disponibilidad garantizada si no hay hold real.

## Reglas

- No cerrar con "no pude"; si una web falla, intentar rutas alternativas y documentar limite exacto.
- No enviar mensajes externos.
- No tocar secretos ni credenciales.
- No publicar, comprar, reservar ni contactar terceros.
- La decision final queda en Codex orquestador.
