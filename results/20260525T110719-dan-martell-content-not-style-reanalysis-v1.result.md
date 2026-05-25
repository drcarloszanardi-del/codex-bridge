---
job_id: 20260525T110719-dan-martell-content-not-style-reanalysis-v1
worker: personal-xh
status: completed
completed_at: 2026-05-25T11:20:19-03:00
front: CODEX-OPS
---

# Result

## summary

Analisis de contenido, no de estilo. Los transcripts locales mencionados pertenecen a la Mac de trabajo (`/Users/jarvis/...`) y no estan dentro de este repo en la Mac personal. No cierro con bloqueo: uso fallback con fuentes publicas y propongo el paquete minimo exacto para una segunda pasada literal sobre los transcripts.

La idea central aplicable de Dan Martell al sistema del Doctor: comprar tiempo no es "hacer mas con IA", sino sacar al decisor de tareas de bajo apalancamiento mediante playbooks, agentes, contexto portable, delegacion 10-80-10 y revision final fuerte.

## findings con evidencia

- Los paths locales del job no existen en esta Mac/repo; son paths de work-mac.
- El puente Git ya tiene arquitectura compatible: jobs, results, claims, status, contextos y proposals de router Telegram.
- Fuentes publicas usadas como fallback:
  - https://www.danmartell.com/buy-back-your-time-boost-profits/
  - https://www.danmartell.com/aichallenge/
  - https://www.danmartell.com/the-assistant-is-dead-long-live-the-ai-architect/
  - https://www.danmartell.com/5-ways-to-make-money-with-ai-starting-today/
  - https://www.danmartell.com/ai-businesses-will-make-you-1m-with-zero-employees/

## paquete minimo exacto pedido al orquestador

Para analisis literal de videos/transcripts, subir al bridge un paquete sanitizado:

```text
context/dan_martell/
  manifest.json
  danmartell_ai_search_flat_20260524.jsonl
  danmartell_agent_search_flat_20260524.jsonl
  danmartell_channel_flat_20260524.jsonl
  expanded/
    *.vtt
```

`manifest.json` minimo:

```json
{
  "source": "work-mac youtube_transcripts",
  "created_at": "2026-05-25T11:20:19-03:00",
  "files": [
    {"path": "expanded/video.vtt", "title": "", "url": "", "published_at": ""}
  ],
  "redactions": ["credentials", "private notes", "cookies"]
}
```

## top ideas accionables

### 1. Buy Back Time aplicado a Codex

No medir el sistema por "cuantas tareas hace Codex", sino por cuantas decisiones del Doctor deja preparadas. Cada frente debe transformar pedidos sueltos en decisiones listas: resumen, opciones, riesgos, recomendacion y siguiente accion.

Aplicacion: todo job debe terminar en `decision_suggested`, `blocked_reason` o `needs_human_authorization`, no en informe descriptivo.

### 2. Delegacion 10-80-10

El humano/orquestador aporta el primer 10%: objetivo, criterio, restricciones y definicion de terminado. Workers hacen el 80%. Codex principal hace el ultimo 10%: decision, integracion y control de riesgo.

Aplicacion:

- Doctor: objetivo y correccion de rumbo.
- Codex principal: brief, routing, approval.
- Pablo/personal-xh: razonamiento profundo y propuestas.
- 5.3/subagentes: extraccion, clasificacion, OCR, snippets, QA barato.

### 3. AI Architect / Fleet Commander

Martell empuja el rol de asistente hacia arquitecto de sistemas. En este ecosistema, eso significa que el Codex principal no debe actuar como operador de cada tarea, sino como comandante de cola: divide, asigna, controla estado y decide.

Aplicacion: Telegram Directo debe crear jobs; no debe intentar resolver tareas largas dentro del mismo turno.

### 4. Digital Brain portable, no historial crudo

La idea util no es subir todo Gmail/Drive/Telegram a un modelo, sino construir una memoria portable, resumida, versionada y segura.

Aplicacion:

```text
context/global.md
context/fronts/clinica.md
context/fronts/inversiones.md
context/fronts/reels_cmp.md
context/topics/<topic_id>.md
decisions/*.md
```

No usar historial completo de Telegram como memoria.

### 5. EHR / costo de atencion

El Effective Hourly Rate se traduce aca como "costo de atencion del modelo". 5.5 XHT no debe hacer parsing barato. Debe reservarse para ambiguedad, estrategia, seguridad, medico-legal y decisiones con alto costo de error.

Aplicacion: 5.3 hace intake, dedupe, resumen, tests, comparables; Pablo hace segunda mirada y sintesis; principal decide.

### 6. Agentes despues de playbooks

No crear agente para caos. Primero SOP: input, output, criterios de aceptacion, errores, escalamiento. Despues agente.

Aplicacion: cada frente necesita `RUNBOOK.md`:

- Clinica: route guard + fixtures + gates.
- Telegram: event/router/job/run.
- Inversiones: anti informe vacio.
- Reels: album completo + storyboard + QA medico.

### 7. Reverse prompting

Antes de pedir una tarea larga, hacer que el sistema pregunte que input falta o genere el brief. En Telegram esto evita que el Doctor tenga que escribir perfecto.

Aplicacion: `brief_compiler` barato:

```text
mensaje crudo -> objetivo -> frente -> datos faltantes -> riesgo -> job listo
```

### 8. Tareas largas no deben bloquear respuestas nuevas

Martell insiste en sistemas que compran tiempo permanentemente. Si Telegram queda ocupado esperando una tarea larga, no compra tiempo: lo secuestra.

Aplicacion: al recibir tarea larga, Telegram responde una sola vez con ACK y job id; el trabajo corre asincronico en Git/runs; nuevos mensajes entran a cola sin esperar.

### 9. Outcome over instructions

La delegacion madura no pide pasos, pide resultados verificables. Cada job debe especificar output final y tests.

Aplicacion: reemplazar "analiza esto" por "entregar tabla top 10, comparables, riesgos, accion hoy, fuentes".

### 10. Hacer productos internos

Martell orienta AI hacia sistemas repetibles. Para el Doctor, cada frente deberia convertirse en producto interno, no chat aislado:

- Radar de inversiones.
- Redactor medico-legal con gates.
- Productor CMP premium.
- Asistente tesis con corpus.
- Router Telegram Directo.

## cambios concretos para nuestro flujo

1. `telegram_event -> job` obligatorio antes de llamar a modelo pesado.
2. `brief_compiler_5_3` que convierta Telegram en workorder limpio.
3. `context_compiler` por frente, no historial global.
4. `run_store` con `queued/running/blocked/done`.
5. ACK no ruidoso: recibido, bloqueado, necesita aprobacion, terminado.
6. Workers baratos para intake y QA.
7. Pablo solo para segunda pasada, fallos de razonamiento y sintesis ejecutiva.
8. Codex principal solo para decidir, integrar y hablar al Doctor.
9. Dashboard local para ver cola y bloqueos.
10. Gate anti informe vacio en radares y reviews.

## que automatizar con 5.3 bajo costo

- Clasificacion de Telegram por frente/topic/intencion.
- Deteccion de album/media incompleto.
- OCR/transcripcion preliminar.
- Dedupe/idempotencia.
- Resumen de transcripts.
- Extraccion de entidades: precios, direcciones, links, modelos, riesgos.
- Validacion de formato de results.
- Secret scan y policy scan.
- Watchlists y comparables.
- Preparacion de briefs para Pablo.

## que reservar a Pablo 5.5 XHT

- Segunda mirada de estrategia.
- Sintesis de muchos resultados.
- Diagnostico de fallos operativos.
- Tareas con fuentes incompletas y necesidad de inferencia prudente.
- Riesgo medico-legal.
- Arquitectura de agentes, gates y workflows.
- Priorizacion de oportunidades de inversion.
- Reanalisis de contenido externo para mejorar el sistema.

## que reservar a Codex principal

- Decision final y autorizaciones.
- Comunicacion con el Doctor.
- Integracion real en work-mac.
- Acceso a rutas locales sensibles si corresponde.
- Telegram/Gmail/Drive/Calendar si el Doctor lo aprueba.
- Cambios sobre app real clinica.
- Publicacion, compra, contacto o acciones irreversibles.

## reformas para que Telegram se parezca mas a este chat

1. Contexto estructurado por frente antes de responder.
2. Job queue asincronica para tareas largas.
3. Mensaje entrante tratado como evento no confiable, no como prompt de sistema.
4. Topics como routing hints, no como memoria.
5. Resultados escritos a archivos y luego resumidos al Doctor.
6. Capacidad de decir "estoy trabajando en job X" sin perder mensajes nuevos.
7. Album/media buffering antes de llamar al modelo.

## primeras 5 reformas para implementar

1. `brief_compiler_5_3` para Telegram Directo.
2. `media_album_buffer` con ventana de silencio antes de responder.
3. `context/fronts/*.md` actualizado por decisiones aprobadas.
4. `validate_result_contract.py` para impedir resultados vacios.
5. `model_routing_policy.yaml` con reglas 5.3 / Pablo / principal.

## riesgos/limites

- Sin los transcripts locales, este analisis es una sintesis de contenido publico y no una auditoria literal de los archivos descargados.
- Extraer "digital brain" desde Gmail/Drive/Telegram puede exponer datos sensibles; debe hacerse con redaccion y autorizacion.
- Agentes sin gates aumentan velocidad del error.
- Telegram no debe convertirse en memoria canonica.
- Modelos baratos deben tener salida verificable y no autoridad final.

## recommendation

Implementar primero el flujo 10-80-10:

```text
Doctor/orquestador define objetivo -> 5.3 compila brief -> Pablo analiza/profundiza -> Codex principal decide e integra
```

Esto alinea mejor con el contenido util de Martell que intentar que un solo chat "haga todo".

## confidence

Medium. Alta confianza en las reformas porque encajan con el sistema actual; media sobre referencias especificas a videos porque no estan disponibles los transcripts locales de work-mac.

## evidence_paths

- `jobs/20260525T110719-dan-martell-content-not-style-reanalysis-v1.md`
- `results/20260525T012657-auditoria-telegram-contexto-global.result.md`
- `results/20260525T015132-telegram-context-router-especificacion-implementable.result.md`
- `results/20260525T084316-telegram-codex-direct-router-observability-mvp-v2.result.md`
- `decisions/telegram_router_patch_proposal_v1.md`
