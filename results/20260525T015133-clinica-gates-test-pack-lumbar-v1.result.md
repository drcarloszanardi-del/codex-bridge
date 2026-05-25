---
id: 20260525T015133-clinica-gates-test-pack-lumbar-v1
job_id: 20260525T015133-clinica-gates-test-pack-lumbar-v1
created_at: 2026-05-25T01:59:19-03:00
created_by: personal-xh
status: completed
no_external_actions: true
no_secrets: true
---

# clinica gates test pack lumbar v1 result

## summary

Paquete v1 propuesto para probar gates lumbares de alto riesgo medico-legal. Cubre topografia, raiz, abordaje, separacion diagnostico/indicacion, descompresion directa, cierre y duplicados.

## table

| id | input sintetico | esperado | prohibido | severidad | gate |
|---|---|---|---|---|---|
| LUM-001 | Hernia extraforaminal L4-L5 derecha. Microdiscectomia extraforaminal. | raiz L4, abordaje foraminal/extraforaminal | interlaminar, hemilaminotomia, flavectomia | critical | extraforaminal_no_interlaminar |
| LUM-002 | Hernia posterolateral L4-L5 izquierda. | radiculopatia L5 izquierda | raiz L4 | critical | habitual_root_by_level |
| LUM-003 | Radiculopatia L5 derecha sin topografia de hernia. | no inventar topografia | posterolateral, extraforaminal | critical | no_inventar_topografia |
| LUM-004 | Fijacion/artrodesis L4-L5. | artrodesis L4-L5 | artrodesis derecha | high | artrodesis_sin_lateralidad |
| LUM-005 | Fijacion L4-L5 sin descompresion directa. | no se realizo descompresion directa | laminectomia, flavectomia, liberacion radicular | critical | sin_descompresion_directa |
| LUM-006 | Parte con cierre antes de recuento. | bloquear | recuento despues del cierre | critical | recuento_antes_cierre |
| LUM-007 | Diagnostico: hernia L4-L5 con indicacion de microdiscectomia. | diagnostico puro | indicacion dentro de diagnostico | high | diagnostico_separado_indicacion |
| LUM-008 | PLIF L4-L5 repetido en tecnica y materiales. | una sola tecnica principal | duplicacion PLIF | high | no_duplicados |
| LUM-009 | Parche dural no informado. | no mencionar parche | parche dural inventado | critical | no_inventar_adjunto |
| LUM-010 | Durotomia informada con parche. | marca/lote si disponible o faltante critico | parche duplicado | high | adjunto_dural_trazable |

## json-like proposal

```json
[
  {"id":"LUM-001","input":"Hernia discal extraforaminal L4-L5 derecha. Microdiscectomia extraforaminal L4-L5 derecha.","expected":["raiz L4 derecha","abordaje foraminal/extraforaminal"],"forbidden":["espacio interlaminar","hemilaminotomia","flavectomia","raiz pasante"],"severity":"critical","gate":"extraforaminal_no_interlaminar"},
  {"id":"LUM-002","input":"Hernia discal posterolateral L4-L5 izquierda. Microdiscectomia tubular L4-L5 izquierda.","expected":["radiculopatia L5 izquierda","abordaje interlaminar/tubular compatible"],"forbidden":["raiz L4","extraforaminal"],"severity":"critical","gate":"habitual_root_by_level"},
  {"id":"LUM-003","input":"Radiculopatia L5 derecha. Descompresion radicular L4-L5 derecha. No se informa hernia.","expected":["radiculopatia","descompresion"],"forbidden":["hernia posterolateral","hernia extraforaminal","fragmento discal"],"severity":"critical","gate":"no_inventar_topografia"},
  {"id":"LUM-004","input":"Patologia degenerativa L4-L5. Fijacion transpedicular y artrodesis L4-L5 derecha por via Wiltse.","expected":["fijacion L4-L5","abordaje derecho si corresponde"],"forbidden":["artrodesis L4-L5 derecha"],"severity":"high","gate":"artrodesis_sin_lateralidad"},
  {"id":"LUM-005","input":"Fijacion L4-L5 sin descompresion directa, solo instrumentacion y artrodesis.","expected":["no se realizo descompresion neural directa"],"forbidden":["laminectomia","flavectomia","liberacion radicular"],"severity":"critical","gate":"sin_descompresion_directa"}
]
```

## recommendation

Agregar estos casos como fixtures estables y exigir que todo bug clinico real nuevo agregue fixture antes de corregirse.

## confidence

Alta.

## evidence_paths

- `jobs/20260525T015133-clinica-gates-test-pack-lumbar-v1.md`
- `tmp/clinica_app_snapshot_review/app/product.html`
- `tmp/clinica_app_snapshot_review/scripts/qa/validate_20_pathology_scenarios.js`
