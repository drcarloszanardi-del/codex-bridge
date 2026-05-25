# Auditoria de contenido Maxmaxdata para CMP / Codex

Fecha: 2026-05-25

Fuente revisada: canal YouTube `@maxmaxdata`, 35 videos publicos actuales.

Evidencia local:
- Inventario plano: `/Users/jarvis/.openclaw/workspace/reels-studio/research/maxmaxdata_2026-05-25/content_audit/youtube_current_flat_80.jsonl`
- Metadata completa: `/Users/jarvis/.openclaw/workspace/reels-studio/research/maxmaxdata_2026-05-25/content_audit/youtube_current_full_35.jsonl`
- Subtitulos descargados: `/Users/jarvis/.openclaw/workspace/reels-studio/research/maxmaxdata_2026-05-25/content_audit/subtitles/`

## Veredicto corregido

El valor no esta en su estilo de hablar ni en la gestualidad. El valor esta en cuatro lineas de contenido:

1. Agentes de IA que actuan sobre interfaces reales.
2. Uso de IA generativa como laboratorio rapido de prueba visual.
3. Criterio de reset/contexto para evitar que una IA quede "viciada".
4. Seguridad, privacidad y limites humanos como parte del flujo, no como agregado posterior.

Para nuestro sistema sirve mas para Codex/Telegram/reels/CMP que para copiar una pieza puntual.

## Lo que conviene adoptar

### 1. Agentes que navegan interfaces

Video base: `HACK: Asi actua un agente de IA`

Contenido util:
- Define al agente como sistema que percibe entorno y actua sobre el.
- Muestra un agente buscando un PC, comparando webs y actuando como navegador operativo.
- Lo compara con Selenium/autotouch, pero con interpretacion visual y objetivos.

Aplicacion nuestra:
- Consolidar en Codex Directo una regla: tareas web repetibles deben transformarse en "agente con objetivo + evidencia + limites".
- Usarlo para radar de propiedades, instrumental, proveedores, precios, busquedas de papers y QA de publicaciones.
- No aceptar "la IA lo hace" sin captura, fuente, ruta y decision verificable.

### 2. Sora / video generativo como storyboard, no como verdad

Videos base:
- `SORA de Open AI, jugando un poco...`
- `SORA de Openai | IA de texto e imagen a video`

Contenido util:
- La idea fuerte es editar video desde referencia: remix, recut, extender antes/despues, ordenar secuencias por frames.
- Sirve para prototipar antes de producir.

Aplicacion nuestra:
- Para CMP: usar IA video como storyboard o b-roll no clinico.
- No usarla para simular acto medico real, resultado quirurgico o anatomia dudosa.
- Flujo recomendado: guion medico -> storyboard IA -> QA anatomico -> produccion final.

### 3. Canvas / separacion conversacion-resultado

Video base: `Review GPT 4o with Canvas`

Contenido util:
- Separar el chat de trabajo del resultado final.
- Editar longitud, nivel de lectura, revision y sugerencias sin mezclar todo en una conversacion caotica.

Aplicacion nuestra:
- Es exactamente lo que necesitamos en Telegram: separar orden del Doctor, razonamiento interno, artefacto final y entrega con recibo.
- Para reels: separar guion, storyboard, copy, caption y checklist.
- Para clinica: separar datos del caso, documento, QA y envio.

### 4. Reset de contexto cuando la IA queda contaminada

Video base: `Tu IA se queda viciada? Aprende a resetearla`

Contenido util:
- Cuando un modelo se fija en una premisa falsa, insiste aunque se lo corrija.
- El remedio no es discutir indefinidamente: resetear contexto, explicitar nueva premisa y reencuadrar la tarea.

Aplicacion nuestra:
- Regla operativa para Codex Directo: si el Doctor corrige "no hablo de eso", no insistir sobre el marco anterior.
- Crear un mini-protocolo: `correccion recibida -> antecedente real -> nuevo alcance -> evidencia -> accion`.
- Este caso actual confirma que esa regla debe quedar aplicada a YouTube/reels.

### 5. IA generativa con criterio humano

Videos base:
- `Inteligencia Artificial Generativa: Innovacion sin Deshumanizacion ni Desinformacion`
- Entrevistas en EITB/Onda Vasca/Radio Marca.

Contenido util:
- Desmitifica: IA no reemplaza por si sola criterio humano.
- Enfatiza convivencia, cambio cultural, productividad y supervision.
- Plantea riesgos de desinformacion y necesidad de criterio.

Aplicacion nuestra:
- Mensaje publico CMP: "tecnologia con criterio medico".
- Mensaje interno Codex: modelos y automatizaciones ayudan, pero Codex debe verificar y el Doctor aprueba lo publicable.

### 6. Privacidad y ciberseguridad

Video base: `SECUESTROS de DATOS...`

Contenido util:
- Riesgo real de ransomware, robo de informacion, exposicion infantil/datos y falsa sensacion de digitalizacion.
- Digitalizar sin seguridad aumenta superficie de riesgo.

Aplicacion nuestra:
- Para CMP/reels: no subir pacientes, pantallas clinicas ni documentos identificables a herramientas externas.
- Para Telegram: no imprimir tokens, rutas sensibles innecesarias ni datos clinicos.
- Para IA visual: usar material neutro o anonimizado.

### 7. Pruebas comparativas de modelos

Videos base:
- `DeepSeek, es mejor que ChatGPT?`
- `Puede la IA hacerlo todo?`
- `Imagen 3 de Gemini`

Contenido util:
- No creer marketing: probar con tareas concretas.
- Modelos fallan en restricciones simples, imagenes, derechos, razonamiento o politicas.
- Lo importante es testear contra casos reales.

Aplicacion nuestra:
- Mantener matriz local de pruebas: Codex, Claude, Gemini/Nano Banana, Sora, Ollama.
- Elegir herramienta por tarea, no por moda.
- En clinica, ningun modelo chico/local es autoridad final.

## Matriz de los 35 videos

| # | Video | Contenido util | Uso para nosotros |
|---|---|---|---|
| 1 | Maxmaxdata en Radio Marca | Divulgacion general IA/salud/cuidado | Poco directo; tomar solo tono de IA aplicada a vida real |
| 2 | Localizacion con IA Tele 5 | Inferencia visual desde imagen/video | QA privacidad: una imagen revela mas de lo que parece |
| 3 | Agente de IA controla webs | Agentes operativos sobre navegador | Muy util para Codex Directo y tareas web verificables |
| 4 | Empiezo el ano 7 | Marca personal, trayectoria, consistencia | Util para estrategia de constancia, no tecnico |
| 5 | DeepSeek vs ChatGPT | Comparacion practica y limites | Usar tests propios antes de adoptar modelos |
| 6 | EITB descifrando IA | Divulgacion y cambio cultural | Util para posicion CMP sobrio sobre IA |
| 7 | 2024 redes 0 a 200k | Crecimiento por consistencia | Aplicable a calendario de reels, no copiar estilo |
| 8 | Sora jugando | Video IA como prueba creativa | Storyboard/b-roll, no acto medico real |
| 9 | Sora texto/imagen a video | Remix, recut, frames, secuencias | Pipeline de storyboard visual para reels |
| 10 | Test de Turing | Distinguir IA/persona, interaccion | Criterio anti-engano y transparencia |
| 11 | IA generativa sin deshumanizar | Charla larga de criterio humano | Base conceptual para "tecnologia con criterio medico" |
| 12 | Onda Vasca | Resumen de charla y reflexiones | Refuerza narrativa publica prudente |
| 13 | Voz avanzada freestyle | Voz/IA en interaccion natural | Uso limitado; no clonar ni simular sin QA/autorizacion |
| 14 | Gemini Imagen 3 | Restricciones de generacion de personas | Testear limites antes de prometer imagenes |
| 15 | Mejorar imagenes IA | Upscale/calidad visual | Util para assets no sensibles y portadas |
| 16 | GPT Canvas | Separar conversacion y resultado | Muy util para estructura Telegram/artefactos |
| 17 | Ahorro de tiempo IA | Automatizacion simple | Util como criterio: ahorrar tareas repetibles |
| 18 | Preparar viaje con IA | Planificacion asistida | Aplicable a viajes/logistica, no prioritario CMP |
| 19 | Reset IA viciada | Contexto contaminado y reset | Muy util; aplicar cuando el Doctor corrige alcance |
| 20 | IA no puede todo | Fallas en tareas simples | Mantener escepticismo y QA |
| 21 | Imagenes maxima calidad | Prompt/calidad/resolucion | Util para imagenes CMP no clinicas |
| 22 | Bits a beats | IA/creatividad/cultura | Poco prioritario; aporta cruce creativo |
| 23 | Tests psicotecnicos | Entrenamiento cognitivo con IA | Poco aplicable |
| 24 | IA en euskera | Idioma/localizacion | Aplicable a tono regional, lenguaje paciente |
| 25 | Freestyle IA | Creatividad con voz/texto | Bajo valor CMP |
| 26 | Secuestros de datos | Ciberseguridad/ransomware | Muy util para politica de privacidad y datos |
| 27 | 5 aniversario | Marca/empresa | Bajo valor tecnico |
| 28 | Redneck Dashboard | Data storytelling | Util para dashboards/reportes claros |
| 29 | Empresa Big Data Bilbao | Servicios/ciclo del dato | Aplicable a enfoque de datos del sistema |
| 30 | Xmas 2020 | Pieza creativa | Sin valor operativo |
| 31 | Sports trends Covid | Google Trends / visualizacion | Util para radar de tendencias |
| 32 | Infografia Covid Spain | Infografia animada | Util como referencia de dataviz sobria |
| 33 | First birthday | Marca | Bajo valor |
| 34 | Comunicacion de insights | Enseñar datos con claridad | Util para reportes ejecutivos |
| 35 | Xmas 2019 | PowerPoint avanzado | Util menor: piezas simples bien animadas |

## Recomendacion unica

Incorporar de Maxmaxdata una capa nueva para nuestro sistema:

`Radar de contenido IA -> extraccion de idea -> prueba local controlada -> QA medico/privacidad -> aplicacion a Codex/CMP`

La primera modificacion concreta debe ser esta:

Cuando llegue un video/canal de YouTube, Codex no debe contestar "me gusta el formato". Debe armar una matriz con:

1. Que dice.
2. Que herramienta o metodo propone.
3. Que parte sirve para Codex/Telegram/CMP.
4. Que parte se descarta.
5. Que accion concreta queda incorporada.

