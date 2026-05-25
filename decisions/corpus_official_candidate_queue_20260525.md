# Corpus official candidate queue 2026-05-25

## candidatos

| Prioridad | Fuente | URL oficial | Busqueda | source_status | Gate posible | Requiere copia completa |
|---|---|---|---|---|---|---|
| P0 | Ley 26.529 Derechos del Paciente | https://servicios.infoleg.gob.ar/infolegInternet/anexos/160000-164999/160432/texact.htm | ley 26529 consentimiento informado historia clinica | official_norm | consentimiento especifico, historia clinica completa | no |
| P0 | Decreto 1089/2012 | https://servicios.infoleg.gob.ar/infolegInternet/anexos/195000-199999/199296/norma.htm | decreto 1089 2012 ley 26529 | official_norm | detalle reglamentario CI/HC | no |
| P0 | Ley 25.326 datos personales | https://servicios.infoleg.gob.ar/infolegInternet/anexos/60000-64999/64790/texact.htm | ley 25326 datos personales salud | official_norm | no exponer datos sensibles | no |
| P0 | CCyC Ley 26.994 | https://servicios.infoleg.gob.ar/infolegInternet/anexos/235000-239999/235975/texact.htm | codigo civil consentimiento responsabilidad profesional | official_norm | responsabilidad profesional/dano | no |
| P1 | JUBA idFallo 161074 | https://juba.scba.gov.ar/VerTextoCompleto.aspx?idFallo=161074 | consentimiento informado mala praxis | official_judiciary_full_text | CI como deber autonomo | no |
| P1 | JUBA idFallo 192025 | https://juba.scba.gov.ar/VerTextoCompleto.aspx?idFallo=192025 | historia clinica consentimiento mala praxis manguito | official_judiciary_full_text | HC con tiempos/controles/material | no |
| P1 | CIJ sentencia SGU d2042623 | https://www.cij.gov.ar/sentencias/d/sentencia-SGU-d2042623-1b80-4473-9c6e-3dd21a04b3e3.pdf | consentimiento informado mala praxis historia clinica | official_judiciary_pdf | CI probado y riesgos posoperatorios | si |
| P1 | Fallos Rio Negro Villacura | https://fallos.jusrionegro.gov.ar/protocoloweb/protocolo/protocolo?id_protocolo=22651551-3d3a-4cde-a2e2-c4ef831189e2&option_text=0&usarSearch=1 | hernia lumbar consentimiento informado | official_judiciary_full_text | hernia lumbar CI/evolucion | no |
| P1 | Fallos Rio Negro Avendano | https://fallos.jusrionegro.gov.ar/protocoloweb/protocolo/protocolo?id_protocolo=e71e6494-30d0-4d45-abf9-b2bbf6e72a17&option_text=0&usarSearch=1 | neurocirugia consentimiento informado alto riesgo | official_judiciary_full_text | alto riesgo/CI | no |
| P2 | SAIJ dossier mala praxis | https://www.saij.gob.ar/docs-f/dossier-f/mala_praxis_medica.pdf | SAIJ mala praxis medica neurocirugia | official_saij_summary | historia completa y parte reconstruible | si para citar fuera |

## reglas de uso

- `official_norm` y `official_judiciary_full_text` pueden alimentar gates tras revision.
- `official_saij_summary` puede alimentar tamiz interno, pero pedir texto completo si se va a citar fuera.
- Fuentes secundarias quedan fuera de gates activos hasta oficializar.

## queries reproducibles

```text
site:juba.scba.gov.ar "consentimiento informado" "mala praxis"
site:juba.scba.gov.ar "historia clínica" "mala praxis médica"
site:cij.gov.ar "consentimiento informado" "mala praxis médica"
site:fallos.jusrionegro.gov.ar "hernia" "consentimiento informado"
site:saij.gob.ar "mala praxis médica" "neurocirugía"
```
