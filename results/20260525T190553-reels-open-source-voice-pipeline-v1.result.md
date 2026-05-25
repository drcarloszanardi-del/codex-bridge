---
id: 20260525T190553-reels-open-source-voice-pipeline-v1
job_id: 20260525T190553-reels-open-source-voice-pipeline-v1
created_at: 2026-05-25T19:10:08-03:00
created_by: personal-xh
worker: personal-xh
status: completed
no_external_actions: true
no_secrets: true
---

# Resultado - REELS open source voice pipeline v1

## summary

La mejor ruta para no volver a entregar una voz artificial es separar maqueta, benchmark y voz final. Para CMP, el objetivo no es "clonar por clonar"; es conseguir una locucion sobria, humana, profesional, argentina o rioplatense neutra, con pausas naturales y sin tono de publicidad generica.

Recomendacion: piloto inicial con `Chatterbox` y `CosyVoice` en local o entorno controlado. Usar `OpenVoice V2` como baseline liviano MIT si el setup de los dos primeros se complica. Mantener `F5-TTS` solo como benchmark tecnico por licencia no comercial de pesos preentrenados. No usar voz del Doctor como final hasta pasar gate de consentimiento, privacidad, naturalidad y aprobacion humana.

## coverage_table

| Candidato | Fuente revisada | Estado para piloto |
|---|---|---|
| Chatterbox | `https://github.com/resemble-ai/chatterbox` | Piloto recomendado. MIT, Spanish, voice cloning, menor friccion. |
| CosyVoice | `https://github.com/FunAudioLLM/CosyVoice` | Piloto recomendado si hay GPU/entorno. Apache-2.0, Spanish, zero-shot. |
| F5-TTS | `https://github.com/SWivid/F5-TTS` | Benchmark no final: codigo MIT, pesos CC-BY-NC. |
| GPT-SoVITS | `https://github.com/RVC-Boss/GPT-SoVITS` | Backup tecnico: potente, mas complejo, Spanish no principal en README. |
| Fish Speech | `https://github.com/fishaudio/fish-speech` | Interesante, pero licencia propia/research; revisar antes de uso publico. |
| OpenVoice V2 | `https://github.com/myshell-ai/OpenVoice` | Baseline liviano: MIT, Spanish, control de estilo. |
| Piper/Kokoro | `https://github.com/rhasspy/piper` | Solo backup de maqueta; no alcanza como voz final premium. |

## tabla_comparativa

| Motor | Naturalidad esperada en espanol | Clonacion/referencia | Licencia uso publico/comercial | Hardware/setup | Privacidad | Diagnostico |
|---|---|---|---|---|---|---|
| Chatterbox | Alta para piloto; soporta Spanish y modelo multilingual. | Referencia corta, ejemplos con clip de 10s. | MIT segun repo. | Setup Python relativamente directo; Turbo promete menor VRAM. | Local si se corre on-device. | Mejor primer candidato. |
| CosyVoice | Alta; repo declara Spanish y naturalidad/prosodia fuerte. | Zero-shot/cross-lingual. | Apache-2.0 segun repo. | Mas pesado; Docker/runtime GPU; setup mas tecnico. | Local si se corre on-device. | Mejor candidato si Codex principal tolera complejidad. |
| OpenVoice V2 | Media/alta; Spanish nativo, buen control de estilo/acento. | Tone color cloning y control de estilo. | MIT, comercial permitido segun repo. | Mas liviano que grandes LLM TTS. | Local si se corre on-device. | Buen baseline y fallback. |
| F5-TTS | Alta como benchmark de naturalidad. | Multi-speaker/voice cloning. | Codigo MIT; modelos preentrenados CC-BY-NC. | Setup razonable, Gradio. | Local. | No usar para final comercial sin resolver licencia. |
| GPT-SoVITS | Media/alta con tuning; muy usado para cloning. | 5s zero-shot, 1 min few-shot segun README. | MIT segun repo. | Setup complejo; WebUI; tuning puede consumir tiempo. | Local, pero requiere cuidar samples. | Buen backup si hay tiempo de tuning. |
| Fish Speech | Alta potencial; Spanish tier 2. | TTS/voice cloning; streaming/SDK/API ecosistema. | Repo indica Fish Audio Research License; SDK Apache-2.0 no equivale a pesos. | Puede ser pesado; docs separan API/SDK y open-source. | API implica subir voz/texto; local requiere revisar licencia. | No primer piloto para CMP hasta revisar licencia. |
| Piper/Kokoro | Media o baja para marca premium. | Piper no es cloning premium. | Piper original MIT; desarrollo nuevo movido a GPL. | Muy liviano. | Local. | Solo maqueta/offline, no final. |

## ranking_recomendado

1. `Chatterbox`: primer piloto por balance naturalidad, Spanish, MIT, clonacion con referencia corta y friccion baja.
2. `CosyVoice`: segundo piloto si la Mac de trabajo puede correrlo; mejor apuesta tecnica para naturalidad/prosodia, pero setup mas pesado.
3. `OpenVoice V2`: baseline MIT para comparar control de acento/ritmo y tener fallback simple.
4. `GPT-SoVITS`: backup si se acepta tuning y mas trabajo de curacion de voz.
5. `F5-TTS`: benchmark de escucha, no final por pesos no comerciales.
6. `Fish Speech`: revisar licencia antes de cualquier uso publico; puede servir como benchmark si se corre sin subir assets personales.
7. `Piper/Kokoro`: descartar como voz final CMP salvo emergencia de maqueta.

## plan_de_piloto_con_pasos_concretos

1. Preparar un guion de 20-30 segundos aprobado para prueba, no el reel completo.
2. Usar 2 variantes de texto: una sobria clinica y una mas conversacional.
3. Generar con Chatterbox:
   - voz sintetica neutral si existe preset usable;
   - voz de referencia solo con audio autorizado y local;
   - 2 velocidades/pausas.
4. Generar con CosyVoice:
   - zero-shot con referencia autorizada;
   - si falla setup, documentar bloqueo y pasar a OpenVoice V2.
5. Generar baseline con OpenVoice V2.
6. No renderizar video completo; solo clips WAV/MP3 de voz.
7. Evaluar con gate QA de audio.
8. Elegir 1 candidato y recien ahi renderizar una micro-maqueta de 8-10 segundos.
9. Si ningun open-source supera gate, usar voz humana grabada o motor pago solo como benchmark auditivo, no como decision automatica.

## criterios_de_rechazo_de_voz

Rechazar una voz si cumple cualquiera:

| Criterio | Umbral |
|---|---|
| Artificialidad evidente | Suena a asistente telefonico, robot, doblaje generico o publicidad barata. |
| Acento incorrecto | Espanol neutro forzado, castellano no rioplatense con entonacion extraña, o mezcla de idiomas. |
| Prosodia mala | Pausas raras, enfasis en palabras clinicas incorrectas, ritmo plano o acelerado. |
| Deterioro tecnico | Ruido, clipping, respiraciones falsas, sibilancia exagerada, artefactos vocoder. |
| Mala pronunciacion medica | Pronuncia mal CMP, columna, lumbar, cervical, Pellegrini, nombres anatomicos. |
| Voz del Doctor no convincente | Se parece pero resulta uncanny, o compromete privacidad/identidad. |
| Tono de marca incorrecto | Demasiado vendedor, dramatico, influencer o paternalista. |

## gate_QA_audio_antes_de_renderizar

Checklist obligatorio antes de render completo:

```yaml
audio_voice_gate_v1:
  required:
    - naturalidad_humana >= 8/10
    - sobriedad_profesional >= 8/10
    - pronunciacion_medica >= 9/10
    - acento_rioplatense_o_neutro_apto >= 7/10
    - ausencia_artefactos >= 8/10
    - privacidad_ok == true
    - licencia_ok_para_publicacion == true
  reject_if:
    - suena_a_ia_obvia
    - tono_publicidad_generica
    - referencia_del_doctor_no_autorizada
    - licencia_no_comercial_para_uso_publico
    - requiere_subir_audio_personal_a_api_sin_aprobacion
```

## voz_doctor_vs_locutor_vs_pago

| Opcion | Recomendacion |
|---|---|
| Voz del Doctor clonada | No como default. Solo si el Doctor autoriza explicitamente muestra, uso y publicacion, y si el resultado no es uncanny. |
| Voz sintetica de locutor | Mejor default para reels CMP: permite consistencia y menor riesgo de identidad. |
| Voz humana grabada | Mejor calidad final si hay tiempo; ideal para piezas clave. |
| Motor pago | Usarlo solo como benchmark de naturalidad o fallback aprobado; no comprar/contactar desde este worker. |

## riesgos_licencias

- `F5-TTS`: codigo MIT, pero pesos preentrenados CC-BY-NC; no usar en pieza publica/comercial sin resolver licencia.
- `Fish Speech`: repo indica licencia propia de investigacion; SDK/API Apache-2.0 no habilita automaticamente uso de pesos/modelos para publicacion.
- `Chatterbox`, `OpenVoice`, `CosyVoice`: licencias mas favorables segun repos revisados, pero Codex principal debe verificar licencia exacta de pesos usados antes de publicar.
- Voz del Doctor: requiere autorizacion explicita, minimizacion de muestras, almacenamiento local y no subir referencias a servicios externos sin permiso.
- APIs pagas o cloud: suben texto/audio; usar solo con aprobacion especifica.

## risks_limits

- No se generaron audios, no se tocaron assets personales y no se usaron credenciales.
- La evaluacion es documental; la decision de calidad final requiere escuchar clips propios.
- Todo uso de voz del Doctor requiere autorizacion humana explicita y flujo local o aprobado.
- Las licencias deben verificarse sobre el repo, los pesos exactos y el modo de distribucion antes de publicar.
- Los rankings pueden cambiar con nuevas versiones; este resultado prioriza candidatos revisados hoy y compatibles con el objetivo CMP.

## recommendation

Piloto inicial: `Chatterbox` primero, `CosyVoice` segundo, `OpenVoice V2` como baseline. No usar `say`, Piper ni Edge Neural para final. No renderizar reel completo hasta que un clip corto pase `audio_voice_gate_v1`.

## confidence

Media-alta. Las licencias/capacidades se basan en repos y documentacion publica revisada hoy, pero la calidad final debe decidirse escuchando clips propios de prueba y verificando la licencia exacta de pesos/modelos instalados en la Mac de trabajo.

## evidence_paths

- `jobs/20260525T190553-reels-open-source-voice-pipeline-v1.md`
- `https://github.com/resemble-ai/chatterbox`
- `https://github.com/FunAudioLLM/CosyVoice`
- `https://github.com/SWivid/F5-TTS`
- `https://github.com/RVC-Boss/GPT-SoVITS`
- `https://github.com/myshell-ai/OpenVoice`
- `https://github.com/fishaudio/fish-speech`
- `https://docs.fish.audio/api-reference/sdk/python/overview`
- `https://github.com/rhasspy/piper`
