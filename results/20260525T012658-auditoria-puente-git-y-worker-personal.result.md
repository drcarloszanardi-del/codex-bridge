---
id: 20260525T012658-auditoria-puente-git-y-worker-personal
job_id: 20260525T012658-auditoria-puente-git-y-worker-personal
created_at: 2026-05-25T01:28:31-03:00
created_by: personal-xh
status: completed
no_external_actions: true
no_secrets: true
---

# auditoria puente git y worker personal result

## summary

El puente Git es una buena base: simple, auditable, asincronico y sin depender de IP local ni Telegram. Ya funciona para handshake, pull, push y resultados. Para convertirlo en worker autonomo de baja friccion faltan tres piezas: claim/idempotencia, sync con retry ante colisiones y validacion minima de secretos/formato.

## findings

- P1: `jobs/`, `results/`, `status/`, `decisions/` y `tmp/` separan bien entrada, salida y estado. Evidencia: `protocol.md` define el flujo y `README.md` define la estructura.
- P1: El repo ya evita secretos basicos con `.gitignore` para `secrets/`, `private/`, `*.log`, `*.tmp`. Falta un chequeo antes de commit para patrones obvios como tokens, private keys y dumps sensibles.
- P1: Hay riesgo de colision de commits si ambos agentes publican al mismo tiempo. El protocolo debe exigir `git pull --rebase` antes de push y retry automatico si el push falla.
- P1: Falta mecanismo explicito de claim. Hoy un job se considera pendiente si no existe `results/<job_id>.result.md`; funciona con un solo worker, pero con varios workers conviene agregar `status/claims/<job_id>.json` o claim por commit.
- P2: `scripts/bridgectl.py list-jobs --pending` no filtra por `assignee`. En cuanto haya mas workers, puede listar trabajos de otros.
- P2: `status/<worker>.json` es util para heartbeat, pero no debe ser la unica fuente de verdad. La fuente de verdad del resultado debe seguir siendo `results/<job_id>.result.md`.
- P2: `tmp/` existe en el repo. Conviene mantener solo `tmp/.gitkeep` versionado e ignorar todo lo demas dentro de `tmp/`.

## changes recommended

- Agregar `scripts/personal_xh_check.sh` como comando unico de revision local.
- Agregar `WORKER_PERSONAL_XH.md` con reglas y ciclo operativo.
- Cambiar el sync operativo a: `git pull --rebase`, procesar, `git add`, `git commit`, `git push`; si falla push, repetir pull rebase y push.
- Extender `bridgectl.py list-jobs` con `--assignee personal-xh`.
- Agregar `scripts/secret_scan.py` o pre-commit manual que bloquee claves privadas, tokens y credenciales obvias.
- Agregar template de resultado para normalizar `summary`, `findings`, `recommendation`, `confidence`, `evidence_paths`.

## minimal worker protocol

```bash
cd /Users/carloszanardi/Documents/Codex/codex-bridge
git pull --rebase
python3 scripts/bridgectl.py list-jobs --pending
# procesar solo jobs assignee=personal-xh sin resultado existente
# escribir results/<job_id>.result.md
# actualizar status/personal-xh.json
git add results status
git commit -m "Complete <job_id>"
git push || (git pull --rebase && git push)
```

## recommendation

Mantener Git como puente canonico. No montar Telegram como canal de resultados entre agentes. Telegram puede crear tareas, pero el intercambio entre Codex debe quedar en Git para auditoria, contexto persistente y recuperacion ante fallos.

## confidence

Alta.

## evidence_paths

- `protocol.md`
- `README.md`
- `.gitignore`
- `scripts/bridgectl.py`
- `WORKER_PERSONAL_XH.md`
- `scripts/personal_xh_check.sh`
