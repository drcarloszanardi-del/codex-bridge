---
id: 20260525T163832-reels-cmp-standard-ultimo-video-y-locucion
job_id: 20260525T163832-reels-cmp-standard-ultimo-video-y-locucion
created_at: 2026-05-25T16:39:37-03:00
created_by: personal-xh
worker: personal-xh
status: completed
no_external_actions: true
no_secrets: true
---

# Resultado - REELS CMP standard ultimo video y locucion

Job: `20260525T163832-reels-cmp-standard-ultimo-video-y-locucion`
Worker: `personal-xh` / Pablo
Fecha: `2026-05-25`

## summary

El ultimo reel CMP aprobado funciono porque dejo de ser una pieza decorativa y paso a tener tesis, material propio, presencia humana, cierre institucional legible y evidencia de QA. El nuevo piso operativo debe ser: idea fuerte en los primeros 3 segundos, progresion narrativa concreta, minimo dos bloques visuales propios/autorizados, contacto CMP correcto, audio decidido explicitamente y contact sheet auditable antes de cualquier envio al Doctor.

No inspeccione los MP4 de la Mac de trabajo porque este worker no tiene acceso a esos paths locales. Use el workorder, el gate premium y los resultados del bridge del 2026-05-25, especialmente el resultado que marco `final_candidate` y `pass_premium_gate=true`. El estandar queda formulado para que Codex principal lo use como checklist ejecutable en los proximos renders.

## source_counts

| Fuente | Archivos revisados | Uso |
|---|---:|---|
| `jobs/20260525T163832-reels-cmp-standard-ultimo-video-y-locucion.md` | 1 | Contrato, referencia al ultimo video aprobado y entregables requeridos. |
| `docs/reels_premium_acceptance_gate.md` | 1 | Criterios hard gate para aprobar/rechazar reels CMP. |
| `context/fronts/reels_cmp.md` | 1 | Datos publicos CMP, estetica y gate visual. |
| `results/20260525T120325-reel-dia-patria-cmp-premium-v1.result.md` | 1 | Concepto inicial, asset request y QA. |
| `results/20260525T122941-reels-dia-patria-assets-and-timeline.result.md` | 1 | Timeline tecnico y checklist frame a frame. |
| `results/20260525T124546-reels-cmp-next-editorial-options.result.md` | 1 | Banco editorial CMP de bajo riesgo. |
| `results/20260525T130220-reels-assets-library-curation-protocol.result.md` | 1 | Politica material propio/no-stock y privacidad. |
| `results/20260525T131149-reels-render-offload-pablo-fast-node-v1.result.md` | 1 | Contrato Pablo como nodo local de render/QA. |
| `results/20260525T132450-reel-dia-patria-v2-content-first-rework.result.md` | 1 | Diagnostico de por que la version previa fallo narrativamente. |
| `results/20260525T133010-reel-dia-patria-v2-render-pablo-own-assets.result.md` | 1 | Preview propio con tesis pero silencioso. |
| `results/20260525T133959-reel-dia-patria-v2-return-premium-gate.result.md` | 1 | Version `final_candidate`, audio, material propio y contact sheet. |
| `context/asset_packs/20260525-dia-patria-v2/qa/contact_sheet_v4.jpg` | 1 | Evidencia visual segura en bridge, 51 KB. |

## coverage_table

| Area pedida | Estado | Resultado |
|---|---|---|
| Gate premium | cubierto | Se convierte en estandar operativo con criterios de rechazo. |
| Por que funciono el aprobado | cubierto | Tesis + propios + humano + audio + QA. |
| Por que fallaron previos | cubierto | Generico, decorativo, silencioso, preview o asset dudoso. |
| Voz en off vs musica | cubierto | Politica por tipo de pieza y destino Instagram. |
| QA antes de Telegram | cubierto | Checklist tecnico/visual/contacto/coherencia/ruta. |
| Proximos 3 reels | cubierto | Tres conceptos 35-45s, sin Photos/iCloud/Drive. |
| Acciones externas | no realizadas | No se envio Telegram, mail, Drive ni publicacion. |

## observation_inference_recommendation

| Tipo | Contenido |
|---|---|
| Observacion | El bridge registra un candidato final con `pass_premium_gate=true`, 36s, contacto correcto, audio ambiente generado y contact sheet seguro. |
| Observacion | La version previa silenciosa estaba bien estructurada pero no era final publicable. |
| Inferencia | La aprobacion del Doctor se explica por el salto de "saludo institucional lindo" a "idea reconocible + presencia real del Doctor/CMP". |
| Recomendacion | Convertir ese patron en un gate obligatorio: ningun reel CMP pasa si no tiene tesis, material propio, audio decidido y evidencia visual auditable. |

## what_worked

1. **Tesis recordable**: `hacerse cargo` conecta Dia de la Patria con medicina concreta. No es una frase de almanaque; organiza todo el reel.
2. **Idea en 3 segundos**: abrir con `No se honra con frases vacias` crea tension y evita que parezca saludo generico.
3. **Progresion real**: fecha -> hacerse cargo -> escuchar/estudiar/explicar/decidir -> comunidad -> CMP.
4. **Material propio**: C01/C04 y visuales del Doctor desde V02 reemplazan stock/generico y hacen que la pieza sea "nuestra".
5. **Presencia humana sin riesgo**: se usaron visuales de V02, pero no el audio original no revisado.
6. **Cierre institucional claro**: `@drcarloszanardi`, `2364384321`, `www.centromedicopellegrini.com.ar`.
7. **Audio no silencioso**: el ultimo candidato ya no queda como preview mudo; tiene audio ambiente seguro.
8. **QA visible**: contact sheet de 8 frames, seguro y liviano, permite auditar sin subir el MP4 al bridge.

## what_failed_before

1. **Decoracion sin punto de vista**: la primera version podia cambiar de logo y seguir funcionando igual.
2. **Texto generico**: palabras como `compromiso` o `cercania` no alcanzan si no se traducen en acciones medicas concretas.
3. **Preview presentado como pieza**: un render silencioso puede servir internamente, pero falla como reel publicable si se pidio entrega final.
4. **Asset dudoso**: C13 aportaba contexto real, pero tenia imagen medica de presentacion y requeria revision; el aprobado lo reemplazo.
5. **Placas predominantes**: solo texto/placas puede quedar prolijo, pero no necesariamente humano ni propio.
6. **Falta de evidencia visual**: sin contact sheet o revision cuadro a cuadro, el orquestador no puede detectar texto chico, cierre pobre o recortes malos.

## CMP_Reel_Standard_v1

### Principio rector

Un reel CMP no se aprueba por estar renderizado. Se aprueba si deja una idea clara, usa material propio/autorizado, se ve premium en celular, no expone datos privados y tiene contacto correcto.

### Material visual aceptable

- Propio/autorizado: Doctor, CMP, consultorio, pasillo, fachada, placa institucional, escritorio o instrumental no sensible.
- Minimo dos bloques visuales reales propios en cada reel final.
- Placas CMP permitidas como apertura, respiracion narrativa o cierre, pero no como todo el reel.
- Fondos generados solo decorativos; nunca como evidencia medica ni como sustituto de material propio.
- Prohibido: stock, fotos externas, pacientes, HC, estudios identificables, pantallas con datos, marcas de agua, logos inventados, anatomia generada como verdad clinica.

### Ritmo y duracion

- Piso recomendado: 35-40 segundos.
- Hasta 45 segundos solo si hay locucion clara y cada bloque aporta una idea nueva.
- Corte cada 3-6 segundos; evitar pausas muertas.
- Cierre con contacto: minimo 4 segundos legibles.
- Si el mensaje no entra en 40 segundos, recortar texto antes que acelerar la lectura.

### Texto en pantalla

- Maximo una idea por placa.
- Maximo 1-2 lineas por escena.
- Tipografia grande, alto contraste, legible en celular.
- Evitar slogans intercambiables. Preferir verbos concretos: escuchar, estudiar, explicar, decidir, acompanar.
- No usar texto legalista, diagnostico individual ni promesas.

### Cierre institucional

Debe incluir, salvo decision expresa del orquestador:

```text
Centro Medico Pellegrini
Dr. Carlos Zanardi
@drcarloszanardi
2364384321
www.centromedicopellegrini.com.ar
```

Si no entran todos legibles, priorizar contacto exacto y usar dos placas de cierre. El telefono correcto es `2364384321`; cualquier otro numero falla.

### Criterios de rechazo automatico

- No hay idea central en los primeros 3 segundos.
- Podria ser de cualquier clinica cambiando el logo.
- Es silencioso sin justificacion explicita.
- Usa stock o material no propio cuando el Doctor pidio algo nuestro.
- No tiene al menos dos bloques visuales propios/autorizados.
- Contacto incorrecto, ilegible o demasiado breve.
- No hay contact sheet o evidencia visual suficiente.
- Muestra pacientes, HC, estudios identificables, pantallas o datos.
- Usa anatomia generada como evidencia clinica.
- Texto excesivo, placeholder, marca de agua o cierre tipo folleto pobre.
- Se intenta mandar por Telegram sin QA y sin ruta `REELS`.

## voiceover_policy

| Caso | Politica |
|---|---|
| Reel institucional/emocional CMP | Preferir locucion humana/neural argentina limpia, sobria, sin tono publicitario exagerado. |
| Reel educativo medico | Preferir voz del Doctor o locucion sobria con copy prudente; evitar dramatizacion. |
| Material del Doctor a camara con audio no revisado | No usar audio original hasta QA completo. Puede usarse visual sin audio. |
| Reel que depende de tesis verbal | Voz en off recomendada; texto solo puede quedar frio o demasiado lento. |
| Reel de placas + b-roll | Locucion eleva calidad si el mensaje es narrativo. Musica sola puede hacerlo generico. |

Regla: la voz debe decir menos que el texto total, no repetir cada placa. La placa fija la idea; la voz le da respiracion humana.

## instagram_music_policy

- Si el Doctor va a agregar musica desde Instagram, exportar version `locutor_clean`: voz en off clara, sin musica incrustada o con cama casi inexistente.
- Ventaja: evita problemas de licencia, permite elegir audio nativo de IG y no compite con la locucion.
- Si no hay locucion, no entregar mudo salvo pedido: incluir audio ambiente seguro o dejar decision explicita `audio pendiente`.
- No mezclar musica comercial externa dentro del MP4 si se publicara con musica de Instagram.
- Mantener una version master sin musica y otra con audio seguro si el orquestador necesita comparar.

## qa_checklist_before_telegram

### Chequeos tecnicos

- MP4 vertical 9:16, 1080x1920 si es posible.
- Duracion objetivo 35-40s; maximo 45s con razon.
- Audio presente o decision explicita `locutor_clean / musica IG`.
- Sin frames negros, saltos, textos cortados o baja resolucion.
- Contact sheet de 8-12 frames, seguro y menor a 800 KB si se commitea al bridge.

### Chequeos visuales

- Minimo dos bloques visuales propios/autorizados.
- No stock, no pacientes, no HC, no estudios identificables, no pantallas con datos.
- Doctor/CMP bien encuadrado, sin recortes que perjudiquen imagen profesional.
- Texto grande, contraste suficiente, sin solapamientos.
- Cierre institucional premium, no aviso improvisado.

### Chequeos de contacto

- IG exacto: `@drcarloszanardi`.
- Telefono exacto: `2364384321`.
- Web exacta: `www.centromedicopellegrini.com.ar`.
- Contacto visible al menos 4 segundos.

### Chequeos de coherencia mensaje-imagen

- La imagen acompana la frase; no usar instrumental/cirugia si el tema es consulta general.
- No prometer resultados, cura, ausencia de riesgo o diagnostico al espectador.
- No usar imagen IA/anatomia como prueba clinica.
- Si el tema es medico, que el CTA sea prudente: consultar/evaluar, no autodiagnosticar.

### Chequeo de ruta topic REELS y recibo real

- El envio a Telegram lo hace solo Codex principal/orquestador, no Pablo.
- Debe salir por topic/front `REELS`.
- Si llegaron assets por Telegram, esperar album completo antes de responder o editar.
- Registrar en bridge: `artifact_path`, `contact_sheet`, `caption`, `qa_pass`, `telegram_topic`, `send_receipt_real`.
- Si el recibo real no existe o falla, no marcar como enviado.

## next_3_reel_concepts

### 1. Prepararse para la consulta de columna

| Campo | Contenido |
|---|---|
| Tema | Como llegar mejor preparado a una consulta por columna. |
| Mensaje central | Una consulta mejor preparada ayuda a decidir mejor. |
| Estructura 35-45s | 0-3s hook: `Si va a consultar por columna...`; 3-10s estudios previos; 10-18s desde cuando duele y hacia donde baja; 18-26s tratamientos probados; 26-34s que actividades limita; 34-40s cierre CMP. |
| Material visual necesario | Doctor a camara o V02 revisado, consultorio/pasillo propio, placas C01/C04 o equivalentes. |
| Posible voz en off | Voz sobria del Doctor o locutor argentino: "Prepare cuatro cosas..." |
| Riesgo principal de calidad | Que parezca lista administrativa sin presencia humana; resolver con Doctor/consultorio real. |

### 2. Dolor lumbar: tres senales para consultar

| Campo | Contenido |
|---|---|
| Tema | Senales de alarma de dolor lumbar redactadas con prudencia. |
| Mensaje central | El dolor lumbar es frecuente, pero algunos sintomas requieren evaluacion profesional. |
| Estructura 35-45s | 0-3s hook; 3-12s perdida de fuerza/sensibilidad; 12-21s fiebre/trauma/dolor intenso segun copy validado; 21-30s cambios esfinterianos como alerta; 30-38s cada caso requiere evaluacion; 38-45s CMP/contacto. |
| Material visual necesario | Doctor a camara o locucion, placas sobrias por cada senal, consultorio sin pacientes. |
| Posible voz en off | Locutor limpio o Doctor; tono calmo, no alarmista. |
| Riesgo principal de calidad | Sonar a triage definitivo o generar miedo; usar "consulte/evalue" y no prometer diagnostico. |

### 3. Mito: toda hernia se opera

| Campo | Contenido |
|---|---|
| Tema | Desarmar ansiedad sobre hernia de disco. |
| Mensaje central | La imagen sola no decide; se mira sintomas, examen, evolucion y respuesta al tratamiento. |
| Estructura 35-45s | 0-3s hook `No toda hernia se opera`; 3-12s la imagen importa pero no decide sola; 12-24s sintomas/examen/evolucion; 24-34s opciones dependen del caso; 34-42s cierre prudente CMP. |
| Material visual necesario | Doctor a camara, placa "mito", consultorio; opcional modelo anatomico real si existe y es correcto. |
| Posible voz en off | Ideal voz del Doctor para autoridad y matiz clinico. |
| Riesgo principal de calidad | Parecer promesa de evitar cirugia; cerrar con evaluacion individual por especialista. |

## risks_limits

- Los MP4 referidos en la Mac de trabajo no estan disponibles en esta Mac; el estandar se apoya en resultados del bridge y en el workorder del orquestador.
- El contact sheet no reemplaza ver el MP4 completo en celular.
- La locucion neural puede mejorar publicabilidad, pero debe revisarse por tono argentino, pronunciacion de CMP/Junin/Zanardi y mezcla con musica IG.
- No se debe usar material nuevo desde Photos/iCloud/Drive sin autorizacion puntual o carpeta curada.
- La decision final de envio/publicacion queda en Codex principal y el Doctor.

## recommendation

Codex principal deberia adoptar `CMP Reel Standard v1` como gate previo a cualquier envio REELS. Para el reel aprobado, conservar dos masters: `locutor_clean` sin musica incrustada para Instagram, y version con audio seguro para revision interna. Para los proximos reels, empezar por `Prepararse para la consulta de columna`, porque usa material propio simple, tiene bajo riesgo medico-legal y permite validar el nuevo estandar sin pedir biblioteca completa.

## confidence

Alta para el estandar operativo, criterios de rechazo y QA, porque derivan de gate premium, resultados previos y aprobacion reportada por el orquestador. Media para detalles creativos del ultimo MP4 aprobado hasta que Codex principal confirme frame/audio completo en la Mac de trabajo.

## evidence_paths

- `jobs/20260525T163832-reels-cmp-standard-ultimo-video-y-locucion.md`
- `docs/reels_premium_acceptance_gate.md`
- `context/fronts/reels_cmp.md`
- `context/asset_packs/20260525-dia-patria-v2/qa/contact_sheet_v4.jpg`
- `results/20260525T120325-reel-dia-patria-cmp-premium-v1.result.md`
- `results/20260525T122941-reels-dia-patria-assets-and-timeline.result.md`
- `results/20260525T124546-reels-cmp-next-editorial-options.result.md`
- `results/20260525T130220-reels-assets-library-curation-protocol.result.md`
- `results/20260525T131149-reels-render-offload-pablo-fast-node-v1.result.md`
- `results/20260525T132450-reel-dia-patria-v2-content-first-rework.result.md`
- `results/20260525T133010-reel-dia-patria-v2-render-pablo-own-assets.result.md`
- `results/20260525T133959-reel-dia-patria-v2-return-premium-gate.result.md`
