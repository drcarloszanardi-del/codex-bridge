# P1 corpus schema gates

## Objetivo

Separar corpus fuente de gates derivados.

## Propuesta

- `data/corpus/items/*.json`: fuente normativa/jurisprudencial/doctrinal.
- `data/corpus/gates/*.json`: regla verificable derivada.
- `data/corpus/review_queue/*.json`: candidato pendiente de fuente oficial o validacion legal.

## Regla de promocion

Ningun item del corpus modifica la app si no produce:

- gate detectable;
- ajuste de plantilla;
- frase prohibida/reemplazo seguro;
- faltante critico;
- cola de revision.

## Riesgo

No promover fallos de fuente secundaria como regla fuerte hasta obtener copia oficial o marcar `pending_official_copy`.
