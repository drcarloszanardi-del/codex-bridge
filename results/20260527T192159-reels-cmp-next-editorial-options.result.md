---
job_id: 20260527T192159-reels-cmp-next-editorial-options
worker: personal-xh
status: completed
completed_at: 2026-05-27T19:26:06-03:00
front: REELS
no_external_actions: true
no_secrets: true
---

# Resultado - Reels CMP proximas piezas premium

## summary honesto

Las proximas piezas CMP deberian ser utiles, sobrias y producibles con material
propio no sensible. Propongo tres: consulta de columna preparada, no se opera una
imagen, y senales de alarma del dolor lumbar. La recomendada sigue siendo
**Consulta de columna: llegue preparado**, porque tiene alto valor, bajo riesgo y
no requiere caso clinico ni cirugia.

Separacion pedida:

- Evidencia: `context/fronts/reels_cmp.md` fija estetica CMP, datos publicos y
  gate visual.
- Inferencia: tras problemas de exceso de texto o improvisacion, conviene un
  reel educativo simple con assets propios.
- Opinion: si no hay video del Doctor, no conviene reemplazarlo con placas
  largas ni stock.

No renderice, no use Telegram, no publique y no use assets privados.

## coverage_table

| Fuente | Estado | Uso |
| --- | --- | --- |
| `jobs/20260527T192159-reels-cmp-next-editorial-options.md` | Revisada | Objetivo, restricciones y entregables. |
| `context/fronts/reels_cmp.md` | Revisada | Datos publicos, estetica y gate visual. |
| `results/20260525T122941-reels-dia-patria-assets-and-timeline.result.md` | Revisada | Asset pack, timeline y QA frame a frame. |
| `results/20260525T021049-reels-cmp-premium-pipeline-qa-v1.result.md` | Revisada | Pipeline premium, QA y datos publicos. |
| `results/20260527T011700-reels-cmp-next-editorial-options.result.md` | Revisada como fuente operativa | Opciones previas y recomendacion editorial. |

## editorial_options

| Opcion | Hook | Guion corto | Riesgo | Duracion |
| --- | --- | --- | --- | --- |
| Consulta preparada | `Consulta de columna: llegue preparado` | Traiga estudios, anote desde cuando duele, si baja a la pierna, medicacion probada y que actividades limita. | Bajo | 30-38s |
| No se opera una imagen | `No se opera una imagen` | La resonancia ayuda, pero la decision se construye con sintomas, examen neurologico y evolucion. | Medio | 25-35s |
| Senales de alarma | `Dolor de espalda: cuando consultar sin esperar` | Dolor que baja con debilidad, fiebre, perdida de control, trauma o dolor progresivo merecen consulta. | Medio | 30-40s |

Guion recomendado para la opcion 1:

```text
0-3s: Consulta de columna: llegue preparado
3-8s: Traiga sus estudios previos
8-14s: Anote desde cuando duele y como empeora
14-21s: Cuente si baja a la pierna, hormiguea o pierde fuerza
21-28s: Lleve medicacion probada y que actividades limita
28-38s: CMP + @drcarloszanardi + 2364384321 + web
```

## asset_requests

Pedido minimo para `Consulta preparada`:

```text
Mandame por REELS:
1 video vertical tuyo de 12-18s diciendo que llevar a una consulta de columna.
1 plano de mano anotando estudios/sintomas en papel blanco.
1-2 planos de consultorio o escritorio limpio sin pacientes ni papeles.
Nota de voz opcional con tus palabras exactas.
```

Pedido para `No se opera una imagen`:

```text
Mandame 1 video tuyo de 12-18s con la frase "No se opera una imagen",
1 RM totalmente anonima o dibujo propio,
1 plano de mano senalando/dibujando,
y 1 plano de consultorio limpio.
```

Pedido para `Senales de alarma`:

```text
Mandame 1 video corto tuyo nombrando senales de alarma,
1 plano de consultorio limpio,
y si queres 1 toma de mano marcando una lista en papel, sin datos personales.
```

## risk_filter

- Rechazar assets con pacientes, nombres, HC, turnos, pantallas, fechas,
  reflejos con datos o voces no autorizadas.
- No usar anatomia generada como evidencia clinica.
- No prometer cura, resultado o indicacion quirurgica.
- No diagnosticar por reel.
- No publicar si cierre no muestra legibles `@drcarloszanardi`, `2364384321` y
  `www.centromedicopellegrini.com.ar`.
- No convertir falta de material en slideshow largo.

## recommended_next_reel

Recomendacion unica: **Consulta de columna: llegue preparado**.

Motivo: alto valor educativo, bajo riesgo medico-legal, no depende de caso real,
permite tono humano y se puede producir con video corto del Doctor mas dos planos
limpios. Si no llega video propio, dejar en brief/guion y no improvisar con stock.

## telegram_topic_report

Texto listo para el orquestador si decide pedir material:

```text
Para el proximo reel CMP sugiero hacerlo simple y util: "Consulta de columna: llegue preparado".
Necesito 1 video tuyo corto, 1 plano de mano anotando y 1-2 planos de consultorio limpio.
Sin pacientes, papeles, pantallas ni datos privados.
```

## risks / limits

- Sin assets reales, estas son opciones editoriales, no piezas publicables.
- `No se opera una imagen` requiere RM anonima o dibujo propio para no volverse
  generica.
- `Senales de alarma` exige prudencia para no sonar alarmista ni diagnosticar.
- La calidad final depende de luz, audio y plano del Doctor.

## recommendation

Pedir primero assets para `Consulta de columna: llegue preparado`. Codex
principal puede preparar guion, storyboard y cierre CMP mientras espera material.
Hard stop: sin material propio no publicar, no usar stock y no rellenar con
placas largas.

## confidence

Alta para la recomendacion editorial y QA; media para calidad final hasta ver
assets reales.

## evidence_paths

- `jobs/20260527T192159-reels-cmp-next-editorial-options.md`
- `context/fronts/reels_cmp.md`
- `results/20260525T122941-reels-dia-patria-assets-and-timeline.result.md`
- `results/20260525T021049-reels-cmp-premium-pipeline-qa-v1.result.md`
- `results/20260527T011700-reels-cmp-next-editorial-options.result.md`
- `claims/20260527T192159-reels-cmp-next-editorial-options.json`
