---
id: 20260528T021145-clinica-evento-complicacion-manejo-detect-only-pack-v1
created_at: 2026-05-28T02:11:45-03:00
created_by: orchestrator
assignee: personal-xh
front: CLINICA
model: gpt-5.5-xh
reasoning_effort: xhigh
status: queued
no_external_actions: true
no_secrets: true
---

# clinica-evento-complicacion-manejo-detect-only-pack-v1

## Objetivo

Pablo, preparar el siguiente ciclo clinico P0 recomendado: `evento_complicacion_manejo_estado_final`, empezando en modo `detect-only/report-only`.

El foco inicial es parte quirurgico: evento dural/LCR/parche dural y sangrado relevante. La regla no debe inventar complicaciones ni bloquear documentos reales; solo debe marcar `needs_review` cuando el texto afirma una complicacion sin manejo/estado final, o cuando aparece reparacion/parche dural sin evento/source claro.

## Contexto

Usar como entrada principal:

- `results/20260528T015145-clinica-next-p0-gates-prioritization-safe-pack-v1.result.md`
- `results/20260527T183421-clinica-correcciones-a-fixtures-implementacion.result.md`
- `results/20260527T223530-clinica-protocolo-secuencia-hemostasia-detect-only-plan-v1.result.md`
- `results/20260527T230844-clinica-hemostasia-secuencia-postfixture-review-v2.result.md`
- `results/20260528T000957-clinica-trazabilidad-frontier-implementation-review-v1.result.md`

Gates ya integrados localmente en detect-only/report-only segun estado vigente:

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

- Revisar la app canonica solo si hace falta ubicar patrones de gates/fixtures:
  `/Users/jarvis/.openclaw/workspace/clinica/app-clinica-medicolegal`
- Leer solo archivos directamente relevantes a validadores, fixtures y tests clinicos.
- Preparar un pack implementable con nombres de archivos, fixtures y criterio de test.
- Si el cambio es pequeno y seguro en tu copia, proponer patch minimo; no tocar plantillas finales.
- No leer historias clinicas reales, adjuntos, Drive, iCloud, Photos, Gmail ni datos personales.
- No enviar Telegram ni mails.

## Entregable esperado

1. Confirmar si ya existe algun gate equivalente; si existe, auditar brechas y no duplicar.
2. Proponer fixture pack sintetico minimo:
   - `CLIN-P0-069-dural-event-without-management-review`
   - `CLIN-P0-070-no-dural-event-pass`
   - `CLIN-P0-071-patch-without-event-review`
   - `CLIN-P0-072-dural-event-managed-pass`
3. Definir lexicon inicial, negaciones locales y secciones excluidas para evitar falsos positivos en consentimiento/riesgos hipoteticos.
4. Definir resultado esperado `needs_review` o `pass`, siempre `detect-only/report-only`.
5. Indicar comando exacto de test/regresion recomendado y riesgo de falsos positivos.
6. Si hay patch propuesto, mantenerlo acotado a validadores/fixtures/tests y explicar por que es seguro.

## Reglas

- No convertir a hard block.
- No corregir ni reescribir el parte automaticamente.
- No inventar evento, manejo, material ni estado final.
- No analizar consentimientos/riesgos hipoteticos como evento ocurrido.
- Si falta evidencia, dejarlo como `needs_review`, no como afirmacion clinica.
- La integracion final queda a cargo de Codex orquestador en la Mac de trabajo.
