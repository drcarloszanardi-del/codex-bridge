---
job_id: 20260525T103949-anti-informe-vacio-qa-radares-v1
worker: personal-xh
status: completed
completed_at: 2026-05-25T10:47:50-03:00
front: CODEX-OPS
---

# Result

## summary

Propuesta de gate QA para impedir radares vacios o respuestas tipo "NO PUEDO". El radar solo puede cerrar `completed` si trae candidatos, fuentes intentadas, rutas alternativas, comparables, pendientes y proxima accion. Si no llega al minimo, debe cerrar `blocked` o `needs_review`, con evidencia y ruta concreta.

## findings con evidencia

- El job de rescate explicita que una pagina bloqueada no puede ser respuesta final.
- Los radares de inversiones/inmobiliaria/instrumental requieren datos externos publicos y triangulacion; un solo bloqueo no prueba ausencia de oportunidad.
- Ya hay datos suficientes para definir formato: fuente directa, snippet, PDF, marketplace, comparable, decision operativa y pendiente concreto.

## formato obligatorio de reporte

Todo resultado de radar debe incluir:

```markdown
## summary
## fuentes intentadas
## rutas alternativas usadas
## candidatos
## comparables
## descartes con motivo
## pendientes y ruta concreta
## decision recomendada
## confidence
```

Cada candidato debe tener:

```yaml
id:
titulo:
categoria:
fuente_url:
evidence_type: direct_page | snippet | pdf | marketplace | official | comparable
precio:
ubicacion_o_item:
m2_o_specs:
motivo_oportunidad:
comparables:
riesgos:
decision: investigar | descartar | pedir_aprobacion | watchlist
next_action:
verified_at:
```

## criterios de rechazo automatico

Rechazar `completed` si se cumple cualquiera:

- Contiene "NO PUEDO", "no pude", "no encontre nada" o equivalente sin seccion de rutas alternativas.
- Tiene menos de 5 fuentes intentadas para radar amplio.
- Tiene menos de 2 rutas alternativas cuando hubo bloqueo de fuente.
- Tiene 0 candidatos y no explica universo revisado con evidencia.
- Tiene candidatos sin link/fuente.
- Tiene candidatos sin precio o sin "pendiente de precio" + ruta concreta.
- Tiene candidatos sin decision operativa.
- No incluye comparables.
- No incluye pendientes y proxima accion.
- Mezcla compra/contacto/login con solo lectura.
- Para productos medicos: no incluye riesgo regulatorio/ANMAT cuando aplica.

## minimos por tipo de radar

### Inmobiliaria

- Minimo 6 fuentes intentadas o 4 fuentes + 2 snippets/PDFs.
- Minimo 5 candidatos o 3 candidatos fuertes + 3 descartes documentados.
- Cada candidato: precio, direccion/zona, m2 si existe, motivo de oportunidad, duda principal y decision.
- Comparables por zona/precio.
- Si es "radio 12 cuadras", indicar distancia confirmada o "radio pendiente".

### Instrumental / productos medicos

- Minimo 5 fuentes: local, marketplace, fabricante/distribuidor local, China/B2B, regulatoria.
- Minimo 6 items en matriz.
- Separar instrumental reusable de implantes.
- Incluir riesgo: calidad, esterilizacion, trazabilidad, registro, garantia, usado/nuevo.
- Implantes sin ANMAT/importador habilitado no pueden quedar en "comprar"; solo `watchlist` o `descartar`.

### Otros radares de inversion

- Minimo 5 fuentes.
- Minimo 3 candidatos o explicacion de mercado agotado.
- Cada candidato debe tener costo/riesgo/proxima accion.

## scoring sugerido

```text
100 puntos
- 20 fuentes suficientes
- 20 candidatos suficientes
- 15 comparables
- 15 decisiones operativas
- 10 pendientes concretos
- 10 manejo de bloqueos
- 10 riesgos/regulatorio

>= 75 completed
50-74 needs_review
< 50 blocked
```

## algoritmo

1. Parsear el markdown del resultado.
2. Detectar secciones obligatorias.
3. Contar fuentes y clasificarlas.
4. Contar candidatos.
5. Verificar campos minimos por candidato.
6. Buscar frases prohibidas tipo "no pude" sin justificacion.
7. Verificar que cada bloqueo tenga ruta alternativa.
8. Calcular score.
9. Si score < 75, no permitir status `completed`.

## propuesta de CLI

```bash
python3 scripts/qa/validate_radar_report.py results/<job_id>.result.md --kind inmobiliaria
python3 scripts/qa/validate_radar_report.py results/<job_id>.result.md --kind instrumental
python3 scripts/qa/validate_radar_report.py results/<job_id>.result.md --kind general
```

Salida esperada:

```json
{
  "ok": false,
  "score": 62,
  "status_required": "needs_review",
  "errors": [
    "candidatos: expected >=5 got 2",
    "missing comparables",
    "blocked source without alternative route"
  ]
}
```

## tests

- Reporte con "NO PUEDO" y sin fuentes alternativas falla.
- Reporte con 0 candidatos y 8 fuentes + pendientes concretos queda `needs_review`, no `completed`.
- Reporte inmobiliario con 5 candidatos, precios, links y comparables pasa.
- Reporte instrumental con implantes sin ANMAT y decision "comprar" falla.
- Reporte con fuente bloqueada pero snippets/PDF/comparables pasa si tiene candidatos.
- Reporte sin `next_action` por candidato falla.

## recommendation

Integrar el gate como paso obligatorio antes de commitear results de radares. Si falla, el worker debe publicar resultado `blocked` con score y faltantes, no un informe vacio. El objetivo no es forzar oportunidades falsas: es forzar evidencia, rutas alternativas y proxima accion concreta.

## confidence

High. Los criterios derivan directamente de los fallos observados y de los workorders de rescate.

## evidence_paths

- `jobs/20260525T103949-anti-informe-vacio-qa-radares-v1.md`
- `jobs/20260525T103407-rescate-radar-inversiones-sin-no-puedo-v1.md`
- `results/20260525T103407-rescate-radar-inversiones-sin-no-puedo-v1.result.md`
