---
id: 20260526T111217-clinica-p0-gates-local-integration-review-v1
created_at: 2026-05-26T11:12:17-03:00
created_by: orchestrator
assignee: personal-xh
front: CLINICA
model: gpt-5.5-xh
reasoning_effort: high
status: queued
priority: high
no_external_actions: true
no_secrets: true
---

# Workorder: Clinica P0 gates - revision de integracion local segura

## Contexto

El Doctor pidio que la app clinica no vuelva a generar inconsistencias medico-legales ni partes/consentimientos con diagnosticos, niveles, abordajes o secuencias operatorias incorrectas. El orquestador ya viene integrando fixtures/gates, pero necesita una segunda mirada de alto razonamiento para priorizar el siguiente paso local de menor riesgo.

## Objetivo

Revisar los resultados previos de Pablo sobre Clinica P0 y convertirlos en una recomendacion ejecutable para el orquestador local: que gate/fixture se debe conectar primero a la app canonica y que prueba debe bloquear salida mala antes de cualquier documento final.

## Fuentes permitidas

- `results/20260525T153318-clinica-lumbar-inconsistency-gates-v2.result.md`
- `results/20260525T173726-clinica-lumbar-fixture-pack-draft-v2.result.md`
- `results/20260525T181000-clinica-lumbar-validator-detect-only-spec-v1.result.md`
- `results/20260525T184100-clinica-lumbar-v2-stress-artifacts-v1.result.md`
- `results/20260525T221902-clinica-lumbar-regression-pack-from-prior-results-v1.result.md`
- `results/20260525T224750-clinica-v2-gates-next-hardening-audit-v1.result.md`
- `results/20260526T001920-clinica-corpus-gates-hardening-v3.result.md`
- `results/20260526T063207-clinica-correcciones-a-fixtures-implementacion.result.md`
- `results/20260526T064839-clinica-corpus-gates-backlog-v2.result.md`
- `protocol.md`

No abrir Drive, iCloud, Photos, Gmail, Telegram real, Downloads, ObraCash ni bibliotecas completas.

## Entregable esperado

Crear:

- `results/20260526T111217-clinica-p0-gates-local-integration-review-v1.result.md`
- `results/20260526T111217-clinica-p0-gates-local-integration-review-v1.manifest.json`

Debe incluir:

1. Top 5 gates P0 por impacto clinico medico-legal.
2. El primer gate que recomienda integrar en app real y por que.
3. Fixtures sinteticos minimos, sin pacientes reales.
4. Criterio de aceptacion/fallo.
5. Riesgos de sobrebloqueo o falsos positivos.
6. Patch plan acotado para el orquestador local, sin modificar plantillas finales a ciegas.

## Reglas

- No acciones externas.
- No secretos.
- No datos reales de pacientes.
- No modificar ObraCash.
- No redactar documentos clinicos libres.
- No promover reglas al corpus fuerte sin que el orquestador revise fuente/caso.
- Mantener enfoque detect-only/review-only: proponer bloqueo y evidencia, no reescritura automatica libre.
