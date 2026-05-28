---
job_id: 20260527T231641-clinica-ayudantes-no-duplicar-cirujano-review-v1
worker: personal-xh
status: completed
completed_at: 2026-05-27T23:19:33-03:00
front: CLINICA
no_external_actions: true
no_secrets: true
---

# Resultado - Clinica ayudantes no duplicar cirujano review v1

## summary

Propuesta detect-only/report-only para evitar que `Ayudantes` duplique al
cirujano principal en partes quirurgicos. El guardrail debe ser una regla
documental interna, estrecha y conservadora: detectar duplicaciones claras,
marcar ambiguos como `needs_review`, y nunca completar automaticamente el campo
ayudante con el cirujano.

Regla central: si `cirujano_principal` normaliza a `Dr Carlos Zanardi`, entonces
`ayudantes` no debe contener `Dr Carlos Zanardi`, `Dr Carlos Zanardi y equipo`
ni un ayudante literal igual al cirujano. Si no hay ayudante nominal, el fallback
seguro declarado es `equipo quirurgico de sala` o dejar pendiente/observacion
segun flujo.

## coverage_table

| Fuente local | Estado | Uso |
| --- | --- | --- |
| `jobs/20260527T231641-clinica-ayudantes-no-duplicar-cirujano-review-v1.md` | Revisada | Objetivo, contexto durable y entregables. |
| `context/fronts/clinica.md` | Revisada | Regla de convertir correcciones del Doctor en gates/fixtures sin tocar plantillas a ciegas. |
| `results/20260527T030306-clinica-documental-p0-gates-detect-only-plan-v1.result.md` | Revisada | Contrato detect-only/report-only, severidades y fixtures sinteticos. |
| `results/20260527T003215-clinica-correcciones-a-fixtures-implementacion.result.md` | Revisada | Correcciones clinicas como fixtures/gates. |
| `jobs/20260527T231641-clinica-ayudantes-no-duplicar-cirujano-review-v1.md` | Revisada | Frases exactas del incidente y fallback permitido. |

## criterio_detect_only

Aplicar solo a campos estructurados del parte o al encabezado parseado:
`cirujano_principal`, `cirujano`, `ayudantes`, `ayudante`, `equipo_quirurgico`.
No aplicar a texto libre del cuerpo tecnico salvo que el parser ya haya
identificado esos campos.

Normalizacion recomendada:

1. Pasar a minusculas, quitar acentos, puntos y dobles espacios.
2. Eliminar honorificos: `dr`, `dra`, `doctor`, `doctora`.
3. Normalizar conectores de lista: coma, punto y coma, salto de linea y ` y `.
4. Conservar frases genericas permitidas como entidad completa:
   `equipo quirurgico de sala`.
5. Comparar entidades normalizadas, no substrings amplios.

Severidad:

| Expected | Criterio |
| --- | --- |
| `fail` | Un ayudante normalizado es igual al cirujano principal, o `ayudantes` contiene al cirujano principal mas un generic tail como `y equipo`. |
| `pass` | Ayudante nominal distinto del cirujano, o fallback exacto `equipo quirurgico de sala`. |
| `needs_review` | Ayudante ausente, `equipo` generico sin la frase canonica, iniciales/apellido ambiguo, o no se pudo separar cirujano de ayudantes. |

## fixtures_sinteticos

| Fixture | Input sintetico | Expected |
| --- | --- | --- |
| `CLIN-P0-042-assistant-surgeon-and-team-fail` | `cirujano_principal="Dr. Carlos Zanardi"; ayudantes="Dr. Carlos Zanardi y equipo"` | `fail` |
| `CLIN-P0-043-assistant-equals-surgeon-literal-fail` | `cirujano_principal="Dr Carlos Zanardi"; ayudantes="Dr. Carlos Zanardi"` | `fail` |
| `CLIN-P0-044-distinct-nominal-assistant-pass` | `cirujano_principal="Dr. Carlos Zanardi"; ayudantes="Dr. Juan Perez"` | `pass` |
| `CLIN-P0-045-operating-room-team-pass` | `cirujano_principal="Dr. Carlos Zanardi"; ayudantes="equipo quirurgico de sala"` | `pass` |
| `CLIN-P0-046-empty-assistant-review` | `cirujano_principal="Dr. Carlos Zanardi"; ayudantes=""` | `needs_review` o pendiente segun flujo, no autofill. |
| `CLIN-P0-047-generic-team-review` | `cirujano_principal="Dr. Carlos Zanardi"; ayudantes="equipo"` | `needs_review` por fallback no canonico. |
| `CLIN-P0-048-surname-only-review` | `cirujano_principal="Dr. Carlos Zanardi"; ayudantes="Dr. Zanardi"` | `needs_review`, no `fail` automatico por posible ambiguedad nominal. |
| `CLIN-P0-049-multiple-assistants-one-duplicate-fail` | `cirujano_principal="Dr. Carlos Zanardi"; ayudantes="Dr. Juan Perez; Dr. Carlos Zanardi"` | `fail` con evidence path al segundo ayudante. |
| `CLIN-P0-050-surgeon-field-with-team-pass` | `cirujano_principal="Dr. Carlos Zanardi"; ayudantes="Dr. Maria Gomez y equipo"` | `pass` si Maria Gomez es asistente nominal distinto. |

## frases_fail

- `Ayudantes: Dr. Carlos Zanardi y equipo`
- `Ayudante: Dr. Carlos Zanardi`
- `Ayudantes: Carlos Zanardi`
- `Ayudantes: Dr Carlos Zanardi; ...` cuando el cirujano principal es el mismo
- cualquier entidad de ayudante que normalice exactamente igual que
  `cirujano_principal`

Estas frases solo deben disparar si estan en el campo `ayudantes` o en un bloque
parseado como tal. Si aparecen en una nota historica, correccion o comentario de
QA, el gate debe ignorarlas o marcarlas como no aplicables.

## falsos_positivos_y_limites

| Riesgo | Como limitarlo |
| --- | --- |
| Otro profesional con mismo apellido. | No hacer `fail` por apellido solo; usar nombre completo normalizado. |
| Frase `Dr. Carlos Zanardi` en campo `cirujano`, no en `ayudantes`. | Usar evidence path exacto y scope de campo. |
| `equipo` generico puede ser fallback institucional local. | Marcar `needs_review`; aceptar solo `equipo quirurgico de sala` como pass inicial. |
| Variantes con iniciales o abreviaturas. | `needs_review` salvo alias versionado y aprobado. |
| Lista mal parseada con `y equipo`. | Si el nombre previo es un ayudante distinto, pass; si el nombre previo es el cirujano, fail. |
| Correccion del Doctor indica ayudante concreto. | No sobreescribir; validar que el nombre indicado sea distinto del cirujano. |

## recomendacion

Integrar como gate nuevo y separado, por ejemplo
`ayudantes_no_duplican_cirujano`, en modo `detect_only/report_only`.

Contrato de salida sugerido:

```json
{
  "gate_id": "ayudantes_no_duplican_cirujano",
  "mode": "report_only",
  "status": "fail|pass|needs_review",
  "evidence_path": "$.parte_quirurgico.ayudantes[0]",
  "expected": "ayudante nominal distinto o equipo quirurgico de sala",
  "observed": "ayudante duplica cirujano principal",
  "recommendation": "revisar campo Ayudantes; no completar con cirujano principal"
}
```

Implementacion segura:

1. Agregar fixtures sinteticos primero, sin pacientes reales.
2. Implementar normalizador de nombres local y acotado.
3. Comparar solo campos estructurados/parseados de equipo quirurgico.
4. `fail` solo en duplicacion clara; `needs_review` para ausente o ambiguo.
5. No tocar plantillas finales ni autocompletar ayudantes.
6. Mantener fallback canonico `equipo quirurgico de sala` como pass inicial.

## confidence

Alta para la regla documental estrecha y los fixtures sinteticos, porque el
workorder trae el incidente, el nombre del cirujano habitual y el fallback
permitido. Media para integracion real porque no se inspecciono la app canonica
ni se ejecuto QA local de la app desde esta Mac.

## attempted_routes

- Se hizo `git pull --rebase`.
- Se ejecuto `./scripts/personal_xh_check.sh` y se detecto el job asignado.
- Se reviso `jobs/20260527T231641-clinica-ayudantes-no-duplicar-cirujano-review-v1.md`.
- Se reviso `context/fronts/clinica.md`.
- Se busco contexto local con `rg` sobre `context/`, `jobs/` y `results/`.
- No se uso Telegram, Gmail, Drive, Calendar, iCloud, Photos, adjuntos, datos de
  pacientes ni fuentes externas.

## risks_limits

- Este resultado es una propuesta de gate y fixtures; no modifica la app real.
- No valida identidad profesional fuera de los campos estructurados del parte.
- No debe usarse para decidir dotacion quirurgica real; solo QA documental.
- La promocion a hard block requiere observacion, revision humana y aprobacion
  explicita del orquestador/Doctor.

## evidence_paths

- `jobs/20260527T231641-clinica-ayudantes-no-duplicar-cirujano-review-v1.md`
- `claims/20260527T231641-clinica-ayudantes-no-duplicar-cirujano-review-v1.json`
- `results/20260527T231641-clinica-ayudantes-no-duplicar-cirujano-review-v1.result.md`
- `context/fronts/clinica.md`
- `results/20260527T030306-clinica-documental-p0-gates-detect-only-plan-v1.result.md`
- `results/20260527T003215-clinica-correcciones-a-fixtures-implementacion.result.md`
