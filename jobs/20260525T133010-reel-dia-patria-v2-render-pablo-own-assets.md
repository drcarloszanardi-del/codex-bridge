---
id: 20260525T133010-reel-dia-patria-v2-render-pablo-own-assets
assignee: personal-xh
model: gpt-5.5-xh
created_at: 2026-05-25T13:30:10-03:00
front: REELS
no_external_actions: true
no_secrets: true
status: pending
---

# Workorder: render profesional Día de la Patria v2 con material propio en Mac de Pablo

## 10 inicial - dirección del orquestador

El Doctor rechazó la v1 por contenido vacío. Pide explícitamente:

- Agregar imágenes/videos nuestros.
- Revisar lo que Pablo recopiló.
- Armar un video de reel, profesional.
- Usar la Mac de Pablo porque es mucho más rápida.

Esta tarea debe ejecutarse en la Mac personal de Pablo, con material propio/autorizado que ya recopiló localmente. El orquestador conserva decisión final. No generar otra pieza de placas vacías.

## Seguridad obligatoria antes de tocar assets

Usar solo carpetas autorizadas:

- `/Users/carloszanardi/CodexAssetInbox/`
- `/Users/carloszanardi/CodexAssets/`
- Si el material ya recopilado está en la carpeta local previa, mover o copiar derivados de trabajo a una de esas raíces antes de renderizar.

Prohibido:

- Abrir/recorrer `Photos Library.photoslibrary`.
- Recorrer `~/Pictures`, `~/Downloads`, `~/Desktop`, iCloud, Google Drive/DriveFS o carpetas personales amplias.
- Subir originales, videos privados, HEIC/MOV/MP4 o fotos grandes al bridge.
- Publicar, enviar Telegram/Gmail/Drive o usar acciones externas.

Antes de usar el material:

```bash
python3 scripts/asset_gate.py validate-manifest <manifest.json> --check-exists
```

Antes de commitear cualquier resultado:

```bash
python3 scripts/asset_gate.py scan-bridge
python3 scripts/secret_scan.py
```

## Dirección editorial

Tesis de contenido:

```text
El 25 de Mayo no se honra con frases vacías. También se honra haciéndose cargo del trabajo cotidiano.
En salud, hacerse cargo es escuchar, estudiar el caso, explicar con claridad y acompañar decisiones difíciles.
```

Tono:

- sobrio;
- humano;
- local/JUNÍN;
- médico serio, no marketing hueco;
- compatible con Centro Médico Pellegrini.

Contacto obligatorio:

- `@drcarloszanardi`
- `2364384321`
- `www.centromedicopellegrini.com.ar`

## Material sugerido

Revisar el material propio que Pablo ya seleccionó:

- `V02`: Doctor hablando a cámara, si es seguro completo.
- `C01`, `C04`, `C15`: placas CMP.
- Cualquier imagen/video propio adicional seguro dentro de la carpeta autorizada: fachada, consultorio, pasillo, quirófano sin paciente identificable, Doctor/equipo sin datos sensibles.

Si hay material quirúrgico, usarlo solo si no expone paciente ni datos y si aporta al mensaje. Evitar shock visual o sensacionalismo.

## 80 delegado - trabajo del agente

Producir un borrador real, no solo storyboard, si el material pasa el gate:

- `asset_review`: qué usó y qué descartó, con motivo.
- `manifest_path`: manifest validado.
- `script_v2`: texto final exacto.
- `storyboard_v2`: tiempos y visuales.
- `render_status`: ruta local del MP4 exportado en la Mac de Pablo, duración, resolución y tamaño.
- `qa_visual`: contacto, legibilidad, privacidad, coherencia narrativa, solapamientos, audio.
- `transfer_plan`: cómo pasar el MP4 final al orquestador sin exponer biblioteca completa. Si el render es apto para revisión interna y no contiene datos sensibles, puede quedar en carpeta autorizada para transferencia controlada, pero no lo suba al bridge.
- `needs_orchestrator_decision`: ajustes concretos antes de mandar al Doctor.

Si no puede renderizar por riesgo real, entregue evidencia del gate, alternativas y un plan de render seguro. No cierre con “no pude”.

## Criterio de aceptación

La pieza debe:

- decir algo claro en los primeros 3 segundos;
- tener al menos 2 bloques visuales con material nuestro;
- no depender de texto genérico;
- sostener una progresión: tesis -> medicina concreta -> cierre CMP;
- parecer una pieza del Doctor/CMP, no una plantilla genérica;
- estar lista para que Codex orquestador la evalúe y decida si se envía al Doctor.

## 10 final - retorno al orquestador

Incluir `summary honesto`, `coverage_table`, `risks / limits`, `recommendation`, `confidence`, `evidence_paths`.
Validar contra `scripts/validate_result_contract.py`.
