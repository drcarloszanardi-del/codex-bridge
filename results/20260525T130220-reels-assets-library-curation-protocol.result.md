# Resultado - reels assets library curation protocol

Job: `20260525T130220-reels-assets-library-curation-protocol`
Worker: `personal-xh` / Pablo
Fecha: `2026-05-25`

## summary honesto

El Doctor pidio que los reels CMP se armen con material propio, sin fotos de stock ni imagenes de otro lugar. En esta Mac ya existe una primera revision local en copias, fuera del bridge, con reglas de privacidad escritas y una seleccion preliminar para el reel "Como prepararse para la consulta de columna". No se deben subir fotos privadas al bridge; el orquestador debe recibir solo codigos, manifest y decisiones, y delegar a Pablo el render cuando haga falta usar los assets reales.

## coverage_table

| Area | Estado | Evidencia |
|---|---|---|
| Politica no-stock | definida | Instruccion directa del Doctor: material propio, no fotos externas. |
| Privacidad | definida | Reglas locales en `reels_photo_review/PRIVACY_RULES.md` fuera del bridge. |
| Primer lote | disponible localmente | Copias locales codificadas en carpeta de revision personal. |
| Bridge | protegido | No se commitean fotos/videos privados; solo protocolo y rutas/codigos. |
| Reel recomendado | definido | `results/20260525T124546-reels-cmp-next-editorial-options.result.md`. |

## folder_structure

Estructura recomendada para material autorizado, sin abrir la fototeca completa en cada trabajo:

```text
~/CodexAssets/Reels/
  README_PRIVACY.md
  intake/
    YYYYMMDD_reel_tema/
      originals_authorized/
      selected/
      rejects_privacy/
      manifest.tsv
      notes.md
  working/
    reel_consulta_columna/
      assets/
      renders/
      qa/
  approved_templates/
```

Estado actual local: Pablo preparo una carpeta de revision fuera del bridge en el hilo personal:

```text
/Users/carloszanardi/Documents/Codex/2026-05-24/vos-podrias-comunicarte-con-codex-que/reels_photo_review/
```

La seleccion preliminar para el primer reel esta en:

```text
reels_photo_review/selected_for_reel_consulta_columna/
```

Importante: esas rutas son locales de la Mac personal; el Codex orquestador no debe esperar tener esos archivos en la Mac de trabajo.

## asset_manifest_schema

Manifest minimo, sin nombres privados ni metadata sensible:

```tsv
asset_code	local_path	role	privacy_status	usage_status	notes
C01	local_only	branding_cmp	safe	selected	placa vertical CMP
C04	local_only	cta_cmp	safe	selected	placa CTA institucional
C13	local_only	context_professional	needs_crop	selected_possible	contexto profesional, revisar texto visible
C15	local_only	branding_cmp_alt	safe	selected	placa vertical CMP alternativa
V02	local_only	doctor_to_camera	safe_candidate	selected	mejor base para reel consulta columna
```

Campos obligatorios:

- `asset_code`: codigo anonimo, no filename privado.
- `local_path`: `local_only` en el bridge; path real queda solo en la Mac de Pablo.
- `role`: branding, doctor_to_camera, broll_consultorio, fachada, cierre, etc.
- `privacy_status`: safe, needs_crop, reject_privacy_review.
- `usage_status`: selected, possible, rejected.
- `notes`: solo descripcion general.

## privacy_filter

Reglas duras:

- No stock, no fotos externas, no imagenes genericas de internet.
- No subir fotos/videos privados al bridge.
- No publicar ni mandar por Telegram/Gmail/Drive.
- No usar pacientes identificables.
- No usar historias clinicas, pantallas, estudios con datos, nombres, DNI, telefonos, direcciones o fechas sensibles.
- No usar quirofano/procedimientos si hay pacientes o si sugiere evidencia clinica especifica.
- No usar anatomia generada como evidencia clinica.
- Si hay duda, `reject_privacy_review`.

## selection_workflow

1. Doctor autoriza una fuente local o carpeta curada.
2. Pablo exporta o copia a carpeta local de revision, nunca al bridge.
3. Pablo crea `PRIVACY_RULES.md`, contacto visual y manifest con codigos.
4. Pablo selecciona assets propios aptos.
5. Pablo informa al orquestador por bridge solo codigos, roles y estado.
6. Orquestador decide guion/storyboard.
7. Pablo renderiza prueba local y devuelve solo artefactos permitidos o QA; no publica.

## doctor_instructions_minimal

Pedido minimo al Doctor para mantenerlo propio y seguro:

```text
Para reels CMP, mande o autorice solo material propio: fachada/placa CMP, consultorio o pasillo sin pacientes, usted hablando a camara, logo/placa institucional. No enviar pacientes, estudios, historias clinicas ni pantallas con datos.
```

Si el Doctor ya autorizo revision local de Fotos, usar esa autorizacion solo para crear una carpeta curada; no volver a escanear toda la fototeca salvo pedido expreso.

## how_to_report_assets_to_orchestrator

Formato de reporte por bridge:

```yaml
front: REELS/CMP
asset_policy: own_material_only_no_stock
asset_location: local_to_pablo_not_in_bridge
selected_assets:
  - code: V02
    role: doctor_to_camera
    use: primary talking-head base
    privacy: safe_candidate
  - code: C01
    role: branding_cmp
    use: opening or closing plate
    privacy: safe
  - code: C04
    role: cta_cmp
    use: contact/whatsapp plate
    privacy: safe
next_reel: consulta_columna_preparacion
```

## risks / limits

- El orquestador no tiene acceso directo a los archivos locales de Pablo.
- El primer lote contiene material medico/quirurgico que debe quedar fuera salvo aprobacion puntual.
- Las copias locales pueden servir para render, pero no deben commitearse.
- La autorizacion del Doctor para Fotos fue operacional; la politica estable debe ser carpeta curada.

## recommendation

Codex principal debe ordenar el reel "Como prepararse para la consulta de columna" usando solo assets propios ya seleccionados por Pablo: V02 como base de Doctor a camara y C01/C04/C15 como placas CMP. Cero stock. Pablo debe renderizar localmente cuando el orquestador mande storyboard o guion final.

## confidence

Alta para protocolo, privacidad y seleccion inicial. Media para calidad final del reel hasta revisar el video completo y no solo miniatura/seleccion preliminar.

## evidence_paths

- `jobs/20260525T130220-reels-assets-library-curation-protocol.md`
- `context/fronts/reels_cmp.md`
- `results/20260525T124546-reels-cmp-next-editorial-options.result.md`
- Local no commiteado: `/Users/carloszanardi/Documents/Codex/2026-05-24/vos-podrias-comunicarte-con-codex-que/reels_photo_review/PRIVACY_RULES.md`
- Local no commiteado: `/Users/carloszanardi/Documents/Codex/2026-05-24/vos-podrias-comunicarte-con-codex-que/reels_photo_review/REVIEW_NOTES.md`
