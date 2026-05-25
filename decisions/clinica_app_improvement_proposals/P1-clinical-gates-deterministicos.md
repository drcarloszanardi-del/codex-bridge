# P1 clinical gates deterministicos

## Objetivo

Agregar gates deterministas antes de enviar/generar documentos clinicos.

## Pseudopatch

```diff
+ gate no_inventar_topografia:
+   if input no contiene posterolateral/central/foraminal/extraforaminal:
+     output no puede contener esos terminos.
+
+ gate extraforaminal_no_interlaminar:
+   if input contiene hernia extraforaminal:
+     parte debe contener abordaje foraminal/extraforaminal o Wiltse
+     parte no puede contener espacio interlaminar, hemilaminotomia, flavectomia, hombro de raiz.
+
+ gate fijacion_sin_lateralidad_artrodesis:
+   if procedimiento es fijacion/artrodesis por nivel:
+     operacion no puede ser "artrodesis L4-L5 derecha/izquierda".
+
+ gate sin_descompresion_directa:
+   if input contiene "sin descompresion directa" o "solo fijacion":
+     parte no puede insertar laminectomia, flavectomia, liberacion radicular/recesos.
+
+ gate cierre_quirurgico:
+   hemostasia y recuento deben aparecer antes de cierre.
```

## Archivos objetivo en app real

- `app/product.html`
- `scripts/jarvis/clinical_document_handoff.js`
- `scripts/qa/validate_clinical_inconsistency_audit.js`
- `scripts/qa/validate_20_pathology_scenarios.js`

## Tests necesarios

- hernia extraforaminal L4-L5 derecha
- radiculopatia sin topografia de hernia
- fijacion L4-L5 sin descompresion directa
- artrodesis L4-L5 bilateral sin lateralidad de artrodesis
- parte con recuento despues de cierre
