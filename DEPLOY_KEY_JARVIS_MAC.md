# Deploy key de esta Mac

Esta es la clave publica que corresponde a la clave privada guardada en esta Mac:

```text
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIAjewWXco+U/MXuqBx6O14IEOwQR8hlF0NFQqgIgtpS8 codex-bridge-jarvis-mac
```

Debe cargarse en:

```text
GitHub -> drcarloszanardi-del/codex-bridge -> Settings -> Deploy keys
```

Con:

```text
Allow write access: activo
```

No reemplazar por otra clave publica, porque esta Mac no tendria la clave privada correspondiente y no podria hacer `git push`.

