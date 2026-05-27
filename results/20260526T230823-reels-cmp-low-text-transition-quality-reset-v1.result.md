---
job_id: 20260526T230823-reels-cmp-low-text-transition-quality-reset-v1
worker: personal-xh
status: completed
completed_at: 2026-05-26T23:24:30-03:00
front: REELS
no_external_actions: true
no_secrets: true
---

# Resultado - Reels CMP low text transition quality reset v1

## summary

Verdict: **reiniciar direccion editorial, no salvar el reel rechazado**. Si el
Doctor rechazo transiciones, exceso de texto y calidad visual baja, el siguiente
intento no debe sumar mas placas ni explicar mas: debe contar con imagen real,
ritmo y una tesis clinica clara.

Direccion recomendada para retomar manana: **menos texto, mas video propio,
cortes motivados y transiciones invisibles**. El texto en pantalla debe anclar
ideas, no narrar todo el film. Si falta material real del Doctor/CMP, la accion
correcta es pedir assets, no improvisar con stock, slides o plantillas genericas.

No renderice nada, no envie Telegram, no abri Fotos/iCloud/Drive/Downloads ni
bibliotecas privadas.

## coverage_table

| Fuente | Estado | Uso |
| --- | --- | --- |
| `jobs/20260526T230823-reels-cmp-low-text-transition-quality-reset-v1.md` | Revisada | Rechazo del Doctor y entregable pedido. |
| `docs/reels_premium_acceptance_gate.md` | Revisada | Hard stop tras rechazo, feedback especifico 2026-05-26/27 y gate premium. |
| `context/fronts/reels_cmp.md` | Revisada | Contacto canonico, estetica sobria y gate visual. |
| `results/20260526T223347-reels-cmp-slate-diario-premium-v1.result.md` | Revisada | Slate previo y conceptos posibles. |
| `results/20260526T155816-reels-cmp-reference-reset-no-improvisar-v1.result.md` | Revisada | No improvisar, pedir material propio y evitar placas genericas. |
| `results/20260526T191159-reels-professional-open-source-tooling-and-style-research-v1.result.md` | Revisada | Workflow diario, ritmo, material real, subtitulos y QA. |
| `results/20260526T184909-reels-cmp-quality-ceo-review-felipe-y-estandar-v1.result.md` | Revisada | No aprobar sin evidencia visual auditable ni legibilidad mobile. |
| Fotos/iCloud/Drive/Downloads/bibliotecas completas | No abiertas | Cumplimiento de restriccion del job. |

## findings

### Diagnostico breve: por que falla un reel con demasiado texto

1. **El texto compite con el film.** Si cada plano trae una frase descriptiva,
   el espectador lee en vez de mirar. El resultado se siente como presentacion,
   no como reel.
2. **Las transiciones quedan expuestas.** Cuando una escena no tiene accion
   visual real, el editor intenta resolver con zooms, wipes o cortes llamativos;
   eso evidencia plantilla y baja calidad.
3. **La medicina pierde cuerpo.** Un reel CMP debe mostrar criterio medico con
   persona, espacio real, manos, estudio sanitizado o esquema propio. Texto sin
   material parece generico.
4. **No hay progresion visual.** Un slideshow cambia placas, pero no avanza una
   historia. El benchmark 25 de Mayo funciono porque tenia tesis, ritmo, imagen
   real, audio y cierre institucional.
5. **El cierre se siente publicitario si el resto no construye autoridad.** El
   contacto debe rematar una pieza util, no compensar falta de contenido.

### Reglas visuales concretas de transicion y cadencia

#### Principios

- Una transicion debe responder a una accion o idea, no decorar.
- El corte debe sentirse "inevitable": mirada -> objeto, mano -> esquema,
  estudio -> explicacion, consultorio -> cierre.
- Preferir cortes limpios, J-cuts/L-cuts de audio, match cuts simples y
  disolvencias cortas. Evitar zooms de foto, wipes, flashes, giros, glitches o
  plantillas llamativas.
- Cada plano debe tener una razon editorial: rostro, evidencia, contexto, accion
  medica o cierre. Si no cumple ninguna, no entra.

#### Cadencia 40-60s

| Tipo de plano | Duracion sugerida | Regla |
| --- | ---: | --- |
| Hook con Doctor o imagen real | 2-3s | Una frase visual y verbal, nunca logo primero. |
| Plano humano a camara | 4-7s | Si supera 7s, cortar con B-roll real o punch-in leve. |
| Mano dibujando / esquema | 3-5s | Mostrar accion completa, no placa estatica. |
| RM/TC sanitizada o material tecnico | 3-6s | Solo si es propio/seguro y aporta al argumento. |
| Consultorio/pasillo/CMP | 2-4s | Usar como respiracion visual, no relleno largo. |
| Cierre institucional | 4s minimo | Estable, legible, sin transicion ruidosa. |

#### Transiciones permitidas

| Transicion | Uso correcto | Evitar |
| --- | --- | --- |
| Corte por accion | Mano entra al cuadro -> corte a dibujo/RM | Cortar al azar entre fotos. |
| J-cut de voz | La voz entra antes del plano siguiente | Silencio entre bloques. |
| L-cut | Mantener voz mientras cambia a B-roll real | Cortes bruscos de audio. |
| Match cut | Linea del dibujo -> linea en RM/esquema | Match artificial con stock. |
| Disolvencia corta 6-10 frames | Pasar a cierre o respiracion institucional | Disolvencias largas entre todas las escenas. |
| Push-in leve 3-5% | Enfatizar palabra clave en plano real | Ken Burns repetido sobre fotos. |

#### Texto en pantalla

- Maximo 4-6 palabras por beat.
- Maximo 1 idea por pantalla.
- No subtitular todo si hay voz; usar captions grandes solo para palabras clave.
- Texto total del reel: ideal 25-45 palabras, excluyendo contacto final.
- Si una frase necesita coma larga, va en voz/caption, no como placa.

## storyboard_template_40_60s

Plantilla recomendada para el siguiente intento, usando el concepto
**No se opera una imagen** porque permite menos texto y mas presencia real.

| Tiempo | Funcion | Imagen real requerida | Texto maximo |
| --- | --- | --- | --- |
| 0-3s | Hook | Doctor en consultorio mirando a camara o RM segura sobre mesa | `No se opera una imagen.` |
| 3-8s | Tension | Doctor senala RM/esquema sin datos | `La imagen ayuda.` |
| 8-15s | Criterio | Mano dibuja columna/raiz en papel blanco | `El examen ordena.` |
| 15-24s | Explicacion | Doctor a camara, corte con J-cut | `Sintomas. Fuerza. Evolucion.` |
| 24-34s | Medicina concreta | RM anonima o esquema propio, con marca simple | `La decision se construye.` |
| 34-44s | Humanizacion | Plano consultorio/pasillo CMP + Doctor trabajando | `Criterio y prudencia.` |
| 44-52s | Cierre | Placa CMP sobria o Doctor + banda institucional limpia | `Centro Medico Pellegrini` |
| 52-56s opcional | Contacto | Cierre quieto legible | `@drcarloszanardi` / `2364384321` / web |

### Guion de voz sugerido

```text
No se opera una imagen.

Una resonancia puede mostrar un problema, pero la decision no empieza ni termina
ahi. Hay que escuchar al paciente, examinar fuerza y sensibilidad, entender la
evolucion y ordenar el contexto.

La imagen ayuda. El examen ordena. El criterio medico define el camino.

Centro Medico Pellegrini.
```

### Texto maximo total en pantalla

```text
No se opera una imagen.
La imagen ayuda.
El examen ordena.
Sintomas. Fuerza. Evolucion.
La decision se construye.
Centro Medico Pellegrini.
@drcarloszanardi
2364384321
www.centromedicopellegrini.com.ar
```

## qa_checklist_before_send

### Editorial

- La primera frase se entiende en 3 segundos.
- Se puede explicar el reel en una frase sin sonar generico.
- Cada plano tiene una razon: rostro, accion, evidencia segura, contexto o
  cierre.
- No hay mas de 6 palabras por beat visual.
- No se intenta rescatar la estructura rechazada.

### Visual

- Minimo 2 bloques de video propio o material real autorizado.
- No parece slideshow de fotos con zoom/pan.
- Transiciones limpias: corte por accion, J-cut/L-cut, match cut o disolvencia
  corta solo donde corresponda.
- Planos humanos bien expuestos, sin recortes raros, sin texto diminuto.
- Cierre quieto y legible al menos 4 segundos.

### Privacidad

- Sin pacientes, HC, nombres, DNI, fechas, turnos, estudios identificables,
  pantallas ni reflejos con datos.
- RM/TC solo si esta anonimizada o recortada sin headers/metadatos.
- Papeles en blanco o esquema ficticio; no agenda ni formularios reales.

### Marca/contacto

- `@drcarloszanardi` correcto.
- `2364384321` correcto.
- `www.centromedicopellegrini.com.ar` correcto.
- Estetica CMP sobria, no flyer ni aviso de WhatsApp.

### Evidencia obligatoria

```yaml
publication_hold: true
source_manifest_path: required
storyboard_path: required
contact_sheet_path: required
privacy_frame_pass: required
subtitle_status: manual_review_required
audio_status: voice_or_music_decided
final_candidate_path: required_before_publish
pass_premium_gate: false_until_visual_evidence
```

## material_a_pedir_al_doctor

Pedido corto para topic REELS, a enviar solo por el orquestador:

```text
Para retomar el reel CMP sin tanto texto y con mejor imagen, mandame por REELS:

1. Un video vertical tuyo de 12-18s en consultorio diciendo la idea: "No se opera una imagen".
2. Dos planos verticales de 6-10s del consultorio/escritorio sin pacientes ni papeles.
3. Un plano vertical de tu mano dibujando columna/raiz en papel blanco.
4. Si tenes, una RM totalmente anonima o autorizada para recortar, sin nombre, fecha, ID ni interfaz.
5. Una nota de voz corta si queres que usemos tus palabras exactas.

No mandes pacientes, pantallas con datos, HC, nombres, fechas ni estudios identificables.
```

Asset minimo si el Doctor esta apurado:

```text
1 video del Doctor + 1 plano de mano dibujando + 1 plano consultorio limpio.
```

Con eso se puede construir un reel educativo sobrio sin stock y sin simular
evidencia clinica. Si no llega ni ese minimo, recomiendo no producir manana.

## recommendation

Retomar manana con una **direccion de bajo texto**:

1. Elegir un solo concepto: `No se opera una imagen`.
2. Pedir el asset minimo antes de editar.
3. Armar primero un storyboard visual, no un guion largo.
4. Limitar texto en pantalla a anchors de 4-6 palabras.
5. Usar transiciones motivadas por accion/voz, no plantillas.
6. Exportar preview + contact sheet antes de cualquier envio.
7. Si el preview no transmite con imagen sin leer todo el texto, rechazarlo
   internamente.

No producir otra version basada en el reel rechazado salvo que el orquestador lo
marque explicitamente como rescate. La regla del gate es clara: rechazo del
Doctor implica nueva direccion editorial desde cero.

## risks_limits

- No hay assets nuevos disponibles en este job; la aprobacion visual queda en
  hold hasta recibir material real y auditarlo.
- No inspeccione bibliotecas privadas ni rutas externas de reels-studio.
- El resultado no es un render ni un storyboard final con paths; es una
  direccion editorial accionable para que el orquestador pida material.

## confidence

**high** para el diagnostico editorial y reglas de transicion, porque derivan
del feedback especifico agregado al gate, del rechazo del Doctor y de resultados
REELS previos. **medium** para el storyboard final hasta ver assets reales.

## evidence_paths

- `jobs/20260526T230823-reels-cmp-low-text-transition-quality-reset-v1.md`
- `claims/20260526T230823-reels-cmp-low-text-transition-quality-reset-v1.json`
- `docs/reels_premium_acceptance_gate.md`
- `context/fronts/reels_cmp.md`
- `results/20260526T223347-reels-cmp-slate-diario-premium-v1.result.md`
- `results/20260526T155816-reels-cmp-reference-reset-no-improvisar-v1.result.md`
- `results/20260526T191159-reels-professional-open-source-tooling-and-style-research-v1.result.md`
- `results/20260526T184909-reels-cmp-quality-ceo-review-felipe-y-estandar-v1.result.md`
