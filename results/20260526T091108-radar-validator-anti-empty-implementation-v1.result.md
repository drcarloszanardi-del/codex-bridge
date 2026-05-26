# Resultado - 20260526T091108-radar-validator-anti-empty-implementation-v1

## summary

Diseno portable para implementar un validator anti informe vacio de radares. El objetivo no es forzar oportunidades falsas: es impedir que un radar cierre como final cuando solo tiene errores tecnicos, fuentes bloqueadas, candidatos sin evidencia o conclusiones sin comparables.

El validador debe correr localmente antes de que el orquestador acepte un resultado de inmobiliaria, inversiones, instrumental o viajes. Si falla, devuelve `blocked` o `needs_review` con faltantes accionables; nunca convierte una pagina caida o una busqueda parcial en una conclusion sobre el mercado.

## source_counts

| Fuente permitida | Estado | Uso |
| --- | ---: | --- |
| `results/20260526T065253-radares-source-recovery-playbook.result.md` | Revisada | Rutas de recuperacion, thresholds por frente y ban de lenguaje de fracaso tecnico. |
| `results/20260526T073800-batch-results-priority-triage-v1.result.md` | Revisada | Prioridad de integrar el validator como mejora local de bajo riesgo/alto impacto. |
| `results/20260525T103949-anti-informe-vacio-qa-radares-v1.result.md` | Revisada | Formato obligatorio, criterios de rechazo, scoring y tests minimos. |
| `results/20260525T234822-radares-hardening-anti-informe-vacio-v2.result.md` | Revisada | Reglas P0, contrato parseable, source recovery ladder y casos de regresion. |
| `protocol.md` | Revisado | Reglas duras: sin acciones externas, sin secretos, y bloqueo tecnico no es resultado final. |

## contract_input_output

Entrada CLI propuesta:

```bash
python3 scripts/qa/validate_radar_report.py results/<job_id>.result.md --kind inmobiliaria
python3 scripts/qa/validate_radar_report.py results/<job_id>.result.md --kind instrumental
python3 scripts/qa/validate_radar_report.py results/<job_id>.result.md --kind inversiones
python3 scripts/qa/validate_radar_report.py results/<job_id>.result.md --kind viajes
python3 scripts/qa/validate_radar_report.py results/<job_id>.result.md --kind general
```

Entrada minima parseable dentro del informe:

```yaml
radar_report:
  job_id: string
  kind: inmobiliaria | inversiones | instrumental | viajes | general
  scope:
    query: string
    geography_or_market: string
    constraints: [string]
  sources_attempted:
    - name: string
      type: direct_page | marketplace | search | pdf | official | snippet | cache | comparable | local_context
      outcome: success | blocked | no_results | partial | error
      evidence: string
  fallback_routes_used:
    - failed_source: string
      route: string
      outcome: success | partial | failed
      evidence: string
  candidates:
    - title: string
      source: string
      price_or_value: string
      location_or_specs: string
      comparable_basis: [string]
      risks: [string]
      decision: investigar | watchlist | descartar | pedir_aprobacion
      next_action: string
  rejected_candidates:
    - title: string
      reason: string
  conclusion:
    recommendation: string
    confidence: low | medium | medium-high | high
    next_run_or_handoff: string
```

Salida JSON del validator:

```json
{
  "ok": false,
  "score": 62,
  "status_required": "needs_review",
  "hard_fails": ["missing_comparables"],
  "warnings": ["low_sources_for_broad_scope"],
  "counts": {
    "sources": 4,
    "fallbacks": 1,
    "candidates": 2,
    "rejected_candidates": 3,
    "comparables": 1
  },
  "next_action": "Agregar fuente secundaria y comparables antes de informe final."
}
```

Semantica:

| Campo | Regla |
| --- | --- |
| `ok=true` | Solo si `status_required=completed`, score >= 75 y cero hard fails. |
| `status_required=completed` | Informe final permitido localmente; decision final sigue en el orquestador. |
| `status_required=needs_review` | Borrador interno util; puede generar handoff o pedido humano, no informe final automatico. |
| `status_required=blocked` | No hay contrato minimo; debe volver a busqueda/fallback o registrar bloqueo accionable. |
| Exit code `0` | Gate pasa. |
| Exit code `1` | Needs review o blocked por calidad. |
| Exit code `2` | Input ilegible, ruta inexistente o schema roto. |

## hard_fails_blocking_doctor_send

Estos hard fails bloquean `completed` y bloquean envio al Doctor como informe final:

| Hard fail | Criterio |
| --- | --- |
| `technical_failure_as_conclusion` | Cierre basado en "no pude", "no encontre nada", "pagina no hallada", "mercado agotado" o equivalente sin rutas alternativas y evidencia. |
| `missing_required_sections` | Faltan fuentes, fallback, candidatos/descartes, comparables, recomendacion, confianza o proxima accion. |
| `zero_sources` | No hay fuentes intentadas. |
| `low_sources_broad_scope` | Radar amplio con menos de 5 fuentes/queries relevantes y sin justificacion de scope estrecho. |
| `blocked_source_without_fallback` | Fuente con outcome `blocked` o `error` sin ruta alternativa asociada. |
| `only_technical_errors` | Todas las fuentes son error/bloqueo y no hay cache, snippet, comparable, descarte ni handoff concreto. |
| `zero_candidates_without_universe` | Cero candidatos sin universo revisado, descartes y proxima corrida concreta. |
| `candidate_without_source` | Candidato sin fuente/evidencia. |
| `candidate_without_price_or_route` | Precio/valor ausente sin `pending_price` y ruta concreta. |
| `candidate_without_comparables` | Candidato positivo sin comparable o fundamento equivalente. |
| `candidate_without_decision` | Falta decision operativa: investigar, watchlist, descartar o pedir_aprobacion. |
| `candidate_without_next_action` | Falta siguiente accion concreta. |
| `medical_buy_without_traceability` | Instrumental/producto medico con decision `comprar` sin trazabilidad, regulatorio, soporte o compatibilidad cuando aplica. |
| `external_action_or_credentials` | Reporte propone login, contacto, compra, reserva, mensaje externo o uso de credenciales desde el worker. |
| `raw_technical_payload` | Informe final contiene diff, traceback, stack trace, logs internos o ruido tecnico. |

## warnings_internal_draft_only

Estos warnings permiten borrador interno, pero no deberian permitir informe final automatico si se acumulan o bajan score:

| Warning | Criterio |
| --- | --- |
| `partial_source_mix` | Hay fuentes, pero pocas categorias independientes. |
| `single_candidate` | Un solo candidato, aunque parezca fuerte. |
| `pending_price` | Falta precio pero hay ruta concreta. |
| `weak_comparable_basis` | Comparables genericos, viejos o no equivalentes. |
| `few_rejections` | No hay suficientes descartes para demostrar criterio. |
| `scope_ambiguous` | No queda claro mercado, radio, categoria o restricciones. |
| `needs_human_decision` | La siguiente accion exige autorizacion, material propio o criterio medico/comercial humano. |
| `instrumental_regulatory_pending` | Falta ANMAT/importador/lote/garantia/soporte en producto medico o equipo relevante. |
| `travel_time_sensitive` | Viajes: precio/disponibilidad puede vencer y requiere verificacion humana antes de actuar. |

## scoring_model

Score base de 100:

| Area | Puntos | Reglas |
| --- | ---: | --- |
| Fuentes suficientes | 20 | 5+ fuentes para scope amplio; mezcla de directa/marketplace/search/pdf/snippet/comparable. |
| Fallbacks | 15 | Cada fuente bloqueada tiene alternativa; fuentes principales idealmente dos rutas. |
| Candidatos o universo | 20 | Candidatos completos o, si cero, universo revisado con descartes y comparables. |
| Comparables | 15 | Comparables por zona/precio/specs/modelo/mercado. |
| Decisiones operativas | 10 | Cada candidato tiene decision y proxima accion. |
| Riesgos y pendientes | 10 | Riesgos concretos, pendientes con ruta y handoff claro. |
| Frente especifico | 10 | Inmobiliaria: zona/precio/m2; instrumental: marca/modelo/trazabilidad; inversiones/viajes: costo/riesgo/vencimiento. |

Mapeo:

| Score | Estado maximo |
| ---: | --- |
| 75-100 sin hard fails | `completed` |
| 50-74 | `needs_review` |
| 0-49 | `blocked` |

Hard fails siempre degradan a `blocked` salvo los siguientes, que pueden quedar en `needs_review` si hay evidencia parcial y next action claro: `single_candidate`, `pending_price`, `weak_comparable_basis`, `instrumental_regulatory_pending`.

## proposed_python_script

```python
#!/usr/bin/env python3
"""
Local QA gate for radar reports.

This script is intentionally dependency-light. It accepts markdown reports that
either include a radar_report YAML-ish block or at least the required markdown
sections used by the bridge results.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


REQUIRED_SECTIONS = {
    "summary": ("summary", "resumen"),
    "sources": ("fuentes intentadas", "sources_attempted", "fuentes"),
    "fallbacks": ("rutas alternativas usadas", "fallback_routes_used", "fallbacks"),
    "candidates": ("candidatos", "candidates"),
    "comparables": ("comparables", "comparable_basis"),
    "rejections": ("descartes", "rejected_candidates"),
    "next_action": ("pendientes y ruta concreta", "next_action", "proxima accion", "next_run_or_handoff"),
    "recommendation": ("decision recomendada", "recommendation", "recomendacion"),
    "confidence": ("confidence", "confianza"),
}

FAILURE_PHRASES = (
    "no pude",
    "no encontre nada",
    "no encontre nada",
    "pagina no hallada",
    "pagina no hallada",
    "la pagina no abre",
    "la pagina no abre",
    "mercado agotado",
    "sin oportunidades",
)

RAW_TECH_PATTERNS = (
    "traceback (most recent call last)",
    "stack trace",
    "exception:",
    "git diff",
    "@@ ",
    "fatal:",
)

DECISIONS = {"investigar", "watchlist", "descartar", "pedir_aprobacion"}


@dataclass
class Validation:
    score: int = 100
    hard_fails: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    counts: dict[str, int] = field(default_factory=dict)
    status_required: str = "completed"
    next_action: str = "Gate aprobado."

    def fail(self, code: str, penalty: int = 100) -> None:
        if code not in self.hard_fails:
            self.hard_fails.append(code)
        self.score = max(0, self.score - penalty)

    def warn(self, code: str, penalty: int = 5) -> None:
        if code not in self.warnings:
            self.warnings.append(code)
        self.score = max(0, self.score - penalty)


def normalize(text: str) -> str:
    return text.lower().replace("\r\n", "\n").replace("\r", "\n")


def section_present(text: str, aliases: Iterable[str]) -> bool:
    for alias in aliases:
        pattern = rf"(^|\n)#+\s+{re.escape(alias)}\b|(^|\n)\s*{re.escape(alias)}\s*:"
        if re.search(pattern, text, flags=re.IGNORECASE):
            return True
    return False


def count_list_items(text: str, section_aliases: Iterable[str]) -> int:
    section = extract_section(text, section_aliases)
    if not section:
        return 0
    bullet_count = len(re.findall(r"(?m)^\s*(?:[-*]|\d+\.)\s+", section))
    yaml_item_count = len(re.findall(r"(?m)^\s*-\s+(?:name|title|titulo|source|fuente|route|failed_source|reason)\s*:", section))
    pipe_rows = max(0, len(re.findall(r"(?m)^\s*\|.*\|\s*$", section)) - 2)
    return max(bullet_count, yaml_item_count, pipe_rows)


def extract_section(text: str, aliases: Iterable[str]) -> str:
    headings = list(re.finditer(r"(?m)^#{2,6}\s+(.+?)\s*$", text))
    lowered_aliases = tuple(a.lower() for a in aliases)
    for idx, match in enumerate(headings):
        title = match.group(1).strip().lower()
        if any(alias in title for alias in lowered_aliases):
            start = match.end()
            end = headings[idx + 1].start() if idx + 1 < len(headings) else len(text)
            return text[start:end]
    return ""


def has_failure_phrase_without_recovery(text: str) -> bool:
    has_phrase = any(phrase in text for phrase in FAILURE_PHRASES)
    if not has_phrase:
        return False
    recovery_words = ("fallback", "rutas alternativas", "fuentes intentadas", "comparables", "descartes", "next_action", "proxima accion")
    return not any(word in text for word in recovery_words)


def has_blocked_source_without_fallback(text: str) -> bool:
    source_blocked = bool(re.search(r"\b(blocked|bloquead[ao]|error|no_results|sin resultados)\b", text))
    fallback_count = count_list_items(text, REQUIRED_SECTIONS["fallbacks"])
    return source_blocked and fallback_count == 0


def has_medical_buy_without_traceability(text: str, kind: str) -> bool:
    if kind != "instrumental":
        return False
    buy_signal = bool(re.search(r"\b(comprar|compra directa|buy)\b", text))
    traceability = bool(re.search(r"\b(anmat|trazabilidad|importador|lote|garantia|soporte|registro)\b", text))
    return buy_signal and not traceability


def validate_report(path: Path, kind: str) -> Validation:
    if not path.exists() or not path.is_file():
        result = Validation(score=0, status_required="blocked", next_action="Ruta inexistente o no es archivo.")
        result.fail("input_path_missing", penalty=0)
        return result

    raw = path.read_text(encoding="utf-8")
    text = normalize(raw)
    v = Validation()

    missing = [name for name, aliases in REQUIRED_SECTIONS.items() if not section_present(text, aliases)]
    if missing:
        v.fail("missing_required_sections:" + ",".join(missing), penalty=25)

    sources = count_list_items(raw, REQUIRED_SECTIONS["sources"])
    fallbacks = count_list_items(raw, REQUIRED_SECTIONS["fallbacks"])
    candidates = count_list_items(raw, REQUIRED_SECTIONS["candidates"])
    rejections = count_list_items(raw, REQUIRED_SECTIONS["rejections"])
    comparables = count_list_items(raw, REQUIRED_SECTIONS["comparables"])
    v.counts = {
        "sources": sources,
        "fallbacks": fallbacks,
        "candidates": candidates,
        "rejected_candidates": rejections,
        "comparables": comparables,
    }

    broad_kinds = {"inmobiliaria", "instrumental", "inversiones", "viajes", "general"}
    if sources == 0:
        v.fail("zero_sources", penalty=30)
    elif kind in broad_kinds and sources < 5:
        v.fail("low_sources_broad_scope", penalty=18)

    if has_failure_phrase_without_recovery(text):
        v.fail("technical_failure_as_conclusion", penalty=30)

    if has_blocked_source_without_fallback(text):
        v.fail("blocked_source_without_fallback", penalty=20)

    if sources > 0 and candidates == 0 and rejections < 3 and comparables == 0:
        v.fail("zero_candidates_without_universe", penalty=25)

    if candidates > 0 and comparables == 0:
        v.fail("candidate_without_comparables", penalty=15)

    if candidates == 1:
        v.warn("single_candidate", penalty=10)

    if re.search(r"\bpending_price\b|\bprecio pendiente\b", text):
        v.warn("pending_price", penalty=5)

    if not any(decision in text for decision in DECISIONS):
        v.fail("candidate_without_decision", penalty=10)

    if "next_action" not in text and "proxima accion" not in text:
        v.fail("candidate_without_next_action", penalty=10)

    if any(pattern in text for pattern in RAW_TECH_PATTERNS):
        v.fail("raw_technical_payload", penalty=30)

    external_action = re.search(r"\b(login|credencial|password|contactar|comprar ahora|reservar|enviar telegram|gmail|drive)\b", text)
    if external_action:
        v.fail("external_action_or_credentials", penalty=30)

    if has_medical_buy_without_traceability(text, kind):
        v.fail("medical_buy_without_traceability", penalty=30)

    if kind == "inmobiliaria":
        if not re.search(r"\b(zona|direccion|radio|m2|superficie|lote)\b", text):
            v.fail("inmobiliaria_missing_location_or_specs", penalty=10)
    elif kind == "instrumental":
        if not re.search(r"\b(marca|modelo|version|fabricante)\b", text):
            v.fail("instrumental_missing_model_identity", penalty=10)
        if not re.search(r"\b(regulatorio|anmat|trazabilidad|soporte|garantia)\b", text):
            v.warn("instrumental_regulatory_pending", penalty=10)
    elif kind == "viajes":
        if not re.search(r"\b(fecha|disponibilidad|precio|vencimiento|politica)\b", text):
            v.warn("travel_time_sensitive_fields_missing", penalty=10)

    v.score = max(0, min(100, v.score))
    if v.hard_fails:
        v.status_required = "blocked" if v.score < 50 else "needs_review"
        v.next_action = "Corregir hard fails antes de informe final al Doctor."
    elif v.score < 50:
        v.status_required = "blocked"
        v.next_action = "Reabrir busqueda/fallback; evidencia insuficiente."
    elif v.score < 75 or v.warnings:
        v.status_required = "needs_review"
        v.next_action = "Completar warnings o dejar handoff interno; no enviar como final automatico."
    else:
        v.status_required = "completed"
        v.next_action = "Gate aprobado para revision del orquestador."

    return v


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("report", type=Path)
    parser.add_argument("--kind", choices=["inmobiliaria", "instrumental", "inversiones", "viajes", "general"], default="general")
    args = parser.parse_args()

    result = validate_report(args.report, args.kind)
    payload = {
        "ok": result.status_required == "completed" and not result.hard_fails,
        "score": result.score,
        "status_required": result.status_required,
        "hard_fails": result.hard_fails,
        "warnings": result.warnings,
        "counts": result.counts,
        "next_action": result.next_action,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    if result.hard_fails or result.status_required != "completed":
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

## minimal_fixtures

### R_VALID_INM_001 - informe valido

```markdown
## summary
Shortlist inmobiliaria Junin con 5 fuentes, 3 candidatos y 4 descartes.

## fuentes intentadas
- Portal A: success, aviso con precio y zona.
- Marketplace B: success, comparable.
- Inmobiliaria local C: partial, precio pendiente.
- Snippet/cache D: success, replica de aviso.
- PDF/revista E: success, comparable historico.

## rutas alternativas usadas
- Portal A bloqueado inicialmente: busqueda por direccion + marketplace espejo, success.

## candidatos
- Casa 1; fuente Portal A; precio USD X; zona centro; comparable Casa 2; riesgos refaccion; decision investigar; next_action validar documentacion.
- Casa 2; fuente Marketplace B; precio USD Y; zona radio 12 cuadras; comparable Casa 1; riesgos precio alto; decision watchlist; next_action revisar m2 cubiertos.
- Casa 3; fuente Inmobiliaria C; pending_price con ruta a fuente publica; zona apta; comparable Casa 1; decision pedir_aprobacion; next_action validar precio.

## comparables
- Casa 1 vs Casa 2 por zona/precio/m2.
- Casa 3 vs comparable historico PDF.

## descartes con motivo
- Aviso D1: fuera de radio.
- Aviso D2: sin precio y sin ruta.
- Aviso D3: estado de refaccion incompatible.
- Aviso D4: precio fuera de tesis.

## pendientes y ruta concreta
- Confirmar precio de Casa 3 en fuente publica o proxima corrida.

## decision recomendada
Investigar Casa 1, watchlist Casa 2, pedir aprobacion para Casa 3.

## confidence
medium-high
```

Esperado: `completed`, score >= 75.

### R_EMPTY_TECH_001 - solo errores tecnicos

```markdown
## summary
No se pudo revisar el mercado porque las paginas no abren.

## fuentes intentadas
- Portal A: error tecnico.
- Portal B: blocked.
- Marketplace C: error.

## decision recomendada
No hay oportunidades.

## confidence
low
```

Esperado: `blocked`, hard fails `low_sources_broad_scope`, `blocked_source_without_fallback`, `technical_failure_as_conclusion`, `zero_candidates_without_universe`, `missing_required_sections`.

### R_ZERO_CANDIDATES_EXHAUSTIVE_001 - sin candidatos pero no vacio

```markdown
## summary
No hay candidatos suficientes para cierre final; queda needs_review con universo revisado.

## fuentes intentadas
- Fuente 1: success.
- Fuente 2: success.
- Fuente 3: success.
- Fuente 4: success.
- Fuente 5: success.
- Fuente 6: partial.

## rutas alternativas usadas
- Fuente 6 parcial: cache y comparable secundario, partial.

## candidatos

## comparables
- Comparable de zona/precio usado para calibrar busqueda.

## descartes con motivo
- 12 descartes por fuera de radio, sin precio, estado malo, precio incompatible.

## pendientes y ruta concreta
- Proxima corrida ampliando radio 4 cuadras y usando fuente secundaria.

## decision recomendada
No enviar como informe final; conservar borrador interno y reintentar con criterio ampliado.

## confidence
medium
```

Esperado: `needs_review`, no `completed`.

### R_NO_SOURCES_001 - sin fuentes

```markdown
## summary
Radar de inversion con conclusion sin fuentes.

## candidatos
- Candidato aparente sin fuente ni precio.

## decision recomendada
Investigar.

## confidence
low
```

Esperado: `blocked`, hard fail `zero_sources`.

### R_NO_COMPARABLES_001 - candidatos sin comparables

```markdown
## summary
Radar instrumental con items aparentes pero sin comparables.

## fuentes intentadas
- Marketplace A: success.
- Fabricante B: success.
- Distribuidor C: partial.
- Fuente D: success.
- Fuente E: success.

## rutas alternativas usadas
- Distribuidor C parcial: fabricante B, partial.

## candidatos
- Set reusable; marca X modelo Y; precio USD X; fuente Marketplace A; riesgos soporte; decision investigar; next_action validar garantia.

## descartes con motivo
- Item D1: implante sin trazabilidad.
- Item D2: usado sin soporte.
- Item D3: modelo no compatible.

## pendientes y ruta concreta
- Agregar comparable local y regulatorio antes de final.

## decision recomendada
Watchlist interno.

## confidence
medium
```

Esperado: `needs_review` o `blocked` por `candidate_without_comparables`; no `completed`.

## retry_fallback_policy

| Situacion | Reintento obligatorio | Si sigue fallando |
| --- | --- | --- |
| Fuente web bloqueada | Query por titulo/direccion/modelo, marketplace espejo, snippet/cache, comparable. | `needs_review` con fuente fallida, rutas usadas y next action. |
| Cero candidatos | Ampliar queries dentro del scope, documentar descartes, agregar comparables. | `needs_review`, no "mercado agotado" final salvo evidencia amplia. |
| Sin precio | Replica exacta, vendedor/fuente publica, comparable local/historico. | `pending_price` + decision watchlist/pedir_aprobacion. |
| Instrumental ambiguo | Marca/modelo/version/fabricante, soporte local, regulatorio si aplica. | `watchlist` o `descartar`, nunca compra directa. |
| Viajes con disponibilidad cambiante | Fecha/precio/politica, fuente secundaria, captura autorizada si aplica. | Handoff humano; no reservar ni contactar. |
| Fuente requiere login o credencial | No usar credenciales; buscar equivalente publico. | Bloqueo valido con limite exacto y alternativa propuesta. |

## orchestrator_first_local_application

La primera integracion local deberia ser:

1. Crear `scripts/qa/validate_radar_report.py` con el script propuesto o una version equivalente.
2. Agregar fixtures en `tests/fixtures/radares/` o `scripts/qa/fixtures/radares/`:
   - `R_VALID_INM_001.md`
   - `R_EMPTY_TECH_001.md`
   - `R_ZERO_CANDIDATES_EXHAUSTIVE_001.md`
   - `R_NO_SOURCES_001.md`
   - `R_NO_COMPARABLES_001.md`
3. Conectar el validator como check pre-commit/pre-send para resultados cuyo front sea `RADARES`, `INVERSIONES`, `INMOBILIARIA`, `INSTRUMENTAL` o `VIAJES`.
4. Regla de despliegue inicial: si exit code != 0, guardar artifact local de QA y crear job/handoff; no enviar informe final al Doctor.
5. Despues de 5-10 corridas reales, recalibrar pesos, pero no relajar hard fails P0.

## attempted_routes

- Se revisaron solo las fuentes permitidas por el workorder.
- No se navego web, no se uso Telegram, Gmail, Drive, Calendar ni bibliotecas personales.
- No se tocaron credenciales ni contenido ObraCash.
- La propuesta se mantiene como implementacion portable para que el orquestador la integre localmente.

## risks_limits

- El script propuesto usa heuristicas sobre markdown; si el orquestador ya tiene reportes estructurados, conviene parsear JSON/YAML real primero y usar markdown como fallback.
- Los conteos por seccion son conservadores; pueden requerir ajuste segun formato final de los reportes.
- Un agente podria inflar fuentes/candidatos para pasar el gate. Por eso los hard fails y la revision de comparables/riesgos siguen siendo obligatorios.
- El validator no verifica oportunidades reales ni precios actuales; valida que el informe sea util, accionable y no tecnicamente resignado.
- Cualquier accion externa, captura real, OCR sobre material privado, login, compra, contacto o envio sigue requiriendo autorizacion del orquestador/Doctor.

## recommendation

Implementar primero el validator local como gate de calidad de salida, no como buscador. Debe bloquear reportes con solo errores tecnicos, candidatos sin fuente/precio/comparables/next action, instrumental medico sin trazabilidad y cualquier conclusion de ausencia de oportunidad basada en evidencia incompleta.

La version inicial debe aplicarse antes del envio al Doctor y antes de marcar un radar como `completed`. `needs_review` es aceptable como borrador interno; `blocked` debe volver a fallback o generar handoff concreto.

## confidence

Alta para el contrato, hard fails y fixtures, porque consolidan reglas ya repetidas en resultados previos y en `protocol.md`. Media para el scoring exacto hasta calibrarlo contra reportes reales del pipeline.

## evidence_paths

- `jobs/20260526T091108-radar-validator-anti-empty-implementation-v1.md`
- `results/20260526T065253-radares-source-recovery-playbook.result.md`
- `results/20260526T073800-batch-results-priority-triage-v1.result.md`
- `results/20260525T103949-anti-informe-vacio-qa-radares-v1.result.md`
- `results/20260525T234822-radares-hardening-anti-informe-vacio-v2.result.md`
- `protocol.md`
