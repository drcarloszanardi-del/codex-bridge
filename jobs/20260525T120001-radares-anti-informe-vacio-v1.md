---
id: 20260525T120001-radares-anti-informe-vacio-v1
assignee: personal-xh
model: gpt-5.5-xh
created_at: 2026-05-25T12:00:01-03:00
no_external_actions: true
no_secrets: true
status: pending
---

# Workorder: gate anti informe vacio para inmobiliaria e instrumental

## 10 inicial - direccion del orquestador

- Objetivo: disenar un gate implementable para que los radares no reporten "no pude" o cero oportunidades sin evidencia, rutas alternativas y proxima accion.
- Frente: INMOBILIARIA / INVERSIONES-INSTRUMENTAL.
- Contexto minimo:
  - Contexto de frente: `context/fronts/radares.md`.
  - Decisiones existentes: `decisions/radar_scorecards_v1.md`.
  - Claims previos utiles: `claims/*radar*`, `claims/*inmobiliaria*`, `claims/*instrumental*`, `claims/*anti-informe-vacio*`.
  - El Doctor exige oportunidad real, no reporte vacio. Si una web falla, se prueban rutas alternativas o se delega.
- Herramientas permitidas: leer bridge repo y resultados previos; proponer schema/script; no navegar ni contactar terceros desde este job.
- Herramientas prohibidas: compras, mails, contacto a vendedores, credenciales, datos sensibles.
- Riesgos:
  - Declarar "no hay casas" cuando en realidad el barrido fallo.
  - Confundir producto/instrumental y creer que es negocio sin comparable real.
  - Enviar informe que obligue al Doctor a hacer manualmente lo que el agente debio resolver.
- Criterio de terminado: schema de salida, criterios de bloqueo, intentos alternativos obligatorios, thresholds minimos y plan de integracion en scripts.

## 80 delegado - trabajo del agente

Pablo debe producir:

- contrato de reporte minimo por radar;
- lista de fuentes y rutas alternativas esperables;
- reglas para distinguir "cero oportunidades reales" vs "barrido degradado";
- scorecard de oportunidad inmobiliaria;
- scorecard de instrumental/reventa;
- plan para que 5.3 ejecute rutina y Pablo solo reciba casos dificiles;
- propuesta de archivos/scripts a tocar en la Mac de trabajo.

## 10 final - retorno al orquestador

El resultado debe incluir:

- `summary honesto`
- `source_counts` o `coverage_table`
- `radar_contract`
- `anti_empty_gate`
- `fallback_routes`
- `scorecards`
- `implementation_plan`
- `risks / limits`
- `recommendation`
- `confidence`
- `evidence_paths`

Validar el resultado contra `scripts/validate_result_contract.py` antes de marcarlo completado.
