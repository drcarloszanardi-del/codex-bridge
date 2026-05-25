---
id: 20260525T013125-corpus-jurisprudencia-leyes-gates-app-clinica
job_id: 20260525T013125-corpus-jurisprudencia-leyes-gates-app-clinica
created_at: 2026-05-25T01:36:58-03:00
created_by: personal-xh
status: completed
no_external_actions: true
no_secrets: true
---

# corpus jurisprudencia leyes gates app clinica result

## summary

El corpus medico-legal debe ser una fabrica de gates y plantillas verificables, no una biblioteca de notas. Cada fuente aceptada debe terminar en una regla accionable: campo obligatorio, redaccion minima, contradiccion bloqueante, alerta de consentimiento o evidencia requerida.

## taxonomia de fuentes

- Normativa nacional: derechos del paciente, historia clinica, consentimiento informado, proteccion de datos, responsabilidad civil profesional.
- Jurisprudencia nacional/federal: CIJ/CSJN y fallos relevantes sobre responsabilidad medica, carga probatoria, consentimiento y documentacion.
- Jurisprudencia provincial Buenos Aires: JUBA/SCBA para criterios locales frecuentes.
- SAIJ: consolidacion normativa y jurisprudencial.
- Doctrina tecnica curada: solo si se traduce a criterio verificable y queda separada de ley/fallo.
- Protocolos clinicos internos: criterios del Dr. Zanardi y equipo, siempre marcados como fuente interna.

## metadatos por norma/fallo

- `source_id`
- `tipo`: norma, fallo, doctrina, protocolo interno
- `jurisdiccion`
- `tribunal_organismo`
- `fecha`
- `estado`: vigente, historico, dudoso, derogado/no usar
- `tema`: consentimiento, historia clinica, mala praxis, neurocirugia, columna, datos personales
- `hecho_relevante`
- `criterio_util`
- `gate_derivado`
- `plantilla_afectada`
- `nivel_confianza`
- `requiere_revision_legal`

## conversion a gates

| Hallazgo del corpus | Gate/plantilla |
|---|---|
| Exigencia de consentimiento informado especifico | Consentimiento debe listar riesgos especificos del procedimiento y alternativas razonables |
| Historia clinica como documento clave | Parte debe tener fecha, profesional, diagnostico, indicacion, tecnica, hallazgos, complicaciones, cierre y firma |
| Falta de informacion como riesgo litigioso | Bloquear consentimiento generico sin procedimiento, nivel, lado y riesgos principales |
| Contradicciones documentales | Gate de consistencia entre diagnostico, indicacion, procedimiento, tecnica y consentimiento |
| Datos personales sensibles | Prohibir envio a canales externos y exigir minimizacion/anonimizacion |

## ejemplos de reglas redaccionales

- No escribir "se explicaron riesgos" sin enumerar riesgos relevantes.
- No escribir diagnostico con conducta terapeutica mezclada.
- No documentar tecnica quirurgica incompatible con topografia o procedimiento.
- Si hay complicacion, debe figurar manejo, estado final y comunicacion al paciente/familia si aplica.
- Si se usa material de osteosintesis/interbody, debe quedar claro nivel, tipo de implante y control.

## riesgos de alucinacion

- Citar fallos inexistentes o criterios no vigentes.
- Confundir jurisdiccion nacional, provincial y doctrina.
- Convertir una regla contextual de un fallo en regla universal.
- Sobrelegalizar plantillas y volverlas inutiles clinicamente.
- Incluir datos identificables de pacientes en el corpus.

## plan por etapas

1. Crear esquema `corpus_item` y `gate_item`.
2. Cargar normativa base revisada manualmente.
3. Incorporar fallos solo con fuente oficial y metadatos completos.
4. Traducir cada item a gate o plantilla; descartar lo que no produzca control util.
5. Ejecutar pruebas sinteticas con casos de columna.
6. Revisar por Dr. Zanardi y, si corresponde, asesor legal.

## recommendation

Empezar por normativa y gates de documentacion/consentimiento antes de jurisprudencia amplia. La jurisprudencia debe entrar despues, como refinamiento de riesgos y lenguaje, no como base inicial del sistema.

## confidence

Media-alta. No se consultaron fuentes externas en este workorder; requiere verificacion legal actualizada antes de uso productivo.

## evidence_paths

- `jobs/20260525T013125-corpus-jurisprudencia-leyes-gates-app-clinica.md`
