# Resultado - 20260526T104237-artifactdraft-topic-router-implementation-review-v1

## summary

Segunda mirada sobre la integracion local declarada de ArtifactDraft en el topic router. Veredicto: **aceptar solo como piloto dry-run limitado, con flag apagado por defecto; ajustar antes de activar envio real con flag activo**.

La direccion es correcta: feature flag, dry-run, `delivered` solo con `message_id`, y pruebas de receipt gate reducen los riesgos P0 principales. Pero los scripts/tests listados por el orquestador no estan presentes en este bridge (`scripts/artifacts/*`, `scripts/send_codex_topic_message.py`, `tests/*`), por lo que esta revision no valida codigo real linea por linea. El resultado debe tratarse como revision de seguridad/regresion sobre el contrato reportado, no como aprobacion de implementacion productiva.

## source_counts

| Fuente permitida | Estado | Uso |
| --- | ---: | --- |
| `results/20260526T101406-artifactdraft-router-pilot-safe-plan-v1.result.md` | Revisada | Plan de integracion, fixtures P0/P1 y criterio de activacion parcial. |
| `protocol.md` | Revisado | Reglas: sin acciones externas, orquestador conserva decision final, no secretos. |
| `scripts/artifacts/new_artifact.py` | Ausente en bridge | Ruta declarada por orquestador, no inspeccionable aqui. |
| `scripts/artifacts/validate_artifact.py` | Ausente en bridge | Ruta declarada por orquestador, no inspeccionable aqui. |
| `scripts/send_codex_topic_message.py` | Ausente en bridge | Ruta declarada por orquestador, no inspeccionable aqui. |
| `tests/artifacts/test_artifactdraft_gate.py` | Ausente en bridge | Ruta declarada por orquestador, no inspeccionable aqui. |
| `tests/telegram/test_artifactdraft_topic_router_pilot.py` | Ausente en bridge | Ruta declarada por orquestador, no inspeccionable aqui. |

## verdict

| Decision | Estado recomendado |
| --- | --- |
| Mantener merge/local integration | Si, si queda detras de feature flag apagado por defecto. |
| Activar dry-run limitado | Si, solo en entorno local del orquestador y sin envio externo. |
| Activar con envio real | Todavia no; requiere fixtures adicionales y revision de archivos reales. |
| Revertir | No hay evidencia suficiente para revertir; el diseno reduce riesgo si el flag funciona. |

Recomendacion exacta para el orquestador:

```text
ARTIFACTDRAFT_ROUTER_PILOT=0 por defecto.
ARTIFACTDRAFT_DRY_RUN=1 para piloto local.
Activar ARTIFACTDRAFT_ROUTER_PILOT=1 solo en pruebas controladas de mensajes largos/adjuntos/reels/radar/viajes/presentaciones.
No activar envio real con el piloto hasta confirmar fixtures P0 y revisar los scripts reales.
```

## p0_risks_detected

| Riesgo P0 | Estado observado | Ajuste recomendado |
| --- | --- | --- |
| Feature flag no sea fail-closed | El job declara flag apagado por defecto, pero el codigo no esta visible aqui. | Test obligatorio: sin env var, artifact `null`, sin carpetas nuevas y flujo anterior intacto. |
| `delivered` sin recibo real | El job declara receipt gate con `message_id`; buen control. | Agregar test negativo: `ok=true` sin `message_id` no puede marcar `delivered`. |
| Topic contamination | El job declara tests de router pilot, pero no se ve suite. | Fixture con topic esperado vs topic resuelto, y bloqueo si difieren. |
| Dry-run que escribe fuera de area segura | No verificable sin codigo. | Asegurar root configurable bajo workspace autorizado y sin rutas absolutas sensibles en resultados. |
| Payload tecnico crudo | No verificable sin codigo. | Test con `Traceback`, `git diff`, logs y stack trace debe bloquear pre-send. |
| Datos de paciente/material personal | El contrato lo contempla. | Test `contains_patient_data=true` + target externo debe bloquear incluso si QA pass. |
| Envio externo accidental en dry-run | El job declara que no envia nada. | Test con monkeypatch/fake sender que falla si se invoca en dry-run. |

## p1_risks_detected

| Riesgo P1 | Estado | Ajuste |
| --- | --- | --- |
| Doble artifact en retry | No verificable. | `artifact_id` deterministico por job/run y reuse si existe. |
| Repo pesado | No verificable. | Mantener binarios fuera de git; manifestar rutas/derivados seguros. |
| Overhead en mensajes cortos | Dry-run corto sin flag dio artifact `null`, buen indicio. | Sumar caso con flag activo pero healthcheck corto debe bypass. |
| Estado `blocked` sin handoff | No verificable. | Al bloquear, escribir `qa/qa_report.md` con reason y next action. |
| Incompatibilidad con tests historicos | El job declara postfix regression pasado. | Mantener esa suite como gate antes de activar. |

## missing_fixtures

Los tests declarados son una buena base, pero faltan o deben confirmarse estos fixtures antes de activar fuera de dry-run:

| Fixture | Proposito | Esperado |
| --- | --- | --- |
| `A_FLAG_DEFAULT_OFF_NO_ARTIFACT` | Seguridad del default. | Sin env var, comportamiento identico al anterior y `artifact_id=null`. |
| `A_DRY_RUN_NEVER_CALLS_SENDER` | Impedir envio accidental. | Sender fake no se llama; no hay `message_id`. |
| `A_FLAG_ON_SHORT_HEALTHCHECK_BYPASS` | Evitar overhead. | Con flag activo, mensaje corto/heartbeat no crea artifact. |
| `A_LONG_TELEGRAM_DRAFT_ONLY` | Mensaje largo. | Crea artifact local y queda `draft`/`qa_ready`, sin delivery. |
| `A_TOPIC_MISMATCH_BLOCKED` | Contaminacion de topic. | `blocked`, no outbox. |
| `A_RAW_TRACEBACK_BLOCKED` | Payload tecnico. | QA fail, no envio. |
| `A_PATIENT_DATA_BLOCKS_EXTERNAL` | Privacidad. | `queued_external` y `delivered` prohibidos. |
| `A_OK_NO_MESSAGE_ID_NOT_DELIVERED` | Recibo incompleto. | `blocked` o `queued_external`, nunca `delivered`. |
| `A_MESSAGE_ID_AND_CHAT_ID_REQUIRED` | Recibo real minimo. | `delivered` solo con ambos valores. |
| `A_RETRY_REUSES_ARTIFACT_ID` | Idempotencia. | Segundo intento no duplica carpetas ni pierde QA. |

## acceptance_criteria

Aceptar el piloto en dry-run si:

1. `ARTIFACTDRAFT_ROUTER_PILOT` esta apagado por defecto y probado.
2. `ARTIFACTDRAFT_DRY_RUN=1` impide llamadas al sender real.
3. Mensajes cortos/healthchecks no crean artifact aunque el flag este activo.
4. Mensajes largos o frentes `REELS`, `VIAJES`, `RADAR`, `INM`, `INV`, `PRESENTACIONES` crean artifact bajo raiz controlada.
5. `validate_artifact.py` falla si falta manifest, QA o receipt obligatorio.
6. `delivered` requiere `message_id` y `chat_id` en Telegram.
7. Los tests `test_delivery_receipt_gate.py` y `test_postfix_regression_fixtures.py` quedan como gate de CI/local antes de activar.
8. El resultado/log externo no expone rutas sensibles, payload tecnico crudo ni material personal.

## minimal_patch_recommendations

Si el orquestador decide parchear, mantenerlo minimo:

1. Agregar test fail-closed del feature flag:

```python
def test_artifactdraft_flag_default_off_short_message(tmp_path, monkeypatch):
    monkeypatch.delenv("ARTIFACTDRAFT_ROUTER_PILOT", raising=False)
    result = run_topic_message("estado corto", dry_run=True, artifact_root=tmp_path)
    assert result.get("artifact_id") is None
```

2. Agregar test dry-run no invoca sender:

```python
def test_artifactdraft_dry_run_never_calls_sender(monkeypatch):
    called = False
    def fake_sender(*args, **kwargs):
        nonlocal called
        called = True
        raise AssertionError("sender should not be called in dry-run")
    monkeypatch.setattr("router_module.send_telegram", fake_sender)
    run_topic_message("texto largo " * 200, dry_run=True, artifactdraft=True)
    assert called is False
```

3. Agregar check de recibo Telegram completo:

```python
def assert_telegram_receipt(delivery):
    if delivery.get("target") == "telegram" and delivery.get("status") == "delivered":
        assert delivery.get("message_id")
        assert delivery.get("chat_id")
```

4. Agregar bloqueo por payload tecnico antes del outbox:

```python
RAW_TECH_MARKERS = ("Traceback", "git diff", "@@ ", "Exception:", "stack trace")
if any(marker in final_text for marker in RAW_TECH_MARKERS):
    artifact.status = "blocked"
    return {"ok": False, "blocked_reason": "raw_technical_payload"}
```

No propongo cambiar arquitectura ni activar envio real en este paso.

## recommendation

Mantener `ARTIFACTDRAFT_ROUTER_PILOT=0` por defecto. Activar `ARTIFACTDRAFT_ROUTER_PILOT=1` solo con `ARTIFACTDRAFT_DRY_RUN=1` en corridas locales controladas para mensajes largos y frentes de alto riesgo. No activar envio real hasta que el orquestador confirme los fixtures faltantes y revise el codigo real de:

- `scripts/send_codex_topic_message.py`
- `scripts/artifacts/new_artifact.py`
- `scripts/artifacts/validate_artifact.py`
- `tests/artifacts/test_artifactdraft_gate.py`
- `tests/telegram/test_artifactdraft_topic_router_pilot.py`
- `tests/telegram/test_delivery_receipt_gate.py`

## attempted_routes

- Se hizo `git pull --rebase`.
- Se inspecciono el job, `results/20260526T101406-artifactdraft-router-pilot-safe-plan-v1.result.md`, `protocol.md`, y el arbol local de `scripts/` y `tests/`.
- Las rutas de implementacion declaradas por el orquestador no existen en este bridge; se registra como limite de revision.
- No se abrio Drive, iCloud, Photos, Gmail, Telegram real, Downloads, ObraCash ni bibliotecas completas.
- No se hicieron acciones externas ni se tocaron credenciales.

## risks_limits

- Esta no es una auditoria de codigo real; es una revision de seguridad del contrato declarado y del material disponible en el bridge.
- Si los archivos viven en otro repo/local workspace, el orquestador debe correr alli los tests y revisar el diff.
- La recomendacion puede endurecerse tras ver codigo real, especialmente alrededor de sender, root paths y sanitizacion de payload.
- El piloto en dry-run es de bajo riesgo; el piloto con envio real sigue siendo de riesgo medio hasta probar recibo, topic y privacy gates.

## confidence

Media-alta para recomendar dry-run limitado y flag apagado porque el contrato declarado cubre los P0 correctos. Media para aceptar la implementacion completa porque los archivos reales no estan disponibles en el bridge.

## evidence_paths

- `jobs/20260526T104237-artifactdraft-topic-router-implementation-review-v1.md`
- `results/20260526T101406-artifactdraft-router-pilot-safe-plan-v1.result.md`
- `protocol.md`
- `scripts/` (arbol local inspeccionado; rutas de ArtifactDraft declaradas ausentes)
