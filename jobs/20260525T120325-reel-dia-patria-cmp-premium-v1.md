---
id: 20260525T120325-reel-dia-patria-cmp-premium-v1
assignee: personal-xh
model: gpt-5.5-xh
created_at: 2026-05-25T12:03:25-03:00
no_external_actions: true
no_secrets: true
status: pending
---

# Workorder: reel premium Dia de la Patria 40s - CMP / Dr. Zanardi

## 10 inicial - direccion del orquestador

- Objetivo: preparar una propuesta premium de reel de 40 segundos para publicar en redes del Dr. Zanardi/Centro Medico Pellegrini por el Dia de la Patria argentino.
- Frente: REELS / CMP.
- Contexto minimo:
  - Estetica CMP: sobria, clara, profesional, gama suave, no saturada.
  - Datos sensibles publicables:
    - IG: `@drcarloszanardi`
    - Web: `www.centromedicopellegrini.com.ar`
    - Telefono CMP: `2364384321`
  - Contexto de frente: `context/fronts/reels_cmp.md`.
  - Taste library si esta disponible en la Mac de trabajo: `/Users/jarvis/.openclaw/workspace/reels-studio/taste_library_cmp_v1.json`.
- Tono buscado: humano, sobrio, institucional, cercano. No propaganda patriotera excesiva; unir trabajo, compromiso, salud y comunidad.
- Duracion: 40 segundos maximo. Si conviene, proponer tambien version corta 25-30 segundos.
- Material probable:
  - fotos/videos de quirofano o consultorio que el Doctor puede compartir;
  - imagen institucional CMP;
  - b-roll medico sobrio;
  - fondo con guiño patrio sutil, no invasivo.
- Posible carpeta de material en la Mac personal: sugerir estructura simple para que el Doctor/Pablo pueda usarla si se habilita, por ejemplo `~/CodexAssets/Reels/DiaPatria2026/`, pero no pedir acceso a Drive ni tocar archivos privados sin autorizacion.
- Herramientas permitidas: analizar contexto local del bridge, proponer storyboard, guion, asset list, QA checklist y prompt visual; no publicar ni enviar a terceros.
- Herramientas prohibidas: acciones externas, publicar, enviar Telegram, usar datos de pacientes visibles, inventar material existente, pedir credenciales.
- Riesgos: pieza demasiado publicitaria, imagen medica no representativa, telefono incorrecto, exceso de texto, uso patriotico cursi o generico.
- Criterio de terminado: entregar propuesta ejecutable que Codex principal pueda convertir en edicion real cuando el Doctor pase material.

## 80 delegado - trabajo del agente

Pablo debe producir:

- 2 conceptos posibles, con recomendacion de uno;
- guion de texto en pantalla por escenas;
- storyboard segundo a segundo para 40s;
- plan de assets: obligatorio / deseable / opcional;
- indicaciones de color, tipografia, transiciones y ritmo;
- prompt o direccion para mejorar/generar fondos con Gemini/Nano Banana si fuera util;
- caption en estilo del Doctor, sobrio y breve;
- musica sugerida por clima, no por copyright especifico;
- checklist de QA antes de publicar.

## 10 final - retorno al orquestador

El resultado debe incluir:

- `summary honesto`
- `conceptos`
- `concepto recomendado`
- `storyboard_40s`
- `texto_en_pantalla`
- `asset_request`
- `visual_direction`
- `caption`
- `qa_checklist`
- `risks / limits`
- `recommendation`
- `confidence`
- `evidence_paths`

Validar el resultado contra `scripts/validate_result_contract.py` antes de marcarlo completado.
