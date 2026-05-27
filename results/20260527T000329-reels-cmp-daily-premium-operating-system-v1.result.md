---
job_id: 20260527T000329-reels-cmp-daily-premium-operating-system-v1
worker: personal-xh
status: completed
completed_at: 2026-05-27T00:05:10-03:00
front: REELS
no_external_actions: true
no_secrets: true
---

# Resultado - Reels CMP daily premium operating system v1

## summary

Propongo **CMP Daily Reel OS v1**: un flujo diario que produce solo si hay
material propio suficiente, bloquea piezas pobres antes del render y convierte
cada pedido al Doctor en una lista concreta de planos. La regla central es:
**calidad diaria no significa publicar diario; significa decidir diario si se
puede publicar, pedir assets o poner en hold**.

No renderice, no envie mensajes externos, no abri Fotos/iCloud/Drive/Gmail ni
bibliotecas privadas, y no toque credenciales.

## coverage_table

| Fuente | Estado | Uso |
| --- | --- | --- |
| `jobs/20260527T000329-reels-cmp-daily-premium-operating-system-v1.md` | Revisada | Objetivo y entregables. |
| `context/fronts/reels_cmp.md` | Revisada | Contacto canonico, tono CMP y gate visual. |
| `docs/reels_premium_acceptance_gate.md` | Revisada | Regla CEO, hard stops y salida minima diaria. |
| `context/fronts/reels_cmp_cinematic_references_2026-05-26.md` | Revisada | Gramatica de planos, transiciones y bajo texto. |
| `results/20260526T230823-reels-cmp-low-text-transition-quality-reset-v1.result.md` | Revisada | Reset por rechazo: no salvar con texto/placas. |
| `results/20260526T233419-reels-lumbar-cinematic-v3-shotlist-and-gate-review.result.md` | Revisada | Hold lumbar y necesidad de assets propios. |
| `results/20260526T191159-reels-professional-open-source-tooling-and-style-research-v1.result.md` | Revisada | Workflow local, herramientas y formatos diarios. |
| `results/20260526T184909-reels-cmp-quality-ceo-review-felipe-y-estandar-v1.result.md` | Revisada | No aprobar sin evidencia visual auditable. |
| `context/fronts/reels_daily/2026-05-26-brief-operativo-reel-cmp.md` | Revisada | Brief diario previo y tema educativo seguro. |

## daily_reel_pipeline

1. **Idea diaria, 1 frase.** Elegir un solo tema: pregunta de paciente + tesis
   medica prudente. Si no se puede escribir en una frase, no se edita.
2. **Asset request por tipo.** El orquestador pide 3-5 clips concretos por topic
   REELS; no pide "mandame fotos" ni acceso a bibliotecas.
3. **Manifest de origen.** Registrar material recibido, permiso, privacidad,
   que se puede usar y que queda excluido.
4. **Brief de 10 minutos.** Definir hook, 3 beats, cierre CMP, texto maximo,
   audio previsto y riesgos.
5. **Storyboard visual.** Primero planos y funcion narrativa; despues guion.
   Prohibido empezar por placas de texto.
6. **Gate pre-render.** Si faltan 2 bloques visuales propios/autorizados, se
   pide mas material o se cambia a pieza institucional de bajo riesgo.
7. **Edicion.** Corte sobrio, ritmo 25-40s salvo justificacion, transiciones por
   accion/forma/audio, no slideshow.
8. **Subtitulos y copy.** Texto en pantalla como ancla; Instagram copy como
   explicacion prudente.
9. **QA visual.** Contact sheet 8-12 frames, preview 540x960, privacidad
   frame-by-frame, contacto exacto y cierre >= 4s.
10. **Decision.** `renderizar`, `pedir_mas_material` o `bloquear`. Solo el
    orquestador decide si se envia al Doctor/publica.

## asset_request_templates

### Educativo

```text
Para un reel educativo CMP, mandame por REELS:

1. Un video vertical tuyo de 12-18s diciendo la idea principal en una frase.
2. Un plano de 6-10s de mano dibujando o senalando el punto clave en papel/RM anonima.
3. Dos planos limpios de consultorio/CMP de 6-10s, sin pacientes ni papeles.
4. Una nota de voz opcional con las palabras exactas que queres conservar.

No mandes pacientes, HC, nombres, fechas, pantallas con datos ni estudios identificables.
```

### Caso clinico

```text
Para un caso clinico anonimo CMP, mandame por REELS:

1. La ensenanza del caso en una frase, sin datos personales.
2. RM/TC/foto solo si esta anonima o autorizada para recortar.
3. Dos o tres clips reales del proceso: planificacion, mano, instrumental o consultorio.
4. Que NO se puede mostrar y si hay autorizacion publica.

No mandes cara de paciente, voz de paciente, HC, nombre, DNI, fecha, ID de estudio ni pantalla completa.
```

### Historia humana

```text
Para una historia humana CMP, mandame por REELS:

1. La idea humana en una frase: que queremos que se sienta o entienda.
2. Un video vertical tuyo o del espacio CMP de 10-15s.
3. Dos planos de contexto: pasillo, consultorio, manos, objeto o gesto, sin datos privados.
4. Si aparece otra persona, confirmar autorizacion antes de usarla.

El tono debe ser sobrio; no mandes material sensible ni testimonios sin permiso.
```

### Institucional

```text
Para un reel institucional CMP, mandame por REELS:

1. Que servicio/valor queremos mostrar en una frase.
2. Fachada, ingreso o pasillo CMP en vertical, 8-12s.
3. Consultorio/equipo/trabajo real, 2-3 clips de 6-10s.
4. Logo/placa CMP real si existe y contacto a confirmar.

Sin pacientes, agendas, formularios, pantallas con turnos ni papeles visibles.
```

## premium_gate_decision_tree

```text
START
  |
  |-- Hay una idea clara en 1 frase y hook de 0-3s?
  |     |-- no -> BLOQUEAR: pedir concepto al orquestador/Doctor.
  |     |-- si
  |
  |-- Hay minimo 2 bloques visuales propios/autorizados?
  |     |-- no -> PEDIR_MAS_MATERIAL o cambiar a institucional simple.
  |     |-- si
  |
  |-- Hay riesgo de privacidad no resuelto?
  |     |-- si -> BLOQUEAR hasta sanitizar o reemplazar plano.
  |     |-- no
  |
  |-- El storyboard evita slideshow, stock y placas largas?
  |     |-- no -> REESCRIBIR STORYBOARD.
  |     |-- si
  |
  |-- Audio/subtitulos/cierre/contacto estan decididos?
  |     |-- no -> HOLD_PRE_RENDER.
  |     |-- si
  |
  |-- Contact sheet + preview 540x960 pasan gate?
  |     |-- no -> NO ENVIAR; iterar o hold.
  |     |-- si -> ORQUESTADOR_REVISA; recien despues enviar/publicar.
```

Estados de salida:

- `renderizar`: hay assets, idea, privacidad, audio y storyboard.
- `pedir_mas_material`: idea buena, assets insuficientes.
- `bloquear`: privacidad, mala base, texto excesivo, stock/IA como evidencia o
  pieza por debajo del benchmark.

## shot_grammar_library

| Plano propio | Uso narrativo | Conexion sin slideshow |
| --- | --- | --- |
| Doctor a camara | Autoridad humana y hook. | J-cut hacia B-roll. |
| Mano dibujando | Explicar decision sin placas. | Match cut linea -> RM/esquema. |
| RM/TC anonima recortada | Evidencia segura del tema. | Push-in leve o corte por zona marcada. |
| Consultorio limpio | Contexto y confianza. | L-cut con voz del Doctor. |
| Pasillo/ingreso CMP | Institucional sin flyer. | Corte de respiracion antes del cierre. |
| Instrumental preparado | Medicina concreta. | Match-on-action hacia detalle. |
| Campo/tecnica autorizado | Momento tecnico fuerte. | Usar corto, con contexto y salida suave. |
| Monitor sin datos | Control o seguimiento. | Solo si aporta informacion nueva. |
| Doctor revisando estudio | Criterio medico. | Mirada -> estudio -> mano. |
| Detalle de escritura | Preparacion/orden. | Corte por accion de lapiz/mano. |
| Equipo/CMP trabajando | Comunidad y solvencia. | Montaje breve con audio continuo. |
| Placa CMP final | Contacto y marca. | Entrar desde plano real, no desde cirugia abrupta. |

Regla de biblioteca: cada plano debe cumplir una funcion entre autoridad,
evidencia, accion, contexto o cierre. Si solo decora, no entra.

## text_and_copy_rules

Texto en pantalla:

- Maximo 4-6 palabras por beat.
- Maximo 25-45 palabras en todo el reel, excluyendo contacto.
- Una idea por pantalla.
- No subtitular todo con texto gigante si hay voz; captions son para entender,
  anchors son para recordar.
- No usar frases epicas, motivacionales ni promesas clinicas.
- Si una frase necesita coma larga, va al copy o a la voz, no a placa.

Copy de Instagram:

- Primer renglon: utilidad concreta, no slogan.
- 2-4 lineas explicativas prudentes.
- Cerrar con CMP y contacto canonico: `@drcarloszanardi`, `2364384321`,
  `www.centromedicopellegrini.com.ar`.
- Lenguaje medico-legal prudente: "puede", "hay que evaluar", "en consulta se
  revisa". Evitar "cura", "garantiza", "siempre", "nunca" salvo aclaracion.

## pablo_role

Pablo hace:

- Auditar jobs REELS y resultados previos.
- Convertir objetivos en brief, shotlist, pedidos de asset y gates.
- Revisar contact sheets/previews seguros cuando existan.
- Marcar `pass_premium_gate=false` si falta evidencia visual.
- Producir resultados en `results/`, actualizar `status/personal-xh.json`,
  commitear y pushear.

El orquestador decide:

- Enviar pedidos al Doctor o publicar.
- Aprobar overrides editoriales.
- Abrir/gestionar Telegram u otros canales externos.
- Aceptar material sensible o confirmar permisos clinicos.
- Lanzar renders cuando el gate pre-render esta completo.

## failure_modes

Hard stops que no deben repetirse:

- Renderizar "para ver que onda" sin idea, manifest y storyboard.
- Rehacer una pieza rechazada con la misma estructura.
- Compensar falta de imagen con mas texto.
- Usar stock, IA o anatomia generica como evidencia clinica.
- Slideshow de fotos/RM con zoom repetido.
- Monitor de pared repetido como eje del reel.
- Cierre tipo flyer/WhatsApp con contacto chico.
- Publicar sin audio decidido o con silencio no aprobado.
- Aprobar sin contact sheet/preview 540x960.
- Abrir bibliotecas privadas completas para "buscar algo".

## risks_limits

- Este resultado es sistema operativo, no render ni storyboard final de un reel
  especifico.
- No inspeccione assets nuevos ni bibliotecas privadas; por lo tanto no certifico
  disponibilidad real de material para manana.
- Los templates deben ser enviados por el orquestador, no por este worker.
- Si manana no llegan al menos 2 bloques visuales propios/autorizados, la salida
  premium correcta es hold, no pieza generica.

## recommendation

Proxima accion unica para manana: **el orquestador debe pedir el pack minimo
educativo por topic REELS antes de abrir render**.

Pedido recomendado: un reel educativo de columna de bajo riesgo con el concepto
`No se opera una imagen`: 1 video del Doctor de 12-18s, 1 mano/esquema, 1 RM
anonima si existe, 1-2 planos CMP limpios y nota de voz opcional. Si llega ese
pack, renderizar preview con contact sheet. Si no llega, poner en hold y no
improvisar con placas.

## confidence

Alta para el sistema operativo, gates y templates porque se apoya en el gate CMP
vigente, el rechazo editorial reciente y los resultados REELS previos. Media
para la accion de manana hasta ver assets reales.

## evidence_paths

- `jobs/20260527T000329-reels-cmp-daily-premium-operating-system-v1.md`
- `context/fronts/reels_cmp.md`
- `docs/reels_premium_acceptance_gate.md`
- `context/fronts/reels_cmp_cinematic_references_2026-05-26.md`
- `results/20260526T230823-reels-cmp-low-text-transition-quality-reset-v1.result.md`
- `results/20260526T233419-reels-lumbar-cinematic-v3-shotlist-and-gate-review.result.md`
- `results/20260526T191159-reels-professional-open-source-tooling-and-style-research-v1.result.md`
- `results/20260526T184909-reels-cmp-quality-ceo-review-felipe-y-estandar-v1.result.md`
- `context/fronts/reels_daily/2026-05-26-brief-operativo-reel-cmp.md`
