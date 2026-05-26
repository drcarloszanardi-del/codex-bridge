# Resultado - 20260526T065253-reels-cmp-next-editorial-options

## summary honesto

Las proximas piezas CMP deben ser utiles, sobrias y producibles con material propio o institucional, sin pacientes ni datos sensibles. La opcion mas segura sigue siendo una pieza de preparacion para consulta de columna; permite calidad alta con bajo riesgo y poca dependencia de material medico delicado.

**Evidencia:** el frente REELS fija estetica CMP, contacto correcto y QA visual. Los resultados previos establecen pipeline premium, asset pack minimo y aprobacion humana.

**Inferencia:** para sostener continuidad editorial conviene alternar reels educativos de bajo riesgo con piezas institucionales propias, no depender de imagenes genericas.

**Opinion:** mejor publicar menos piezas, pero con verdad visual y contacto perfecto, que acelerar con stock o anatomia decorativa.

## coverage_table

| Fuente | Uso | Limite |
| --- | --- | --- |
| `context/fronts/reels_cmp.md` | Datos publicos, estetica CMP y gate visual. | No define calendario editorial. |
| `results/20260525T122941-reels-dia-patria-assets-and-timeline.result.md` | Timeline, asset pack minimo y QA frame a frame. | Pieza especifica Dia de la Patria. |
| `results/20260525T021049-reels-cmp-premium-pipeline-qa-v1.result.md` | Pipeline premium y aprobacion humana. | Resumen corto, sin guiones nuevos. |

## editorial_options

| Opcion | Valor | Riesgo | Guion corto | CTA prudente |
| --- | --- | --- | --- | --- |
| Prepararse para la consulta de columna | Mejora calidad del turno y reduce ida y vuelta | Bajo | "Si va a consultar por columna, traiga estudios previos, anote desde cuando duele, si baja a la pierna, que medicacion probo y que limita. Una consulta mejor preparada ayuda a decidir mejor." | "Solicite turno en Centro Medico Pellegrini." |
| Dolor lumbar: 3 senales para consultar | Alta utilidad publica | Medio-bajo | "El dolor lumbar es frecuente, pero conviene consultar si hay perdida de fuerza o sensibilidad, fiebre/trauma, o cambios en control de esfinteres. Cada caso requiere evaluacion profesional." | "Ante sintomas de alarma, consulte." |
| Mito: toda hernia se opera | Baja ansiedad y posiciona criterio medico | Medio-bajo | "No toda hernia de disco termina en cirugia. La decision depende de sintomas, examen fisico, evolucion, imagenes y respuesta al tratamiento. La imagen sola no decide." | "Evaluelo con un especialista." |

## asset_requests

| Opcion | Minimo obligatorio | Deseable | Prohibido |
| --- | --- | --- | --- |
| Consulta de columna | Doctor a camara o voz en off, consultorio sin datos, placa final CMP | B-roll escritorio, agenda, pasillo, logo | HC, estudios con nombre, pacientes. |
| Senales de alarma | Doctor a camara, placas de texto, fondo sobrio | B-roll consultorio y caminata neutra | Imagenes quirurgicas, pacientes, anatomia generada como evidencia. |
| Mito hernia/cirugia | Doctor a camara, placa "mito", consultorio | Modelo anatomico real si es correcto | Promesas, RM con datos, claims absolutos. |

Datos de cierre a verificar en todos: `@drcarloszanardi`, `2364384321`, `www.centromedicopellegrini.com.ar`.

## risk_filter

- No diagnosticar al espectador ni indicar tratamiento individual.
- No prometer resultados, evitar "cura", "sin riesgo" o "evita cirugia".
- No usar pacientes, historias clinicas, pantallas, estudios identificables, marcas de agua ni placeholders.
- No usar anatomia generada como evidencia clinica.
- Procesar album completo antes de editar si llegan varias fotos/videos.
- Verificar contacto y cierre frame a frame; cierre visible al menos 4 segundos.
- Publicar solo con aprobacion humana y QA completo.

## recommended_next_reel

Recomiendo producir primero "Prepararse para la consulta de columna".

Motivo: es util para pacientes, no requiere estudios reales, evita promesas clinicas y sirve como plantilla premium reutilizable. Version sugerida: 25 a 35 segundos, Doctor a camara o voz en off, 4 placas cortas y cierre institucional.

## telegram_topic_report

Reporte para el orquestador, sin enviar mensajes externos desde este worker:

- Frente: `REELS/CMP`.
- Topic sugerido: `asset_request_reel_consulta_columna`.
- Pedido al Doctor cuando el orquestador decida avanzar: 1 toma suya hablando o foto sobria, 2 tomas de consultorio/pasillo sin pacientes, logo o placa CMP y confirmacion de datos publicos.
- Si el material llega por Telegram o carpeta local, revisar todo el paquete antes de editar y descartar cualquier archivo con paciente, HC o datos visibles.
- Mantener la norma de proteccion: usar material propio aprobado, no exponer nombres de archivos privados ni publicar rutas internas.

## risks_limits

- Sin assets reales solo se puede cerrar guion, storyboard y checklist; no montaje final.
- La pieza de senales de alarma requiere redaccion prudente para no sonar a triage definitivo.
- La pieza de hernia/cirugia puede atraer mas, pero tiene mayor riesgo de absolutismos.
- Musica, imagenes y logos deben tener permiso o fuente segura.
- No se usaron acciones externas ni material personal en este job.

## recommendation

Codex principal debe preparar plantilla editable CMP y pedir assets solo para "Prepararse para la consulta de columna". Las otras dos opciones quedan como backlog inmediato si el primer reel valida tono, flujo de QA y disponibilidad de material propio.

## confidence

Alta para seleccion editorial y filtro de riesgo. Media para ejecucion visual hasta ver material real.

## evidence_paths

- `jobs/20260526T065253-reels-cmp-next-editorial-options.md`
- `context/fronts/reels_cmp.md`
- `results/20260525T122941-reels-dia-patria-assets-and-timeline.result.md`
- `results/20260525T021049-reels-cmp-premium-pipeline-qa-v1.result.md`
- `results/20260525T124546-reels-cmp-next-editorial-options.result.md`
