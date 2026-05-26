---
id: 20260526T094214-artifactdraft-minimal-filesystem-implementation-v1
created_at: 2026-05-26T09:42:14-03:00
created_by: orchestrator
assignee: personal-xh
front: CODEX-OPS
model: gpt-5.5-xh
reasoning_effort: high
status: queued
priority: normal
no_external_actions: true
no_secrets: true
---

# Workorder: ArtifactDraft minimo filesystem-first

## Contexto

El triage `results/20260526T073800-batch-results-priority-triage-v1.result.md` marco ArtifactDraft minimo como una de las integraciones de menor riesgo y mayor impacto. La meta es evitar que entregas largas por Telegram, reels, presentaciones o informes se mezclen con borradores, estados falsos o envios sin `message_id`.

Ya existe `results/20260526T064631-artifactdraft-implementation-review.result.md`; el orquestador necesita una especificacion implementable y acotada para portar localmente.

## Objetivo

Proponer un helper/contrato local de ArtifactDraft con carpetas y manifest, sin acciones externas. Debe servir para preparar artefactos y hacer QA antes de Telegram, correo, Drive o cualquier envio real.

## Fuentes permitidas

- `results/20260526T064631-artifactdraft-implementation-review.result.md`
- `results/20260526T073800-batch-results-priority-triage-v1.result.md`
- `protocol.md`
- `docs/reels_premium_acceptance_gate.md` solo para alinear gates de reels

No abrir Drive, iCloud, Photos, Gmail, Telegram real, Downloads, ObraCash ni bibliotecas completas.

## Entregable esperado

Crear:

- `results/20260526T094214-artifactdraft-minimal-filesystem-implementation-v1.result.md`
- `results/20260526T094214-artifactdraft-minimal-filesystem-implementation-v1.manifest.json`

Debe incluir:

1. Estructura de carpetas propuesta.
2. `artifact.json` schema minimo.
3. Estados permitidos: `draft`, `qa_ready`, `approved_local`, `queued_external`, `delivered`, `blocked`.
4. Reglas para no declarar entrega sin recibo real (`message_id`, email sent id, drive file id, etc.).
5. Pseudocodigo o script Python/JS pequeno para crear y validar un artifact draft.
6. Fixtures minimos: reel candidato, informe viaje, informe radar bloqueado, documento listo para revision.
7. Que debe implementar primero el orquestador local.

## Reglas

- No acciones externas.
- No secretos.
- No tocar contenido ObraCash.
- No mandar Telegram.
- No proponer almacenamiento de material sensible fuera de carpetas autorizadas.
- Mantenerlo implementable y corto.
