---
job_id: 20260526T191159-reels-professional-open-source-tooling-and-style-research-v1
worker: personal-xh
status: completed
completed_at: 2026-05-26T19:23:35-03:00
front: REELS
no_external_actions: true
no_secrets: true
---

# Resultado - reels professional open source tooling and style research v1

## summary

Recomendacion ejecutiva: implementar **CMP Daily Reel OS v1**, un sistema de
produccion diaria basado en material real del Doctor, templates repetibles,
edicion local/open-source y gate CEO antes de publicar. El objetivo no debe ser
"subir algo todos los dias"; debe ser subir piezas breves con tesis clara,
presencia humana, evidencia visual segura, subtitulos legibles, cierre CMP y QA
auditable.

La combinacion recomendada es:

1. `Kdenlive` como NLE diario principal.
2. `FFmpeg` como motor de proxies, normalizacion, exports, contact sheets y QA.
3. `whisper.cpp` para transcripcion local inicial.
4. `Aegisub` o editor de subtitulos equivalente para pulido final de captions.
5. `Blender`/`Natron` solo para motion graphics, placas premium y compositing
   cuando el reel lo justifique.
6. `Audacity` para limpieza y nivelado de audio.
7. `OpenTimelineIO` como puente de metadatos/timelines si el flujo crece.

El benchmark interno sigue siendo el reel 25 de Mayo aprobado: funciono porque
no parecia una suma de fotos con zoom; tenia tesis, progresion, material real,
audio, cierre institucional y contact sheet. Ese criterio debe convertirse en
rutina, no en excepcion.

## coverage_table

| Fuente / ruta | Estado | Uso en decision |
| --- | --- | --- |
| `/Users/jarvis/.openclaw/workspace/reels-studio/taste_library_cmp_v1.json` | No existe en esta Mac | No se infiere gusto desde archivo ausente. |
| `/Users/jarvis/.openclaw/workspace/codex-bridge/docs/reels_premium_acceptance_gate.md` | No existe en esta Mac | Se uso el equivalente local `docs/reels_premium_acceptance_gate.md`. |
| `/Users/jarvis/.openclaw/workspace/reels-studio/exports/reels/cmp_reel_25_mayo_creatividad_real_cmp_v4_locutor_jorge_graves_naturales_2026-05-26.mp4` | No existe en esta Mac | Se uso el resultado aprobado local del 25 de Mayo como benchmark documental. |
| `docs/reels_premium_acceptance_gate.md` | Revisada | Gate CEO: no aprobar sin evidencia visual, contacto correcto, QA y cierre. |
| `context/fronts/reels_cmp.md` | Revisada | Datos canonicos CMP, privacidad, estetica sobria y contacto. |
| `docs/pablo_asset_inbox_protocol.md` | Revisada | Forma segura de pedir y recibir material por carpetas/topic REELS. |
| `results/20260525T133959-reel-dia-patria-v2-return-premium-gate.result.md` | Revisada | Benchmark narrativo y tecnico del reel 25 de Mayo. |
| `results/20260525T190553-reels-open-source-voice-pipeline-v1.result.md` | Revisada | Criterios de voz/audio local y herramientas TTS. |
| `results/20260526T184909-reels-cmp-quality-ceo-review-felipe-y-estandar-v1.result.md` | Revisada | Regla de no aprobar piezas sin evidencia visual segura. |
| `https://kdenlive.org/` y `https://docs.kdenlive.org/` | Revisada | NLE principal, proxies, efectos, titulos, subtitulos y export. |
| `https://ffmpeg.org/ffmpeg.html` y `https://ffmpeg.org/ffmpeg-filters.html` | Revisada | Automatizacion de export, filtros, loudness, drawtext/contact sheets. |
| `https://github.com/ggerganov/whisper.cpp` | Revisada | Transcripcion local y captions sin subir audio a servicios externos. |
| `https://docs.blender.org/manual/en/latest/video_editing/` | Revisada | VSE/motion graphics cuando Kdenlive no alcance. |
| `https://natrongithub.github.io/` | Revisada | Compositing/motion puntual, no como editor diario. |
| `https://shotcut.org/` | Revisada | Fallback simple multiplataforma. |
| `https://www.audacityteam.org/` | Revisada | Limpieza, compresion y revision de voz/audio. |
| `https://github.com/Aegisub/Aegisub` | Revisada | Subtitulado fino cuando el reel tenga mucho texto. |
| `https://github.com/AcademySoftwareFoundation/OpenTimelineIO` | Revisada | Intercambio de timelines y metadata si hay varios editores. |
| `https://github.com/WyattBlue/auto-editor` | Revisada | Utilidad opcional para detectar silencios/cortes preliminares. |
| `https://github.com/yt-dlp/yt-dlp` | Revisada | Solo referencia/analisis legal de material publico; no reutilizar contenido. |
| Canales publicos: Doctor Mike, Doctorly, Mayo Clinic, Cleveland Clinic, HealthyGamerGG, Dr Tracey Marks, MedCram, Dr Pimple Popper | Revisados via paginas publicas/busqueda | Patrones de hook, ritmo, captions, rostro, autoridad y cierre. |

## findings

### Ranking de herramientas open source/locales

1. **Kdenlive** - Editor principal para reels verticales. Uso CMP: proyecto
   1080x1920, proxies, corte narrativo, titulos, subtitulos simples, color
   basico, capas de B-roll, export final y version preview. Es el centro del
   flujo porque permite operar todos los dias sin depender de servicios cloud.

2. **FFmpeg** - Motor de automatizacion. Uso CMP: generar proxies, normalizar
   audio, convertir formatos, crear contact sheets, extraer frames, aplicar
   `drawtext` para checks, medir duracion/resolucion y producir previews
   livianos para gate. Debe ser parte del QA, no solo del render.

3. **whisper.cpp** - Transcripcion local. Uso CMP: sacar captions del audio del
   Doctor o locucion sin subir material sensible. Produce borrador de subtitulos
   que despues se corrige manualmente.

4. **Aegisub / Subtitle Edit equivalente** - Pulido de captions. Uso CMP:
   corregir timing, line breaks, palabras medicas y legibilidad mobile. Para
   crecimiento, los subtitulos son pieza editorial, no decoracion.

5. **Audacity** - Audio/voz. Uso CMP: limpiar ruido, comprimir, limitar picos,
   revisar respiraciones y generar masters sobrios. Para reels diarios, el
   audio pobre degrada mas que una transicion simple.

6. **Blender** - Motion graphics y armado avanzado cuando el concepto lo exige.
   Uso CMP: placas cinematicas, animaciones limpias, zooms controlados sobre
   material sanitizado, fondos institucionales, no como NLE diario salvo casos
   especiales.

7. **Natron** - Compositing puntual. Uso CMP: borrar datos sensibles de un
   estudio, tracking simple, mascaras y placas mas premium. No conviene para
   todos los dias; si se usa mucho, el flujo se vuelve pesado.

8. **Shotcut** - Fallback y edicion rapida. Uso CMP: estacion secundaria o
   backup cuando Kdenlive falle. Menos ideal para templates complejos, pero
   viable en Mac/Windows/Linux.

9. **OpenTimelineIO** - Gestion de intercambio. Uso CMP: guardar estructura de
   timeline, permitir que otro editor o worker entienda assets/cortes, y reducir
   dependencia de un proyecto cerrado.

10. **auto-editor / yt-dlp** - Utilidades, no base creativa. Uso CMP:
    `auto-editor` para pre-cortes por silencio cuando hay entrevistas largas;
    `yt-dlp` solo para metadata/referencia de videos publicos cuando sea legal y
    necesario. Nunca copiar material de terceros al reel final.

### Patrones de estilo observados y aplicables

1. **Rostro o situacion humana en los primeros 1-3 segundos.** Las cuentas que
   crecen no empiezan con logo ni portada estatica; empiezan con persona,
   tension o imagen clinica segura.

2. **Un solo conflicto por pieza.** Ejemplos aplicables: "no se opera una
   imagen", "este dolor no siempre viene de la columna", "cuando la ubicacion
   cambia la estrategia".

3. **Hook verbal concreto, no titulo generico.** Mejor "Tres datos que cambian
   una consulta de columna" que "Consejos de columna".

4. **Cortes cada 2-5 segundos si hay cara a camara.** El cambio puede ser B-roll,
   zoom leve, plano de manos, pasillo CMP, placa breve o estudio sanitizado.

5. **Subtitulos grandes y editados.** No transcribir todo en bloque: 1-2 lineas,
   palabras clave resaltadas, alto contraste y margen seguro.

6. **Material propio como prueba de vida.** Consultorio, pasillos, pizarron,
   manos dibujando, quirofano seguro, walking y voz del Doctor hacen que el reel
   parezca real y premium.

7. **Lenguaje prudente medico-legal.** Evitar promesas, diagnosticos por redes o
   "cura". Usar "puede", "hay que evaluar", "en consulta revisamos".

8. **Cierre institucional breve.** El contacto va al final, pero la pieza no
   debe sentirse como publicidad. Cierre recomendado: idea humana + CMP +
   `@drcarloszanardi`, `2364384321`, `www.centromedicopellegrini.com.ar`.

9. **Historias complementarias, no duplicadas.** Reel ensena; stories preguntan,
   muestran backstage, encuesta, antes/despues del tema o caja de preguntas.

10. **Cadencia serial.** Las cuentas grandes repiten formatos reconocibles:
    mito/verdad, caso anonimo, reaccion a pregunta, detras de escena,
    explicacion con objeto, error frecuente.

### Referencias publicas revisadas

Referencias medicas/profesionales por arriba de 100K segun paginas publicas y
senales visibles en busqueda al momento de revisar:

- `https://www.youtube.com/@DoctorMike` - Hook de pregunta, humor controlado,
  autoridad facial y ritmo rapido.
- `https://www.youtube.com/@Doctorly` - Dermatologia educativa, captions,
  formato pregunta/respuesta y explicacion compacta.
- `https://www.youtube.com/@MayoClinic` - Autoridad institucional, tono seguro,
  claridad y presencia de marca sin volverse flyer.
- `https://www.youtube.com/@ClevelandClinic` - Educacion simple, lenguaje para
  pacientes, autoridad de institucion.
- `https://www.youtube.com/@HealthyGamerGG` - Hook humano, narrativa de dolor
  real, autoridad profesional y tono conversacional.
- `https://www.youtube.com/@DrTraceyMarks` - Explicacion medica estructurada,
  temas sensibles tratados con sobriedad.
- `https://www.youtube.com/@Medcram` - Pizarron/visual didactico, foco en una
  idea y jerarquia explicativa.
- `https://www.youtube.com/@DrPimplePopper` - Caso/curiosidad visual fuerte,
  pero para CMP solo sirve como advertencia: no copiar espectacularizacion.

## recommendation

### Workflow diario CMP Daily Reel OS v1

1. **Tema del dia.** Elegir un tema de backlog semanal. Debe tener una pregunta
   de paciente y una tesis de 1 frase.

2. **Pedido de material por topic REELS.** Mandar checklist especifico al Doctor:
   3-5 videos verticales reales, 1 nota de contexto, restricciones de privacidad
   y autorizacion publica si aparece otra persona.

3. **Ingesta segura.** Guardar assets en carpeta local, crear manifest, marcar
   que es publico/sanitizado/no publico. Nada de bibliotecas completas.

4. **Storyboard 40-60 segundos.** Definir hook, 3 beats, cierre CMP y stories
   complementarias antes de editar.

5. **Edicion local.** Kdenlive + proxies. FFmpeg para proxies/contact sheet.
   Blender/Natron solo si hacen falta placas o saneamiento visual.

6. **Subtitulos.** whisper.cpp genera borrador; humano corrige medicina, ritmo y
   legibilidad. No publicar captions crudos.

7. **Audio.** Audacity para niveles. Voice AI solo si hay necesidad y gate de
   naturalidad; preferir voz real del Doctor cuando sea posible.

8. **Privacidad.** Revisar frame-by-frame: sin nombres, historias clinicas,
   pantallas, datos en estudios, caras no autorizadas ni reflejos reveladores.

9. **Gate premium.** Export preview + contact sheet 8-12 frames + manifest +
   copy. Si falta evidencia visual segura, `pass_premium_gate=false`.

10. **Publicacion sugerida.** Orquestador decide. Este worker no publica ni
    envia mensajes externos.

### Estructura de carpetas propuesta

```text
reels-studio/
  inbox/REELS/YYYYMMDD-slug/
    originals_local_not_git/
    notes/
    manifest_inbox.json
  projects/YYYYMMDD-slug/
    00_brief/
    01_assets_safe_derivatives/
    02_storyboard/
    03_script/
    04_edit/
      kdenlive/
      blender_or_natron_optional/
    05_audio/
    06_subtitles/
    07_exports/
      preview/
      final_candidate/
    08_qa/
      contact_sheet/
      frame_checks/
      gate_report.md
```

### Pack minimo a pedir por topic REELS

- 1 frase del Doctor: que quiere que el paciente recuerde.
- 3-5 videos verticales de 8-20 segundos: cara a camara, walking, consultorio,
  mano dibujando, pasillo/fachada CMP, preparacion segura, detalle de trabajo.
- 1 audio o nota de voz opcional con tono/ideas reales.
- 1 foto vertical del Doctor si no hay video de rostro ese dia.
- Estudios o imagenes medicas solo si estan sanitizados; si no, pedir permiso
  para crear derivado seguro local.
- Restricciones: que no mostrar, palabras a evitar, si aplica caso anonimo.
- Consentimiento publico cuando aparezca paciente/familiar/voz/testimonio.
- CTA elegido: consulta, educacion, caja de preguntas, guardar/compartir.

### Cinco formatos diarios repetibles (40-60 segundos)

1. **Mito / verdad columna-neuro.**
   - 0-3s: "No toda hernia se opera."
   - 3-15s: mito frecuente.
   - 15-40s: criterio medico simple.
   - 40-55s: que llevar a consulta.
   - Cierre: CMP + contacto.

2. **Caso anonimo de decision.**
   - 0-3s: "La imagen parecia una cosa, el examen cambio todo."
   - 3-15s: problema sin datos personales.
   - 15-40s: como se piensa la decision.
   - 40-55s: aprendizaje para pacientes.
   - Cierre: prudente, sin prometer resultado.

3. **Detras de escena sobrio.**
   - 0-3s: plano real de pasillo/consultorio/OR seguro.
   - 3-20s: que se prepara antes de atender u operar.
   - 20-45s: por que ese paso cuida al paciente.
   - 45-60s: CMP/contacto.

4. **Tres preguntas antes de consultar.**
   - 0-3s: "Si te duele la pierna, contame estas 3 cosas."
   - 3-45s: tres preguntas con B-roll.
   - 45-60s: invitacion a preparar consulta, no diagnostico online.

5. **Historia de confianza / humanidad.**
   - 0-3s: gesto humano o frase del Doctor.
   - 3-25s: escena real, sin datos sensibles.
   - 25-45s: valor CMP: escuchar, explicar, decidir bien.
   - 45-60s: cierre institucional calido.

### Cambios recomendados al gate premium

Agregar `daily_reel_gate_v1`:

- `has_real_own_video_block`: minimo 2 bloques de video propio/autoridad CMP,
  no solo fotos con zoom.
- `first_3_seconds_thesis`: el primer cuadro/voz debe declarar conflicto o
  beneficio concreto.
- `mobile_subtitles_pass`: captions legibles en 1080x1920 y 540x960.
- `privacy_frame_pass`: revision frame-by-frame contra HC, nombres, pantallas,
  estudios identificables, caras sin permiso y reflejos.
- `contact_pass`: `@drcarloszanardi`, `2364384321`,
  `www.centromedicopellegrini.com.ar` legibles.
- `source_manifest_pass`: cada asset tiene origen, permiso y estado
  publico/sanitizado.
- `contact_sheet_pass`: 8-12 frames con timestamps y decision.
- `ai_truth_pass`: IA no inventa evidencia medica ni reemplaza material real.
- `stories_companion_pass`: propuesta de 2-3 stories complementarias.
- `publication_hold`: si falta una evidencia, no publicar.

### Proximos 7 temas sugeridos

1. **No se opera una imagen.**
   - Pedir: cara a camara, manos dibujando columna, B-roll consultorio, estudio
     sanitizado opcional.

2. **No toda hernia necesita cirugia.**
   - Pedir: explicacion breve del Doctor, pizarron simple, plano CMP, nota de
     criterios generales.

3. **Cuando la ubicacion cambia la estrategia.**
   - Pedir: dibujo o modelo anatomico, voz del Doctor, estudio sanitizado si lo
     permite privacidad.

4. **Que llevar a una consulta de columna.**
   - Pedir: lista en papel, walking al consultorio, Doctor mostrando carpeta sin
     datos reales.

5. **Monitoreo neurofisiologico: operar con informacion.**
   - Pedir: B-roll seguro de preparacion/equipo sin pacientes, frase del Doctor
     sobre seguridad, no mostrar pantallas identificables.

6. **Dolor que baja a la pierna: que importa contar.**
   - Pedir: cara a camara, 3 preguntas, plano de caminata, cierre con consulta.

7. **El seguimiento tambien es tratamiento.**
   - Pedir: consultorio, agenda sin datos, walking, frase humana sobre control y
     recuperacion.

### Uso opcional de IA

- **Gemini / Opus**: brainstorm de hooks, variaciones de storyboard, copy y
  calendario editorial. Siempre pasa por voz/criterio del Doctor.
- **Nano Banana u otra imagen/video IA**: solo backgrounds, limpieza visual o
  placas abstractas. No usar para simular paciente, quirofano, estudio o
  evidencia clinica.
- **TTS local**: usar solo cuando la voz suene sobria y natural. Prioridad:
  voz real del Doctor o locutor validado; IA como fallback controlado.
- **Vision AI**: util para checklist de legibilidad/privacidad, pero no como
  aprobacion final. El gate humano/CEO manda.

## attempted_routes

- Se intento cubrir las tres fuentes obligatorias en `/Users/jarvis/...`; no
  existen en esta Mac.
- Se usaron fuentes locales equivalentes del bridge para gate CMP, inbox de
  assets y resultados previos aprobados.
- Se revisaron rutas publicas web y paginas oficiales de herramientas. Para
  referencias sociales, Instagram puede bloquear o esconder metricas; se uso
  YouTube/public search como ruta alternativa verificable.
- No se contacto a terceros, no se publico contenido y no se accedio a
  Telegram/Gmail/Drive/Calendar/Fotos/iCloud.

## risks/limits

- Las metricas de seguidores/subscriptores cambian y algunas plataformas no
  muestran conteos completos sin login. Por eso las referencias se tratan como
  patrones de estilo, no como benchmark numerico exacto.
- Kdenlive/Blender/Natron son open source, pero la calidad diaria depende de
  templates y material real. Sin videos verticales propios, el sistema cae en
  slideshow.
- DaVinci Resolve puede ser excelente para color/edicion, pero no es open
  source; queda como benchmark opcional, no como base del flujo pedido.
- `yt-dlp` debe usarse solo para referencia/metadata cuando sea legal. Nunca
  reutilizar audio/video de terceros en piezas CMP.
- La decision de publicacion queda en Codex orquestador y en el Doctor; este
  resultado solo propone sistema y gate.

## confidence

**medium_high**.

Alta confianza en el pipeline local/open-source porque combina fuentes oficiales
de herramientas, gates locales CMP y resultados previos del bridge. Confianza
media en la lectura de cuentas >100K porque los conteos publicos pueden variar y
no conviene depender de Instagram sin login; aun asi, los patrones de estilo son
consistentes entre referencias medicas/profesionales publicas.

## evidence_paths

Locales:

- `jobs/20260526T191159-reels-professional-open-source-tooling-and-style-research-v1.md`
- `claims/20260526T191159-reels-professional-open-source-tooling-and-style-research-v1.json`
- `docs/reels_premium_acceptance_gate.md`
- `context/fronts/reels_cmp.md`
- `docs/pablo_asset_inbox_protocol.md`
- `results/20260525T133959-reel-dia-patria-v2-return-premium-gate.result.md`
- `results/20260525T190553-reels-open-source-voice-pipeline-v1.result.md`
- `results/20260526T184909-reels-cmp-quality-ceo-review-felipe-y-estandar-v1.result.md`

Herramientas:

- `https://kdenlive.org/`
- `https://docs.kdenlive.org/`
- `https://ffmpeg.org/ffmpeg.html`
- `https://ffmpeg.org/ffmpeg-filters.html`
- `https://github.com/ggerganov/whisper.cpp`
- `https://docs.blender.org/manual/en/latest/video_editing/`
- `https://natrongithub.github.io/`
- `https://shotcut.org/`
- `https://www.audacityteam.org/`
- `https://github.com/Aegisub/Aegisub`
- `https://github.com/AcademySoftwareFoundation/OpenTimelineIO`
- `https://github.com/WyattBlue/auto-editor`
- `https://github.com/yt-dlp/yt-dlp`

Referencias de estilo:

- `https://www.youtube.com/@DoctorMike`
- `https://www.youtube.com/@Doctorly`
- `https://www.youtube.com/@MayoClinic`
- `https://www.youtube.com/@ClevelandClinic`
- `https://www.youtube.com/@HealthyGamerGG`
- `https://www.youtube.com/@DrTraceyMarks`
- `https://www.youtube.com/@Medcram`
- `https://www.youtube.com/@DrPimplePopper`
- `https://creators.youtube.com/`
- `https://support.google.com/youtube/answer/10059070`
- `https://creators.instagram.com/`
