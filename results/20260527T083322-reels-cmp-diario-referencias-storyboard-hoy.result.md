---
job_id: 20260527T083322-reels-cmp-diario-referencias-storyboard-hoy
worker: personal-xh
status: completed
completed_at: 2026-05-27T09:08:00-03:00
front: REELS
no_external_actions: true
no_secrets: true
---

# Resultado - Reels CMP diario referencias + storyboard hoy

## summary

Veredicto operativo: **hold_pre_render hasta recibir material propio minimo**.

El tema de hoy, `Consulta de columna: llegue preparado`, es correcto para un
reel diario CMP: bajo riesgo, util, no depende de pacientes ni de claims
medicos fuertes. Las referencias publicas revisadas favorecen formato de
checklist corto, doctor/persona real, B-roll propio y cierre claro. Pero el gate
premium CMP no permite resolverlo como slideshow con placas; con el material
declarado hoy falta al menos un video vertical del Doctor, un plano de mano
anotando/dibujando y 1-2 planos limpios de consultorio/CMP.

La recomendacion unica es pedir ese faltante minimo y renderizar solo si llega.

## source_counts

| Tipo | Cantidad | Uso |
| --- | ---: | --- |
| Brief/OS local REELS CMP | 2 | Tema diario, hard stops y pipeline. |
| Resultados REELS previos | 2 | Gate anti-slideshow, benchmark y pedido de assets. |
| Referencias publicas web/YouTube abiertas | 9 | Patrones de formato, no contenido clinico propio. |
| Bibliotecas privadas / Drive / Telegram / Gmail / Photos | 0 | No usadas. |

## public_reference_patterns

| Ref | Fuente publica | Patron aplicable | Adaptacion CMP segura |
| --- | --- | --- | --- |
| 1 | Mayo Clinic - back pain appointment preparation: https://www.mayoclinic.org/diseases-conditions/back-pain/diagnosis-treatment/drc-20369911 | Preparar consulta con lista de sintomas, inicio, medicacion y preguntas. | Reel checklist: estudios, tiempo de dolor, irradiacion/debilidad, medicacion probada. |
| 2 | Mayo Clinic Health System - spine care FAQ: https://www.mayoclinichealthsystem.org/services-and-treatments/spine-care | Define cuando consultar y que sintomas importan: dolor que interfiere, empeora, debilidad, adormecimiento, irradiacion. | Beat visual: "si baja a la pierna / hormigueo / debilidad" sin prometer diagnostico. |
| 3 | Cleveland Clinic - preparing for your visit: https://my.clevelandclinic.org/patients/information/appointment-checklist | Lista simple antes de consulta: instrucciones, medicacion, informacion clave. | Formato de 4 items, no clase larga. |
| 4 | Cleveland Clinic - 5 ways to make appointment useful: https://health.clevelandclinic.org/5-ways-to-make-the-most-of-your-doctors-appointment/ | Tono practico y paciente activo. | Hook: "Llegar preparado mejora la consulta". |
| 5 | Mayo Clinic News Network - prepare for sensitive appointment: https://newsnetwork.mayoclinic.org/discussion/mayo-clinic-minute-tips-to-prepare-for-a-sensitive-medical-appointment/ | Registros/antecedentes, acompanante y preguntas como parte de preparacion. | B-roll de papeles limpios/mano anotando, sin datos reales. |
| 6 | Doctorly stats/format: https://vidiq.com/youtube-stats/channel/UCHCZnC9akNA9pBP7aJGNKdg/ | Canal medico grande con alto peso de Shorts; formato de educacion rapida por tema unico. | Un solo tema por reel, texto corto como ancla, no explicacion completa en pantalla. |
| 7 | Dr Karan Raj official about: https://www.drkaranrajan.com/about | Educacion medica social con mezcla de claridad, ritmo y personalidad profesional. | Doctor/humano primero; evitar reel puramente institucional. |
| 8 | Dr. Glaucomflecken stats: https://vidiq.com/youtube-stats/channel/UCYDVFfp_AN1WBiNwaf9522w/ | Skits/shorts medicos funcionan por conflicto reconocible y hook rapido. | Abrir con problema cotidiano: "No llegue a la consulta sin esta info". |
| 9 | Holy Cross spine video Q&A: https://www.holycrosshealth.org/services/neurosciences/neurosurgery/spine/videos-treating-back-pain-and-spine-problems | Especialistas responden preguntas comunes de dolor, debilidad y cuando consultar. | Estructura Q&A visual: "Que traer / que anotar / que contar". |

## findings

| Severidad | Hallazgo | Evidencia | Accion |
| --- | --- | --- | --- |
| OK | El tema diario es publicable si hay material propio minimo. | `context/fronts/reels_daily/2026-05-27-brief-operativo-reel-cmp.md` propone consulta preparada y declara faltante minimo. | Mantener tema, no cambiar a caso quirurgico. |
| OK | Referencias publicas convergen en checklist practico y preparacion de consulta. | Mayo/Cleveland recomiendan sintomas, medicacion, preguntas, registros y preparacion previa. | Usar formato de 4 beats, sin promesa clinica. |
| P0 editorial | Sin video propio, el reel cae en slideshow. | `operating_system_v1.md` marca hard stop: no compensar falta de imagen con placas, stock, texto largo ni anatomia generica. | No renderizar final hasta tener Doctor/mano/consultorio. |
| P1 | Faltan planos que hagan "CMP real". | Brief diario declara disponibles logo y fotos previas, pero faltan video Doctor, mano anotando y consultorio actual. | Pedir 3 tomas minimas. |
| P1 | El cierre debe ser mobile-first. | Gate premium exige contacto correcto y legible, cierre >=4s y preview 540x960. | Cierre con `@drcarloszanardi`, `2364384321`, web, grande y quieto. |

## storyboard_35_45s

Objetivo: 38-42s, video vertical 1080x1920, tono sobrio, sin pacientes ni datos.

| Tiempo | Funcion | Plano propio requerido | Texto en pantalla |
| ---: | --- | --- | --- |
| 0-3s | Hook | Doctor a camara o entrando a consultorio, plano vertical limpio. | `Consulta de columna` |
| 3-7s | Promesa util | Doctor/voz: "llegar preparado mejora la consulta". | `Llegue preparado` |
| 7-13s | Item 1 | Mano acomodando estudios anonimos o carpeta sin datos. | `Estudios previos` |
| 13-19s | Item 2 | Mano anotando en papel blanco. | `Desde cuando duele` |
| 19-26s | Item 3 | Doctor senala pierna/columna en esquema simple. | `Si baja a la pierna` |
| 26-33s | Item 4 | Papel limpio con lista ficticia: medicacion / actividades. | `Que probo. Que limita.` |
| 33-38s | Criterio medico | Doctor mirando estudio anonimo o consultorio sobrio. | `Decision mas clara` |
| 38-42s | Cierre CMP | Placa CMP quieta, logo/contacto grande. | `Centro Medico Pellegrini` |

Texto maximo en pantalla, excluyendo contacto: 18-24 palabras. Si hay voz del
Doctor, usar captions solo como anclas.

## gate_checklist

```yaml
material_propio:
  required: true
  minimum:
    - video_vertical_doctor_12_18s
    - plano_mano_anotando_o_esquema
    - uno_o_dos_planos_consultorio_cmp_limpio
  status: missing
privacy:
  pacientes: forbidden
  pantallas_o_papeles_con_datos: forbidden
  estudios_identificables: forbidden
  status: pending_frame_review
contacto:
  instagram: "@drcarloszanardi"
  telefono: "2364384321"
  web: "www.centromedicopellegrini.com.ar"
  cierre_minimo: "4s quieto legible"
narrativa:
  idea_en_3s: true
  anti_slideshow: true_if_assets_arrive
  stock_o_anatomia_generica: forbidden
decision:
  render_now: false
  next_step: pedir_faltante_minimo
```

## faltantes_exactos

Pedido minimo listo para orquestador/topic REELS:

```text
Para el reel diario CMP de hoy ("Consulta de columna: llegue preparado"), mandame por REELS:

1. Un video vertical tuyo de 12-18s diciendo: "Si vas a consultar por dolor de columna, llegar preparado mejora la consulta".
2. Un plano vertical de 6-8s de mano anotando en papel limpio: estudios, desde cuando duele, si baja a la pierna, medicacion.
3. Uno o dos planos verticales de 5-8s del consultorio/CMP limpio, sin pacientes, pantallas ni papeles con datos.

No mandar pacientes, HC, nombres, fechas, estudios identificables ni pantallas con informacion privada.
```

## qa_commands

Cuando existan assets y render:

```bash
rg -n "2364384321|@drcarloszanardi|centromedicopellegrini" context/fronts/reels_daily docs results
python3 scripts/validate_result_contract.py results/20260527T083322-reels-cmp-diario-referencias-storyboard-hoy.result.md
git diff --check
python3 scripts/secret_scan.py
```

QA editorial requerido fuera de este result:

```text
1. export 1080x1920;
2. contact sheet 8-12 frames;
3. preview 540x960;
4. frame review de privacidad;
5. lectura mobile de cierre;
6. decision final del orquestador antes de enviar/publicar.
```

## attempted_routes

- Se hizo `git pull --rebase`.
- Se inspeccionaron jobs con `./scripts/personal_xh_check.sh`.
- Se reclamo el job con `python3 scripts/bridgectl.py claim`.
- Se reviso el workorder y el brief operativo diario local.
- Se reviso `operating_system_v1.md` como criterio editorial interno.
- Se hizo busqueda web abierta de referencias medicas/profesionales publicas,
  sin scraping agresivo ni login.
- TikTok directo quedo limitado por acceso/robots; se usaron fuentes web
  abiertas y paginas publicas verificables.
- No se envio Telegram/Gmail/Drive/Calendar ni se contacto a terceros.
- No se abrieron bibliotecas privadas ni se usaron datos reales.

## risks_limits

- Las referencias publicas son inspiracion de formato, no fuente clinica para
  claims ni bibliografia.
- No hay assets nuevos ni video renderizado en este bridge; por eso la decision
  es hold, no aceptacion.
- La verificacion de seguidores/canales es orientativa y cambiante; se priorizo
  patron aplicable y seguridad editorial.
- Sin preview/contact sheet final no puede pasar gate premium CMP.

## recommendation

Proxima accion unica: **pedir el faltante minimo de material propio y mantener
hold_pre_render**. Si llegan las tres tomas, renderizar v1 de 38-42s con el
storyboard anterior. Si no llegan, no compensar con placas ni fotos: dejar el
reel de hoy en hold y preservar calidad premium.

## confidence

Media-alta para storyboard y gate, porque se apoya en brief local, OS diario y
referencias publicas consistentes. Media para referencias de short-form, porque
no se abrieron cuentas privadas ni TikTok directo.

## evidence_paths

- `jobs/20260527T083322-reels-cmp-diario-referencias-storyboard-hoy.md`
- `context/fronts/reels_daily/2026-05-27-brief-operativo-reel-cmp.md`
- `context/fronts/reels_daily/operating_system_v1.md`
- `docs/reels_premium_acceptance_gate.md`
- `context/fronts/reels_cmp.md`
- `results/20260526T230823-reels-cmp-low-text-transition-quality-reset-v1.result.md`
- `results/20260526T233419-reels-lumbar-cinematic-v3-shotlist-and-gate-review.result.md`
- `https://www.mayoclinic.org/diseases-conditions/back-pain/diagnosis-treatment/drc-20369911`
- `https://www.mayoclinichealthsystem.org/services-and-treatments/spine-care`
- `https://my.clevelandclinic.org/patients/information/appointment-checklist`
- `https://health.clevelandclinic.org/5-ways-to-make-the-most-of-your-doctors-appointment/`
- `https://newsnetwork.mayoclinic.org/discussion/mayo-clinic-minute-tips-to-prepare-for-a-sensitive-medical-appointment/`
- `https://vidiq.com/youtube-stats/channel/UCHCZnC9akNA9pBP7aJGNKdg/`
- `https://www.drkaranrajan.com/about`
- `https://vidiq.com/youtube-stats/channel/UCYDVFfp_AN1WBiNwaf9522w/`
- `https://www.holycrosshealth.org/services/neurosciences/neurosurgery/spine/videos-treating-back-pain-and-spine-problems`
- `claims/20260527T083322-reels-cmp-diario-referencias-storyboard-hoy.json`
