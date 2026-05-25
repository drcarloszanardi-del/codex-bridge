---
id: 20260525T192345-reels-generate-premium-voice-sample-chatterbox-v1
created_at: 2026-05-25T19:23:45-03:00
created_by: orchestrator
assignee: personal-xh
front: REELS
model: gpt-5.5-xh
reasoning_effort: xhigh
status: queued
no_external_actions: true
no_secrets: true
---

# REELS - Generate Premium Voice Sample Chatterbox V1

## Contexto

El Doctor pidio probar una voz nueva pegada al video. En la Mac de trabajo:

- XTTS CPU no produjo WAV tras varios minutos.
- Chatterbox no instala por dependencia `torch==2.6.0` sin wheel compatible para `macosx_x86_64`.
- El texto/copy fue aprobado, pero la voz Edge/macOS fue rechazada por artificial.

Necesitamos que Pablo, si su Mac/entorno lo permite, genere una muestra de voz natural para que Codex orquestador la pegue al video base.

## Texto para locucion

Usar esta version para TTS. En pantalla se escribe `Pellegrini`, pero en audio debe pronunciarse `Pelegrini`.

```text
En Argentina aprendimos algo desde temprano:
cuando falta lo ideal, aparece el ingenio.

No siempre estan dadas las condiciones.
Pero hay una forma muy nuestra de seguir:
observar, adaptarnos y resolver.

En medicina tambien pasa.
Cada dia exige precision, equipo y compromiso.

Este 25 de Mayo recordamos de donde venimos,
y seguimos trabajando por lo que queremos construir.

Centro Medico Pelegrini.
Estamos para ayudarlo.
```

## Objetivo

Generar un archivo de audio de prueba, no publicarlo. Prioridad:

1. Chatterbox Multilingual, Spanish `es`, voz default o referencia publica segura si hace falta.
2. OpenVoice V2 si Chatterbox falla.
3. Solo si no se puede generar audio, devolver bloqueo con evidencia exacta y siguiente ruta.

## Entregable esperado

- WAV o MP3 corto/full apto para que Codex principal lo pegue al video.
- Guardarlo dentro del repo bridge solo si pesa poco razonable. Ruta sugerida:
  `context/asset_packs/20260525-reels-voice-test/voice_pablo_chatterbox_v1.wav`
- Resultado markdown con:
  - motor usado
  - version/comando
  - licencia asumida
  - duracion
  - si pronuncia `Pelegrini` correctamente
  - riesgos o defectos auditivos

## Reglas

- No usar voz del Doctor ni archivos personales.
- No abrir Photos/iCloud/Drive.
- No subir audio a APIs externas.
- No enviar Telegram.
- No tocar secretos ni credenciales.
- No publicar ni contactar terceros.
- Si el audio suena artificial, marcarlo como `reject_candidate`, no como final.
