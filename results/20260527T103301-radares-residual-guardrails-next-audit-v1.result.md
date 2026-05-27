---
job_id: 20260527T103301-radares-residual-guardrails-next-audit-v1
worker: personal-xh
status: completed
completed_at: 2026-05-27T10:38:30-03:00
front: RADARES
no_external_actions: true
no_secrets: true
---

# Resultado - Radares residual guardrails next audit v1

## summary

Veredicto: **ajustar tests y aceptar en observacion, no abrir otro ciclo
grande de logica**.

Con la evidencia del bridge, los guardrails ya cubren la causa principal:
informe vacio, error tecnico como conclusion, `force` como bypass, replay de
artifact y publicador directo. El riesgo residual que todavia vale atacar no es
"mas fuentes" ni "mas heuristicas", sino **coherencia de borde**: que el texto
renderizado sea el mismo que valido el guard, que los artifacts internos no
salgan por digest/resumen, que las fuentes no se cuenten de forma artificial, y
que los negativos validos no queden bloqueados.

No use web externa, Telegram, Gmail, Drive, Calendar ni ObraCash. El checkout
del bridge no contiene el codigo real de `radar_delivery_guard` ni el runner de
regresion; por eso esta auditoria revisa contratos, resultados previos y
bypasses especificos, no implementacion linea a linea.

## coverage_table

| Fuente | Estado | Uso |
| --- | --- | --- |
| `jobs/20260527T103301-radares-residual-guardrails-next-audit-v1.md` | Revisada | Objetivo, restricciones y entregable. |
| `context/fronts/radares.md` | Revisada | Canon anti informe vacio y source recovery obligatorio. |
| `results/20260526T155816-radares-root-cause-no-error-report-v1.result.md` | Revisada | Causa raiz: bypass post-reporter y chokepoint final. |
| `results/20260526T164745-radares-delivery-guard-post-integration-review-v1.result.md` | Revisada | Riesgos de wrapper, replay, force y evidencia no versionada. |
| `results/20260526T174756-radar-delivery-guard-residual-bypass-audit-v2.result.md` | Revisada | Tests faltantes de rutas laterales. |
| `results/20260526T230315-radares-delivery-guard-residual-night-audit-v3.result.md` | Revisada | Criterios exactos de bloqueo de topic. |
| `results/20260527T011700-radares-source-recovery-playbook.result.md` | Revisada | Thresholds de recuperacion y lenguaje permitido. |
| `results/20260526T091108-radar-validator-anti-empty-implementation-v1.result.md` | Revisada | Contrato parseable y hard fails. |
| `scripts/` | Revisada | En bridge solo hay scripts del puente; no hay codigo real de radares. |

## top_5_residual_risks

| Pri | Riesgo residual especifico | Por que sigue vivo | Test o ajuste concreto |
| --- | --- | --- | --- |
| P1 | **Drift entre contrato validado y texto renderizado.** | El guard puede validar `contract.json` o un markdown previo, pero un template posterior puede quitar fuentes, agregar "no pude", o dejar un payload tecnico. | Validar el **texto final renderizado** justo antes de publicar y guardar hash `contract_hash`, `report_hash`, `rendered_text_hash` en `delivery_guard.json`. |
| P1 | **Leak de artifacts internos por digest/resumen.** | Aunque `publishRadarReportWithGuard` bloquee el topic, otro proceso podria resumir artifacts `audience:"orchestrator_only"` y exponer el error como digest humano. | Gate de audiencia comun: todo selector de digest/topic debe rechazar `audience != public_summary` y `can_publish != true`. |
| P1 | **Conteo artificial de fuentes.** | Los thresholds de 5 fuentes pueden cumplirse con duplicados: misma URL via portal espejo, misma fuente en search/cache, o 5 queries sobre el mismo dominio. | Normalizar `source_family` y `canonical_url`; exigir familias independientes, no solo filas. |
| P1 | **Negativos validos sobrebloqueados.** | Bloquear globalmente frases como "no encontre" puede impedir reportes honestos donde una fuente fallo pero hubo recuperacion, descartes y universo revisado. | Tests negativos permitidos: frase tecnica dentro de tabla de fuente + fallback + universo completo debe quedar `needs_review` o `completed`, no `blocked` automatico. |
| P1 | **`run_radar_regression_gates OK` no ligado a la corrida real.** | Si el OK no queda versionado junto al artifact, no prueba que ese reporte paso esa version del guard y fixture set. | Persistir `regression_gate_summary.json` con `guard_version`, `fixture_set_hash`, `git_sha`, `started_at`, `exit_code`, y exigirlo para publicar. |

## tests_to_add_or_tighten

| Test | Fixture minimo | Expected |
| --- | --- | --- |
| `R_RENDERED_TEXT_REVALIDATED_AFTER_TEMPLATE` | Contract valido + template final que agrega `ENOTFOUND` o borra `sources_attempted`. | `can_publish:false`, `sent:false`, `reason:"rendered_text_failed_guard"`. |
| `R_REPORT_HASH_MATCHES_GUARDED_TEXT` | `delivery_guard.json` con hash de reporte A, publish intenta reporte B. | Bloqueo por `guard_hash_mismatch`; revalidar o abortar. |
| `R_ORCHESTRATOR_ONLY_ARTIFACT_NOT_IN_PUBLIC_DIGEST` | Artifact `audience:"orchestrator_only"`, `can_publish:false`, texto tecnico. | Ningun digest/topic externo lo selecciona; solo dashboard interno. |
| `R_SOURCE_FAMILY_DEDUP_COUNTS_ONCE` | 5 sources del mismo dominio/query equivalente. | Maximo `needs_review`; no `completed` por cantidad inflada. |
| `R_VALID_ZERO_CANDIDATES_NOT_FALSE_BLOCKED` | 6 fuentes, 3 familias, 5 descartes, 2 comparables, cero oportunidades, next run claro. | Puede ser `completed_no_action` o `needs_review`, pero no `blocked`. |
| `R_BLOCKED_SOURCE_WITH_FALLBACK_ALLOWED` | Una fuente con `pagina no hallada`, dos fallbacks exitosos y candidato con comparable. | No bloquear por la frase aislada; evaluar contrato completo. |
| `R_FORCE_STRIPS_DESTINATION_AND_REPORT_HASH` | `force=true` con artifact local y payload externo simulado. | Remueve `topic_id`, `chat_id`, `telegram_payload`, `message_id`; destino solo local. |
| `R_REGRESSION_SUMMARY_REQUIRED_FOR_TOPIC` | Reporte con guard OK pero sin `regression_gate_summary.json`. | No publica; `status:"blocked_operational"`. |

## negative_cases_that_must_not_block_valid_reports

Estos casos evitan que el gate se vuelva tan duro que mate informes utiles:

1. **No oportunidad real, universo completo.** Si hay fuentes suficientes,
   familias independientes, descartes, comparables y proxima corrida, el cierre
   "no avanzar hoy" es valido. No debe ser tratado como informe vacio.
2. **Una fuente caida con recuperacion exitosa.** Una fila que diga "pagina no
   hallada" no debe bloquear si el reporte demuestra fallback y no usa esa frase
   como conclusion.
3. **Precio pendiente con ruta concreta.** Un candidato inmobiliario o
   instrumental sin precio exacto puede quedar `needs_review` si trae ruta de
   obtencion, comparables y riesgo; no debe ser `completed`.
4. **Instrumental reusable vs implante.** Falta de ANMAT/importador debe bloquear
   decision `comprar` para implantes o productos regulados, pero puede permitir
   `watchlist` conservador para instrumental reusable con compatibilidad
   pendiente.
5. **Candidato unico fuerte.** No debe publicarse como compra/avance automatico,
   pero tampoco descartarse si tiene fuente, precio, comparables, riesgos y
   next action humano.

## acceptance_observation_gate

Recomiendo aceptar en observacion solo si el orquestador puede responder "si" a
estos cinco checks:

```yaml
accept_in_observation_if:
  - final_rendered_text_is_guarded: true
  - public_digest_respects_audience_and_can_publish: true
  - source_family_dedup_is_enforced: true
  - valid_negative_market_reports_have_tests: true
  - regression_gate_summary_is_persisted_per_run: true
```

Si alguno falta, el patch a pedir es chico y de tests/enforcement, no un nuevo
ciclo de busqueda.

## recommendation

Recomendacion unica: **ajustar tests con los 5 checks anteriores y aceptar en
observacion cuando pasen**.

No pediria nuevo ciclo grande salvo que falle `R_RENDERED_TEXT_REVALIDATED_AFTER_TEMPLATE`
o `R_ORCHESTRATOR_ONLY_ARTIFACT_NOT_IN_PUBLIC_DIGEST`, porque esos dos si
pueden reintroducir el bug por fuera del guard ya integrado.

## confidence

**medium_high** para los riesgos residuales y fixtures, porque se derivan de la
causa raiz ya repetida y de los contratos previos. **medium** para el estado
concreto de implementacion, porque el codigo real de radares y la salida de
`run_radar_regression_gates` no estan versionados en este checkout del bridge.

## attempted_routes

- Se hizo `git pull --rebase`.
- Se verifico la cola con `./scripts/personal_xh_check.sh`.
- Se reclamo el job con `python3 scripts/bridgectl.py claim`.
- Se revisaron el workorder, contexto canonico de RADARES y resultados previos
  de root cause, delivery guard, residual bypass y source recovery.
- Se inspecciono `scripts/`; el bridge no contiene los subdirectorios reales de
  radares/qa declarados por resultados previos.
- No se uso web externa, Telegram, Gmail, Drive, Calendar, ObraCash ni
  credenciales.

## risks_limits

- Esta auditoria no certifica codigo real ni logs de suite; solo valida el
  contrato y propone pruebas especificas.
- Si el repo real ya contiene estos tests, la recomendacion baja a cerrar en
  observacion y versionar el resumen de corrida.
- Si el sistema publica tambien por digest, dashboard o resumen diario, esos
  caminos deben compartir el mismo gate de audiencia.

## evidence_paths

- `jobs/20260527T103301-radares-residual-guardrails-next-audit-v1.md`
- `claims/20260527T103301-radares-residual-guardrails-next-audit-v1.json`
- `context/fronts/radares.md`
- `results/20260526T155816-radares-root-cause-no-error-report-v1.result.md`
- `results/20260526T164745-radares-delivery-guard-post-integration-review-v1.result.md`
- `results/20260526T174756-radar-delivery-guard-residual-bypass-audit-v2.result.md`
- `results/20260526T230315-radares-delivery-guard-residual-night-audit-v3.result.md`
- `results/20260527T011700-radares-source-recovery-playbook.result.md`
- `results/20260526T091108-radar-validator-anti-empty-implementation-v1.result.md`
- `context/fronts/radares.md`
- `scripts/`
