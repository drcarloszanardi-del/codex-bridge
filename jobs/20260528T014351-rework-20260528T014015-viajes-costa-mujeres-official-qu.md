---
id: 20260528T014351-rework-20260528T014015-viajes-costa-mujeres-official-qu
assignee: personal-xh
model: gpt-5.5-xh
created_at: 2026-05-28T01:43:51-03:00
front: VIAJES
no_external_actions: true
no_secrets: true
status: pending
---

# Workorder: corregir resultado de Pablo rechazado por QA

## 10 inicial - direccion del orquestador

- Objetivo: Revisar y corregir `20260528T014015-viajes-costa-mujeres-official-quote-request-pack-v1` porque el resultado no paso el contrato minimo del bridge.
- Frente: VIAJES
- Resultado a corregir: `results/20260528T014015-viajes-costa-mujeres-official-quote-request-pack-v1.result.md`
- Herramientas permitidas: leer archivos del bridge, corregir el resultado y explicar cambios.
- Herramientas prohibidas: acciones externas, compras, mails, Telegram, secretos, credenciales, datos sensibles no sanitizados.

## Errores de validacion

- missing required section: recommendation
- missing required section: confidence
- missing coverage section: coverage_table or source_counts

## 80 delegado - trabajo del agente

Entregar un nuevo resultado completo que resuelva esos errores. No cerrar con `no pude` sin rutas alternativas, limite exacto y proxima accion. Separar evidencia, inferencia y opinion.

## 10 final - retorno al orquestador

El resultado debe incluir:

- `summary honesto`
- `coverage_table` o `source_counts`
- secciones pedidas por el job original
- `risks / limits`
- `recommendation`
- `confidence`
- `evidence_paths`

Validar contra `scripts/validate_result_contract.py` antes de marcarlo completado.
