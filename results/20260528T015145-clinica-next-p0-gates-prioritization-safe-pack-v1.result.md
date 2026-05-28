## summary_honesto

Priorizacion segura del proximo P0 clinico-documental, usando solo resultados previos del bridge y contexto declarativo. No lei historias clinicas reales, no toque la app canonica, no edite validadores ni plantillas, y no use fuentes externas.

Despues de los gates ya declarados como integrados en detect-only/report-only, el mayor riesgo residual no cubierto como gate propio es el manejo de eventos/complicaciones en el parte quirurgico, en especial evento dural/parche dural: no inventarlo si no fue indicado, y si se menciona una complicacion, exigir manejo y estado final como `needs_review`.

Recomendacion unica: abrir el proximo ciclo para `evento_complicacion_manejo_estado_final`, con foco inicial en dural/durotomia/LCR/parche dural y sangrado relevante, siempre detect-only/report-only.

## coverage_table

| Fuente revisada | Estado | Uso |
|---|---|---|
| `jobs/20260528T015145-clinica-next-p0-gates-prioritization-safe-pack-v1.md` | Revisada | Contrato, restricciones y lista de gates ya integrados. |
| `context/fronts/clinica.md` | Revisada | Canon de seguridad: corpus a gates, no tocar plantillas sin baseline/test. |
| `results/20260527T190454-clinica-corpus-gates-backlog-v2.result.md` | Revisada | Backlog: parte quirurgico debe cubrir tecnica, hallazgos, implantes, complicaciones, hemostasia, recuento, cierre y estado final. |
| `results/20260527T233900-clinica-next-p0-gates-prioritization-after-ayudantes-v1.result.md` | Revisada | Priorizacion previa que llevo a `trazabilidad_implantes_materiales`. |
| `results/20260528T000957-clinica-trazabilidad-frontier-implementation-review-v1.result.md` | Revisada | Cierre del ciclo trazabilidad en observacion, sin hard block. |
| `results/20260527T223530-clinica-protocolo-secuencia-hemostasia-detect-only-plan-v1.result.md` | Revisada | Contrato de secuencia quirurgica y separacion del cuerpo tecnico. |
| `results/20260527T230844-clinica-hemostasia-secuencia-postfixture-review-v2.result.md` | Revisada | Cierre de hemostasia/secuencia en observacion. |
| `results/20260527T183421-clinica-correcciones-a-fixtures-implementacion.result.md` | Revisada | Fixtures previos: `LUM-DOC-013` parche/refuerzo dural solo si indicado y en secuencia correcta. |

## ranking_candidatos

| Rank | Candidato P0 siguiente | Riesgo medico-legal | Decision |
|---:|---|---|---|
| 1 | `evento_complicacion_manejo_estado_final` | Alto: una complicacion narrada sin manejo/estado final, o un parche dural inventado sin evento/source, cambia hechos criticos del parte quirurgico. | Recomendar para proximo ciclo. |
| 2 | `hallazgos_intraoperatorios_no_inventados` | Alto-medio: el parte puede afirmar fragmentos, fibrosis, compresion, sangrado o hallazgos no provistos por input/tecnica aprobada. | Dejar como siguiente si el primero queda estable. |
| 3 | `no_duplicar_acto_tecnico_materiales_o_abordaje` | Medio-alto: duplicar PLIF, implantes, descompresion, posicion o abordaje puede producir parte confuso o contradictorio. | Mantener en backlog de estabilidad. |

## candidato_1_evento_complicacion_manejo_estado_final

Objetivo: detectar en partes quirurgicos menciones afirmadas de evento/complicacion relevante y verificar que haya manejo y estado final. Primera frontera recomendada: durotomia, lesion/ apertura dural, LCR/fuga, reparacion/parche dural, sangrado relevante, deficit neurologico intraoperatorio o evento anestesico narrado en cuerpo tecnico.

Ejemplo falso positivo: `sin durotomia ni perdida de LCR` o `no fue necesario parche dural` no debe disparar como complicacion. Tambien una frase de consentimiento sobre riesgos posibles no debe analizarse como hecho ocurrido.

Ejemplo falso negativo: el texto dice `se observa salida de LCR` o `pequena apertura dural` sin usar la palabra "durotomia"; si el lexicon solo busca "durotomia", no detecta el evento.

Fixture minimo seguro:

```json
{
  "id": "CLIN-P0-069-dural-event-without-management-review",
  "document_type": "parte_quirurgico",
  "technical_body": "Durante la exposicion se constata salida de LCR. Se continua el procedimiento y se realiza cierre por planos.",
  "expected": "needs_review",
  "gate_id": "evento_complicacion_manejo_estado_final",
  "reason": "evento dural mencionado sin manejo especifico ni estado final"
}
```

Controles minimos:

```json
[
  {
    "id": "CLIN-P0-070-no-dural-event-pass",
    "technical_body": "No se constata durotomia ni salida de LCR. Hemostasia, recuento y cierre.",
    "expected": "pass"
  },
  {
    "id": "CLIN-P0-071-patch-without-event-review",
    "technical_body": "Se coloca parche dural y se realiza cierre, sin otra descripcion.",
    "expected": "needs_review"
  },
  {
    "id": "CLIN-P0-072-dural-event-managed-pass",
    "technical_body": "Se constata pequena apertura dural, se repara con sutura y parche, sin fuga al control final. Hemostasia, recuento y cierre.",
    "expected": "pass"
  }
]
```

Criterio detect-only: generar finding `needs_review` si hay evento/complicacion afirmada y falta al menos uno de estos elementos: manejo, control/resultado final, o evidencia de que el parche/reparacion corresponde a un evento. En documentos reales no usar `hard_fail`; en fixtures sinteticos puede fallar el test si no aparece el finding esperado.

Riesgo de implementacion: alto si se analizan secciones equivocadas. Debe limitarse al `technical_body` o cuerpo clinico admitido, excluir consentimiento/riesgos hipoteticos/checklists, y tener negacion local fuerte. Requiere aprobacion humana antes de cualquier promocion a hard block real. No requiere material real para el ciclo sintetico detect-only.

## candidato_2_hallazgos_intraoperatorios_no_inventados

Objetivo: marcar hallazgos intraoperatorios afirmados que no provienen de `source_fields.approved_findings`, `technical_body` original autorizado o fixture sintetico. El foco no es estilo: es evitar que el parte agregue hechos clinicos nuevos, por ejemplo fragmento herniario calcificado, fibrosis severa, compresion de raiz especifica o sangrado abundante no informados.

Ejemplo falso positivo: una frase generica de objetivo tecnico, como `se explora el espacio`, no debe exigirse como hallazgo fuente. Tampoco debe bloquear si el input estructurado contiene el hallazgo con sinonimo normalizado.

Ejemplo falso negativo: `se evidencia fibrosis perirradicular` puede escaparse si el gate solo busca "fragmento" o "hernia".

Fixture minimo seguro:

```json
{
  "id": "CLIN-P0-073-invented-intraoperative-finding-review",
  "document_type": "parte_quirurgico",
  "source_fields": {
    "diagnosis": "hernia lumbar L4-L5 derecha",
    "approved_findings": []
  },
  "technical_body": "Se identifica gran fragmento herniario calcificado adherido a la raiz.",
  "expected": "needs_review"
}
```

Criterio detect-only: comparar hallazgos afirmados de alto impacto contra campos aprobados. Si no hay fuente, `needs_review`; si el hallazgo aparece en `approved_findings`, `pass`. No corregir ni sugerir el hallazgo correcto.

Riesgo de implementacion: medio-alto por sinonimos y por dependencia de campos estructurados. Antes de integrarlo ampliamente conviene autorizacion humana sobre la lista de hallazgos de alto impacto; no requiere historias reales para fixtures iniciales.

## candidato_3_no_duplicar_acto_tecnico_materiales_o_abordaje

Objetivo: detectar duplicaciones peligrosas dentro del mismo parte quirurgico: repetir PLIF, duplicar colocacion de implantes, duplicar descompresion/recalibraje como si fueran actos independientes, o repetir posicion/protecciones/abordaje de manera que parezca doble procedimiento.

Ejemplo falso positivo: procedimientos bilaterales, por etapas o multinivel pueden repetir acciones legitimas. Si el texto delimita nivel/etapa distinto, debe pasar o quedar como `advisory`, no `fail`.

Ejemplo falso negativo: `se realiza artrodesis intersomatica` y luego `se efectua PLIF` pueden ser duplicado conceptual aunque no repitan la misma frase.

Fixture minimo seguro:

```json
{
  "id": "CLIN-P0-074-duplicate-plif-materials-review",
  "document_type": "parte_quirurgico",
  "procedure_family": "fijacion_lumbar",
  "technical_body": "Se realiza PLIF L4-L5 con caja intersomatica. Luego se realiza nuevamente PLIF L4-L5 con caja intersomatica y se colocan barras.",
  "expected": "needs_review"
}
```

Criterio detect-only: detectar repeticion del mismo acto de alto impacto sobre mismo nivel/lado/material sin marcador de etapa distinta. Resultado inicial `needs_review`; nunca autocorregir ni eliminar texto.

Riesgo de implementacion: medio por normalizacion semantica y por procedimientos multi-etapa. No requiere autorizacion humana para fixtures sinteticos, pero si para convertirlo en bloqueo real.

## recommendation

Abrir el proximo workorder para `evento_complicacion_manejo_estado_final`, empezando por fixtures sinteticos `CLIN-P0-069` a `CLIN-P0-072` y modo detect-only/report-only. Es el mejor siguiente P0 porque cubre un hecho medico-legal critico que no queda agotado por hemostasia, ayudantes, trazabilidad ni consistencia general: si se menciona una complicacion, el documento debe poder explicar manejo y estado final; si no hubo evento, no debe inventar parche dural ni reparacion.

No pedir material real para este ciclo. Si el orquestador quiere subir severidad despues, ahi si requiere revision humana explicita, inspeccion de findings de observacion y definicion clinica/legal del set de complicaciones.

## confidence

Media-alta para el ranking relativo: deriva de resultados previos y del backlog de parte quirurgico. Media para nombres finales de gates/fixtures porque no inspeccione la app real ni su validator actual. Baja para cualquier promocion a hard block real sin autorizacion humana, observacion de falsos positivos y revision medico-legal.

## attempted_routes

- Se sincronizo el bridge con `git pull --rebase origin main`.
- Se ejecuto `./scripts/personal_xh_check.sh` y se detecto este job asignado a `personal-xh`.
- Se reviso el job actual y solo resultados/contexto declarativo del bridge.
- Se revisaron resultados previos de backlog, trazabilidad, secuencia de hemostasia y correcciones lumbares.
- No se leyeron historias clinicas reales, adjuntos, Drive, iCloud, Photos, Gmail, Telegram ni datos personales.
- No se toco la app real, validadores, plantillas finales ni corpus operativo.

## risks_limits

- Este resultado es priorizacion y pack seguro; no implementa codigo.
- La app canonica no fue inspeccionada en esta Mac, por lo que rutas y nombres exactos quedan para el orquestador.
- Los tres candidatos deben quedarse como `detect_only/report_only` al inicio.
- Los fixtures son sinteticos y no sustituyen revision clinica/legal para promocion futura.
- Si el orquestador informa que `evento_complicacion_manejo_estado_final` ya existe en observacion, el siguiente recomendado pasa a ser `hallazgos_intraoperatorios_no_inventados`.

## evidence_paths

- `jobs/20260528T015145-clinica-next-p0-gates-prioritization-safe-pack-v1.md`
- `claims/20260528T015145-clinica-next-p0-gates-prioritization-safe-pack-v1.json`
- `results/20260528T015145-clinica-next-p0-gates-prioritization-safe-pack-v1.result.md`
- `context/fronts/clinica.md`
- `results/20260527T190454-clinica-corpus-gates-backlog-v2.result.md`
- `results/20260527T233900-clinica-next-p0-gates-prioritization-after-ayudantes-v1.result.md`
- `results/20260528T000957-clinica-trazabilidad-frontier-implementation-review-v1.result.md`
- `results/20260527T223530-clinica-protocolo-secuencia-hemostasia-detect-only-plan-v1.result.md`
- `results/20260527T230844-clinica-hemostasia-secuencia-postfixture-review-v2.result.md`
- `results/20260527T183421-clinica-correcciones-a-fixtures-implementacion.result.md`

## draft_para_topic_clinica

Proximo P0 recomendado: `evento_complicacion_manejo_estado_final`, en detect-only/report-only. Foco inicial: evento dural/LCR/parche dural y sangrado relevante. La regla no debe inventar complicaciones ni bloquear documentos reales: solo marcar `needs_review` si una complicacion aparece sin manejo/estado final, o si se coloca/repara parche dural sin evento/source claro. Candidatos secundarios: `hallazgos_intraoperatorios_no_inventados` y `no_duplicar_acto_tecnico_materiales_o_abordaje`.
