---
id: 20260525T132057-reel-consulta-columna-preparacion-render-v1
assignee: personal-xh
model: gpt-5.5-xh
created_at: 2026-05-25T13:20:57-03:00
front: REELS
no_external_actions: true
no_secrets: true
status: pending
---

# Workorder: primer render operativo con Pablo - consulta de columna

## 10 inicial - dirección del orquestador

- Objetivo: producir un primer borrador premium de reel CMP usando la Mac rápida de Pablo, con material propio/autorizado local, sin publicar ni enviar afuera.
- Reel ID: `consulta_columna_preparacion_v1`
- Duración objetivo: 25-35 segundos.
- Formato: vertical 9:16, legible en celular.
- Estética: Centro Médico Pellegrini, sobria, clara, profesional, sin stock genérico ni efectos ruidosos.
- Contacto visible correcto: `@drcarloszanardi`, `2364384321`, `www.centromedicopellegrini.com.ar`.
- Contexto:
  - `results/20260525T131149-reels-render-offload-pablo-fast-node-v1.result.md`
  - `results/20260525T124546-reels-cmp-next-editorial-options.result.md`
  - `context/fronts/reels_cmp.md`
- Assets sugeridos por Pablo, solo si están realmente disponibles y autorizados en su Mac:
  - `V02`: Doctor hablando a cámara.
  - `C01`, `C04`, `C15`: placas CMP.
- Restricciones:
  - No usar Photos.app completa.
  - No subir videos/fotos privadas al bridge.
  - No usar pacientes, estudios, HC, pantallas, datos identificables ni claims médicos absolutos.
  - Si el video `V02` contiene datos sensibles o audio no apto, no renderizar con ese material; devolver QA y alternativa.

## Guion base

```text
Si va a consultar por dolor de columna, prepare cuatro cosas:
sus estudios previos,
desde cuándo empezó y hacia dónde corre el dolor,
qué medicación o tratamientos probó,
y qué actividades le limita.

Una consulta bien preparada ayuda a decidir mejor.

Centro Médico Pellegrini.
```

## 80 delegado - trabajo del agente

Producir:
- `asset_review`: qué assets usó o descartó y por qué.
- `storyboard_final`: tiempos, placas, textos y transiciones.
- `render_status`: ruta local del render en la Mac de Pablo si se generó, duración, resolución, tamaño.
- `qa_visual`: contacto, legibilidad, privacidad, estética CMP, audio, solapamientos.
- `corrections_needed`: ajustes concretos para que el orquestador apruebe o devuelva.
- `share_plan`: cómo entregar el video al orquestador sin exponer material privado, preferentemente carpeta autorizada o export manual controlado.

Si puede renderizar sin riesgo, renderice. Si no puede, entregue un storyboard preciso y QA del bloqueo con alternativa concreta.

## 10 final - retorno al orquestador

Incluir `summary honesto`, `coverage_table`, `risks / limits`, `recommendation`, `confidence`, `evidence_paths`.
Validar contra `scripts/validate_result_contract.py`.
