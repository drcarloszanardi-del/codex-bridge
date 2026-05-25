# Pablo Autonomous Worker Setup

Actualizado: 2026-05-25.

## Objetivo

Evitar que Pablo quede esperando autorizaciones manuales cuando el Doctor no esta frente a la Mac personal, sin abrir acceso amplio a archivos privados.

## Modelo operativo

Pablo corre como worker no interactivo con:

- `codex -a never --search exec`
- sandbox `workspace-write`
- `--add-dir` solo al repo `codex-bridge`
- opcionalmente `CodexAssets`, `CodexAssetInbox` y `CodexPublicablePhotos` si existen
- caches de `uv`, `pip`, Hugging Face y Torch dentro de `codex-bridge/tmp/pablo-cache`

Esto permite instalar dependencias y descargar modelos publicos dentro del repo, pero no concede Photos.app, iCloud, Drive, Downloads, Desktop, Pictures ni Full Disk Access.

`CodexPublicablePhotos` funciona como carpeta fuente de fotos publicables. Pablo puede revisarla y elegir material, pero no debe borrar, renombrar ni sobrescribir originales. El worker toma una foto de control de tamanos/fechas antes y despues de cada job; si detecta cambios en esa carpeta, deja una alerta para el orquestador.

## Instalacion unica en la Mac personal

En la Mac personal, desde el repo:

```bash
cd /Users/carloszanardi/Documents/Codex/codex-bridge
git pull --ff-only
chmod +x scripts/install_personal_xh_autonomous_launchd.sh scripts/personal_xh_autonomous_worker.py
./scripts/install_personal_xh_autonomous_launchd.sh
```

Despues de eso, launchd ejecuta el worker cada 180 segundos.

El instalador tambien crea estas carpetas:

```text
/Users/carloszanardi/CodexPublicablePhotos
/Users/carloszanardi/CodexAssetInbox
/Users/carloszanardi/CodexAssets
```

Para posteos/reels, copiar o exportar alli solo material que el Doctor considere publicable o apto para seleccion. No apuntar el worker a `Photos Library.photoslibrary`.

## Logs

```text
/Users/carloszanardi/Documents/Codex/codex-bridge/tmp/personal_xh_autonomous_worker.out.log
/Users/carloszanardi/Documents/Codex/codex-bridge/tmp/personal_xh_autonomous_worker.err.log
```

## Comportamiento esperado

1. Hace `git fetch` y `git pull --ff-only`.
2. Busca jobs `assignee: personal-xh`.
3. Reclama un job.
4. Ejecuta `codex exec` sin prompts humanos.
5. Escribe `results/<job_id>.result.md`.
6. Actualiza `status/personal-xh.json`.
7. Corre `secret_scan`.
8. Hace commit y push.

## Limites de seguridad

El worker no debe:

- abrir Photos, iCloud, Drive o bibliotecas completas;
- modificar originales dentro de `CodexPublicablePhotos`;
- enviar Telegram, Gmail, Calendar o mensajes externos;
- publicar, comprar, reservar ni contactar terceros;
- imprimir secretos;
- usar carpetas personales fuera del repo o asset inbox autorizado.

Si una tarea necesita algo fuera de esos limites, debe reportar bloqueo al orquestador.
