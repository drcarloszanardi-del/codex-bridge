---
id: 20260526T101406-artifactdraft-router-pilot-safe-plan-v1
created_at: 2026-05-26T10:14:06-03:00
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

# Workorder: ArtifactDraft router pilot seguro

## Contexto

El orquestador integro localmente el ArtifactDraft minimo en:

- `scripts/artifacts/new_artifact.py`
- `scripts/artifacts/validate_artifact.py`
- `tests/artifacts/test_artifactdraft_gate.py`

El helper crea carpetas `drafts/`, `assets/`, `qa/`, `final/`, `delivery/`, agrega `artifact.json`, `assets/manifest.json`, `delivery/receipt.json` y valida que no se declare `delivered` sin recibo real ni se pase material con datos de paciente a cola externa.

## Objetivo

Proponer el siguiente paso de bajo riesgo para conectar ArtifactDraft al router operativo sin enviar nada afuera:

1. Donde interceptar respuestas largas, adjuntos, reels, presentaciones e informes para crear ArtifactDraft antes de cualquier envio.
2. Que campos minimos debe pasar el router al helper.
3. Que estados debe usar el router: `draft`, `qa_ready`, `approved_local`, `queued_external`, `delivered`, `blocked`.
4. Que fixtures/regresiones se necesitan para evitar entregas falsas, contaminacion de topics y envio sin `message_id`.
5. Un patch plan acotado para el orquestador local, priorizando seguridad y compatibilidad.

## Fuentes permitidas

- `results/20260526T094214-artifactdraft-minimal-filesystem-implementation-v1.result.md`
- `results/20260526T073800-batch-results-priority-triage-v1.result.md`
- `docs/telegram_topic_routing_regression_suite_v1.md` si existe localmente en el bridge/contexto permitido
- `protocol.md`

No abrir Drive, iCloud, Photos, Gmail, Telegram real, Downloads, ObraCash ni bibliotecas completas.

## Entregable esperado

Crear:

- `results/20260526T101406-artifactdraft-router-pilot-safe-plan-v1.result.md`
- `results/20260526T101406-artifactdraft-router-pilot-safe-plan-v1.manifest.json`

Debe incluir:

1. Mapa de puntos de integracion con archivos/rutas probables.
2. Riesgos P0/P1 antes de tocar router real.
3. Fixtures minimos obligatorios.
4. Criterio de aceptacion para el orquestador.
5. Recomendacion final: aplicar ahora, aplicar parcial o esperar.

## Reglas

- No acciones externas.
- No secretos.
- No tocar contenido ObraCash.
- No mandar Telegram.
- No pedir acceso amplio a Drive/iCloud/Photos/Gmail.
- Si falta una ruta exacta, proponer como localizarla sin asumir.
