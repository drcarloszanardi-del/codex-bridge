# P1 lumbar test pack v1

## Objetivo

Convertir las reglas del Dr. Zanardi en casos sinteticos versionados.

## Formato sugerido

```json
{
  "id": "lumbar_extraforaminal_l4_l5_der_001",
  "input": "Hernia discal extraforaminal L4-L5 derecha. Microdiscectomia extraforaminal L4-L5 derecha.",
  "expected": ["raiz L4 derecha", "abordaje foraminal/extraforaminal"],
  "forbidden": ["espacio interlaminar", "hemilaminotomia", "flavectomia", "raiz pasante"],
  "severity": "critical",
  "gate": "extraforaminal_no_interlaminar"
}
```

## Archivos objetivo

- `scripts/qa/validate_20_pathology_scenarios.js`
- nuevo `data/derived/clinical_test_cases/lumbar_gates_v1.json`

## Criterio de aceptacion

Cada bug clinico real detectado debe tener al menos un caso sintetico que falle antes del fix y pase despues.
