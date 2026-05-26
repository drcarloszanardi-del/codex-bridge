---
id: 20260526T104237-artifactdraft-topic-router-implementation-review-v1
created_at: 2026-05-26T10:42:37-03:00
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

# Workorder: revisar implementacion local ArtifactDraft topic router

## Contexto

El orquestador aplico una integracion parcial y segura del plan `20260526T101406`:

- `scripts/artifacts/new_artifact.py`
- `scripts/artifacts/validate_artifact.py`
- `scripts/send_codex_topic_message.py`
- `tests/artifacts/test_artifactdraft_gate.py`
- `tests/telegram/test_artifactdraft_topic_router_pilot.py`

El piloto esta detras de feature flag `ARTIFACTDRAFT_ROUTER_PILOT=1`. Por defecto queda apagado. En modo dry-run crea ArtifactDraft local para mensajes largos o rutas como REELS/VIAJES/RADAR/INM/INV/PRESENTACIONES, valida el manifest y no envia nada. Si se envia con flag activo, registra `delivered` solo cuando hay `message_id` real.

Pruebas locales pasadas:

- `python3 -m py_compile ...`
- `python3 tests/artifacts/test_artifactdraft_gate.py`
- `python3 tests/telegram/test_artifactdraft_topic_router_pilot.py`
- `python3 tests/telegram/test_delivery_receipt_gate.py`
- `python3 tests/telegram/test_postfix_regression_fixtures.py`
- dry-run corto sin flag: artifact `null`

## Objetivo

Hacer una segunda mirada de seguridad/regresion sobre la integracion local y proponer ajustes puntuales si hay riesgo real.

## Fuentes permitidas

- `results/20260526T101406-artifactdraft-router-pilot-safe-plan-v1.result.md`
- Las rutas de scripts/tests listadas arriba si estan disponibles en el bridge o por contexto del resultado.
- `protocol.md`

No abrir Drive, iCloud, Photos, Gmail, Telegram real, Downloads, ObraCash ni bibliotecas completas.

## Entregable esperado

Crear:

- `results/20260526T104237-artifactdraft-topic-router-implementation-review-v1.result.md`
- `results/20260526T104237-artifactdraft-topic-router-implementation-review-v1.manifest.json`

Debe incluir:

1. Veredicto: aceptar, ajustar antes de activar o revertir.
2. Riesgos P0/P1 detectados.
3. Fixtures faltantes si los hay.
4. Recomendacion exacta para el orquestador: mantener flag apagado, activar dry-run limitado, o no activar.
5. Si propone patch, que sea minimo y sin acciones externas.

## Reglas

- No acciones externas.
- No secretos.
- No tocar contenido ObraCash.
- No mandar Telegram.
- No pedir acceso amplio a Drive/iCloud/Photos/Gmail.
- No asumir que el piloto esta activo por defecto: validar la seguridad del feature flag.
