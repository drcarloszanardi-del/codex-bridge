---
job_id: 20260525T084316-bridge-claim-expiration-release-proposal-v1
worker: personal-xh
status: completed
completed_at: 2026-05-25T08:52:07-03:00
front: CODEX-OPS
---

# Result

## summary

Se propone un patch minimalista para `scripts/bridgectl.py`: mantener claims auditables en `claims/<job_id>.json`, agregar expiracion por TTL, release explicito y takeover controlado. El objetivo es evitar claims stale sin abrir carrera entre workers ni borrar evidencia.

## findings con evidencia

- `scripts/bridgectl.py` ya usa `os.O_EXCL` al crear el claim, lo cual evita doble adquisicion inicial.
- `claim_job()` actualmente solo escribe `job_id`, `assignee`, `claimed_at` y `host`; no guarda `expires_at`, `heartbeat_at`, `status`, `release_reason` ni historial de takeover.
- `list_jobs --available` excluye jobs reclamados por otro assignee de forma indefinida; un worker caido puede dejar jobs bloqueados para siempre.
- No existe CLI para `release`, `claim-status`, `takeover` ni refresh de heartbeat.

## riesgos

- Stale claims: un claim de un worker caido bloquea trabajo pendiente.
- Takeover accidental: permitir takeover sin TTL/razon puede duplicar ejecucion.
- Clock skew: comparar tiempos locales entre Macs puede generar falsos expirados.
- Perdida de auditoria: borrar claims para liberar jobs oculta quien los tomo.
- Race condition: dos workers pueden intentar takeover simultaneo si no se usa escritura atomica.

## recommendation

### CLI sugerida

```bash
python3 scripts/bridgectl.py claim --job-id "$JOB_ID" --assignee personal-xh --ttl-minutes 240
python3 scripts/bridgectl.py claim-status --job-id "$JOB_ID"
python3 scripts/bridgectl.py heartbeat --job-id "$JOB_ID" --assignee personal-xh --ttl-minutes 240
python3 scripts/bridgectl.py release --job-id "$JOB_ID" --assignee personal-xh --reason "blocked: waiting orchestrator"
python3 scripts/bridgectl.py takeover --job-id "$JOB_ID" --assignee work-mac-orchestrator --reason "expired claim" --after-minutes 240
python3 scripts/bridgectl.py list-jobs --pending --assignee personal-xh --available
```

### Formato JSON claim actualizado

```json
{
  "job_id": "20260525T084316-example",
  "assignee": "personal-xh",
  "claimed_at": "2026-05-25T08:43:16-03:00",
  "heartbeat_at": "2026-05-25T08:52:07-03:00",
  "expires_at": "2026-05-25T12:52:07-03:00",
  "host": "MacBook-Air-de-Carlos.local",
  "status": "active",
  "release_reason": null,
  "takeover_reason": null,
  "previous_assignee": null,
  "previous_claimed_at": null,
  "taken_over_at": null
}
```

Valores permitidos para `status`: `active`, `released`, `expired`, `taken_over`, `completed`.

### Algoritmo

1. Leer claim existente si existe.
2. Si no existe, crear claim atomico con `O_EXCL`, `status=active`, `claimed_at`, `heartbeat_at` y `expires_at`.
3. Si existe y `status=released`, permitir nuevo claim atomico mediante rewrite con lock temporal.
4. Si existe y es del mismo `assignee`, actualizar `heartbeat_at` y extender `expires_at`; esto vuelve idempotente el reclamo propio.
5. Si existe y es de otro `assignee` con `status=active` y `expires_at` futuro, rechazar con `claimed_by`.
6. Si existe y `expires_at` vencio, marcar takeover solo con `--reason`; guardar `previous_assignee`, `previous_claimed_at`, `taken_over_at` y nuevo `assignee`.
7. `release` solo debe aceptar el mismo `assignee` o el orquestador; exigir `--reason`.
8. `list-jobs --available` debe tratar claims vencidos o released como disponibles, y claims activos de otros como no disponibles.

Implementacion segura: escribir en archivo temporal dentro de `claims/`, hacer `fsync`, luego `os.replace()`. Evitar borrar claims.

### Pruebas esperadas

- Claim nuevo crea JSON completo.
- Claim repetido por mismo assignee es idempotente y refresca heartbeat.
- Claim activo de otro assignee se rechaza.
- Claim vencido permite takeover solo con `--reason`.
- Release sin `--reason` falla.
- Release por assignee distinto falla salvo orquestador.
- `list-jobs --available` incluye released/expired y excluye active no vencidos.
- JSON corrupto en `claims/` no habilita ejecucion silenciosa; debe reportar `invalid_claim_json`.

### Comandos exactos para que el orquestador integre

```bash
git checkout -b bridge-claim-expiration-release-v1
$EDITOR scripts/bridgectl.py
mkdir -p tests
$EDITOR tests/test_bridgectl_claims.py
python3 -m pytest tests/test_bridgectl_claims.py
python3 scripts/secret_scan.py
python3 scripts/bridgectl.py list-jobs --pending --assignee personal-xh --available
git diff -- scripts/bridgectl.py tests/test_bridgectl_claims.py
git add scripts/bridgectl.py tests/test_bridgectl_claims.py
git commit -m "Add claim expiration release and takeover"
git push
```

## confidence

High. La evidencia local alcanza para identificar el gap y el patch puede mantenerse acotado a `bridgectl.py` mas tests.

## evidence_paths

- `scripts/bridgectl.py`
- `claims/`
- `jobs/20260525T084316-bridge-claim-expiration-release-proposal-v1.md`
