---
job_id: 20260526T230315-radares-delivery-guard-residual-night-audit-v3
worker: personal-xh
status: completed
completed_at: 2026-05-26T23:16:30-03:00
front: RADARES
no_external_actions: true
no_secrets: true
---

# Resultado - radares delivery guard residual night audit v3

## summary

Verdict: **cerrar solo en observacion, con 5 bypass residuales convertidos en
tests obligatorios**. La linea correcta sigue siendo un `radar_delivery_guard`
como ultimo chokepoint antes de publicar INM-001/INV-001, pero el riesgo que
queda no es de "mas heuristicas"; es de rutas laterales, replay de artifacts,
`force`, estados parciales y evidencia de suite no versionada.

No ejecute scraping externo, no use Telegram, no toque ObraCash, no abri
bibliotecas privadas y no inspeccione secretos. La auditoria fue read-only sobre
el bridge; el unico archivo fuente solicitado (`scripts/qa/validate_radar_report.py`)
no esta presente en este checkout.

## coverage_table

| Fuente | Estado | Uso |
| --- | --- | --- |
| `jobs/20260526T230315-radares-delivery-guard-residual-night-audit-v3.md` | Revisada | Workorder y criterios de entrega. |
| `context/fronts/radares.md` | Revisada | Estado canonico y reglas anti informe vacio. |
| `results/20260526T155816-radares-root-cause-no-error-report-v1.result.md` | Revisada | Causa raiz: bypass post-reporter y chokepoint final. |
| `results/20260526T164745-radares-delivery-guard-post-integration-review-v1.result.md` | Revisada | Riesgos residuales post-integracion. |
| `results/20260526T174756-radar-delivery-guard-residual-bypass-audit-v2.result.md` | Revisada | Tests faltantes de rutas laterales. |
| `results/20260526T091108-radar-validator-anti-empty-implementation-v1.result.md` | Revisada | Contrato validator anti-empty. |
| `results/20260525T214513-telegram-radar-regression-fixtures-v1.result.md` | Revisada | Fixtures base de radar/Telegram. |
| `results/20260525T234822-radares-hardening-anti-informe-vacio-v2.result.md` | Revisada | Reglas P0, source recovery ladder y test cases. |
| `scripts/qa/validate_radar_report.py` | No existe en bridge | Se marca limite; no hay revision linea a linea. |
| `scripts/radares`, `scripts/inmobiliaria`, `scripts/inversiones`, `scripts/qa` | No existen en bridge | No se certifica implementacion real; se audita contrato y bypasses. |

## findings

### Top 5 bypass residuales concretos

1. **Publicador directo fuera del guard.**
   - Evidencia: los resultados v1/v2 insistieron en que el bug reaparece despues
     del reporter, cuando un wrapper/router/topic puede formatear `sent:false` o
     `blocked` como texto publicable.
   - Bypass: cualquier helper que llame a Telegram/topic con `sendMessage`,
     `postTopic`, `bot.send`, `topic_id`, `chat_id` o payload equivalente sin
     pasar por `publishRadarReportWithGuard`.
   - Impacto: el guard puede estar perfecto y aun asi no ser obligatorio.

2. **Replay de artifact viejo o stale `delivery_guard.json`.**
   - Evidencia: v1 pidio revalidar artifacts heredados; v2 pidio fixture
     dedicado.
   - Bypass: `report.md` generado antes del guard, o con `guard_version` viejo,
     se vuelve a usar para publicar sin revalidar.
   - Impacto: reaparecen "pagina no hallada", `ENOTFOUND`, WAF/captcha o logs
     crudos aunque los reports nuevos esten protegidos.

3. **Estado parcial que lava un error tecnico.**
   - Evidencia: el validator anti-empty cubre "solo errores", pero el hardening
     advierte que una fuente real, un candidato debil o cero candidatos sin
     universo no deben cerrar.
   - Bypass: un reporte con 1 fuente parcial + varias fallas tecnicas termina
     como `completed` porque ya no es "all technical failures".
   - Impacto: informe malo sin decir literalmente "no pude", pero igual no
     accionable.

4. **`force=true` local-only que conserva payload publicable.**
   - Evidencia: v1/v2 separan `force_local_artifact=true` de publicar al Doctor.
   - Bypass: `force` devuelve `sent:false`, pero deja `topic_id`, `chat_id`,
     `telegram_payload`, `message_id` falso o texto final listo para topic en
     artifact/log.
   - Impacto: otro runner puede tomar ese payload y mandarlo.

5. **Suite verde no versionada ni atada al artifact de corrida.**
   - Evidencia: las revisiones anteriores no pudieron ver codigo real ni logs de
     `run_radar_regression_gates.sh` en el bridge.
   - Bypass: se dice "tests OK", pero el artifact de la corrida no conserva
     `guard_version`, hash de suite, fixture set ni salida resumida.
   - Impacto: no hay prueba reproducible de que la corrida que se intenta enviar
     paso el guard vigente.

### Fixtures o tests sugeridos

| Test | Objetivo | Expected |
| --- | --- | --- |
| `R_ALL_RADAR_TOPIC_SENDS_USE_DELIVERY_GUARD` | Escanear publicadores INM/INV y bloquear envio directo fuera de allowlist. | Falla si hay `sendMessage`, `telegram`, `topic_id`, `chat_id`, `bot.send`, `postTopic` fuera del wrapper aprobado. |
| `R_CRON_SENT_FALSE_NOT_FORMATTED_TO_TOPIC` | Mock de reporter con `sent:false`, `can_publish:false`, `report_text:"pagina no hallada"`. | Cron/wrapper no publica; crea artifact local `audience:"orchestrator_only"`. |
| `R_LEGACY_ARTIFACT_REPLAY_REVALIDATES_GUARD` | Reusar artifact viejo sin `delivery_guard.json`, con `ENOTFOUND`. | Replay bloqueado o revalidado; nunca `sent:true`; escribe nuevo guard `can_publish:false`. |
| `R_FORCE_LOCAL_ONLY_STRIPS_TOPIC_PAYLOAD` | Ejecutar con `force=true` y texto tecnico. | `sent:false`, `destination:"local_artifact_only"` y ausencia de payload topic/Telegram. |
| `R_PARTIAL_SOURCE_WITH_TECH_ERRORS_NEEDS_REVIEW` | 1 fuente parcial + 3 errores tecnicos + 0 comparables. | Maximo `needs_review`; no `completed`, no topic. |
| `R_ZERO_CANDIDATES_REQUIRES_UNIVERSE_AND_NEXT_RUN` | 0 candidatos con fuentes escasas o sin descartes. | `blocked`; si hay universo amplio, `needs_review` con next run, no final automatico. |
| `R_GUARD_VERSION_REQUIRED_FOR_TOPIC` | Artifact con guard faltante o version vieja. | Bloquea topic hasta revalidar con guard vigente. |
| `R_TECH_TEXT_PATTERN_MATRIX_ES_EN` | Matriz WAF/captcha/403/429/ENOTFOUND/ECONNRESET/traceback/no encontre/pagina no hallada. | Todos quedan `can_publish:false`. |

### Cambios de bajo riesgo recomendados para el orquestador

1. Crear un wrapper unico:

```text
publishRadarReportWithGuard(report_contract, report_text, destination)
```

Ninguna ruta INM-001/INV-001 deberia publicar sin pasar por ahi.

2. Persistir en cada corrida:

```text
artifacts/radares/<run_id>/contract.json
artifacts/radares/<run_id>/report.md
artifacts/radares/<run_id>/delivery_guard.json
artifacts/radares/<run_id>/regression_gate_summary.json
```

3. Exigir `delivery_guard.guard_version` y `regression_gate_summary.fixture_set`
antes de publicar. Si faltan, revalidar o bloquear.

4. Centralizar patrones tecnicos en el guard, no duplicarlos en senders. Los
senders pueden aportar contexto; el bloqueo final debe vivir en un solo lugar.

5. Hacer que `--force` escriba solo artifact local y borre cualquier campo de
destino externo antes de persistir: `topic_id`, `chat_id`, `telegram_payload`,
`message_id`, `send_request`.

6. Separar publicacion humana de observabilidad interna: un bloqueo tecnico
puede ir a dashboard/orquestador, pero no al topic del Doctor como "informe".

## exact_topic_block_criterion

Bloquear envio al topic cuando ocurra cualquiera de estas condiciones:

```yaml
block_topic_send_if:
  - delivery_guard missing
  - delivery_guard.can_publish != true
  - delivery_guard.guard_version missing_or_stale
  - report_contract.status_by_gate != completed
  - report_contract.can_publish != true
  - force == true
  - destination != doctor_topic and audience != public_summary
  - report_text contains technical_failure_pattern
  - report_text contains raw_payload_pattern
  - source outcome in [blocked, error] without fallback_routes_used
  - candidates_count == 0 and universe_reviewed != true
  - candidates_count == 1 and comparables_count == 0
  - next_action missing
  - regression_gate_summary missing_or_failed
```

Patrones tecnicos minimos para `technical_failure_pattern`:

```text
no pude
no encontre
pagina no hallada
pagina no abre
DNS
ENOTFOUND
ECONNRESET
WAF
captcha
HTTP 403
HTTP 429
timeout
Traceback
stack trace
fatal:
raw diff
@@
```

La salida correcta cuando se bloquea:

```json
{
  "sent": false,
  "can_publish": false,
  "status": "blocked_operational",
  "audience": "orchestrator_only",
  "artifact_local_required": true,
  "next_action": "reintentar fuentes/fallbacks o crear job especifico"
}
```

## que_no_tocar

- No tocar ObraCash.
- No ejecutar scraping externo para esta auditoria.
- No abrir Telegram, Gmail, Drive, Calendar, Fotos, iCloud, Downloads ni
  bibliotecas privadas.
- No relajar thresholds P0 para "destrabar" envios.
- No agregar mas fuentes o heuristicas como solucion principal; primero cerrar
  rutas de entrega.
- No permitir que `force` publique al Doctor.
- No mezclar instrumental reusable con implantes sin trazabilidad.
- No convertir bloqueos tecnicos en mensajes humanos tipo "no pude" o "pagina no
  hallada".

## recommendation

Recomendacion operativa: **aplicar un patch minimo de enforcement y cerrar en
observacion solo si pasa**:

1. Wrapper unico de publicacion con guard obligatorio.
2. Tests: `R_ALL_RADAR_TOPIC_SENDS_USE_DELIVERY_GUARD`,
   `R_LEGACY_ARTIFACT_REPLAY_REVALIDATES_GUARD`,
   `R_FORCE_LOCAL_ONLY_STRIPS_TOPIC_PAYLOAD`,
   `R_PARTIAL_SOURCE_WITH_TECH_ERRORS_NEEDS_REVIEW`.
3. `regression_gate_summary.json` versionado por corrida.
4. Regla fail-closed: si falta guard, falta suite, o hay texto tecnico, no hay
   topic del Doctor.

No conviene hacer otro ajuste grande de busqueda hasta que estos tests cierren
las rutas laterales. El problema repetido fue entrega de informe malo, no falta
de teoria de scouting.

## risks_limits

- No se reviso codigo real linea a linea porque los subdirectorios y
  `scripts/qa/validate_radar_report.py` no estan en este checkout del bridge.
- El diagnostico se basa en evidencia de resultados previos y contratos
  declarados; el orquestador debe confirmar en el repo real que no quedan
  publicadores directos.
- Si el sistema tiene un dashboard interno, el bloqueo puede avisarse alli; este
  resultado solo bloquea el topic externo del Doctor.

## confidence

**medium_high** para los bypasses y fixtures, porque repiten la causa raiz de
v1/v2 y el contrato canonico de radares. **medium** para el estado concreto de
implementacion, porque el codigo real de guard/wrapper/QA no esta presente en el
bridge revisado.

## evidence_paths

- `jobs/20260526T230315-radares-delivery-guard-residual-night-audit-v3.md`
- `claims/20260526T230315-radares-delivery-guard-residual-night-audit-v3.json`
- `context/fronts/radares.md`
- `results/20260526T155816-radares-root-cause-no-error-report-v1.result.md`
- `results/20260526T164745-radares-delivery-guard-post-integration-review-v1.result.md`
- `results/20260526T174756-radar-delivery-guard-residual-bypass-audit-v2.result.md`
- `results/20260526T091108-radar-validator-anti-empty-implementation-v1.result.md`
- `results/20260525T214513-telegram-radar-regression-fixtures-v1.result.md`
- `results/20260525T234822-radares-hardening-anti-informe-vacio-v2.result.md`
- `protocol.md`
