# Martell YouTube - reformas operativas para Codex/Zanardi

Fecha: 2026-05-24

## Evidencia revisada

- Inventario local: `state/youtube_transcripts/danmartell_channel_flat_20260524.jsonl` y `state/youtube_transcripts/danmartell_ai_search_flat_20260524.jsonl`.
- Subtitulos iniciales revisados: `0Tch0N5nsRU`, `BuwPnrMmhzQ`, `y5jL8KsUwaI`.
- Subtitulos ampliados descargados: `FK5UNNBPbgM`, `bkM-lYgAxh0`, `7zPQV1BSH_k`, `XRU-CjzYt_o`, `D_YzcH0VsGY`, `4JMH-4kKMC8`, `wZeOwqmSw84`, `np6CwvTYTAM`.
- Segunda lectura externa: Claude API por router y Opus explicito `claude-opus-4-1-20250805`, requestId `20260525001318`, registrado en `state/claude_consult/consult.log.jsonl`.

## Lo util de Martell para nosotros

- Prompt maestro por rol/frente, no un prompt unico para todo.
- Contexto real antes de responder: documentos, transcripciones, estado del frente y reportes ya enviados.
- Project folders: cada frente debe tener carpeta, memoria compacta, rubrica y criterio de QA.
- System prompts versionados: si una respuesta sale bien, el patron debe quedar reusable.
- Context compression: resumir y preservar lo relevante del frente, no arrastrar todo el chat.
- Taste library: ejemplos buenos/malos anotados para multimedia, copy, presentaciones y estilo CMP.
- Agentes que hacen trabajo verificable: entrada clara, salida esperada, evidencia y criterio de escalamiento.
- Ciclo de QA corto: probar, puntuar, ajustar; no esperar al reclamo humano para descubrir drift.

## Reformas aplicadas

- Topics quedan con guardrail duro a `gpt-5.3-codex/medium` salvo pedido explicito de 5.5 o riesgo.
- Canal principal/directo conserva `gpt-5.5/high` como orquestador con contexto global.
- `scripts/codex_telegram_direct.py` ahora registra `model_policy_override`, `channel_kind`, `policy_expected_model`, `policy_applied_model` y `policy_mismatch`.
- Se agrego memoria compacta por topic en `state/codex-telegram-direct/topic_memory/<ROUTE>.json`.
- El prompt preflight registra hash y largo del prompt para detectar drift.
- Los errores desde Telegram pasan a formato operativo: Frente, Estado, Evidencia, Proxima accion unica.
- `scripts/send_codex_topic_message.py` sanea GENERAL para no reutilizar threads muertos.
- Se agrego presupuesto de contexto por topic en `config/codex_topic_context_budgets.json`.
- Se agrego taste library CMP en `reels-studio/taste_library_cmp_v1.json`.

## Reformas siguientes recomendadas

- Response scoring post-send con 5.3: completitud, tono y adherencia al topic; score bajo va a postmortem, no bloquea envio.
- Prompt diffing con baseline aprobado por ruta: si el prompt cambia demasiado, marcar `prompt_drift_alert`.
- Fallback explicito: si 5.5 falla, degradar a 5.3 con marca `degraded_mode` antes de devolver error final.
- Cache simple para preguntas repetidas de bajo riesgo, con TTL corto y sin usarla para clinica, mails, precios o informacion cambiante.
- Rate limit por topic/usuario para evitar loops o gasto accidental.
- Rubricas especificas por frente: CLINICA, TESIS, INMUEBLES, INVERSIONES, MAIL y CONTADOR.
- Background jobs para toda tarea que huela a video/audio/edicion larga; Telegram no debe esperar 900 segundos.
- Biblioteca de ejemplos aprobados/no aprobados para reels y presentaciones, con version semantica.

## Gemini

Veredicto actual: no comprar Ultra de entrada. Google anuncio en 2026 un AI Ultra de USD 100/mes y bajo el Ultra superior de USD 250 a USD 200/mes; tiene valor si vamos a usar video generativo, Flow/Veo, NotebookLM avanzado o agente multimodal. Para texto, codigo y orquestacion, Codex + subagentes 5.3 + Opus sidecar ya cubren mejor el trabajo.

Recomendacion: probar primero Google AI Pro/Advanced si esta disponible en la cuenta y region. Escalar a Ultra solo si en 2-4 semanas lo usamos para videos/reels/presentaciones o research multimodal de forma real.

## No adoptar

- Tono de hype de negocio.
- "Un agente para todo".
- Tool lists sin prueba local.
- Mas contexto sin compresion.
- Automatizar decisiones clinicas o medico-legales sin gate canonico.
