---
id: 20260525T120000-clinica-fixtures-lumbares-v1
assignee: personal-xh
model: gpt-5.5-xh
created_at: 2026-05-25T12:00:00-03:00
no_external_actions: true
no_secrets: true
status: pending
---

# Workorder: fixtures clinicos lumbares desde correcciones del Doctor

## 10 inicial - direccion del orquestador

- Objetivo: convertir las correcciones clinicas del Doctor Zanardi en fixtures/gates concretos para la app medico-legal, sin tocar la app real desde este worker.
- Frente: CLINICA / app medico-legal.
- Contexto minimo:
  - App canonica en la Mac de trabajo: `/Users/jarvis/.openclaw/workspace/clinica/app-clinica-medicolegal`.
  - Snapshot disponible si aplica: `context/clinica_app_snapshot_20260525T0155.tar.gz`.
  - Contexto de frente: `context/fronts/clinica.md`.
  - Resultado esperado: especificacion implementable con casos, inputs, asserts y archivos sugeridos.
- Correcciones criticas del Doctor que deben transformarse en test:
  - Hernia extraforaminal no debe usar abordaje interlaminar, hemilaminotomia/flavectomia ni "hombro de raiz" como secuencia principal.
  - Hernia extraforaminal L4-L5 derecha compromete raiz L4, no L5.
  - Si el caso dice "sin descompresion directa", no puede aparecer laminectomia/hemilaminectomia/flavectomia/liberacion directa como hecho operatorio.
  - Fijacion L4-L5 no debe decir "L4-L5 derecha" como artrodesis/fijacion derecha; la lateralidad aplica al abordaje/sintoma/raiz, no al segmento instrumentado.
  - En fijacion, "descompresion" y "recalibraje" no deben duplicarse como sinonimos; permitir "fijacion instrumentada y artrodesis L4-L5 con o sin descompresion segun situacion" si el caso no define directa.
  - Diagnostico no debe incluir "con indicacion de descompresion/instrumentacion"; indicacion no es diagnostico.
  - No inventar hernia posterolateral derecha si el caso no la menciona.
  - No transformar espondilolistesis degenerativa en degenerativa o istmica si el Doctor especifico degenerativa.
  - Evitar frase tautologica "canal estrecho lumbar con compromiso del canal".
  - Posicion/proteccion ocular/puntos de apoyo no debe duplicarse en el parte.
  - Hemostasia y recuento van antes del cierre de piel, no como cierre administrativo posterior.
  - PLIF/implantes/materiales no deben duplicarse.
  - Parche dural/refuerzo no debe aparecer al final despues del cierre; solo si fue indicado y en secuencia quirurgica correcta.
- Herramientas permitidas: leer snapshot, docs, results y propuestas previas del bridge; no usar secretos; no accionar externo.
- Herramientas prohibidas: enviar Telegram, tocar datos de ObraCash, modificar app real, inventar criterio clinico nuevo no derivado del Doctor.
- Riesgos: repetir errores clinicos en documentos que se muestren al equipo; sobreajustar plantillas a un caso puntual.
- Criterio de terminado: resultado con coverage, fixture matrix, suggested test names, expected failing phrases, expected passing language, risk notes y next implementation steps.

## 80 delegado - trabajo del agente

Pablo debe revisar el contexto disponible y producir:

- matriz de fixtures por patologia/situacion;
- asserts negativos y positivos;
- reglas que son universales vs reglas condicionadas por input;
- propuesta de ubicacion de archivos/tests;
- orden de implementacion por riesgo;
- exclusion_log de lo que no se puede inferir sin app real.

## 10 final - retorno al orquestador

El resultado debe incluir:

- `summary honesto`
- `source_counts` o `coverage_table`
- `fixture_matrix`
- `negative_asserts`
- `positive_asserts`
- `implementation_plan`
- `risks / limits`
- `recommendation`
- `confidence`
- `evidence_paths`

Validar el resultado contra `scripts/validate_result_contract.py` antes de marcarlo completado.
