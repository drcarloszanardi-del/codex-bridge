---
id: 20260528T031057-viajes-costa-mujeres-email-final-preflight-v1
created_at: 2026-05-28T03:10:57-03:00
created_by: orchestrator
assignee: personal-xh
front: VIAJES
model: gpt-5.5-xh
reasoning_effort: xhigh
status: queued
no_external_actions: true
no_secrets: true
---

# viajes-costa-mujeres-email-final-preflight-v1

## Objetivo

Pablo, preparar una preflight final para enviar mails formales de Costa Mujeres desde identidad "Administración Zanardi", con el Doctor en copia oculta, sin enviar nada.

El pedido humano vigente por Telegram fue: "Manda los mails desde administración Zanardi. Lenguaje formal conmigo en copia oculta". Codex Desktop no debe enviar desde heartbeat; este job debe dejar la pieza lista y detectar faltantes concretos.

## Contexto principal

Usar solo estos resultados y contexto local del bridge:

- `results/20260528T010945-viajes-costa-mujeres-vuelos-hoteles-all-inclusive-v1.result.md`
- `results/20260528T013026-viajes-costa-mujeres-direct-flight-price-validation-v2.result.md`
- `results/20260528T014015-viajes-costa-mujeres-official-quote-request-pack-v1.result.md`
- `results/20260528T014351-rework-20260528T014015-viajes-costa-mujeres-official-qu.result.md`

## Alcance permitido

- Revisar los resultados anteriores, extraer destinatarios hoteleros/aereos ya citados y consolidar cuerpos de mail.
- Buscar solo en web publica si falta confirmar un email institucional visible, priorizando sitios oficiales.
- No enviar mails.
- No abrir Gmail, Drive, Calendar, iCloud, Photos ni adjuntos personales.
- No usar ni imprimir secretos.
- No cargar datos personales de la familia.
- No iniciar reserva, hold, compra ni formulario con datos personales.

## Entregable esperado

1. Lista final de destinatarios separados por mail:
   - Catalonia Grand Costa Mujeres.
   - RIU Dunamar.
   - RIU Palace Costa Mujeres si corresponde como alternativa.
   - Aerolineas/Copa solo si hay email institucional claro para cotizacion; si no, declarar ruta alternativa de cotizacion sin inventar correo.
2. Asunto y cuerpo formal de cada mail, en español, con remitente conceptual "Administración Zanardi".
3. Campos obligatorios que faltan antes del envio real:
   - email real del Doctor para BCC, si no esta disponible de forma segura;
   - cuenta/remitente Gmail configurado o alias disponible para que figure "Administración Zanardi";
   - cantidad final adultos/menores y edad exacta del menor al 17/07/2026;
   - si acepta habitaciones conectadas o adyacentes;
   - rango maximo aceptable para aereo directo.
4. Checklist de seguridad antes del envio: no enviar desde cuenta improvisada, no declarar reserva, no incluir datos personales innecesarios, no prometer compra.
5. Un `draft_para_orquestador` breve con decision: listo para enviar / faltantes que bloquean envio.

## Reglas

- No cerrar con "enviado"; este job no envia.
- No inventar destinatarios.
- No inventar datos de pasajeros.
- No usar lenguaje informal.
- No mezclar con Bayahibe ni pedidos de computadora.
- Si una fuente oficial no expone email, proponer ruta alternativa concreta: formulario oficial, telefono, agencia o pedido de cotizacion humana.
