---
id: 20260525T015335-jurisprudencia-argentina-neuro-columna-plan-busqueda-completa
job_id: 20260525T015335-jurisprudencia-argentina-neuro-columna-plan-busqueda-completa
created_at: 2026-05-25T01:59:19-03:00
created_by: personal-xh
status: completed
no_external_actions: true
no_secrets: true
---

# jurisprudencia argentina neuro columna plan busqueda completa result

## summary

Estrategia reproducible: buscar primero fuentes oficiales, etiquetar confiabilidad y convertir cada hallazgo solo en gate/plantilla verificable. No usar Microjuris/medios como corpus fuerte sin copia oficial.

## official sources

- CIJ/CSJN: https://www.cij.gov.ar/
- SAIJ dossier y buscador: https://www.saij.gob.ar/dossier
- JUBA/SCBA: https://juba.scba.gov.ar/
- Fallos Rio Negro: https://fallos.jusrionegro.gov.ar/
- Infoleg normativa: https://servicios.infoleg.gob.ar/
- Normas PBA: https://normas.gba.gob.ar/

## queries

```text
site:saij.gob.ar "mala praxis médica" neurocirugía consentimiento informado
site:saij.gob.ar columna lumbar mala praxis historia clínica consentimiento
site:juba.scba.gov.ar "consentimiento informado" "historia clínica" "mala praxis"
site:juba.scba.gov.ar "historia clínica" "mala praxis médica"
site:cij.gov.ar "mala praxis médica" "consentimiento informado"
site:fallos.jusrionegro.gov.ar hernia lumbar consentimiento informado mala praxis
site:fallos.jusrionegro.gov.ar columna lumbar historia clínica pericia médica
```

## candidates from snapshot

- `NSJ-009 Villacura c/ Pilafis`: fuente oficial Rio Negro, hernia foraminal/postoperatorio, consentimiento y evolucion.
- `NSJ-010 Marchan c/ Gomez`: fuente oficial Rio Negro, hernia disco, pericia, completitud documental.
- `NSJ-011 Olivares c/ Sanatorio Juan XXIII`: fuente oficial Rio Negro, bloqueo/canal estrecho, consentimiento y evolucion.
- `NSJ-018 I., A. S. c/ Clinica y Maternidad Maria Auxiliadora`: fuente oficial JUBA, parte/historia/acto quirurgico.
- `NSJ-019 M., E. y otros c/ Hospital Municipal Vicente Lopez`: fuente oficial JUBA, historia clinica.
- `NSJ-001/002/003/004`: SAIJ dossier, utiles como summary oficial, pedir texto completo si se cita hacia afuera.

## criteria

- Inclusion: fuente oficial, tribunal, fecha, caratula/id, texto o sumario oficial, impacto documental concreto.
- Exclusion: nota periodistica sin fallo, fuente secundaria sin localizador, fallo sin relacion con documentacion clinica/gate.
- Promocion a gate: solo si el criterio produce check verificable.

## gates derived

- Historia clinica completa: sintomas, examen, estudios, diagnostico y motivo de indicacion.
- Consentimiento especifico: patologia, procedimiento, riesgos propios, alternativas, revocacion, fecha/firma.
- Parte quirurgico reconstruible: posicion, abordaje, hallazgo, maniobra, hemostasia, recuento, cierre, incidentes, destino.
- Columna: nivel, lateralidad, raiz y control por imagen si aplica.
- Implantes: tipo/material/control radioscopico/lote cuando corresponda.

## web notes

Busqueda publica confirmo fuentes oficiales utiles: Infoleg Ley 26.529, Decreto 1089/2012, JUBA fallos sobre consentimiento e historia clinica, SAIJ dossier de mala praxis. No se copiaron textos largos.

## recommendation

Work-mac debe ejecutar crawler oficial por fuente, no por Google general. Guardar cada resultado como `corpus_item` y no activar gates hasta revision.

## confidence

Media-alta. Requiere busqueda oficial exhaustiva y validacion legal.

## evidence_paths

- `tmp/clinica_app_snapshot_review/data/derived/jurisprudence_neuro_spine/jurisprudence_neuro_spine_corpus_latest.json`
- `tmp/clinica_app_snapshot_review/data/derived/jurisprudence_neuro_spine/jurisprudence_neuro_spine_impact_matrix_latest.md`
- `jobs/20260525T015335-jurisprudencia-argentina-neuro-columna-plan-busqueda-completa.md`
