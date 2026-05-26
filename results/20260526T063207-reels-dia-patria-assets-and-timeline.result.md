# Resultado - 20260526T063207-reels-dia-patria-assets-and-timeline

## summary honesto

Se convierte el reel Dia de la Patria CMP en timeline tecnico editable, pedido minimo de assets y QA frame a frame. No se pidio material externo ni se publico nada. La pieza debe ser institucional, sobria y con material propio del Doctor/CMP.

**Evidencia:** el concepto recomendado previo fue "La patria tambien se cuida", 40s, tono cercano, cierre con `@drcarloszanardi`, `2364384321` y web CMP.

**Inferencia:** la version editable debe separar timeline, assets, montaje, caption y QA para que Codex principal pueda renderizar sin inventar material.

**Opinion:** el reel sirve si se siente propio y humano; si faltan assets reales, conviene producir una version corta sobria antes que rellenar con stock.

## coverage_table

| fuente | uso | limite |
| --- | --- | --- |
| `context/fronts/reels_cmp.md` | Datos canonicos, estetica CMP y gate visual. | No provee assets. |
| `results/20260525T120325-reel-dia-patria-cmp-premium-v1.result.md` | Concepto, storyboard, asset request, visual direction y QA. | Requiere material real/aprobado antes de render final. |

## timeline_40s

| tiempo | visual | texto | nota tecnica |
| ---: | --- | --- | --- |
| 0-3s | Detalle celeste/blanco, bandera real suave o fondo propio CMP | `25 de Mayo` | Hook limpio, sin logo inventado. |
| 3-7s | Fachada, placa, ingreso o pasillo CMP sin pacientes | `Dia de la Patria` | Corte/fundido corto; estabilizar vertical 9:16. |
| 7-12s | Consultorio preparado, escritorio, guardapolvo, manos | `Cuidar tambien es construir` | Plano cercano, sin historias clinicas ni datos. |
| 12-18s | B-roll medico no sensible: sala preparada, instrumental general, monitor sin datos | `Compromiso. Ciencia. Cercania.` | No usar anatomia generada ni pantalla con datos. |
| 18-24s | Dr. Zanardi/equipo caminando o saludo institucional | `Acompanamos a nuestra comunidad` | Rostros solo de equipo autorizado; sin pacientes. |
| 24-31s | Plano institucional CMP, luz natural, movimiento suave | `Centro Medico Pellegrini` | Mantener paleta blanco/celeste/gris. |
| 31-36s | Dr. Carlos Zanardi o placa sobria | `Dr. Carlos Zanardi` | Preparar cierre, bajar densidad visual. |
| 36-40s | Placa final limpia | `@drcarloszanardi` / `2364384321` / `www.centromedicopellegrini.com.ar` | Contacto minimo 3-4s, legible en celular. |

## minimal_asset_pack

Obligatorio:

- 1 logo/placa CMP real si existe.
- 1 fachada/ingreso/pasillo CMP sin pacientes.
- 1 plano consultorio o escritorio sin datos privados.
- 1 plano del Doctor o equipo autorizado.
- 1 placa final o permiso para crear placa con datos canonicos.

Deseable:

- 1 plano de manos preparando material no sensible.
- 1 sala/quirofano vacio o b-roll medico sin paciente.
- 1 detalle patrio real y sobrio: bandera, escarapela o luz celeste/blanca.

Fallback si falta material:

- Version 25-30s con 3-4 assets propios + placa final, evitando stock generico.

## editing_notes

- Formato vertical 1080x1920, ritmo calmo, cortes limpios y fundidos breves.
- Texto maximo 1-2 lineas por escena, alto contraste.
- No usar patriotismo estridente ni marcha literal como obligacion.
- Si hay musica, elegir pista con licencia apta y volumen bajo.
- Separar versiones: `40s_full`, `25s_short`, `story_cut`.
- No usar pacientes, HC, monitores con datos, logos inventados ni watermark.
- Si se usa fondo generado, solo como textura abstracta; nunca como evidencia clinica.

## qa_frame_checklist

- Telefono exacto: `2364384321`.
- Instagram exacto: `@drcarloszanardi`.
- Web exacta: `www.centromedicopellegrini.com.ar`.
- Cierre legible en proxy movil.
- Ningun paciente identificable.
- Ningun dato clinico o administrativo visible.
- Ningun placeholder, watermark, logo falso o texto cortado.
- Imagenes medicas solo si son propias y no sensibles; para este reel no son necesarias.
- Contacto visible minimo 3 segundos.
- Aprobacion humana final antes de publicar.

## doctor_asset_request

Doctor, para armarlo bien nuestro, alcance con una carpeta de 6 a 8 archivos:

1. Fachada, ingreso o pasillo del CMP sin pacientes.
2. Consultorio/escritorio preparado, sin historias clinicas ni pantallas con datos.
3. Un plano suyo o del equipo autorizado, sobrio.
4. Manos preparando material o detalle de trabajo medico no sensible.
5. Bandera/escaparapela/detalle celeste-blanco real si tiene.
6. Logo o placa CMP real, si existe.

No hace falta mandar Drive ni fotos personales amplias. Solo esos archivos, y si algo muestra pacientes o datos, mejor no usarlo o avisar para recortar localmente.

## risks_limits

- Sin assets reales, no conviene declarar pieza premium final.
- Stock generico debilita el pedido del Doctor de hacer algo propio.
- El logo/paleta exacta deben verificarse con material institucional real.
- La musica y publicacion requieren aprobacion/licencia externa por fuera de este worker.

## recommendation

Renderizar primero version 40s si hay al menos 5 assets propios seguros. Si llegan menos, hacer corte 25-30s institucional y pedir el resto puntualmente.

## confidence

Alta para timeline, QA y datos canonicos; media para acabado final hasta ver assets reales.

## evidence_paths

- `jobs/20260526T063207-reels-dia-patria-assets-and-timeline.md`
- `context/fronts/reels_cmp.md`
- `results/20260525T120325-reel-dia-patria-cmp-premium-v1.result.md`
