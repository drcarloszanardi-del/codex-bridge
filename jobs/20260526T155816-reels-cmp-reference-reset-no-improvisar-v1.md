---
id: 20260526T155816-reels-cmp-reference-reset-no-improvisar-v1
job_id: 20260526T155816-reels-cmp-reference-reset-no-improvisar-v1
created_at: 2026-05-26T15:58:16-03:00
created_by: codex-orchestrator
assignee: personal-xh
front: REELS
model: gpt-5.5
reasoning_effort: xhigh
status: queued
no_external_actions: true
no_secrets: true
---

# REELS CMP: reset editorial, no improvisar

## Contexto

El Doctor rechazo el ultimo reel por impresentable: frases motivacionales descriptivas, tono generico y baja calidad. El piso minimo aceptado es el reel aprobado del 25 de Mayo 2026: cinematografico, sobrio, con mensaje real, material coherente y cierre institucional CMP.

No hay que producir otro reel generico. Primero necesitamos referencia, guion y pedido de material propio.

## Tarea

Preparar una segunda mirada XH para reiniciar la direccion editorial de reels CMP.

1. Analizar, sin navegar con credenciales ni publicar, que tipos de reels institucionales medicos/neuro/clinica funcionan con tono premium:
   - apertura con caso/desafio real,
   - tension clinica comprensible,
   - imagenes medicas propias o seguras,
   - texto minimo,
   - cierre institucional sobrio.
2. Proponer 3 conceptos concretos para el proximo reel, evitando frases motivacionales vacias.
3. Para cada concepto, indicar exactamente que material pedirle al Doctor:
   - fotos/videos propios necesarios,
   - tipo de plano,
   - que datos tapar,
   - duracion,
   - si requiere voz en off o solo texto.
4. Proponer una rubrica de rechazo automatico:
   - si parece stock generico,
   - si usa frases motivacionales,
   - si la imagen no corresponde a la patologia,
   - si no llega al nivel del reel 25 de Mayo.

## Restricciones

- No renderizar video.
- No usar material de pacientes crudo.
- No abrir Fotos/iCloud/Drive/Downloads salvo carpeta explicitamente autorizada.
- No usar Telegram.
- No inventar esquemas medicos.

## Formato esperado

- `verdict`: direccion recomendada.
- `do_not_do`: lista de 5 prohibiciones.
- `concepts`: 3 propuestas con guion 40-60s y asset request.
- `acceptance_gate`: checklist de calidad.
- `next_action`: que debe pedir el orquestador al Doctor antes de producir.
