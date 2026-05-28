---
id: 20260528T071407-tesis-template-guardrails-safe-pack-v1
created_at: 2026-05-28T07:14:07-03:00
created_by: orchestrator
assignee: personal-xh
front: TESIS
model: gpt-5.5-xh
reasoning_effort: xhigh
status: queued
no_external_actions: true
no_secrets: true
---

# tesis-template-guardrails-safe-pack-v1

## Objetivo

Pablo, preparar un pack seguro y accionable de guardrails para plantillas de
tesis, sin tocar el borrador base ni abrir bibliotecas completas.

Usar solo contexto operativo ya presente en el bridge/resultados previos y
criterios generales de control academico-metodologico. No acceder a Drive,
iCloud, Photos, Zotero local ni carpetas amplias. No modificar archivos
operativos.

## Alcance permitido

- Revisar resultados previos disponibles en el bridge relacionados con TESIS,
  especialmente paquetes de templates/protocolo si estan presentes.
- Proponer una lista corta de reglas detect-only/review-only para evitar:
  - cambios no justificados del borrador base;
  - referencias incompletas;
  - citas sin PDF/full text verificado;
  - variables/metodos cambiados sin evidencia;
  - mezcla entre decision metodologica y redaccion cosmetica;
  - conclusiones que excedan datos disponibles.
- Si falta evidencia concreta, marcarlo como deuda y no inventar contenido.

## Entregable esperado

1. `summary` breve.
2. `proposed_guardrails` con 5 a 10 reglas, cada una con severidad P0/P1/P2 y
   tipo `detect-only` o `review-only`.
3. `safe_next_action` unica para Codex orquestador.
4. `do_not_touch` recordando que el borrador base no se modifica sin necesidad
   metodologica/bibliografica real.

## Reglas

- No enviar Telegram, mails ni usar servicios externos.
- No acceder a Drive, iCloud, Photos, Zotero local ni bibliotecas completas.
- No imprimir datos personales ni secretos.
- Mantener salida breve, formal y operativa.
