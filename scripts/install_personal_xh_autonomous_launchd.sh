#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PLIST="$HOME/Library/LaunchAgents/ai.codex.personal-xh-autonomous.plist"
PY="/usr/bin/python3"
if command -v python3 >/dev/null 2>&1; then
  PY="$(command -v python3)"
fi

mkdir -p "$HOME/Library/LaunchAgents" "$ROOT/tmp"
mkdir -p "$HOME/CodexAssets" "$HOME/CodexAssetInbox" "$HOME/CodexPublicablePhotos"

cat > "$HOME/CodexPublicablePhotos/LEER-PRIMERO-PABLO.md" <<'POLICY'
# CodexPublicablePhotos

Esta carpeta es fuente de fotos publicables para Pablo.

Reglas:

- usar solo fotos que el Doctor haya copiado aca;
- no abrir Photos.app ni Photos Library;
- no borrar, renombrar, corregir ni sobrescribir archivos de esta carpeta;
- para editar, renderizar o probar, copiar primero a CodexAssetInbox o al repo;
- no subir originales a Git ni enviarlos a servicios externos;
- si una pieza requiere publicacion/envio externo, pedir autorizacion al Codex orquestador.
POLICY

cat > "$HOME/CodexAssetInbox/LEER-PRIMERO-PABLO.md" <<'POLICY'
# CodexAssetInbox

Carpeta de trabajo para copias, preselecciones, renders temporales y material derivado.
Los originales publicables viven en CodexPublicablePhotos y no se modifican.
POLICY

cat > "$PLIST" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>ai.codex.personal-xh-autonomous</string>
  <key>ProgramArguments</key>
  <array>
    <string>$PY</string>
    <string>$ROOT/scripts/personal_xh_autonomous_worker.py</string>
    <string>--once</string>
  </array>
  <key>WorkingDirectory</key>
  <string>$ROOT</string>
  <key>StartInterval</key>
  <integer>180</integer>
  <key>RunAtLoad</key>
  <true/>
  <key>StandardOutPath</key>
  <string>$ROOT/tmp/personal_xh_autonomous_worker.out.log</string>
  <key>StandardErrorPath</key>
  <string>$ROOT/tmp/personal_xh_autonomous_worker.err.log</string>
  <key>EnvironmentVariables</key>
  <dict>
    <key>PATH</key>
    <string>$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin</string>
    <key>PABLO_CODEX_MODEL</key>
    <string>gpt-5.5</string>
    <key>PABLO_CODEX_TIMEOUT_SEC</key>
    <string>7200</string>
    <key>PABLO_PUBLIC_PHOTO_DIR</key>
    <string>$HOME/CodexPublicablePhotos</string>
  </dict>
</dict>
</plist>
PLIST

launchctl unload "$PLIST" >/dev/null 2>&1 || true
launchctl load "$PLIST"
launchctl start ai.codex.personal-xh-autonomous || true

echo "Instalado: $PLIST"
echo "Logs:"
echo "  $ROOT/tmp/personal_xh_autonomous_worker.out.log"
echo "  $ROOT/tmp/personal_xh_autonomous_worker.err.log"
echo "Carpetas autorizadas:"
echo "  $HOME/CodexPublicablePhotos"
echo "  $HOME/CodexAssetInbox"
echo "  $HOME/CodexAssets"
