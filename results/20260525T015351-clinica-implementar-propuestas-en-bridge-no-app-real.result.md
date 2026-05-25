---
id: 20260525T015351-clinica-implementar-propuestas-en-bridge-no-app-real
job_id: 20260525T015351-clinica-implementar-propuestas-en-bridge-no-app-real
created_at: 2026-05-25T01:59:19-03:00
created_by: personal-xh
status: completed
no_external_actions: true
no_secrets: true
---

# clinica implementar propuestas en bridge no app real result

## summary

Propuestas creadas en `decisions/clinica_app_improvement_proposals/`. No se modifico la app real de work-mac.

## proposals

- `P1-clinical-gates-deterministicos.md`: gates para topografia, extraforaminal, artrodesis sin lateralidad, sin descompresion directa, cierre.
- `P1-lumbar-test-pack-v1.md`: formato de fixtures clinicos lumbares.
- `P1-corpus-schema-gates.md`: separacion corpus fuente vs gates derivados.
- `P2-route-guard-contexto.md`: ruta canonica y bloqueo de generadores no canonicos.
- `README.md`: indice de propuestas.

## priority

1. Route guard canonico.
2. Fixtures lumbares v1.
3. Corpus schema con estados de fuente.
4. Gate de promocion fuente oficial -> gate activo.

## tests needed

- QA que falla si `app/app.js` genera documento enviable sin pasar por redaction shield.
- QA que falla si fuente secundaria intenta activar gate fuerte.
- QA de 60 casos sinteticos con severidad critical/high.

## confidence

Alta.

## evidence_paths

- `decisions/clinica_app_improvement_proposals/README.md`
- `decisions/clinica_app_improvement_proposals/P1-clinical-gates-deterministicos.md`
- `decisions/clinica_app_improvement_proposals/P1-lumbar-test-pack-v1.md`
- `decisions/clinica_app_improvement_proposals/P1-corpus-schema-gates.md`
- `decisions/clinica_app_improvement_proposals/P2-route-guard-contexto.md`
