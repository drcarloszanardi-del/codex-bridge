# Frente Telegram / Codex Directo

Actualizado: 2026-05-25.

## Estado canonico

- Entrada principal: `/Users/jarvis/.openclaw/workspace/scripts/codex_telegram_direct.py`.
- Canal principal debe comportarse como Codex principal con contexto global.
- Topics deben actuar como bandejas de frente con modelo barato por defecto.
- Entrega confirmada exige `ok=true` y `message_id` real; cola/outbox no equivale a enviado.

## Reformas integradas desde Pablo

- Gate de canal por `stdin`/`text-file` para evitar payloads largos por argv.
- Bloqueo de trazas/diffs tecnicos extensos antes de Telegram.
- Buffer de texto + fotos/videos/adjuntos cercanos para no ejecutar con una sola imagen si el resto llega despues.
- Registro local de eventos, jobs, runs, raw events e idempotencia.
- Brief operativo antes de invocar Codex: ruta, razon, canal, modelo, adjuntos, permisos y salida esperada.
- ContextBinder activo: se adjunta este contexto canonico de frente antes de ejecutar Codex.
- ResetScope activo: `/reset_scope` archiva y limpia contexto local del frente cuando el hilo queda contaminado.

## Deuda activa

- Dashboard simple sobre `router/jobs/runs`.
- ResultContract para respuestas importantes.
- ArtifactDraft separado para trabajos creativos/largos.
