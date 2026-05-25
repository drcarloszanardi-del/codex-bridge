# Resultado - reels render offload Pablo fast node v1

Job: `20260525T131149-reels-render-offload-pablo-fast-node-v1`
Worker: `personal-xh` / Pablo
Fecha: `2026-05-25`

## summary honesto

Pablo puede funcionar como nodo rapido de reels, pero el contrato debe ser local-first: el orquestador define guion, storyboard y decision final; Pablo usa solo material propio autorizado en su Mac, renderiza pruebas, hace QA visual y devuelve resultados al bridge sin subir fotos/videos privados. Para el primer reel, la mejor base propia disponible es V02, un video del Doctor hablando a camara, complementado por placas CMP C01/C04/C15.

## coverage_table

| Area | Estado | Evidencia |
|---|---|---|
| Offload local | definido | Pablo trabaja con assets locales propios, no stock. |
| Control orquestador | preservado | El orquestador manda guion/storyboard y aprueba. |
| Privacidad | definida | No commitear assets privados, solo manifest/codigos/resultados. |
| Primer reel | listo para storyboard | `results/20260525T124546...` recomienda consulta columna. |
| QA visual | definido | `context/fronts/reels_cmp.md` y pipeline QA previo. |

## render_offload_contract

Pablo recibe:

- Guion final o borrador.
- Storyboard con tiempos.
- Manifest de assets por codigo, no archivos en bridge.
- Reglas de contacto CMP: `2364384321`, `@drcarloszanardi`, `www.centromedicopellegrini.com.ar`.
- Restricciones: propio/no stock, no pacientes, no HC, no publicacion.

Pablo devuelve:

- Render de prueba local o ruta local si no debe compartirse.
- QA visual en `results/`.
- Lista de problemas y correcciones.
- Capturas/contact sheet anonimizadas si son seguras.
- Recomendacion: aprobar, ajustar o rechazar.

Limites:

- No publicar.
- No mandar por Telegram/Gmail/Drive.
- No commitear fotos/videos privados.
- No usar material externo.

## asset_manifest_contract

Manifest minimo por reel:

```yaml
reel_id: consulta_columna_preparacion_v1
policy: own_material_only_no_stock
asset_location: pablo_local_only
assets:
  - code: V02
    role: doctor_to_camera
    privacy_status: safe_candidate
    required_review: full_video_audio_check
  - code: C01
    role: opening_brand_plate
    privacy_status: safe
  - code: C04
    role: cta_contact_plate
    privacy_status: safe
  - code: C15
    role: alternate_brand_plate
    privacy_status: safe
```

## pablo_fast_node_runbook

1. Pull bridge.
2. Leer workorder de reel.
3. Verificar que el manifest diga `own_material_only_no_stock`.
4. Resolver codigos a paths locales en la Mac personal.
5. Crear carpeta local de trabajo:

```text
reels_photo_review/working/<reel_id>/
```

6. Renderizar borrador vertical 9:16.
7. Revisar frame a frame contacto, texto, recortes, privacidad y consistencia CMP.
8. Devolver al bridge un resultado con QA y rutas locales del render si corresponde.
9. Esperar decision del orquestador; no publicar.

## queue_protocol

Jobs sugeridos:

```text
jobs/YYYYMMDDTHHMMSS-reels-render-consulta-columna-v1.md
jobs/YYYYMMDDTHHMMSS-reels-qa-consulta-columna-v1.md
```

Resultados:

```text
results/<job_id>.result.md
```

Campos obligatorios del job:

- `reel_id`
- `script`
- `storyboard`
- `asset_manifest`
- `contact_data`
- `privacy_policy`
- `output_expectation`

Aviso de disponibilidad:

- Pablo mantiene `status/personal-xh.json` con `requesting_work=true`.
- Si queda idle, pide backlog/QA/render de reels.

## qa_visual_checklist

| Check | Criterio |
|---|---|
| Propiedad | Todo asset debe ser propio o autorizado; no stock. |
| Privacidad | Sin pacientes, HC, pantallas, datos ni estudios identificables. |
| Contacto | `2364384321`, `@drcarloszanardi`, `www.centromedicopellegrini.com.ar`. |
| Estetica | CMP sobrio/profesional, sin efectos ruidosos. |
| Texto | Maximo 2 lineas por placa, legible en celular, sin clipping. |
| Medico-legal | Sin diagnostico individual, promesas, claims absolutos o evidencia falsa. |
| Audio | Sin datos sensibles y con pista/licencia segura si se usa musica. |
| Duracion | 25-35s para primer reel; cierre legible minimo 4s. |

## first_reel_daily_pipeline

Primer reel recomendado: "Como prepararse para la consulta de columna".

Pipeline:

1. Orquestador manda guion corto.
2. Pablo arma version 25-35s con V02 + placas CMP propias.
3. Pablo produce QA y, si es seguro, render local de prueba.
4. Orquestador decide ajustes.
5. Doctor aprueba o pide cambios.
6. Publicacion queda fuera de Pablo.

Guion base sugerido:

```text
Si va a consultar por dolor de columna, prepare cuatro cosas:
sus estudios previos,
desde cuando empezo y hacia donde corre el dolor,
que medicacion o tratamientos probo,
y que actividades le limita.
Una consulta bien preparada ayuda a decidir mejor.
Centro Medico Pellegrini.
```

## scripts_suggested

Sin tocar datos personales, Codex principal puede crear scripts que operen solo sobre carpetas locales autorizadas:

```text
scripts/reels/build_asset_manifest.py
scripts/reels/render_reel_from_manifest.py
scripts/reels/qa_reel_visual_contract.py
```

Regla: si el script recibe un path fuera de `~/CodexAssets/Reels/` o de la carpeta local autorizada de Pablo, debe abortar.

## risks / limits

- El primer video V02 debe revisarse completo: una miniatura no garantiza audio, cortes o ausencia de datos sensibles.
- El orquestador no puede renderizar con esos archivos si no estan en su Mac; debe delegar render a Pablo.
- No debe usarse material quirurgico o estudios medicos en el primer reel; aumenta riesgo y no hace falta.
- Si se necesita fachada/consultorio real mas limpio, pedir al Doctor dos tomas nuevas propias.

## recommendation

El Codex orquestador debe crear el proximo job de render para Pablo con el reel `consulta_columna_preparacion_v1`, usando manifiesto propio/no-stock y assets V02, C01, C04 y C15. Pablo renderiza y devuelve QA/ruta local; el orquestador mantiene decision final.

## confidence

Alta para arquitectura de offload, privacidad y flujo de trabajo. Media para render final hasta revisar video completo y disponer de guion final.

## evidence_paths

- `jobs/20260525T131149-reels-render-offload-pablo-fast-node-v1.md`
- `jobs/20260525T130220-reels-assets-library-curation-protocol.md`
- `context/fronts/reels_cmp.md`
- `results/20260525T122941-reels-dia-patria-assets-and-timeline.result.md`
- `results/20260525T124546-reels-cmp-next-editorial-options.result.md`
- Local no commiteado: `/Users/carloszanardi/Documents/Codex/2026-05-24/vos-podrias-comunicarte-con-codex-que/reels_photo_review/selected_for_reel_consulta_columna/`
