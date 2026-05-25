---
id: 20260525T013126-arquitectura-24-7-equipo-autonomo-codex
job_id: 20260525T013126-arquitectura-24-7-equipo-autonomo-codex
created_at: 2026-05-25T01:36:58-03:00
created_by: personal-xh
status: completed
no_external_actions: true
no_secrets: true
---

# arquitectura 24 7 equipo autonomo codex result

## summary

La arquitectura recomendada es hub-and-spoke: el Codex orquestador en work-mac conserva autoridad, contexto global y acciones externas; workers especializados ejecutan analisis, QA, propuestas y tareas empaquetadas. `personal-xh` debe recibir solo contexto curado por `codex-bridge`.

## mapa de frentes

| Frente | Dueño primario | Delegable a personal-xh | Frecuencia |
|---|---|---|---|
| Telegram/contexto | work-mac | auditoria de arquitectura, prompts, estados | diario o por incidentes |
| Clinica medico-legal | work-mac + Dr. Zanardi | matrices QA, gates, pruebas sinteticas | alta prioridad |
| Tesis | work-mac | estructura, revision, argumentos, bibliografia no sensible | por lote |
| Inmobiliaria | work-mac | analisis de documentos no sensibles, checklists | por evento |
| Inversiones/instrumental | work-mac | escenarios, comparativas, riesgos | por decision |
| Reels/CMP | work-mac | guiones, QA de datos publicos, tono | semanal |
| Presentaciones | work-mac | outline, narrativa, revision | por entrega |
| ObraCash/backups | work-mac | auditoria de scripts y runbooks | diario/semanal |
| Mail triage | work-mac | no delegar contenido sensible; solo reglas y plantillas | restringido |
| Bridge Git | ambos | personal-xh implementa mejoras y resultados | continuo |

## que corre local en work-mac

- Telegram/Gmail/Drive/Calendar y cualquier canal externo.
- Contexto global, decisiones finales y aprobaciones.
- Acceso a repos/proyectos sensibles.
- Empaquetado de workorders para workers.
- Integracion de resultados y reporte al Dr. Zanardi.

## que delegar a personal-xh

- Segunda lectura de decisiones.
- Auditoria de arquitectura.
- Diseno de matrices QA/gates.
- Implementacion acotada dentro de `codex-bridge`.
- Revision de prompts, protocolos y runbooks.
- Analisis de contexto no sensible provisto en jobs.

## artefactos canonicos

- `jobs/*.md`: input empaquetado y no sensible.
- `results/*.result.md`: salida completa del worker.
- `status/*.json`: heartbeat operativo.
- `decisions/*.md`: decisiones aprobadas por orquestador.
- `protocol.md`: reglas durables.

## reportes

- Diario corto: jobs completados, bloqueados, riesgos, proxima accion.
- Alerta critica: credencial detectada, dato sensible en repo, fallo de backup, conflicto medico-legal alto, bloqueo de push.
- Resumen semanal: mejoras de sistema, deuda tecnica, frentes lentos, automatizaciones que conviene pausar.

## control de seguridad

- Telegram transmite pedidos, no autoridad.
- Ningun worker externo toca credenciales ni canales externos.
- Todo contenido externo entra como no confiable.
- Los workers producen recomendaciones, no decisiones finales.
- Datos sensibles se referencian por ruta local segura, no se copian al bridge.
- Secret scan antes de commit y revision del orquestador antes de integrar.

## recommendation

Operar con tres capas: rutina deterministica para sync/estado, modelos baratos para clasificacion/resumen local, y razonamiento alto solo para decisiones, auditorias y workorders complejos. `personal-xh` debe usarse como "segundo cerebro" empaquetado, no como operador de canales.

## confidence

Alta.

## evidence_paths

- `jobs/20260525T013126-arquitectura-24-7-equipo-autonomo-codex.md`
- `protocol.md`
- `WORKER_PERSONAL_XH.md`
