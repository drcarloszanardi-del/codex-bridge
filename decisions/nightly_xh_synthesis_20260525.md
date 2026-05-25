# Nightly XH synthesis 2026-05-25

## top hallazgos

1. El bridge Git ya funciona como canal canonico entre orquestador y `personal-xh`; falta madurar claims stale/release, pero el doble procesamiento ya quedo mitigado.
2. La app clinica tiene QA y corpus avanzados, pero el riesgo mayor es drift entre rutas canonicas y generadores alternativos.
3. Los errores clinicos de alto riesgo deben pasar a fixtures deterministas: extraforaminal, no invencion, sin descompresion directa, artrodesis sin lateralidad y cierre.
4. El corpus medico-legal debe separarse en fuente oficial, cola de revision y gate activo.
5. Telegram debe ser adaptador; la memoria real debe vivir en events/jobs/runs/context.
6. ObraCash queda como frente protegido: backup, integridad y restore, sin tocar contenido operativo.
7. Herramientas externas pueden ayudar, pero solo con contexto empaquetado y sin autoridad.

## incorporar ahora

- `claims/` y `bridgectl.py claim`.
- Route guard canonico para app clinica.
- Fixtures lumbares critical.
- `TOOL_ROUTING.md`.
- Router Telegram con idempotencia y ACK no ruidoso.
- Runbook ObraCash backup/integridad sin contenido.

## incorporar luego

- Claim expiration/release controlado por orquestador.
- Crawler oficial de jurisprudencia por fuente.
- NotebookLM/Zotero para tesis cuando haya corpus curado.
- Scorecards automatizados para radares inmobiliario/instrumental.

## descartar

- Citas legales dentro de documentos clinicos finales.
- Promover fallos secundarios como gates fuertes sin copia oficial.
- Telegram como memoria principal.
- Respuestas automaticas de mail o publicaciones sin aprobacion.

## requiere autorizacion humana

- Cualquier accion externa: publicar, enviar, responder, comprar, contactar.
- Activar cambios clinicos reales en la app de work-mac.
- Usar datos clinicos reales no sanitizados.
- Tocar contenido operativo de ObraCash.
- Validacion legal de gates basados en jurisprudencia.

## riesgos criticos

- Mezcla de frentes si Telegram no enruta por topic/front/task.
- Sobrelegalizar historias clinicas y partes quirurgicos.
- Snapshot clinico con rutas/logs/cache no portables.
- Falsa seguridad si QA pasa pero no contiene los bugs reales del Dr. Zanardi.

## jobs siguiente fase sugeridos

1. Implementar route guard canonico en work-mac.
2. Integrar `lumbar_gates_v1.json` como suite real.
3. Crear `corpus_item`/`gate_item` migrator.
4. Implementar router Telegram MVP con event/job/run store.
5. Agregar release/expire claims al bridge.

## evidence_paths

- `results/`
- `context/frentes_activos_resumen_20260525.md`
- `decisions/clinica_app_improvement_proposals/`
- `TOOL_ROUTING.md`
