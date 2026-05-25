---
id: 20260525T015501-mejoras-mail-triage-obracash-pc-infra-seguridad
job_id: 20260525T015501-mejoras-mail-triage-obracash-pc-infra-seguridad
created_at: 2026-05-25T01:59:19-03:00
created_by: personal-xh
status: completed
no_external_actions: true
no_secrets: true
---

# mejoras mail triage obracash pc infra seguridad result

## summary

Mail y ObraCash deben ser frentes de bajo riesgo: clasificar, alertar y proteger, no actuar. PC/infra debe priorizar backup, restore probado y separacion de credenciales.

## mail triage

- Clasificar: urgente clinico/legal, administrativo, financiero, personal, spam.
- Extraer: remitente, asunto, fecha, accion sugerida, riesgo, deadline.
- Nunca responder automaticamente.
- Gate de privacidad: no copiar cuerpos completos al bridge salvo sanitizacion.

## ObraCash

- Permitido: backup, integridad, hashes, restore drill, alertas de alteracion.
- Prohibido: tocar gastos, registros, categorias, importes, comprobantes, saldos o historial.
- Runbook: backup diario, snapshot semanal, restore mensual en copia aislada.
- Control: hash de archivos criticos y reporte si cambia fuera de ventana esperada.

## PC/infra

- Inventario: hardware, discos, backups, modelos locales, versiones.
- Separar: credenciales en llavero/secret manager, no en scripts.
- Bridge: Git como canal auditado; Telegram solo input.
- Modelos locales: usar para clasificacion/resumen no sensible; XH para decisiones/auditorias.

## alertas

- Backup fallido.
- Restore no probado >30 dias.
- Cambio inesperado en ObraCash.
- Mail clinico/legal urgente sin clasificar.
- Credencial detectada en repo.

## confidence

Alta.

## evidence_paths

- `context/frentes_activos_resumen_20260525.md`
- `AUTHORITY_POLICY.md`
