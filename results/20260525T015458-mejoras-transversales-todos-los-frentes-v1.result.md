---
id: 20260525T015458-mejoras-transversales-todos-los-frentes-v1
job_id: 20260525T015458-mejoras-transversales-todos-los-frentes-v1
created_at: 2026-05-25T01:59:19-03:00
created_by: personal-xh
status: completed
no_external_actions: true
no_secrets: true
---

# mejoras transversales todos los frentes v1 result

## summary

Mejor patron transversal: convertir cada frente en pipeline con intake estructurado, artefactos canonicos, QA, decision boundary y reporte. Evitar que Telegram o chats sueltos sean la memoria.

## table

| Frente | Mejora | Impacto | Costo | Riesgo | Dependencia | Autorizacion | Prioridad |
|---|---|---|---|---|---|---|---|
| Telegram/contexto | Router events/jobs/runs | menos mezcla | medio | bajo | job store | no | P1 |
| Clinica | Gates deterministas + fixtures | baja riesgo medico-legal | medio | medio | validacion Dr. | si para produccion | P0 |
| Corpus juridico | Schema fuente/gate/review | menos alucinacion | medio | bajo | fuentes oficiales | legal para activar | P1 |
| Tesis | Registro de decisiones metodologicas | trazabilidad | bajo | bajo | borrador base | no | P2 |
| Inmobiliaria | Scorecard comparable por propiedad | evita informes pobres | medio | medio | fuentes mercado | no compra | P2 |
| Inversiones/instrumental | Score reputacion/precio/riesgo | reduce errores de compra | medio | medio | fuentes oficiales/mercado | si compra/contacto | P2 |
| Reels/CMP | QA datos publicos y estilo | evita publicar datos mal | bajo | medio | brand sheet | si publica | P1 |
| Presentaciones | Deck brief + checklist visual | calidad estable | bajo | bajo | templates | no | P2 |
| ObraCash | Backup/restore/integridad pasivo | seguridad | medio | alto si toca datos | policy estricta | si contenido | P0 |
| Mail triage | Clasificador sin respuesta automatica | foco | medio | alto privacidad | reglas | si responder | P1 |
| PC/infra | Inventario + backup + modelos locales | robustez 24/7 | medio | medio | hardware | si instala | P1 |
| Arquitectura 24/7 | Orquestador + workers + reportes | escala | alto | medio | bridge | no para diseno | P1 |

## top 10

1. Router canonico para Telegram.
2. Fixtures clinicos lumbares critical.
3. Secret/data scanner para bridge y snapshots.
4. Corpus schema con estados de confiabilidad.
5. Decision log por frente.
6. Reporte diario unico: done/blocked/needs approval.
7. ObraCash backup/restore sin tocar contenido.
8. QA de datos publicos CMP antes de publicar.
9. Scorecards para inmobiliaria/instrumental.
10. Matriz herramienta/modelo por tipo de tarea.

## recommendation

Priorizar seguridad/contexto antes de productividad visible. El orquestador debe integrar solo artefactos con evidencia y decision boundary.

## confidence

Alta.

## evidence_paths

- `context/frentes_activos_resumen_20260525.md`
- `AUTHORITY_POLICY.md`
- `protocol.md`
