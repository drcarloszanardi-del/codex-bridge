# Resultado - reels cmp next editorial options

Job: `20260525T124546-reels-cmp-next-editorial-options`
Worker: `personal-xh` / Pablo
Fecha: `2026-05-25`

## summary honesto

Hay tres piezas de alto valor y bajo riesgo para CMP: preparacion para consulta, senales de alarma de dolor lumbar y mito "toda hernia se opera". La mas segura para producir ahora es preparacion para consulta porque no exige pacientes, estudios reales ni promesas clinicas; ademas mejora la calidad de turnos y puede grabarse con consultorio, Doctor o voz en off.

## source_counts

| Fuente | Archivos revisados | Uso |
|---|---:|---|
| `context/fronts/reels_cmp.md` | 1 | Datos publicos, estetica CMP y gate visual. |
| `results/20260525T122941-reels-dia-patria-assets-and-timeline.result.md` | 1 | Asset pack minimo, timeline y QA frame a frame. |
| `results/20260525T021049-reels-cmp-premium-pipeline-qa-v1.result.md` | 1 | Pipeline premium, aprobacion humana y datos publicos fijos. |

## editorial_options

| Opcion | Valor | Riesgo | Guion corto | CTA prudente |
|---|---|---|---|---|
| Prepararse para la consulta de columna | Ordena demanda, mejora anamnesis y evita ida y vuelta | Bajo | "Si va a consultar por columna, traiga sus estudios previos, anote desde cuando duele, si baja a la pierna, que medicacion probo y que limita en su vida diaria. Una consulta mejor preparada ayuda a decidir mejor." | "Solicite turno en Centro Medico Pellegrini." |
| Dolor lumbar: 3 senales para consultar | Alto interes y utilidad publica | Medio-bajo | "El dolor lumbar es frecuente, pero conviene consultar si aparece perdida de fuerza o sensibilidad, dolor luego de trauma o fiebre, o cambios en control de esfinteres. Cada caso requiere evaluacion profesional." | "Ante sintomas de alarma, consulte." |
| Mito: toda hernia se opera | Desarma ansiedad y posiciona criterio medico | Medio-bajo | "No toda hernia de disco termina en cirugia. La decision depende de sintomas, examen fisico, evolucion, imagenes y respuesta al tratamiento. La imagen sola no decide." | "Evaluelolo con un especialista." |

## asset_requests

| Opcion | Minimo obligatorio | Deseable | Prohibido |
|---|---|---|---|
| Prepararse para consulta | Doctor a camara o voz en off, consultorio sin datos, placa final CMP | B-roll escritorio, agenda, pasillo, logo | Historias clinicas, estudios con nombre, pacientes. |
| Senales de alarma | Doctor a camara, placa de texto por cada senal, fondo sobrio | B-roll consultorio y caminata neutra | Imagenes quirurgicas, pacientes, anatomia generada como evidencia. |
| Mito hernia/cirugia | Doctor a camara, placa "mito", consultorio | Modelo anatomico real si existe y es correcto | Promesas de evitar cirugia, RM con datos, claims absolutos. |

Datos de cierre a verificar en todos: `@drcarloszanardi`, `2364384321`, `www.centromedicopellegrini.com.ar`.

## risk_filter

- No diagnosticar al espectador ni indicar tratamiento individual.
- No prometer resultados, evitar "cura", "sin riesgo" o "evita cirugia".
- No usar pacientes, historias clinicas, pantallas, estudios identificables ni marcas de agua.
- No usar anatomia generada como evidencia clinica.
- Mantener estetica sobria CMP, texto legible y cierre de contacto minimo 4 segundos.
- Publicacion solo con aprobacion humana y QA completo.

## recommended_next_reel

Recomiendo producir primero "Prepararse para la consulta de columna".

Motivo: es el menor riesgo medico-legal, requiere menos assets sensibles, sirve a todas las consultas y permite establecer plantilla premium reutilizable. Version sugerida: 25 a 35 segundos, Doctor a camara o voz en off, 4 placas cortas y cierre institucional.

## telegram_topic_report

Reporte para el orquestador, sin enviar mensajes externos desde este worker:

- Frente: `REELS/CMP`.
- Topic sugerido: `asset_request_reel_consulta_columna`.
- Pedido al Doctor cuando el orquestador decida avanzar: una toma suya hablando o foto sobria, 2 tomas de consultorio/pasillo sin pacientes, logo o placa CMP y confirmacion de datos publicos.
- Si el material llega por Telegram, procesar album completo antes de editar y descartar cualquier archivo con paciente, HC o datos visibles.

## risks / limits

- Sin assets reales solo se puede cerrar guion, storyboard y checklist, no montaje final.
- Las senales de alarma requieren redaccion especialmente prudente para no sonar a triage definitivo.
- La opcion hernia/cirugia puede generar mas engagement, pero debe evitar absolutismos.
- Musica, imagenes y logos deben tener permiso o fuente segura.

## recommendation

Codex principal debe pedir assets solo para la pieza "Prepararse para la consulta de columna" y preparar una plantilla editable CMP. Mantener las otras dos como siguientes piezas si la primera valida tono y flujo de QA.

## confidence

Alta para seleccion editorial y filtro de riesgo. Media para ejecucion visual hasta ver material real.

## evidence_paths

- `jobs/20260525T124546-reels-cmp-next-editorial-options.md`
- `context/fronts/reels_cmp.md`
- `results/20260525T122941-reels-dia-patria-assets-and-timeline.result.md`
- `results/20260525T021049-reels-cmp-premium-pipeline-qa-v1.result.md`
