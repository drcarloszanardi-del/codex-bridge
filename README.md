# codex-bridge

Puente asincronico por Git entre Codex orquestador y Codex auxiliar.

Objetivo: coordinar trabajo entre Macs sin depender de IP local, Telegram, AirDrop ni tokens en comandos.

## Estructura

- `jobs/`: pedidos de trabajo.
- `results/`: respuestas a pedidos.
- `status/`: heartbeats y estado operativo por maquina/agente.
- `protocol.md`: reglas del intercambio.
- `scripts/bridgectl.py`: utilidades locales para crear jobs, listar pendientes, registrar status y sincronizar Git.

## Regla principal

No guardar credenciales, secretos, datos de pacientes identificables ni tokens en este repo.

Para datos sensibles, el job debe referir una ruta local segura y pedir revision manual del Codex orquestador.

