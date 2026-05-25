# Dan Martell / YouTube - reformas aplicadas a Codex Directo

Fecha: 2026-05-24

## Alcance real

Se reviso el canal de YouTube de Dan Martell con inventario publico y subtitulos disponibles para extraer ideas aplicables al sistema de trabajo del Dr. Zanardi. No se tomo como guia el tono comercial ni la promesa de negocio rapido; se tomo la logica operativa: prompts maestros, sistemas repetibles, contexto persistente, salida accionable y agentes por funcion.

Evidencia local:

- Inventario canal: `/Users/jarvis/.openclaw/workspace/state/youtube_transcripts/danmartell_channel_flat_20260524.jsonl`
- Inventario busqueda AI: `/Users/jarvis/.openclaw/workspace/state/youtube_transcripts/danmartell_ai_search_flat_20260524.jsonl`
- Subtitulos revisados: `0Tch0N5nsRU`, `BuwPnrMmhzQ`, `y5jL8KsUwaI`

## Ideas utiles incorporadas

- Prompt maestro: cada frente necesita contexto fijo, objetivo, restricciones, formato de salida y criterio de calidad.
- System prompts: las tareas repetidas no deben depender de memoria humana ni de un chat largo; deben vivir en archivos durables.
- Agentes como sistemas: no alcanza con pedir "busca" o "hace"; cada agente necesita entrada, salida esperada, evidencia minima y regla de escalamiento.
- Contexto antes de ejecucion: referencias como "eso", "lo anterior" o "esas reformas" deben resolverse contra reportes enviados y artefactos locales antes de actuar.
- Menos ruido: las automatizaciones baratas deben reportar solo novedades accionables, no actividad por actividad.

## Cambios aplicados

- Canal principal/directo: queda como inbox global de maxima continuidad con `gpt-5.5` y razonamiento alto.
- Topics: quedan como bandejas operativas por frente con contexto propio y modelo barato por defecto, `gpt-5.3-codex` low/medium.
- Si el Dr. escribe en el principal sobre un frente, Codex razona con 5.5 y publica el resultado en el topic correspondiente.
- Si el Dr. escribe dentro de un topic, Codex responde ahi con contexto del topic y baja a 5.3 salvo pedido explicito de 5.5 o riesgo claro.
- Los reportes enviados con `scripts/send_codex_topic_message.py` ahora se agregan tambien al contexto de Codex Directo, para que una orden posterior pueda referirse a "eso" sin perder el antecedente.
- `scripts/codex_telegram_direct.py` agrega un contexto general liviano aun cuando el mensaje venga de un topic.
- Se fijo una regla especifica por el error observado: Martell/YouTube/reformas globales no debe derivarse a SteelFrame/ConsulSteel salvo que el Dr. nombre explicitamente obra, SteelFrame, ConsulSteel, QCheck, planos o Frame Studio.

## Lo que no se adopta

- No adoptar hooks tipo "hacete rico con IA" como criterio de trabajo.
- No tomar listas de herramientas como verdad tecnica sin prueba local.
- No convertir tareas clinicas o medico-legales en automatizaciones autonomas sin gate canonico y revision fina.

## Pendiente razonable

Convertir esta logica en rubricas por frente: reels, tesis, clinica, inmobiliaria, inversiones, mail y contador. La primera version operativa ya queda iniciada en `docs/rubricas/`.
