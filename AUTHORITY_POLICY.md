# Politica de autonomia para personal-xh

Esta politica define que puede hacer el Codex auxiliar de la Mac personal sin pedir intervencion humana.

## Autorizado sin pedir permiso

- Leer este repo `codex-bridge`.
- Hacer `git pull --rebase`, `git add`, `git commit` y `git push` dentro de este repo.
- Leer `jobs/`, `protocol.md`, `README.md`, `WORKER_PERSONAL_XH.md`, `status/` y `decisions/`.
- Crear o modificar archivos en:
  - `results/`
  - `status/`
  - `decisions/`
  - `scripts/`
  - `templates/`
  - documentacion del repo
- Ejecutar scripts locales del repo cuando sean razonables y no pidan credenciales.
- Usar Codex CLI con razonamiento alto/XH para analizar, proponer, auditar, programar cambios del repo y producir resultados.
- Proponer cambios de arquitectura, seguridad, QA, clinica, corpus, Telegram y automatizaciones.
- Crear resultados extensos cuando el trabajo lo requiera.
- Dividir un problema complejo en subtareas y dejar recomendaciones priorizadas.
- Resolver bloqueos con autonomia: si una ruta falla, probar alternativas razonables antes de reportar. `No pude` solo puede aparecer como bloqueo parcial documentado, con intentos realizados, evidencia, rutas fallidas, alcance aun no verificado y proxima accion concreta.

## Autorizado solo si el orquestador lo empaqueta en el job

- Analizar extractos de logs, codigo, documentos, corpus o datos clinicos que el orquestador coloque expresamente en `jobs/` o en archivos del repo.
- Proponer reglas medico-legales o gates para la app clinica.
- Proponer textos, matrices, prompts, tests o cambios de producto.
- Trabajar sobre fragmentos sanitizados de informacion sensible.

## No autorizado

- No acceder a archivos fuera del repo `codex-bridge` salvo que el job lo indique de forma explicita y segura.
- No modificar contenido de ObraCash: gastos, registros, categorias, importes, comprobantes, datos cargados, saldos, historial ni contenido operativo. ObraCash solo puede auditarse en seguridad, backup, integridad o runbooks, y aun asi sin tocar el contenido salvo orden explicita del Dr. Zanardi transmitida por el orquestador.
- No leer credenciales, llaveros, cookies, tokens, perfiles de navegador ni secretos.
- No enviar Telegram, Gmail, Drive, Calendar, WhatsApp ni mensajes externos.
- No comprar, reservar, publicar, responder mails ni contactar terceros.
- No ejecutar comandos destructivos.
- No modificar datos de pacientes reales ni exponer informacion identificable.
- No tomar decisiones finales ni cambiar prioridades globales.

## Regla de escalamiento

Si una tarea requiere algo fuera de lo autorizado, `personal-xh` debe:

1. Detener esa parte.
2. Continuar todo lo demas que si este autorizado por rutas alternativas razonables.
3. Escribir en `results/<job_id>.result.md` que permiso falta, que se intento, que evidencia parcial existe y que queda pendiente.
4. Proponer el minimo permiso necesario y la proxima accion concreta.
5. Esperar al orquestador solo para esa parte bloqueada.

## Relacion con el orquestador

El orquestador conserva el mando. `personal-xh` funciona como companero rapido de razonamiento alto y productor auxiliar dentro del repo. La salida de `personal-xh` se considera propuesta o insumo hasta que el orquestador la integre.
