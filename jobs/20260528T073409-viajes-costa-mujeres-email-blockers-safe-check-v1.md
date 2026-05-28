---
id: 20260528T073409-viajes-costa-mujeres-email-blockers-safe-check-v1
created_at: 2026-05-28T07:34:09-03:00
created_by: orchestrator
assignee: personal-xh
front: VIAJES
model: gpt-5.5-xh
reasoning_effort: xhigh
status: queued
no_external_actions: true
no_secrets: true
---

# viajes-costa-mujeres-email-blockers-safe-check-v1

## Objetivo

Pablo, preparar un chequeo seguro de bloqueos/datos minimos para avanzar con
los mails de Costa Mujeres solicitados por el Doctor desde Telegram Directo,
sin enviar nada y sin tocar Gmail/Drive/iCloud/Photos.

Contexto operativo:

- Topic VIAJES: thread `4693`.
- Ultimo pedido humano pendiente en handoff: `message_id 5395`, texto:
  "Manda los mails desde administración Zanardi. Lenguaje formal conmigo en
  copia oculta".
- El orquestador no debe enviar mails desde heartbeat sin autorizacion humana
  especifica y sin datos minimos.
- Ya existian resultados previos de Costa Mujeres:
  - `results/20260528T010945-viajes-costa-mujeres-vuelos-hoteles-all-inclusive-v1.result.md`
  - `results/20260528T013026-viajes-costa-mujeres-direct-flight-price-validation-v2.result.md`
  - `results/20260528T014015-viajes-costa-mujeres-official-quote-request-pack-v1.result.md`
  - `results/20260528T031057-viajes-costa-mujeres-email-final-preflight-v1.result.md`

## Alcance permitido

- Revisar solo archivos/resultados del bridge sobre Costa Mujeres y el contexto
  citado arriba.
- No enviar Telegram, mails ni contactar proveedores.
- No acceder a Gmail, Drive, Calendar, iCloud, Photos ni adjuntos reales.
- No imprimir secretos ni datos personales.

## Entregable esperado

1. `summary` breve.
2. `ready_to_send`: true/false.
3. `blocking_missing_fields`: lista concreta de datos faltantes para poder
   preparar/enviar mails formalmente desde Administracion Zanardi.
4. `safe_draft_requirements`: requisitos minimos del texto formal con Doctor en
   copia oculta, sin inventar correo ni identidad de envio.
5. `single_next_action`: una unica accion para Codex orquestador.

## Reglas

- Mantener salida breve, formal y operativa.
- Separar evidencia de inferencias.
- Si falta correo BCC del Doctor, alias/cuenta exacta de Administracion
  Zanardi, pasajeros o datos de habitaciones, marcar como bloqueo.
- La decision final y cualquier envio real queda en Codex orquestador con
  autorizacion humana.
