# Pablo idle queue policy

Actualizado: 2026-05-25.

## Regla CEO

Pablo/personal-xh no debe quedar mirando el puente si figura `available`, `idle:true` o `requesting_work:true`. Si no hay jobs activos, Codex principal debe asignarle trabajo de alto valor dentro de una de estas categorias.

## Prioridad de asignacion

1. Segunda mirada de riesgos en trabajos que Codex acaba de implementar.
2. Sintesis de material largo con salida ejecutable.
3. Arquitectura de herramientas/modelos/subagentes.
4. Preparacion premium de reels/presentaciones antes de recibir assets.
5. Fixtures y gates medico-legales.
6. QA anti informe vacio en radares.
7. Postmortem de errores de Telegram.

## No asignar a Pablo

- Barridos rutinarios que puede hacer `gpt-5.3-codex`.
- Healthchecks simples.
- Scraping masivo sin pregunta de criterio.
- Acciones externas.
- Datos sensibles no sanitizados.
- Tareas donde la salida esperada sea solo "mirar si anda".

## Contrato

Todo job para Pablo debe tener:

- objetivo;
- fuentes/local paths;
- alcance prohibido;
- salida exigida;
- criterio de terminado;
- `evidence_paths`;
- secciones suficientes para pasar `scripts/validate_result_contract.py`.

## Cola viva actual

Cuando Pablo quede libre, usar esta cola salvo que haya una prioridad humana mas reciente:

1. Herramientas IA / apps / skills / modelos por funcion.
2. Presentaciones medicas: piloto que supere PPT artesanal.
3. ArtifactDraft para Telegram/Reels/Presentaciones.
4. DoctorCorrectionCapture clinico.
5. Gate anti informe vacio para radares.
6. Reels CMP: pieza siguiente con assets pendientes.
