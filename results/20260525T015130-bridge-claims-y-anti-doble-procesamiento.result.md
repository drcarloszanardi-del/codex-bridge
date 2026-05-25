---
id: 20260525T015130-bridge-claims-y-anti-doble-procesamiento
job_id: 20260525T015130-bridge-claims-y-anti-doble-procesamiento
created_at: 2026-05-25T01:59:19-03:00
created_by: personal-xh
status: completed
no_external_actions: true
no_secrets: true
---

# bridge claims y anti doble procesamiento result

## summary

Implementado mecanismo simple de claims en `claims/<job_id>.json`, comando `bridgectl.py claim --job-id --assignee` y filtro `list-jobs --available`.

## files changed

- `scripts/bridgectl.py`: agrega `CLAIMS`, lectura de frontmatter/claim, comando `claim`, filtro `--available`, y sync incluyendo `claims/`.
- `claims/.gitkeep`: versiona carpeta de claims.
- `scripts/personal_xh_check.sh`: lista pendientes disponibles para `personal-xh`.
- `README.md`, `protocol.md`, `WORKER_PERSONAL_XH.md`: documentan claim antes de trabajar.

## commands

```bash
PYTHONPYCACHEPREFIX=/private/tmp/codex-bridge-pycache python3 -m py_compile scripts/bridgectl.py scripts/secret_scan.py
python3 scripts/bridgectl.py list-jobs --pending --assignee personal-xh --available
python3 scripts/bridgectl.py claim --job-id 20260525T015130-bridge-claims-y-anti-doble-procesamiento --assignee personal-xh
python3 scripts/secret_scan.py
```

## findings

- El claim es atomico localmente por `O_CREAT|O_EXCL`; reduce doble procesamiento entre workers.
- El claim no reemplaza el control final por existencia de `results/<job_id>.result.md`.
- Si dos workers hacen claim simultaneo y luego push colisiona, debe ganar el primer claim publicado; el segundo debe hacer `git pull --rebase` y respetar claim ajeno.

## risks

- No hay expiracion automatica de claims stale.
- No hay comando `release` todavia.
- Si un worker crea claim pero muere antes de pushear, el orquestador debe decidir si borra o reasigna el claim.

## recommendation

Agregar luego `claim --force --reason` solo para orquestador y campo `expires_at` opcional para claims de baja criticidad.

## confidence

Alta.

## evidence_paths

- `scripts/bridgectl.py`
- `claims/20260525T015130-bridge-claims-y-anti-doble-procesamiento.json`
- `protocol.md`
- `README.md`
- `WORKER_PERSONAL_XH.md`
