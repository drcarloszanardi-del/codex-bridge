---
id: 20260526T005108-reel-cavernoma-premium-safe-derivatives-render-v1
created_at: 2026-05-26T00:51:08-03:00
created_by: orchestrator
assignee: personal-xh
front: REELS
model: gpt-5.5
reasoning_effort: high
status: queued
priority: high
no_external_actions: true
no_secrets: true
asset_policy: authorized_folder_only_no_raw_commit
---

# Reel cavernoma intramedular - derivados seguros y primer candidato premium

## Contexto

El Doctor solicito un reel publicable para manana sobre un caso de `cavernoma intramedular`, patologia desafiante. Quiere nivel cinematografico, 40 a 60 segundos, con material propio del caso, sin musica agregada por ahora. La musica la agregara el Doctor al publicar.

Ya localizaste la carpeta autorizada:

`/Users/carloszanardi/Documents/Codex/codex-bridge/Reel Cavernoma `

Y preparaste el manifiesto:

`context/asset_packs/20260526-reel-cavernoma/manifest.md`

Usar solamente esa carpeta y los derivados locales autorizados. No buscar en Fotos, Drive, Gmail, Telegram, Downloads ni otras carpetas.

## Objetivo

Preparar material seguro para que Codex orquestador pueda revisar calidad real, y si es posible renderizar un primer candidato premium localmente en tu Mac.

## Entregables obligatorios

1. Crear derivados locales anonimizados/sanitizados en:

   `/Users/carloszanardi/CodexAssets/Reels/reel_cavernoma/sanitized/`

   Reglas:
   - No tocar originales.
   - Quitar metadata/EXIF.
   - Recortar o difuminar cualquier dato identificable: nombres, fechas, HC, placas, monitores, rostros, pantallas, audio del video si lo hubiera.
   - No subir al bridge originales ni archivos medicos crudos.

2. Crear contact sheet seguro y liviano para bridge:

   `context/asset_packs/20260526-reel-cavernoma-safe/contact_sheet.jpg`

   Debe mostrar 8 a 12 frames/planos seguros para que el orquestador pueda juzgar encuadre, legibilidad y tono. Si algun plano no es publicable, marcarlo como `rejected` en el manifiesto y no incluirlo.

3. Crear manifiesto de QA:

   `context/asset_packs/20260526-reel-cavernoma-safe/manifest.json`

   Con:
   - `asset_code`
   - `source_local_path`
   - `safe_derivative_local_path`
   - `bridge_preview_path` si aplica
   - `privacy_status`: `passed`, `rejected`, `needs_orchestrator_review`
   - `reason`
   - `suggested_role`: hook/preop/monitoring/surgical/context/postop/control/closing

4. Si la privacidad pasa y tiene herramientas suficientes, renderizar un primer candidato local:

   `/Users/carloszanardi/CodexAssets/Reels/reel_cavernoma/renders/cmp_reel_cavernoma_intramedular_v1.mp4`

   Tambien crear un contact sheet del render para bridge:

   `context/asset_packs/20260526-reel-cavernoma-safe/render_contact_sheet.jpg`

   No hace falta subir el MP4 si pesa mucho o si puede contener informacion sensible. Si lo subes, debe ser proxy seguro y liviano, nunca original crudo.

## Criterio editorial

Titulo de trabajo: `Cavernoma intramedular: cuando el detalle cambia todo`

Estructura sugerida 40-60 s:

1. 0-4 s - Hook: `Hay patologias en las que un milimetro importa.`
2. 4-12 s - Imagen preoperatoria: `Un cavernoma intramedular exige diagnostico preciso y planificacion fina.`
3. 12-24 s - Plan/monitoreo: `La decision no es solo operar: es elegir el corredor, proteger funcion neurologica y anticipar riesgos.`
4. 24-38 s - Microcirugia/material propio: `En estos casos, la tecnica importa tanto como la prudencia.`
5. 38-50 s - Control postoperatorio si es seguro: `El seguimiento permite evaluar evolucion, seguridad y recuperacion.`
6. Cierre institucional: `Centro Medico Pellegrini - Neurocirugia y Cirugia de Columna - @drcarloszanardi - 2364384321 - www.centromedicopellegrini.com.ar`

No prometer resultados. No decir curacion. No convertirlo en "antes/despues". No usar imagenes genericas, esquemas infantiles, stock ni relleno externo.

## Estetica

Usar la linea CMP:

- Fondo claro, sobrio, medico.
- Azul Pellegrini y cian suave.
- Logo integrado, no invasivo.
- Texto corto, legible en celular.
- Contacto solo al final o muy sutil.
- Transiciones cinematograficas, no slideshow duro.
- Si usas movimiento: zoom/parallax lento, pans controlados, cortes limpios.

Referencia de gate:

`docs/reels_premium_acceptance_gate.md`

El resultado no pasa si:

- es solo suma de fotos;
- no transmite una idea clara;
- no usa material propio;
- tiene datos identificables;
- tiene texto generico;
- no trae evidencia visual suficiente;
- el cierre tiene contacto incorrecto.

## Salida esperada en results

Crear:

- `results/20260526T005108-reel-cavernoma-premium-safe-derivatives-render-v1.result.md`
- `results/20260526T005108-reel-cavernoma-premium-safe-derivatives-render-v1.manifest.json`

La respuesta debe incluir:

- `final_or_preview`: `final_candidate`, `safe_derivatives_only`, o `blocked`
- `pass_premium_gate`: true/false
- rutas locales creadas
- rutas bridge creadas
- si hubo render, duracion y resolucion
- decision de privacidad por asset
- que necesita del orquestador

Si algo falla, no responder "no pude" como cierre. Documentar rutas alternativas intentadas y proxima accion concreta.
