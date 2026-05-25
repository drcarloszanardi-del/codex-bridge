# codex-bridge

Puente asincronico por Git entre Codex orquestador y Codex auxiliar.

Objetivo: coordinar trabajo entre Macs sin depender de IP local, Telegram, AirDrop ni tokens en comandos.

## Estructura

- `jobs/`: pedidos de trabajo.
- `claims/`: claims livianos para evitar doble procesamiento.
- `results/`: respuestas del worker.
- `status/`: heartbeats y estado operativo por maquina/agente.
- `decisions/`: decisiones acordadas.
- `tmp/`: archivos temporales no sensibles.
- `protocol.md`: reglas del intercambio.
- `scripts/bridgectl.py`: utilidades locales para crear jobs, listar pendientes, registrar status y sincronizar Git.
- `scripts/personal_xh_check.sh`: ciclo local de revision para el worker `personal-xh`.
- `scripts/personal_xh_poll_loop.sh`: loop opcional de monitoreo con log en `tmp/`.
- `templates/`: formatos normalizados para resultados.

## Regla principal

No guardar credenciales, secretos, datos de pacientes identificables ni tokens en este repo.

Para datos sensibles, el job debe referir una ruta local segura y pedir revision manual del Codex orquestador.

Antes de publicar cambios operativos, ejecutar:

```bash
python3 scripts/secret_scan.py
```

Para tomar un trabajo antes de procesarlo:

```bash
python3 scripts/bridgectl.py claim --job-id <job_id> --assignee personal-xh
```
