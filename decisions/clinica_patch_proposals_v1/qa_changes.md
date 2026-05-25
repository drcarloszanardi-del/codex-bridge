# QA changes

## agregar

- `data/derived/clinical_test_cases/lumbar_gates_v1.json`.
- Suite `validate_lumbar_gates_v1.js`.
- Check de ruta canonica en `validate_clinica_route_guard.js`.
- Check de `source_status` para corpus -> gates.

## criterio de aceptacion

- Cada bug clinico real tiene fixture.
- Un cambio de plantilla que rompe fixture critical bloquea release.
- Corpus secundario no puede activar gate fuerte.
