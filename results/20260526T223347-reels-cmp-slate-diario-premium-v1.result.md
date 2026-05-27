---
job_id: 20260526T223347-reels-cmp-slate-diario-premium-v1
worker: personal-xh
status: completed
completed_at: 2026-05-26T22:44:30-03:00
front: REELS
no_external_actions: true
no_secrets: true
---

# Resultado - Reels CMP slate diario premium v1

## summary

Slate editorial operativo para el proximo reel diario CMP/Dr. Zanardi:
propongo 3 ideas ejecutables de 35-60s, todas sostenidas por material propio
real del Doctor/CMP, sin stock, sin frases epicas y sin slideshow de fotos.

Prioridad recomendada: **Idea 1 - No se opera una imagen**. Es fuerte,
educativa, de bajo riesgo si se usan estudios anonimizados o un esquema en papel,
y transmite criterio medico en una frase. Si no llega RM segura, se puede hacer
con Doctor + consultorio + dibujo simple, sin simular evidencia clinica.

Este worker no envio mensajes externos, no publico, no abrio Fotos/iCloud/Drive
ni bibliotecas completas. El resultado es un slate para que el orquestador pida
assets por topic REELS y decida el siguiente paso.

## coverage_table

| Fuente | Estado | Uso |
| --- | --- | --- |
| `context/fronts/reels_cmp.md` | Revisada | Datos canonicos CMP, privacidad y contacto. |
| `docs/reels_premium_acceptance_gate.md` | Revisada | Gate CEO, benchmark 25 de Mayo, requisitos de reel diario. |
| `context/fronts/reels_daily/2026-05-26-brief-operativo-reel-cmp.md` | Revisada | Tema bajo riesgo: preparacion para consulta de columna. |
| `results/20260526T191159-reels-professional-open-source-tooling-and-style-research-v1.result.md` | Revisada | Workflow diario, material real, subtitulos, QA y herramientas. |
| `results/20260526T155816-reels-cmp-reference-reset-no-improvisar-v1.result.md` | Revisada | Reset editorial: no improvisar, no usar placas genericas, conceptos clinicos. |
| `results/20260526T184909-reels-cmp-quality-ceo-review-felipe-y-estandar-v1.result.md` | Revisada | Gate visual: no aprobar sin evidencia auditable ni legibilidad mobile. |
| Fotos/iCloud/Drive/Downloads/bibliotecas completas | No abiertas | Cumplimiento de restriccion del job. |

## findings

### Reglas editoriales aplicadas

- El reel debe abrir con una idea clinica clara en los primeros 3 segundos.
- Debe tener minimo dos bloques visuales propios/autorizados: Doctor, consultorio,
  CMP, esquema, instrumental seguro o estudio sanitizado.
- No se usan imagenes IA, anatomia generica, stock medico ni material que parezca
  evidencia clinica sin serlo.
- No debe ser una suma de fotos con zoom. Cada bloque visual debe cumplir una
  funcion narrativa.
- Contacto canonico obligatorio al cierre: `@drcarloszanardi`, `2364384321`,
  `www.centromedicopellegrini.com.ar`.
- Publicacion queda en hold hasta que exista manifest de assets, contact sheet y
  revision de privacidad cuadro a cuadro.

### Idea 1 - No se opera una imagen

**Mensaje central:** una resonancia importa, pero la decision se toma con
sintomas, examen fisico, evolucion y contexto del paciente.

**Por que conviene:** es sobria, educativa, concreta y diferencia al Doctor por
criterio medico. Permite usar material propio simple sin depender de un caso
identificable.

**Material exacto a pedir por topic REELS:**

```text
Para el proximo reel CMP: "No se opera una imagen".
Mandame, si podes:
1. Video vertical tuyo de 12-18s en consultorio diciendo la idea o mirando una RM.
2. 2 planos verticales de 6-10s del consultorio/escritorio sin pacientes ni papeles.
3. 1 plano vertical de tu mano dibujando columna/raiz en papel en blanco.
4. Opcional: 1 RM propia totalmente anonimizada o autorizada para recorte, sin nombre,
   fecha, ID, institucion ni interfaz.
5. Confirmame si preferis voz tuya o locucion sobria.
No mandes pacientes, pantallas con datos, HC, nombres ni fechas.
```

**Estructura 40-50s:**

| Tiempo | Video | Texto maximo en pantalla |
| --- | --- | --- |
| 0-3s | Doctor a camara o mano sobre RM anonimizada | `No se opera una imagen.` |
| 3-9s | Plano consultorio / Doctor revisando sin datos | `La imagen ayuda.` |
| 9-17s | Esquema en papel: dolor, raiz, fuerza | `El examen ordena.` |
| 17-27s | Doctor explicando / plano de manos | `Sintomas + evolucion + contexto.` |
| 27-38s | RM segura o esquema, nunca pantalla identificable | `La decision se construye.` |
| 38-47s | Cierre CMP sobrio | `Centro Medico Pellegrini` + contacto |

**Copy sobrio estilo Dr. Zanardi:**

```text
No se opera una imagen.

Una resonancia puede mostrar una hernia, pero la decision no empieza ni termina
ahi. Hay que escuchar el dolor, revisar fuerza y sensibilidad, entender la
evolucion y ordenar el contexto.

La imagen ayuda. El examen ordena. El criterio medico define el camino.

Centro Medico Pellegrini
@drcarloszanardi
2364384321
www.centromedicopellegrini.com.ar
```

**Riesgos de privacidad:**

- RM con nombre, fecha, ID, institucion o metadatos visibles.
- Reflejos o pantallas con datos en consultorio.
- Papeles reales sobre escritorio.

**Gate premium:**

- Pasa solo si hay al menos Doctor + consultorio/esquema o Doctor + RM segura.
- `pass_premium_gate=false` si se reemplaza RM por stock/anatomia generica
  presentada como evidencia.
- Cierre legible 4s minimo, contacto correcto y contact sheet de 8-12 frames.

### Idea 2 - Llegar preparado cambia la consulta

**Mensaje central:** una consulta de columna mejora cuando el paciente trae
estudios, historia del dolor, irradiacion, medicacion probada y limitaciones.

**Por que conviene:** coincide con el brief diario, es bajo riesgo
medico-legal, util para pacientes y no requiere mostrar estudios reales.

**Material exacto a pedir por topic REELS:**

```text
Para un reel educativo de consulta de columna, mandame:
1. Video vertical tuyo de 15-20s en consultorio, tono paciente: "Traer estos datos ayuda".
2. 1 plano de mano escribiendo en papel en blanco: estudios / desde cuando / hacia donde baja.
3. 1 plano del consultorio o puerta CMP sin pacientes.
4. 1 plano corto de una carpeta cerrada o agenda sin datos.
5. Si podes, una nota de voz de 30s explicando como queres decirlo.
No mandes datos de pacientes, estudios identificables ni pantallas.
```

**Estructura 35-42s:**

| Tiempo | Video | Texto maximo en pantalla |
| --- | --- | --- |
| 0-3s | Doctor a camara o entrando al consultorio | `Consulta de columna: llegue preparado` |
| 3-9s | Mano escribiendo lista | `1. Estudios previos` |
| 9-15s | Plano Doctor / escritorio limpio | `2. Desde cuando duele` |
| 15-22s | Esquema pierna/columna en papel | `3. Si baja a la pierna` |
| 22-29s | Carpeta cerrada / consultorio | `4. Que probo y que limita` |
| 29-38s | Doctor a camara | `Evaluar mejor. Decidir con prudencia.` |
| 38-42s | Cierre CMP | contacto canonico |

**Copy sobrio estilo Dr. Zanardi:**

```text
Una consulta de columna mejor preparada permite evaluar mejor.

Traiga estudios previos, anote desde cuando duele, si el dolor baja a la pierna,
que medicacion ya probo y que actividades hoy no puede hacer.

Con esa informacion, la evaluacion es mas clara y la decision medica es mas
precisa.

Centro Medico Pellegrini
@drcarloszanardi
2364384321
www.centromedicopellegrini.com.ar
```

**Riesgos de privacidad:**

- Usar carpetas, agendas o papeles reales con nombres/telefonos.
- Mostrar pantallas de turno o estudios.
- Parecer una placa administrativa si no hay presencia del Doctor.

**Gate premium:**

- Pasa solo con presencia humana o material real CMP; no alcanza una lista
  animada sobre fondo generico.
- Texto legible en celular, maximo 1-2 lineas por bloque.
- Debe sentirse como consejo medico prudente, no como publicidad de consultorio.

### Idea 3 - La ubicacion cambia el plan

**Mensaje central:** en columna, no todas las hernias o lesiones se piensan
igual; la ubicacion puede cambiar el abordaje y la estrategia.

**Por que conviene:** eleva el perfil tecnico del Doctor sin prometer resultado.
Tiene potencial premium si hay RM/TC anonima, plano de planning o instrumental
seguro.

**Material exacto a pedir por topic REELS:**

```text
Para reel "La ubicacion cambia el plan", mandame:
1. 1 video vertical de 10-15s tuyo explicando que no todas las hernias son iguales.
2. 1 RM/TC propia totalmente anonima o recortada donde se pueda marcar ubicacion,
   sin datos de paciente ni institucion.
3. 1 plano de planning: mano marcando un dibujo o impresion sin datos.
4. 1-2 planos de instrumental/equipo/consultorio, sin paciente ni campo quirurgico
   identificable.
5. Confirmame si preferis hablar de foraminal/extraforaminal o dejarlo mas general.
```

**Estructura 45-60s:**

| Tiempo | Video | Texto maximo en pantalla |
| --- | --- | --- |
| 0-3s | Doctor o imagen anonima con marca simple | `No todas las hernias son iguales.` |
| 3-11s | Doctor a camara | `No es solo el tamano.` |
| 11-22s | RM/TC recortada o esquema | `La ubicacion cambia el plan.` |
| 22-34s | Mano dibujando raiz/corredor | `Otra raiz. Otro corredor.` |
| 34-47s | Instrumental o planning seguro | `Planificar tambien es tratar.` |
| 47-56s | Doctor / CMP | `Criterio + seguridad + prudencia` |
| 56-60s | Cierre CMP | contacto canonico |

**Copy sobrio estilo Dr. Zanardi:**

```text
No todas las hernias son iguales.

A veces el problema no es solo el tamano: es la ubicacion. Una lesion puede
exigir pensar otra raiz, otro corredor y otra estrategia.

Planificar bien tambien es parte del tratamiento.

Centro Medico Pellegrini
Dr. Carlos Zanardi
@drcarloszanardi
2364384321
www.centromedicopellegrini.com.ar
```

**Riesgos de privacidad:**

- Estudio medico con datos en headers o metadatos.
- Campo quirurgico o paciente visible.
- Lenguaje demasiado tecnico sin beneficio claro para paciente.

**Gate premium:**

- Pasa si la imagen medica es propia/sanitizada o si se reemplaza por esquema
  propio honesto.
- Falla si usa anatomia generica como si fuera caso real.
- Debe mantener lenguaje prudente: evitar promesas y evitar diagnostico por red.

## recommendation

### Orden de ejecucion

1. **Elegir Idea 1 como slate principal.** Pide pocos assets, tiene tesis clara y
   puede igualar el benchmark 25 de Mayo si se usa Doctor + material real.
2. **Tener Idea 2 como fallback inmediato.** Si no hay RM segura ni material
   tecnico, es la pieza educativa diaria mas robusta.
3. **Reservar Idea 3 para cuando llegue material tecnico sanitizado.** Tiene mas
   impacto premium, pero tambien mas riesgo de privacidad y verdad visual.

### Pedido corto recomendado al Doctor

```text
Para el reel diario CMP, te propongo hacer "No se opera una imagen".
Mandame por REELS: 1 video vertical tuyo en consultorio, 2 planos del consultorio
sin pacientes, 1 video de mano dibujando columna en papel en blanco y, si tenes,
una RM totalmente anonima o que podamos recortar. Sin nombres, fechas, HC,
pantallas ni pacientes.
```

### Stories complementarias si el reel queda publicable

- Story 1: encuesta sobria: `Cuando consulta por columna, suele llevar estudios previos?`
- Story 2: checklist: `Traer: estudios / sintomas / medicacion / limitaciones`.
- Story 3: caja de preguntas: `Que le gustaria saber antes de una consulta de columna?`

### Gate operativo antes de render

```yaml
publication_hold: true
source_manifest_path: required
storyboard_path: required
subtitle_status: draft_then_manual_review
privacy_frame_pass: required_before_final
contact_sheet_path: required
final_candidate_path: required_before_publish
stories_companion_plan: required_if_publicable
pass_premium_gate: false_until_visual_evidence
```

## risks_limits

- Todavia no hay assets nuevos en este job; no se puede afirmar que una idea
  pase gate hasta recibir material real y auditarlo.
- El path `/Users/jarvis/...` del brief diario no existe en esta Mac; se uso la
  evidencia textual disponible dentro del bridge local.
- Si llega material por topic REELS, debe procesarse como conjunto antes de
  editar y debe generarse manifest de origen/permiso/sanitizacion.
- Si no llega video del Doctor, no recomiendo fabricar una pieza premium solo
  con placas. Mejor esperar o usar Idea 2 con material institucional real.

## confidence

**high** para la direccion editorial, porque deriva del gate premium CMP, del
brief diario y de resultados previos de rechazo/reset. **medium** para la idea
final hasta ver assets reales. La aprobacion visual queda necesariamente en
`publication_hold` hasta contar con material propio, contact sheet y QA.

## evidence_paths

- `jobs/20260526T223347-reels-cmp-slate-diario-premium-v1.md`
- `claims/20260526T223347-reels-cmp-slate-diario-premium-v1.json`
- `context/fronts/reels_cmp.md`
- `docs/reels_premium_acceptance_gate.md`
- `context/fronts/reels_daily/2026-05-26-brief-operativo-reel-cmp.md`
- `results/20260526T191159-reels-professional-open-source-tooling-and-style-research-v1.result.md`
- `results/20260526T155816-reels-cmp-reference-reset-no-improvisar-v1.result.md`
- `results/20260526T184909-reels-cmp-quality-ceo-review-felipe-y-estandar-v1.result.md`
