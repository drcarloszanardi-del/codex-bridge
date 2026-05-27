---
job_id: 20260527T183421-reels-dia-patria-assets-and-timeline
worker: personal-xh
status: completed
completed_at: 2026-05-27T18:38:00-03:00
front: REELS
no_external_actions: true
no_secrets: true
---

# Resultado - Reel Dia de la Patria assets y timeline

## summary honesto

Timeline tecnico editable de 40 segundos para el reel Dia de la Patria CMP, con
assets minimos, variantes de montaje, notas de edicion y QA frame a frame. No se
pidieron assets por canales externos, no se publico nada y no se asumio que haya
material real disponible.

## coverage_table

| Fuente | Estado | Uso |
| --- | --- | --- |
| `jobs/20260527T183421-reels-dia-patria-assets-and-timeline.md` | Revisada | Workorder y secciones requeridas. |
| `context/fronts/reels_cmp.md` | Revisada | Datos correctos y gate visual CMP. |
| `results/20260525T120325-reel-dia-patria-cmp-premium-v1.result.md` | Revisada | Concepto A, storyboard 40s, asset request y QA. |

## evidence_inference_opinion

| Tipo | Contenido |
| --- | --- |
| Evidencia | Contacto canonico: `@drcarloszanardi`, `2364384321`, `www.centromedicopellegrini.com.ar`. |
| Inferencia | La pieza necesita material propio de CMP/Doctor para evitar stock o escena clinica inventada. |
| Opinion | La version de 40s debe respirar; derivar 25-30s solo despues de tener master aprobado. |

## timeline_40s

| Timecode | Visual | Texto | Audio/voz | Notas |
| --- | --- | --- | --- | --- |
| 00:00-00:03 | Fondo celeste/blanco suave o bandera real desenfocada | `25 de Mayo` | Inicio musical calmo | Sin bandera dominante ni efecto patriotico fuerte. |
| 00:03-00:07 | Fachada/placa CMP o pasillo limpio | `Dia de la Patria` | "En una fecha que nos une..." | Si no hay fachada, usar placa limpia CMP. |
| 00:07-00:12 | Consultorio preparado, escritorio o guardapolvo | `Cuidar tambien es construir` | "...recordamos el valor del trabajo responsable." | No mostrar historias clinicas. |
| 00:12-00:18 | B-roll medico no sensible, instrumental general o sala vacia | `Compromiso. Ciencia. Cercania.` | "En salud, cada detalle importa." | Evitar anatomia generada como evidencia. |
| 00:18-00:24 | Dr./equipo caminando o saludo institucional | `Acompanamos a nuestra comunidad` | "Estar presentes es parte del compromiso." | Sin pacientes identificables. |
| 00:24-00:31 | Plano CMP calido, movimiento lento | `Centro Medico Pellegrini` | "Con profesionalismo, humanidad y respeto." | Color sobrio, sin saturacion celeste excesiva. |
| 00:31-00:36 | Dr. Carlos Zanardi / consultorio / placa sobria | `Dr. Carlos Zanardi` | "Feliz Dia de la Patria." | Pausa visual antes del cierre. |
| 00:36-00:40 | Placa final limpia | `@drcarloszanardi` `2364384321` `www.centromedicopellegrini.com.ar` | Musica resuelve | Minimo 3s legibles para contacto. |

## minimal_asset_pack

Obligatorio:

```text
01_logo_o_placa_cmp.png
02_fachada_o_pasillo_cmp_vertical.mov|jpg
03_consultorio_limpio_sin_datos.mov|jpg
04_dr_zanardi_plano_institucional_vertical.mov|jpg
05_placa_contacto_confirmada.txt
```

Deseable:

```text
06_manos_preparando_escritorio_o_material_no_sensible.mov
07_bandera_argentina_real_o_detalle_celeste_blanco.mov|jpg
08_sala_vacia_prolija_sin_pacientes.mov|jpg
09_logo_vectorial_si_existe.svg|pdf
```

No usar:

```text
pacientes_identificables
historias_clinicas
monitores_con_datos
stock_generico_de_hospital
logos_inventados
anatomia_generada_como_prueba_clinica
```

## editing_notes

- Formato: vertical 1080x1920, 24 o 30 fps.
- Duracion master: 40s; variante corta: 25-30s.
- Ritmo: cortes limpios y fundidos cortos, sin zooms agresivos.
- Texto: maximo 1-2 lineas por escena, alto contraste, safe margins.
- Color: blanco, gris claro, celeste suave; no azul saturado ni look de flyer.
- Musica: institucional calida, piano/cuerdas/ambient, licencia apta.
- Cierre: datos de contacto visibles y verificados.

Variantes:

| Variante | Uso | Cambio |
| --- | --- | --- |
| Master 40s | Reel principal | Mantiene todas las escenas. |
| Short 30s | Stories / version rapida | Combina 00:12-00:24 y acorta cierre a 4s. |
| Silent captions | Reproduccion sin audio | Texto completo en pantalla, sin depender de voz. |

## qa_frame_checklist

Revisar antes de publicar:

- Telefono exacto: `2364384321`.
- Instagram exacto: `@drcarloszanardi`.
- Web exacta: `www.centromedicopellegrini.com.ar`.
- Ningun paciente, historia clinica, placa, monitor o documento sensible visible.
- Ningun logo inventado ni watermark.
- Ningun texto placeholder.
- No promete resultados medicos.
- No usa anatomia generada como evidencia clinica.
- Placa final visible al menos 3 segundos.
- Texto legible en celular con brillo bajo.
- Musica con licencia.
- Aprobacion humana final antes de publicar.

## doctor_asset_request

Mensaje sugerido para Codex principal, no enviado por este worker:

```text
Doctor, para cerrar el reel institucional del Dia de la Patria sin usar stock ni
material inventado, necesito una carpeta con 4-6 assets propios:

1. logo o placa del Centro Medico Pellegrini;
2. fachada, pasillo o recepcion sin pacientes;
3. consultorio limpio sin historias clinicas ni datos visibles;
4. un plano suyo vertical o foto institucional simple;
5. opcional: bandera argentina real o detalle celeste/blanco sobrio;
6. opcional: manos preparando escritorio o material no sensible.

Con eso armamos una pieza sobria de 40s y una version corta, con cierre:
@drcarloszanardi / 2364384321 / www.centromedicopellegrini.com.ar.
```

## risks / limits

- Sin assets propios, la pieza queda como timeline listo pero no deberia
  cerrarse con stock generico.
- Debe verificarse logo/paleta institucional real.
- No se publico ni se contacto a nadie desde este worker.
- Si aparecen pacientes o datos, esos clips deben descartarse o recortarse.

## recommendation

Codex principal deberia pedir el minimal asset pack y editar el master 40s con
QA frame a frame. Si faltan assets, hacer solo placa/storyboard interno y no
publicar pieza final.

## confidence

Alta para timeline, QA y datos de contacto por contexto canonico. Media para
direccion visual final hasta ver assets reales.

## evidence_paths

- `jobs/20260527T183421-reels-dia-patria-assets-and-timeline.md`
- `context/fronts/reels_cmp.md`
- `results/20260525T120325-reel-dia-patria-cmp-premium-v1.result.md`
