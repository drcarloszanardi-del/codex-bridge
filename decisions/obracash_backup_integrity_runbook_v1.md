# ObraCash backup integrity runbook v1

## regla dura

No tocar contenido operativo de ObraCash: gastos, registros, categorias, importes, comprobantes, saldos, historial ni datos cargados.

## objetivo permitido

Backup, integridad, restore drill, alertas y reporte sin abrir ni modificar contenido.

## controles

1. Backup diario cifrado o en destino seguro.
2. Snapshot semanal retenido.
3. Hash de archivos criticos.
4. Restore drill mensual en copia aislada.
5. Ventana de cambios esperada.
6. Alerta si cambia fuera de ventana o si falla backup.

## reporte

```text
Fecha:
Backup: OK/FAIL
Destino:
Hash manifest: OK/CHANGED
Restore drill: fecha ultimo OK
Alertas:
Accion requerida:
```

## permisos

- Permitido: listar nombres/rutas tecnicas, tamanos, hashes.
- No permitido: leer contenido operativo o modificar datos.

## riesgos

- Un backup no probado no es backup.
- Hash sin restore drill puede ocultar corrupcion funcional.
- Automatizacion con permisos amplios puede alterar datos por error.
