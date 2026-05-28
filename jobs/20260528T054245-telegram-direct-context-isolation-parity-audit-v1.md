---
id: 20260528T054245-telegram-direct-context-isolation-parity-audit-v1
created_at: 2026-05-28T05:42:45-03:00
created_by: orchestrator
assignee: personal-xh
front: TELEGRAM
model: gpt-5.5-xh
reasoning_effort: xhigh
status: queued
no_external_actions: true
no_secrets: true
---

# telegram-direct-context-isolation-parity-audit-v1

## Objetivo

Pablo, hacer una auditoria segura y declarativa del puente Telegram Directo -> Codex Desktop enfocada en dos riesgos que el Doctor marco como inadmisibles:

1. Que un pedido por Telegram Directo tenga una calidad/criterio distinto al de este hilo Desktop.
2. Que el sistema mezcle contextos entre frentes, materiales o reels distintos.

Ejemplos de incidentes a cubrir sin abrir adjuntos reales ni exponer datos sensibles:

- Material nuevo de reel enviado por canal directo no debe mezclarse con un reel previo de otro tema.
- No se deben inventar elementos visuales no presentes en el montaje o material fuente.
- Correcciones clinicas simples pedidas por Telegram Directo no deben aplicarse sobre el protocolo equivocado ni alterar otra seccion.

## Alcance permitido

Solo auditoria de bajo riesgo y propuesta de tests/guardrails:

- Leer, si existen, estas rutas puntuales:
  - `/Users/jarvis/.openclaw/workspace/scripts/codex_telegram_direct.py`
  - `/Users/jarvis/.openclaw/workspace/scripts/codex_desktop_telegram_handoff.py`
  - `/Users/jarvis/.openclaw/workspace/tests/telegram/test_desktop_handoff_guardrail.py`
  - archivos de estado/schema bajo `/Users/jarvis/.openclaw/workspace/state/codex_live/` sin imprimir secretos.
- Revisar solo patrones de routing, `topic/thread`, `last_user_turn`, `latest_turn`, `seen`, material IDs, adjuntos declarados y aislamiento de frentes.
- Si falta alguna ruta, usar contexto declarativo y proponer comandos `rg`/fixtures que el orquestador pueda ejecutar.

## Fuera de alcance

- No enviar Telegram, mails ni notificaciones externas.
- No tocar Gmail, Drive, iCloud, Photos ni adjuntos reales.
- No abrir bibliotecas completas.
- No modificar archivos operativos.
- No imprimir tokens, rutas sensibles de adjuntos, datos clinicos identificables ni contenido multimedia.

## Entregable esperado

1. Mapa breve del flujo Telegram Directo -> handoff -> Desktop, con puntos donde puede perderse contexto.
2. Lista P0/P1/P2 de riesgos de mezcla de contexto o baja calidad entre canales.
3. Propuesta concreta de 3 a 6 fixtures/tests sinteticos, por ejemplo:
   - `direct_reel_new_material_does_not_inherit_previous_topic`
   - `direct_visual_claim_requires_declared_media_evidence`
   - `clinical_edit_requires_target_document_identity`
   - `assistant_turn_never_reopens_seen_user_turn`
4. Recomendacion final: cerrar en observacion, agregar tests locales, o pedir autorizacion humana si detectas un bloqueo real.

## Reglas

- Mantener lenguaje formal y operativo para el Doctor.
- Separar evidencia local verificada de inferencias.
- La decision final queda en Codex orquestador.
