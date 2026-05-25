# Pablo Asset Inbox Protocol

## Objetivo

Permitir que Pablo (`personal-xh`) ayude a seleccionar y preparar material visual del Doctor para presentaciones, reels o documentos sin pedir acceso amplio a Google Drive ni a toda la Mac personal.

## Regla central

Pablo solo puede leer carpetas que el Doctor cree explicitamente para este fin y que el workorder autorice por ruta. No debe pedir OAuth, Google Drive, Gmail, Calendar ni permisos amplios para explorar archivos personales.

Ademas, antes de usar material visual debe pasar el gate local:

```bash
python3 scripts/asset_gate.py validate-manifest <manifest.json> --check-exists
```

Si el gate falla, Pablo no debe renderizar ni copiar material. Debe devolver el error en `results/` y proponer una alternativa segura.

## Carpeta sugerida en la Mac personal

```text
/Users/carloszanardi/CodexAssetInbox/
```

Estructura recomendada:

```text
CodexAssetInbox/
  PRESENTACIONES/
    <proyecto>/
      original/
      selected/
      notes.md
      manifest.json
  REELS/
    <proyecto>/
      original/
      selected/
      notes.md
      manifest.json
```

Tambien se acepta:

```text
/Users/carloszanardi/CodexAssets/
```

No se aceptan como raiz autorizada: `Photos Library.photoslibrary`, `~/Pictures`, `~/Downloads`, `~/Desktop`, iCloud, Google Drive/DriveFS, `CloudStorage` ni carpetas amplias personales.

## Que puede hacer Pablo

- Leer solo la carpeta autorizada en el workorder.
- Crear inventario de imagenes/videos: nombre, dimensiones, peso, fecha, tema probable.
- Armar contact sheet de baja resolucion para revision del orquestador.
- Separar material util, dudoso y descartado.
- Proponer uso por slide/escena: portada, anatomia, quirófano, caso, cierre, fondo, textura.
- Redactar `manifest.json` y `selection.md` con criterio de uso.
- Si el material tiene datos sensibles, advertirlo y no copiarlo al repo Git.

## Que no puede hacer Pablo

- No pedir acceso a Drive ni conectores externos.
- No recorrer `~/Downloads`, `~/Desktop`, Fotos, iCloud, Drive o carpetas personales salvo ruta autorizada.
- No subir pacientes, imagenes sensibles ni material no anonimizado al repo GitHub.
- No commitear originales, videos privados, HEIC/MOV/MP4 originales ni fotos grandes al bridge.
- No usar rutas absolutas de archivos privados en `results/`; reportar codigos y rutas locales solo cuando sea imprescindible para el orquestador.
- No publicar, enviar por Telegram, Gmail o redes.
- No borrar ni modificar originales.

## Transporte hacia Codex orquestador

Para material no sensible y liviano:

- Pablo puede copiar al repo `codex-bridge/context/asset_packs/<fecha>-<proyecto>/`:
  - `manifest.json`
  - `selection.md`
  - contact sheets anonimizadas y de baja resolucion
  - miniaturas anonimizadas de baja resolucion

Antes de commitear, correr:

```bash
python3 scripts/asset_gate.py scan-bridge
python3 scripts/secret_scan.py
```

Para material sensible o pesado:

- Pablo no lo sube a Git.
- Entrega solo manifest, hashes, contact sheet anonimizada y ruta local original.
- El orquestador decide si pide transferencia local controlada, AirDrop, carpeta compartida o procesamiento en la Mac personal.

## Formato minimo de manifest

```json
{
  "schema": "codex_asset_manifest.v1",
  "project": "nombre del proyecto",
  "authorized_root": "/Users/carloszanardi/CodexAssetInbox/PRESENTACIONES/proyecto",
  "created_by": "personal-xh",
  "contains_sensitive_material": true,
  "asset_policy": "curated_folder_only_no_full_library",
  "items": [
    {
      "file": "original/imagen_001.jpg",
      "type": "image",
      "dimensions": "1920x1080",
      "sensitivity": "none | possible_patient | patient_identifiable | document_identifiable",
      "recommended_use": "portada | slide_clinica | broll | descartar",
      "notes": "criterio breve"
    }
  ]
}
```

## Regla de decision

Pablo prepara y clasifica. Codex orquestador decide que entra en una presentacion/reel. El Doctor aprueba cualquier uso publico o transferencia externa de material sensible.

## Reels autonomos

Para armar reels de manera autonoma:

1. El workorder debe nombrar una raiz autorizada.
2. Pablo crea o actualiza `manifest.json`.
3. Pablo corre `asset_gate.py validate-manifest`.
4. Pablo renderiza solo derivados locales dentro de la carpeta autorizada.
5. Pablo devuelve `storyboard`, `qa`, `render_status` y, si corresponde, ruta local del export.
6. El orquestador revisa y decide si se transfiere por una ruta controlada o si se pide nuevo render.
