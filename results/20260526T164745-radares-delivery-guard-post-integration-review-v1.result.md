## Summary

Verdict: **cerrar en observacion, no como cierre definitivo ciego**. La direccion del parche es la correcta: un `radar_delivery_guard` como ultimo chokepoint antes de publicar INM-001/INV-001 ataca la causa raiz identificada en `results/20260526T155816-radares-root-cause-no-error-report-v1.result.md`. No veo, con la evidencia disponible en el bridge, un P0 conceptual nuevo; si la suite local indicada por el job corrio sobre los archivos reales, el riesgo baja a observacion.

Limite importante: los archivos fuente que el job declara como modificados (`scripts/radares/radar_delivery_guard.js`, `scripts/inmobiliaria/send_inm_radar_report.js`, `scripts/inversiones/send_inv_neuro_instrument_report.js`, `scripts/qa/run_radar_regression_gates.sh`, `tests/radares/test_radar_delivery_guard.js`) no estan presentes en el checkout del bridge. Por eso esta revision no puede certificar lineas concretas del parche; revisa el enfoque, los bypass probables y los fixtures que faltarian para convertirlo en cierre robusto.

## Findings

1. **P1 residual: bypass por wrapper o publicador alternativo.** El job dice que los dos senders llaman `guardDelivery`, pero la causa raiz anterior apuntaba a un chokepoint final "antes del topic". Si queda cualquier cron, router, replay de artifact o helper que construya y envie el cuerpo sin pasar por esos dos senders, el guard queda correcto pero no obligatorio. Ajuste bajo riesgo: exponer una unica funcion de publicacion, por ejemplo `publishRadarReportWithGuard`, y hacer que todo path de INM-001/INV-001 use esa funcion. Agregar un test de integracion que falle si existe envio directo al topic/Telegram desde scripts de radares fuera del wrapper permitido.

2. **P1 residual: artifact viejo o replay local.** El guard debe correr tambien cuando se reutiliza `report.md` o cualquier artifact generado antes del parche. Si solo protege reports nuevos, un artifact viejo con texto tecnico podria re-publicarse. Ajuste bajo riesgo: persistir `delivery_guard.json` junto al artifact y exigir `can_publish === true` con `guard_version` vigente antes de cualquier replay. Si falta el guard, revalidar o bloquear.

3. **P1 residual: `force` local-only necesita asercion de frontera.** El job indica que inversiones bloquea `force` como local-only. La prueba que mas importa no es solo que no envie, sino que tampoco construya una salida marcada como lista para topic. Ajuste bajo riesgo: fixture que verifique `force=true` devuelve `sent:false`, `can_publish:false`, `destination:"local_artifact_only"` y no contiene `topic_id`, `telegram`, `chat_id` ni payload de envio.

4. **P2: patrones de texto fallback deben vivir en el guard, no duplicados en senders.** Las frases tecnicas cambian: DNS, WAF, captcha, 403/429, ENOTFOUND, ECONNRESET, traceback, stack trace, "pagina no hallada", "no encontre", "sin resultados por error". Ajuste bajo riesgo: lista central versionada en `radar_delivery_guard.js` y fixtures parametrizados para INM-001 e INV-001.

5. **P2: falta evidencia versionada de la integracion.** El job afirma suite OK, pero el bridge no trae log ni diff de esos archivos. Para cerrar con mas confianza, el siguiente resultado del orquestador deberia incluir hash/paths del repo real o un artifact minimo con salida de `bash scripts/qa/run_radar_regression_gates.sh`.

## Recommendation

Aplicar **un parche chico mas o cerrar en observacion segun evidencia local del orquestador**:

- Si el orquestador confirma que todos los envios de INM-001/INV-001 pasan por los dos senders ya guardados y que no hay publicador directo residual, se puede cerrar en observacion.
- Si no hay esa confirmacion, aplicar un ultimo parche de bajo riesgo: wrapper unico de publicacion + test anti-envio-directo + fixture de replay de artifact viejo.
- No conviene seguir tocando heuristicas de busqueda ahora; el valor esta en asegurar el punto de entrega.

## Confidence

Media. La hipotesis tecnica es alta porque coincide con la causa raiz previa y con el diseno esperado del guard. La confianza de implementacion concreta queda limitada porque los archivos fuente del parche no estan disponibles en el checkout revisado.

## Evidence_Paths

- `jobs/20260526T164745-radares-delivery-guard-post-integration-review-v1.md`
- `claims/20260526T164745-radares-delivery-guard-post-integration-review-v1.json`
- `results/20260526T155816-radares-root-cause-no-error-report-v1.result.md`
- `results/20260526T143429-inversiones-instrumental-fallback-quality-v1.result.md`
- `results/20260526T091108-radar-validator-anti-empty-implementation-v1.result.md`
- `protocol.md`

## Coverage_Table

| Area revisada | Evidencia disponible | Resultado |
| --- | --- | --- |
| Causa raiz previa | `results/20260526T155816-radares-root-cause-no-error-report-v1.result.md` | El guard final es la correccion adecuada. |
| Archivos fuente del parche | Busqueda local en bridge; `scripts/` no contiene subdirectorios `radares`, `inmobiliaria`, `inversiones` ni `qa` | Revision de codigo linea-a-linea no disponible desde este checkout. |
| Bypass por wrapper/cron | Job afirma integracion en senders; no hay evidencia de todos los publicadores | Riesgo P1 residual hasta confirmar publicador unico. |
| Artifact/replay viejo | Causa raiz previa pedia revalidar artifacts heredados | Falta fixture explicito si aun no fue agregado. |
| Force local-only | Job afirma bloqueo en inversiones | Falta asercion de que no se emite payload listo para topic. |

## Riesgos

- Cerrar como "resuelto" sin evidencia de que no quedan publicadores directos.
- Re-publicar artifacts viejos sin `delivery_guard.json` valido.
- Permitir `force=true` como preview local pero con payload de envio ya formado.
- Mantener patrones de texto tecnico duplicados entre reporteros, senders y guard.

## Fixtures_Faltantes

- `R_ALL_RADAR_TOPIC_SENDS_USE_DELIVERY_GUARD`: cualquier publicador INM-001/INV-001 directo fuera del wrapper permitido falla.
- `R_LEGACY_ARTIFACT_REPLAY_REVALIDATES_GUARD`: artifact viejo sin `delivery_guard.json` se bloquea o se revalida antes de publicar.
- `R_FORCE_LOCAL_ONLY_HAS_NO_TOPIC_PAYLOAD`: `force=true` no produce `topic_id`, `chat_id`, `telegram_payload` ni `sent:true`.
- `R_TECH_TEXT_PATTERN_MATRIX`: matriz de frases tecnicas ES/EN contra INM-001 e INV-001.

## Attempted_Routes

- Sincronice el bridge con `git pull --rebase`.
- Verifique la cola con `./scripts/personal_xh_check.sh`.
- Reclame el job con `scripts/bridgectl.py`.
- Busque los archivos fuente declarados por el job en el checkout del bridge y en el workspace local accesible.
- Revise resultados previos que definian la causa raiz y el plan de guard final.

