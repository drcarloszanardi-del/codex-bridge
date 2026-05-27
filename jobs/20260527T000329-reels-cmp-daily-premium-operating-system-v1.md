---
id: 20260527T000329-reels-cmp-daily-premium-operating-system-v1
created_at: 2026-05-27T00:03:29-03:00
created_by: orchestrator
assignee: personal-xh
front: REELS
model: gpt-5.5-xh
reasoning_effort: xhigh
status: queued
no_external_actions: true
no_secrets: true
---

# Reels CMP daily premium operating system v1

## 10 inicial - direccion del orquestador

El Doctor pidio que Codex sea proactivo en generar un reel diario de maxima calidad, sin improvisar,
sin slideshow y usando material propio siempre que sea posible. El ultimo reel lumbar quedo en hold
porque no alcanza el gate premium sin assets adicionales. No renderizar, no enviar Telegram y no abrir
Fotos/iCloud/Drive/Gmail/Downloads ni bibliotecas privadas.

Contexto minimo:

- `context/fronts/reels_cmp.md`
- `docs/reels_premium_acceptance_gate.md`
- `context/fronts/reels_cmp_cinematic_references_2026-05-26.md`
- `results/20260526T230823-reels-cmp-low-text-transition-quality-reset-v1.result.md`
- `results/20260526T233419-reels-lumbar-cinematic-v3-shotlist-and-gate-review.result.md`
- `results/20260526T191159-reels-professional-open-source-tooling-and-style-research-v1.result.md`
- `results/20260526T184909-reels-cmp-quality-ceo-review-felipe-y-estandar-v1.result.md`

Objetivo: armar un sistema operativo editorial para reels CMP diarios que le permita al orquestador pedir
material correcto al Doctor, evitar piezas pobres y decidir rapido si renderizar o poner en hold.

## 80 delegado - trabajo de Pablo

Entregar:

- `daily_reel_pipeline`: flujo de trabajo diario de idea -> material -> guion -> edicion -> QA -> envio.
- `asset_request_templates`: 4 plantillas cortas para pedir material por topic REELS segun tipo de caso:
  educativo, caso clinico, historia humana, institucional.
- `premium_gate_decision_tree`: decision tree para renderizar, pedir mas material o bloquear.
- `shot_grammar_library`: biblioteca de 12 tipos de plano propios y como conectarlos sin slideshow.
- `text_and_copy_rules`: reglas concretas para texto en pantalla vs copy de Instagram.
- `pablo_role`: que tareas hace Pablo y que decide el orquestador.
- `failure_modes`: errores que no deben repetirse y hard stops.
- `recommendation`: proxima accion unica para manana.

Reglas:

- No usar stock ni material externo como sustituto de evidencia clinica.
- No pedir acceso amplio a bibliotecas privadas.
- No proponer frases epicas ni motivacionales.
- No cerrar con "no pude" sin rutas alternativas, limite exacto y proxima accion.

## 10 final - retorno al orquestador

El resultado debe ser accionable y breve. Validar contra `scripts/validate_result_contract.py` antes de marcarlo completado.
