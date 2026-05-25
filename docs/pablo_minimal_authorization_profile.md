# Pablo Minimal Authorization Profile

Actualizado: 2026-05-25.

## Objetivo

Reducir las autorizaciones manuales en la Mac personal sin exponer toda la biblioteca del Doctor.

## Principio

Pablo no necesita acceso amplio a la Mac. Necesita acceso acotado a:

- `/Users/carloszanardi/Documents/Codex/codex-bridge`
- `/Users/carloszanardi/CodexAssets`
- `/Users/carloszanardi/CodexAssetInbox`

No necesita:

- Full Disk Access
- Photos.app
- `Photos Library.photoslibrary`
- iCloud / `Mobile Documents`
- Google Drive / DriveFS
- Downloads, Desktop o Pictures completos

## Comandos permitidos para autorizar

Si Codex de la Mac personal pide aprobación, autorizar solo comandos que operen dentro de esas carpetas y que coincidan con estas familias:

```bash
git pull --rebase
git fetch
git status --short
git add jobs results status claims docs scripts context/asset_packs
git commit -m ...
git push
python3 scripts/bridgectl.py ...
python3 scripts/asset_gate.py ...
python3 scripts/secret_scan.py
python3 scripts/validate_result_contract.py ...
python3 scripts/pablo_next_job.py ...
ffmpeg ...
```

Autorizar FFmpeg solo si los inputs/outputs están dentro de:

- `/Users/carloszanardi/CodexAssets`
- `/Users/carloszanardi/CodexAssetInbox`

## Comandos o accesos a rechazar

Rechazar si pide leer, copiar, subir o recorrer:

```text
/Users/carloszanardi/Pictures
/Users/carloszanardi/Downloads
/Users/carloszanardi/Desktop
/Users/carloszanardi/Library
Photos Library.photoslibrary
Mobile Documents
CloudStorage
Google Drive
DriveFS
```

Rechazar también:

- subir originales o MP4 privados al repo;
- enviar Telegram/Gmail/Drive;
- abrir credenciales;
- borrar originales;
- publicar en redes.

## Ruta operativa segura para reels

1. El Doctor o Pablo coloca material autorizado en `/Users/carloszanardi/CodexAssets/Reels/<proyecto>/`.
2. Pablo crea `manifest.json`.
3. Pablo corre:

```bash
python3 scripts/asset_gate.py validate-manifest <manifest.json> --check-exists
```

4. Pablo renderiza localmente dentro de `renders/`.
5. Pablo genera contact sheet seguro de baja resolución.
6. Pablo no sube el MP4 ni originales al bridge.
7. Pablo devuelve resultado, QA y rutas locales.
8. Codex orquestador decide si se transfiere o se rechaza.

## Regla de calidad

La autorización local solo resuelve permisos. No convierte una pieza en aceptable.
El gate final sigue siendo Codex orquestador con `docs/reels_premium_acceptance_gate.md`.
