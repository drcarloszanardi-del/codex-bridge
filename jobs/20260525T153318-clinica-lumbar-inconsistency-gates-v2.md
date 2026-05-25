---
id: 20260525T153318-clinica-lumbar-inconsistency-gates-v2
assignee: personal-xh
model: gpt-5.5-xh
created_at: 2026-05-25T15:33:18-03:00
front: CLINICA
no_external_actions: true
no_secrets: true
status: pending
---

# Workorder: CLINICA lumbar - gates contra inconsistencias graves v2

## 10 inicial - direccion del orquestador

- Objetivo: convertir las correcciones clinicas del Doctor en un set de gates, fixtures y reglas de redaccion que eviten errores en historia clinica, consentimiento y parte quirurgico de patologia lumbar.
- Prioridad: alta. El Doctor marco estos errores como inaceptables frente a su equipo.
- Alcance: razonamiento y especificacion implementable. No modificar la app real desde la Mac personal; entregar resultado para que Codex principal decida e integre.
- Contexto minimo a leer:
  - `context/fronts/clinica.md`
  - `results/20260525T015336-simulacion-clinica-60-casos-columna-inconsistencias.result.md`
  - `results/20260525T120000-clinica-fixtures-lumbares-v1.result.md`
  - `results/20260525T122941-clinica-correcciones-a-fixtures-implementacion.result.md`
  - `results/20260525T124545-clinica-corpus-gates-backlog-v2.result.md`
- Herramientas permitidas: leer archivos locales del bridge, razonar, sintetizar, proponer fixtures/gates y ejemplos de salida esperada.
- Herramientas prohibidas: acciones externas, Telegram, emails, compras, secretos, credenciales, datos de pacientes, ObraCash contenido, Drive/iCloud/Photos.

## Problemas clinicos que deben quedar cubiertos

- No inventar diagnosticos: "hernia posterolateral derecha" no puede aparecer si el caso no la declara.
- Degenerativa vs istmica: si el Doctor declara espondilolistesis degenerativa, no mezclar con istmica.
- Diagnostico vs indicacion: no incluir "con indicacion de descompresion/instrumentacion" como diagnostico.
- Canal estrecho: evitar tautologias como "canal estrecho con compromiso del canal".
- Consentimiento L4-L5: fijacion instrumentada y artrodesis L4-L5 no llevan lateralidad "derecha"; la lateralidad aplica a sintomas/abordaje/descompresion si corresponde.
- Descompresion directa: si el caso dice sin descompresion directa, no generar laminectomia/hemilaminectomia, flavectomia ni liberacion directa.
- Hernia extraforaminal: no abordar como interlaminar ni describir flavectomia/recesos laterales como si fuera central/lateral.
- PLIF/implantes: no duplicar PLIF; materiales como sustituto oseo/drill deben integrarse con orden quirurgico logico.
- Parche dural: si aplica como refuerzo sobre zona dural expuesta, no ubicarlo despues del cierre.
- Hemostasia y recuento: deben ocurrir antes del cierre por planos/piel, no al final como control posterior.
- Repeticiones: evitar duplicacion de posicionamiento/proteccion ocular/acolchado.

## 80 delegado - trabajo del agente

Pablo debe producir estas secciones:

- `canonical_case_axes`: variables canonicas necesarias para no inventar diagnostico, indicacion, lateralidad, abordaje, tecnica y hallazgos.
- `forbidden_phrases_by_context`: frases prohibidas y razon clinica/medicolegal.
- `positive_templates`: redacciones seguras por contexto: consentimiento, parte quirurgico e historia clinica.
- `fixture_matrix`: al menos 12 casos sinteticos, incluyendo extraforaminal, canal estrecho, espondilolistesis degenerativa con/sin descompresion directa, PLIF, fijacion L4-L5 y parche dural.
- `gate_rules`: reglas deterministicas detect-only con ejemplo de regex/AST/JSON path cuando corresponda.
- `expected_failures`: ejemplos que deben fallar con mensaje claro.
- `integration_plan`: donde deberia integrarlo Codex principal en la app real y como verificar sin tocar produccion.

Separar evidencia clinica, inferencia del caso y opinion. No cerrar con "no pude"; si falta contexto, proponer una regla conservadora y declarar la incertidumbre.

## 10 final - retorno al orquestador

El resultado debe incluir:

- `summary honesto`
- `coverage_table`
- todas las secciones del bloque delegado
- `risks / limits`
- `recommendation`
- `confidence`
- `evidence_paths`

Validar contra `scripts/validate_result_contract.py` antes de marcar completado.
