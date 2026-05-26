---
id: 20260526-reel-cavernoma-authorized-assets
created_at: 2026-05-26T00:45:34-03:00
created_by: personal-xh
front: REELS
asset_policy: authorized_folder_only_no_raw_commit
status: ready_for_orchestrator
updated_at: 2026-05-26T00:48:25-03:00
no_external_actions: true
no_secrets: true
---

# Reel Cavernoma - authorized local asset manifest

## summary

El Doctor indico que el material para el reel de cavernoma esta en la carpeta local:

`/Users/carloszanardi/Documents/Codex/codex-bridge/Reel Cavernoma `

Nota tecnica: el nombre de la carpeta tiene un espacio final despues de `Cavernoma`.

La carpeta fue localizada por Pablo/personal-xh. Contiene 7 medios utilizables y 1 `.DS_Store` excluido. Los originales quedan locales y no deben commitearse ni pushearse al bridge sin confirmacion explicita adicional, por tratarse de material medico/quirurgico potencialmente sensible.

## asset_safety_rules

- Usar solo esta carpeta autorizada para el reel cavernoma.
- No buscar en Fotos, Drive, Gmail, Telegram, Downloads ni otras carpetas personales.
- No commitear ni subir originales medicos al repositorio.
- Antes de publicar o transferir, hacer gate de privacidad: revisar datos visibles, placas, nombres, fechas, identificadores y metadata EXIF.
- Si Codex necesita el contenido visual real fuera de esta Mac, pedir confirmacion explicita para una copia anonimizada o asignar render/curation a Pablo con estos paths locales.
- Para el reel final, evitar datos identificables y usar lenguaje educativo, no historia clinica individual.

## overnight_authorization_update

El Doctor pidio dejar autorizaciones ahora para no frenar el trabajo durante la noche. Autorizaciones concedidas a Pablo/personal-xh para este reel, limitadas a la carpeta `Reel Cavernoma ` y a derivados locales:

- Crear y usar carpeta local de trabajo: `/Users/carloszanardi/CodexAssets/Reels/reel_cavernoma/`.
- Generar miniaturas/contact sheet locales con `qlmanage` para revision y QA.
- Preparar copias derivadas locales con `sips` para quitar/evitar metadata y trabajar sin tocar originales.
- Renderizar pruebas locales del reel con material de esta carpeta si Codex/orquestador lo asigna.
- Publicar por bridge manifiestos, jobs, resultados, QA y rutas locales; no publicar originales medicos crudos.

Autorizacion NO concedida automaticamente:

- Subir, commitear o transferir imagenes/videos medicos crudos fuera de esta Mac.
- Buscar material en Fotos, Drive, Gmail, Telegram, Downloads u otras carpetas.
- Publicar el reel o enviarlo a terceros.

Estado local ya preparado por Pablo:

- Thumbnails: `/Users/carloszanardi/CodexAssets/Reels/reel_cavernoma/qa/thumbs/`
- Working: `/Users/carloszanardi/CodexAssets/Reels/reel_cavernoma/working/`
- Renders: `/Users/carloszanardi/CodexAssets/Reels/reel_cavernoma/renders/`
- Derivados anonimizables: `/Users/carloszanardi/CodexAssets/Reels/reel_cavernoma/sanitized/`

## selected_assets

| code | local_path | type | technical_note | suggested_role | privacy_gate |
|---|---|---|---|---|---|
| CAV-IMG-001 | `/Users/carloszanardi/Documents/Codex/codex-bridge/Reel Cavernoma /Iagen preop.jpeg` | image/jpeg | 4032x3024, EXIF present | preop visual candidate | review identifiers + strip metadata |
| CAV-IMG-002 | `/Users/carloszanardi/Documents/Codex/codex-bridge/Reel Cavernoma /Imagen preop.jpeg` | image/jpeg | 4032x3024, EXIF present | preop visual candidate | review identifiers + strip metadata |
| CAV-IMG-003 | `/Users/carloszanardi/Documents/Codex/codex-bridge/Reel Cavernoma /15b6b5e8-ee7b-4ad8-a102-a7f92691ead8.jpg` | image/jpeg | 1600x1200 | case/supporting visual | review identifiers |
| CAV-IMG-004 | `/Users/carloszanardi/Documents/Codex/codex-bridge/Reel Cavernoma /66072eeb-f180-4ef4-be90-553918281123.jpg` | image/jpeg | 1599x899 | case/supporting visual | review identifiers |
| CAV-IMG-005 | `/Users/carloszanardi/Documents/Codex/codex-bridge/Reel Cavernoma /Pieza quirurgfica .jpg` | image/jpeg | 1200x1600 | surgical piece visual, use only if medically appropriate | high sensitivity review |
| CAV-IMG-006 | `/Users/carloszanardi/Documents/Codex/codex-bridge/Reel Cavernoma /Monitoreo inraoperaorio.jpg` | image/jpeg | 1600x1200 | intraoperative monitoring context | review screen identifiers |
| CAV-VID-001 | `/Users/carloszanardi/Documents/Codex/codex-bridge/Reel Cavernoma /Video control postoperatorio.mp4` | video/mp4 | MP4 | postop control visual candidate | review identifiers/audio/metadata |

## proposed_reel_direction

Tema sugerido: `Cavernoma: de la imagen al control postoperatorio`.

Estructura inicial sugerida para Codex/orquestador:

1. Hook: "Un cavernoma no se cuenta solo con una imagen: se entiende con diagnostico, plan y control."
2. Preoperatorio: usar `CAV-IMG-001` o `CAV-IMG-002` si pasan privacidad.
3. Quirofano/monitoreo: usar `CAV-IMG-006` como contexto tecnico si no muestra datos sensibles.
4. Pieza quirurgica: usar `CAV-IMG-005` solo si el tono del reel lo justifica y el Doctor lo aprueba para publico.
5. Control: usar `CAV-VID-001` o frame derivado si pasa revision.
6. Cierre: mensaje educativo y consulta profesional, sin prometer resultados.

## orchestrator_request

Codex principal debe tomar este manifiesto como handoff de material autorizado y decidir el siguiente job:

- storyboard/guion para reel cavernoma, o
- pedido a Pablo para generar contact sheet anonimizada, o
- pedido a Pablo para renderizar una primera prueba local usando solo estos assets.

Los originales permanecen locales en Pablo. Para no frenar el flujo nocturno, el orquestador puede asignar a Pablo curation/render/QA local con estos assets y usar las carpetas `qa`, `working`, `renders` y `sanitized` ya creadas.

## evidence_paths

- `context/asset_packs/20260526-reel-cavernoma/manifest.md`
- `/Users/carloszanardi/Documents/Codex/codex-bridge/Reel Cavernoma `
- `/Users/carloszanardi/CodexAssets/Reels/reel_cavernoma/`
