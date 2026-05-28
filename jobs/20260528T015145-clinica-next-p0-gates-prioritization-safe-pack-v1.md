---
id: 20260528T015145-clinica-next-p0-gates-prioritization-safe-pack-v1
created_at: 2026-05-28T01:51:45-03:00
created_by: orchestrator
assignee: personal-xh
front: CLINICA
model: gpt-5.5-xh
reasoning_effort: xhigh
status: queued
no_external_actions: true
no_secrets: true
---

# clinica-next-p0-gates-prioritization-safe-pack-v1

## Objetivo

Pablo, preparar una priorizacion segura del proximo P0 clinico documental, sin tocar archivos operativos ni plantillas finales.

## Contexto

Ya estan integrados localmente en detect-only/report-only:

- `no_inventar_diagnostico_topografia`
- `sin_descompresion_directa_bloqueante`
- `extraforaminal_no_interlaminar`
- `diagnostico_separado`
- `datos_sensibles_minimizados`
- `historia_clinica_minima`
- `consistencia_diagnostico_indicacion_procedimiento`
- `consentimiento_especifico_source_pack`
- `hemostasia_secuencia`
- `ayudantes_no_duplicar_cirujano`
- `trazabilidad_implantes_materiales`

## Alcance permitido

- Revisar solo resultados previos del bridge y contexto declarativo.
- No leer historias clinicas reales, adjuntos, Drive, iCloud, Photos ni datos personales.
- No tocar app real ni editar validadores.
- No enviar Telegram ni mails.

## Entregable esperado

1. Proponer 3 candidatos P0 siguientes, ordenados por riesgo medico-legal.
2. Para cada candidato: objetivo, ejemplo de falso positivo/negativo, fixture minimo, criterio detect-only y riesgo de implementacion.
3. Recomendar solo uno para el proximo ciclo.
4. Marcar si alguno requiere autorizacion humana o material real antes de avanzar.

## Reglas

- No inventar clinica ni usar datos de pacientes.
- No tocar plantillas finales.
- No abrir bibliotecas completas.
- No cerrar con "no pude"; si falta evidencia, proponer fixture sintetico seguro.
- La decision final queda en Codex orquestador.
