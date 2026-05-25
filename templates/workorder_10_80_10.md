---
id: <job_id>
assignee: personal-xh
model: gpt-5.5-xh
created_at: <ISO-8601>
no_external_actions: true
no_secrets: true
status: pending
---

# Workorder: <title>

## 10 inicial - direccion del orquestador

- Objetivo:
- Frente:
- Contexto minimo:
- Archivos o carpetas permitidas:
- Herramientas permitidas:
- Herramientas prohibidas:
- Riesgos:
- Criterio de terminado:

## 80 delegado - trabajo del agente

El agente debe:

- leer las fuentes indicadas;
- declarar coverage real;
- separar evidencia, inferencia y opinion;
- intentar rutas alternativas razonables antes de reportar bloqueo;
- no pedir Drive/Gmail/credenciales si el paquete local ya contiene el material necesario;
- no ejecutar acciones externas;
- no modificar datos operativos salvo permiso expreso del orquestador.

## 10 final - retorno al orquestador

El resultado debe incluir estas secciones:

- `summary honesto`
- `source_counts` o `coverage_table`
- `findings`
- `attempted_routes`
- `execution_backlog`
- `recommendation`
- `risks / limits`
- `next_action_if_blocked`
- `confidence`
- `evidence_paths`

## Regla de salida

Si falta evidencia o coverage, el resultado debe decirlo. Si hay bloqueo, debe venir con causa, intentos y proxima accion concreta, no como cierre vacio.
