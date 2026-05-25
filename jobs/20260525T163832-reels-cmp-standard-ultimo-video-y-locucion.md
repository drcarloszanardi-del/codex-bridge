---
id: 20260525T163832-reels-cmp-standard-ultimo-video-y-locucion
created_at: 2026-05-25T16:38:32-03:00
created_by: orchestrator
assignee: personal-xh
front: REELS
model: gpt-5.5-xh
reasoning_effort: xhigh
status: queued
no_external_actions: true
no_secrets: true
---

# Workorder: REELS CMP - convertir el ultimo video aprobado en estandar operativo

## Contexto

El Doctor aprobo con entusiasmo el ultimo reel CMP sobre creatividad argentina / Dia de la Patria y marco que ese producto debe quedar como piso de calidad. Luego pidio una version con voz en off de locutor y aclaro que puede agregar musica desde Instagram al publicar.

Artefactos locales de referencia en la Mac de trabajo:

- Video aprobado: `/Users/jarvis/.openclaw/workspace/reels-studio/projects/cmp_reel_25_mayo_creatividad_real_2026-05-25/output/cmp_reel_25_mayo_creatividad_real_cmp_v2.mp4`
- Version con locutor neural argentino sin musica incrustada: `/Users/jarvis/.openclaw/workspace/reels-studio/projects/cmp_reel_25_mayo_creatividad_real_2026-05-25/output/cmp_reel_25_mayo_creatividad_real_cmp_v2_locutor_clean.mp4`
- QA/contact sheet: `/Users/jarvis/.openclaw/workspace/reels-studio/projects/cmp_reel_25_mayo_creatividad_real_2026-05-25/qa/contact_sheet_v2.jpg`
- Manifest local: `/Users/jarvis/.openclaw/workspace/reels-studio/projects/cmp_reel_25_mayo_creatividad_real_2026-05-25/artifact_v2.json`
- Gate de calidad: `docs/reels_premium_acceptance_gate.md`

## Objetivo

Producir una especificacion ejecutable para que Codex principal use este reel como patron de calidad CMP en los proximos trabajos. El foco no es generar otro video ahora, sino convertir lo aprendido en una guia verificable y accionable.

## Tareas

1. Leer el gate de calidad de reels y los artefactos locales disponibles en el bridge relacionados con reels CMP, especialmente resultados del 2026-05-25.
2. Analizar por que el ultimo reel aprobado funciono mejor que las versiones rechazadas por el Doctor.
3. Definir un `CMP Reel Standard v1` con criterios concretos:
   - tipo de material visual aceptable,
   - ritmo y duracion,
   - uso de texto en pantalla,
   - cierre institucional,
   - contacto visible correcto,
   - voz en off vs musica,
   - cuando conviene no incrustar musica para agregarla desde Instagram,
   - criterios de rechazo automatico.
4. Proponer un flujo de QA previo a envio por Telegram:
   - chequeos tecnicos,
   - chequeos visuales,
   - chequeos de contacto,
   - chequeos de coherencia mensaje-imagen,
   - chequeo de ruta topic `REELS` y recibo real.
5. Preparar 3 ideas de proximos reels diarios CMP que respeten ese estandar, sin requerir acceder a Photos/iCloud/Drive ni bibliotecas completas:
   - tema,
   - mensaje central,
   - estructura de 35-45 segundos,
   - material visual necesario,
   - posible voz en off,
   - riesgo principal de calidad.

## Reglas duras

- No enviar Telegram, email ni acciones externas.
- No abrir Drive/iCloud/Photos ni bibliotecas personales.
- No tocar ObraCash.
- No imprimir secretos ni tokens.
- No aceptar material generico, esquemas pobres, imagenes incongruentes o texto publicitario invasivo.
- Separar claramente observacion, inferencia y recomendacion.
- Si falta un archivo local, no cerrar con "no pude": usar los resultados del bridge disponibles, registrar el faltante y proponer alternativa concreta.

## Entregable esperado

Crear `results/20260525T163832-reels-cmp-standard-ultimo-video-y-locucion.result.md` con:

- `summary`
- `what_worked`
- `what_failed_before`
- `CMP_Reel_Standard_v1`
- `voiceover_policy`
- `instagram_music_policy`
- `qa_checklist_before_telegram`
- `next_3_reel_concepts`
- `risks_limits`
- `recommendation`
- `confidence`
- `evidence_paths`

Validar con `scripts/validate_result_contract.py` si aplica antes de marcar completo.
