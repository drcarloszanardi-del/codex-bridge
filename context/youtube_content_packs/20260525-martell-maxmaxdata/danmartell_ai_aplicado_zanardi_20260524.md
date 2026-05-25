# Informe Dan Martell AI aplicado a nuestro sistema

Fecha: 2026-05-24

## Alcance real

Revisé el perfil público de Instagram de `@danmartell` a través de Chrome y mirrors públicos, y crucé ese material con sus páginas/transcripciones públicas sobre IA. No afirmo haber transcripto manualmente las 3.151 publicaciones históricas del perfil, porque Instagram no expone de manera estable todo el archivo completo. Sí cubrí el núcleo repetido de su contenido actual sobre IA: AI Company Operating System, master prompts, agentes, asistentes, automatización, contenido, ventas, decisiones y herramientas.

## Tesis central

Lo más útil para nosotros no es copiar herramientas aisladas. La idea fuerte de Martell es pasar de "usar IA para tareas" a "dirigir un sistema operativo de IA". Eso encaja muy bien con lo que venimos armando: Codex como orquestador, subagentes baratos para barridos, Telegram por topics, app médico-legal con rutas canónicas, tesis, inmobiliaria/inversiones, ObraCash, reels y presentaciones.

## Qué deberíamos adoptar

1. Master Prompt / Digital Brain de Zanardi

Crear un documento vivo con tus criterios, tono, prioridades, restricciones clínicas, estética CMP, forma de decidir, frentes activos y reglas de seguridad. Esto ya existe parcialmente en memorias y `AGENTS.md`, pero debería convertirse en un "cerebro operativo" explícito y versionado.

Aplicación:
- Codex Directo tendría respuestas más parecidas a este chat.
- Los subagentes no arrancarían a ciegas.
- Reels y presentaciones conservarían tu estilo.
- La app médico-legal mantendría criterios quirúrgicos y legales sin depender de memoria difusa.

2. RCCF para todas las órdenes largas

Martell insiste en estructurar prompts por rol, contexto, comando y formato. Nosotros ya lo hacemos de manera informal. Hay que formalizarlo en Telegram:

- Rol: qué agente actúa.
- Contexto: frente, archivos, antecedentes, restricciones.
- Comando: qué hay que producir.
- Formato: texto, informe, video, PPT, correo, app, Telegram, etc.

Esto reduciría errores como mezclar instrumental con PC, reels con una sola foto, o mandar viajes al topic incorrecto.

3. 10-80-10 para nuestro flujo

Regla aplicable:
- Vos das el primer 10%: intención, criterio experto, límites.
- Los agentes hacen el 80%: investigación, borrador, edición, QA, comparación.
- Vos/Codex 5.5 hacemos el último 10%: juicio fino, aprobación, tono, seguridad.

Esto es ideal para:
- Consentimientos, partes e historias clínicas.
- Reels CMP.
- Presentaciones PowerPoint.
- Búsqueda inmobiliaria/instrumental.
- Tesis.

4. AI Camcorder Method

Martell propone grabar una tarea y convertirla en SOP/checklist. Para nosotros es oro:

- Si me mandás un audio explicando cómo querés un parte quirúrgico, lo convierto en regla canónica.
- Si corregís un reel, esa corrección entra en checklist para el próximo.
- Si cargás gastos en ObraCash, podemos documentar el flujo y blindarlo.
- Si explicás cómo evaluás una propiedad/instrumental, eso se vuelve rúbrica.

5. Agentes por función, no por ocurrencia

Martell separa agentes: assistant, workflow, amplifier, money. Nuestro equivalente:

- Assistant Agent: Telegram, mail, calendario, viajes, recordatorios, archivos.
- Workflow Agent: app médico-legal, ObraCash, backups, QA, SOPs.
- Amplifier Agent: reels, historias IG, presentaciones, copy CMP, repurpose de videos.
- Money/Opportunity Agent: inmobiliaria, instrumental, PC, costos, margen, ObraCash.
- Corpus Agent: jurisprudencia, normativa, tesis, bibliografía.

6. Amplifier Agent para contenido

Para reels y PowerPoint:

- Un video largo se transforma en: reel corto, carrusel, historia, copy, mail, presentación, resumen para pacientes.
- Cada pieza debe pasar por: coherencia texto-imagen, fuente visual válida, estética CMP, CTA sutil, QA de contacto.
- No repetir el error de "imagen linda pero no representativa". El contenido manda, el diseño acompaña.

7. Data moat médico-legal

Martell habla de que la ventaja ya no es solo el software, sino los datos/contexto. Para nosotros:

- Corpus de jurisprudencia oficial neuro/columna.
- Normativa argentina.
- Correcciones clínicas tuyas.
- Modelos reales de historia/parte/consentimiento.
- Errores detectados por QA.

Ese corpus tiene que alimentar la app. Es la ventaja frente a cualquier app genérica.

8. Medir éxito por métrica

No basta con "el agente corrió". Cada frente necesita métrica:

- Telegram: mensaje recibido, topic correcto, estado trabajando, entrega con message_id.
- Reels: coherencia visual, duración, CTA, teléfono correcto, calidad final.
- App médica: cero contradicciones clínicas, ruta canónica, revisión humana obligatoria.
- Inmobiliaria: oportunidades dentro del radio, casas/PH, refacción/desarrollo, no falsos Junín.
- Instrumental: precio compra, costo puesto, comparación ML, reputación proveedor, margen real.
- Tesis: hallazgo bibliográfico/metodológico accionable, sin tocar borrador sin motivo.

## Qué no deberíamos adoptar

- No subir datos clínicos sensibles a herramientas externas sin control.
- No automatizar respuestas médicas o legales finales.
- No perseguir cada herramienta nueva. Elegir pocas y medir ROI.
- No reemplazar tu juicio experto con agentes.
- No dejar que Telegram sea solo "chat"; tiene que ser sistema de trabajo con estados, topics y recibos.

## Prioridades concretas

1. Crear `Zanardi Master Prompt / Digital Brain` local y versionado.
2. Convertir Telegram en sistema 10-80-10: acuse, estado trabajando, entrega, recibo.
3. Hacer una rúbrica fija de reels CMP: guion, imagen representativa, transiciones, cierre/contacto, QA.
4. Hacer rúbrica fija para presentaciones: objetivo, audiencia, narrativa, slides, visuales, speaker notes, fuentes.
5. Integrar el corpus médico-legal como "data moat" de la app, no como carpeta separada.
6. Pasar tareas repetibles a SOPs con el método camcorder.
7. Mantener subagentes 5.3 para búsqueda/lectura y reservar 5.5 para criterio fino.

## Lectura final

Lo que Martell propone valida bastante nuestro camino: no es "comprar otra app", es construir una arquitectura propia donde Codex orquesta, los agentes ejecutan, y tu criterio médico/empresarial define el estándar. Lo que más nos falta no es potencia: es encapsular mejor el contexto, las rúbricas y los estados para que Telegram se comporte como este chat.

## Fuentes revisadas

- Perfil público/mirror de Instagram `@danmartell`: https://www.pixnoy.com/profile/danmartell/
- Categoría AI en DanMartell.com: https://www.danmartell.com/category/ai/
- Get Ahead Using AI in Business: https://www.danmartell.com/get-ahead-with-ai/
- How to Use AI Systems to Actually Achieve Your Goals: https://www.danmartell.com/how-to-use-ai-systems-to-actually-achieve-your-goals/
- 23 ChatGPT Techniques: https://www.danmartell.com/how-to-use-ai-to-work-smarter-23-chatgpt-techniques/
- How to Get So Many Customers with AI: https://www.danmartell.com/how-to-get-so-many-customers-with-ai-it-feels-illegal/
- AI Automation Without Code: https://www.danmartell.com/how-to-use-ai-automation-to-make-a-million-without-writing-code/
- AI Is About to Change Business Forever: https://www.danmartell.com/ai-is-about-to-change-business-forever/
- Agentic AI Tools: https://www.danmartell.com/agentic-ai-tools/
- The Assistant is Dead. Long Live The AI Architect: https://www.danmartell.com/the-assistant-is-dead-long-live-the-ai-architect/
