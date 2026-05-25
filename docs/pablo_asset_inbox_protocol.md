# Pablo Asset Inbox Protocol

## Objetivo

Permitir que Pablo (`personal-xh`) ayude a seleccionar y preparar material visual del Doctor para presentaciones, reels o documentos sin pedir acceso amplio a Google Drive ni a toda la Mac personal.

## Regla central

Pablo solo puede leer carpetas que el Doctor cree explicitamente para este fin y que el workorder autorice por ruta. No debe pedir OAuth, Google Drive, Gmail, Calendar ni permisos amplios para explorar archivos personales.

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
- No publicar, enviar por Telegram, Gmail o redes.
- No borrar ni modificar originales.

## Transporte hacia Codex orquestador

Para material no sensible y liviano:

- Pablo puede copiar al repo `codex-bridge/context/asset_packs/<fecha>-<proyecto>/`:
  - `manifest.json`
  - `selection.md`
  - contact sheets
  - miniaturas anonimizadas

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
