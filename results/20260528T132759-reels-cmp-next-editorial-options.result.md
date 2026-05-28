---
job_id: 20260528T132759-reels-cmp-next-editorial-options
worker: personal-xh
status: completed
completed_at: 2026-05-28T13:28:18-03:00
front: REELS
no_external_actions: true
no_secrets: true
---

# Resultado - Reels CMP next editorial options

## summary honesto

Las proximas piezas CMP deben ser utiles, humanas y de bajo riesgo, no placas largas para compensar falta de material. Propongo tres opciones: consulta de columna preparada, no se opera una imagen y como leer signos de alarma sin asustar. La recomendada sigue siendo `Consulta de columna: llegue preparado`, porque requiere pocos assets propios, no usa pacientes ni caso clinico sensible y puede verse premium con video corto del Doctor, mano anotando y consultorio limpio.

## coverage_table

| Requisito | Estado | Evidencia |
|---|---|---|
| `editorial_options` | cubierto | Frente Reels, OS diario y antecedentes editoriales. |
| `asset_requests` | cubierto | Pack minimo por opcion, sin datos sensibles. |
| `risk_filter` | cubierto | Gate visual CMP y hard stops. |
| `recommended_next_reel` | cubierto | Opcion de menor riesgo y mayor utilidad. |
| `telegram_topic_report` | cubierto | Texto listo para que el orquestador use si decide pedir material. |

## evidencia

- `context/fronts/reels_cmp.md` fija estetica sobria, datos publicos correctos y gate visual.
- `results/20260525T122941-reels-dia-patria-assets-and-timeline.result.md` muestra timeline editable, pedido minimo de assets y QA frame a frame.
- `results/20260525T021049-reels-cmp-premium-pipeline-qa-v1.result.md` exige intake, guion, storyboard, QA medico, QA de datos publicos y licencias.
- `context/fronts/reels_daily/operating_system_v1.md` prohibe compensar falta de imagen con placas, stock, texto largo o anatomia generica.
- `results/20260527T011700-reels-cmp-next-editorial-options.result.md` ya habia priorizado consulta de columna preparada.

## inferencia

- La pieza diaria debe decidirse por material disponible, no por deseo editorial.
- Las ideas que no requieren pacientes, cirugia ni anatomia factual generada son mejores para retomar ritmo.
- Si no hay al menos dos bloques visuales propios/autorizados, corresponde pedir material o dejar en hold.

## opinion

El Doctor gana mas con reels simples y confiables que con piezas visualmente cargadas. Un reel premium de CMP no tiene que impresionar: tiene que dar criterio, calma y una accion concreta.

## editorial_options

| Opcion | Hook | Guion corto | Riesgo | Duracion |
|---|---|---|---|---:|
| Consulta preparada | `Consulta de columna: llegue preparado` | "Traiga estudios, anote desde cuando duele, si baja a la pierna, que medicacion probo y que actividades limita." | Bajo | 30-38s |
| No se opera una imagen | `No se opera una imagen` | "La resonancia ayuda, pero la decision se construye con sintomas, examen, evolucion y objetivos del paciente." | Medio | 28-35s |
| Signos de alarma sin asustar | `Dolor de columna: cuando consultar pronto` | "Debilidad, perdida de fuerza, fiebre, antecedente importante o dolor que progresa merecen evaluacion." | Medio | 25-35s |

Opcion institucional de reserva: `Cuidar empieza antes de la consulta`, solo si llegan planos CMP humanos y limpios.

## asset_requests

### 1. Consulta preparada

```text
Para REELS: 1 video vertical del Doctor de 12-18s diciendo que llevar a una consulta de columna; 1 plano de mano anotando sintomas/estudios; 1-2 planos de consultorio o escritorio limpio. Sin pacientes, papeles, pantallas ni datos privados.
```

### 2. No se opera una imagen

```text
Para REELS: 1 video vertical con la frase "No se opera una imagen"; 1 RM totalmente anonimizada o dibujo propio; 1 plano de mano senalando/dibujando; 1 plano de consultorio limpio. Si no hay RM anonima, usar dibujo propio, no stock.
```

### 3. Signos de alarma sin asustar

```text
Para REELS: 1 video corto del Doctor explicando 3 signos; 1 plano de mano escribiendo la lista; 1 plano CMP limpio. No usar imagenes dramaticas, pacientes ni anatomia generada como evidencia.
```

## risk_filter

- Rechazar cualquier asset con paciente, historia clinica, turno, nombre, fecha, pantalla, reflejo o metadata sensible visible.
- No usar anatomia generada como evidencia clinica.
- No usar RM/TC si no esta completamente anonimizada y autorizada.
- No prometer resultados ni indicar conducta individual.
- No publicar si cierre no muestra `@drcarloszanardi`, `2364384321` y `www.centromedicopellegrini.com.ar` legibles durante al menos 4s.
- No reemplazar video faltante con slideshow, stock o placas largas.
- No enviar sin contact sheet/preview y QA de datos frame a frame.

## recommended_next_reel

Recomendacion: **Consulta de columna: llegue preparado**.

Motivo:

- Mayor utilidad inmediata.
- Bajo riesgo medico-legal.
- No depende de pacientes, RM ni cirugia.
- Puede hacerse con material propio minimo.
- Encaja con tono sobrio y profesional CMP.

Storyboard sugerido:

| Tiempo | Visual | Texto pantalla | Voz/copy |
|---:|---|---|---|
| 0-3s | Doctor a camara | `Consulta de columna` | "Llegue preparado." |
| 3-9s | Mano anotando | `Estudios previos` | "Traiga estudios e informes." |
| 9-15s | Doctor/escritorio | `Desde cuando duele` | "Anote inicio y evolucion." |
| 15-22s | Mano lista breve | `Pierna / fuerza / hormigueo` | "Cuente si baja, adormece o limita." |
| 22-29s | Consultorio limpio | `Medicacion y limites` | "Que probo y que actividades no puede hacer." |
| 29-38s | CMP/cierre | contacto CMP | "Ordenar la informacion ayuda a decidir mejor." |

## telegram_topic_report

Texto listo para el orquestador, si decide pedir material:

```text
Para el proximo reel CMP sugiero "Consulta de columna: llegue preparado".
Necesito 1 video vertical suyo de 12-18s, 1 plano de mano anotando y 1-2 planos de consultorio limpio.
Sin pacientes, papeles, pantallas, turnos ni datos privados.
El reel va a ser sobrio, util y con cierre CMP: @drcarloszanardi / 2364384321 / www.centromedicopellegrini.com.ar.
```

## risks / limits

- Sin assets reales, esto es paquete editorial, no candidato publicable.
- La opcion "No se opera una imagen" requiere RM anonima o esquema propio; si no, queda en hold.
- "Signos de alarma" puede sonar alarmista si se edita con musica/imagenes dramaticas.
- No se uso Telegram ni se pidio material; el topic report es solo texto para el orquestador.
- Ruta alternativa si no llega video del Doctor: dejar solo brief/storyboard y no renderizar.

## recommendation

Pedir material para `Consulta de columna: llegue preparado`. Si llega video propio, avanzar a storyboard/render sobrio. Si no llega, no improvisar con stock ni placas: dejar el reel en hold y preparar guion/caption solamente.

## confidence

Alta para recomendacion editorial y QA de bajo riesgo. Media para calidad final hasta ver assets reales.

## evidence_paths

- `jobs/20260528T132759-reels-cmp-next-editorial-options.md`
- `context/fronts/reels_cmp.md`
- `context/fronts/reels_daily/operating_system_v1.md`
- `results/20260525T122941-reels-dia-patria-assets-and-timeline.result.md`
- `results/20260525T021049-reels-cmp-premium-pipeline-qa-v1.result.md`
- `results/20260527T011700-reels-cmp-next-editorial-options.result.md`
