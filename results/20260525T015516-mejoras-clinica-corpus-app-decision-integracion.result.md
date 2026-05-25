---
id: 20260525T015516-mejoras-clinica-corpus-app-decision-integracion
job_id: 20260525T015516-mejoras-clinica-corpus-app-decision-integracion
created_at: 2026-05-25T01:59:19-03:00
created_by: personal-xh
status: completed
no_external_actions: true
no_secrets: true
---

# mejoras clinica corpus app decision integracion result

## summary

Primero incorporar gates deterministas y fixtures; despues corpus schema. Posponer cambios que sobrelegalicen textos clinicos o dependan de fallos secundarios no oficializados.

## matriz decision

| Decision | Item | Justificacion | Validacion |
|---|---|---|---|
| incorporar | route guard canonico | evita drift entre rutas | orquestador |
| incorporar | fixtures lumbares critical | cubre errores reales | Dr. Zanardi |
| incorporar | no invencion topografia/deficit/material | alto riesgo | Dr. Zanardi |
| incorporar | extraforaminal no interlaminar | bug clinico concreto | Dr. Zanardi |
| incorporar | hemostasia/recuento antes cierre | medico-legal | Dr. Zanardi |
| incorporar | corpus source_status | evita alucinacion juridica | asesor legal opcional |
| posponer | crawler jurisprudencial amplio | requiere tiempo y validacion | orquestador/legal |
| posponer | activar gates por fallos secundarios | falta copia oficial | asesor legal |
| descartar | citas legales en documento final | sobrelegaliza HC/parte | Dr. Zanardi |
| descartar | decision automatica de acciones externas | fuera de autoridad | orquestador |

## recommendation

Roadmap clinico inmediato:

1. Congelar ruta canonica.
2. Agregar 60 casos sinteticos como regression suite.
3. Convertir corpus en schema fuente/gate.
4. Revisar con Dr. Zanardi solo gates critical antes de tocar plantillas reales.

## confidence

Alta.

## evidence_paths

- `context/frentes_activos_resumen_20260525.md`
- `tmp/clinica_app_snapshot_review/docs/contrato_blindaje_redaccion_medicolegal_2026-05-24.md`
- `results/20260525T015336-simulacion-clinica-60-casos-columna-inconsistencias.cases.json`
- `decisions/clinica_app_improvement_proposals/README.md`
