# CMP Daily Reel OS v1

Estado: activo como criterio editorial interno.
Origen: `results/20260527T000329-reels-cmp-daily-premium-operating-system-v1.result.md`

## Regla central

Calidad diaria no significa publicar diario. Significa decidir todos los dias si se puede:

- renderizar;
- pedir mas material;
- o poner en hold.

Si faltan planos propios/autorizados, no se compensa con placas, stock, texto largo ni anatomia generica.

## Pipeline diario

1. Idea diaria en una frase.
2. Pedido de assets por tipo de pieza.
3. Manifest de origen, permiso y privacidad.
4. Brief corto: hook, 3 beats, cierre CMP, audio, riesgos.
5. Storyboard visual antes de guion largo.
6. Gate pre-render.
7. Edicion sobria: video real, cortes por accion/forma/audio, no slideshow.
8. Texto en pantalla como ancla; copy como explicacion.
9. QA: contact sheet, preview 540x960, privacidad, contacto, cierre >= 4s.
10. Decision del orquestador.

## Decision tree

```text
START
  |
  |-- Hay idea clara en 1 frase?
  |     |-- no -> BLOQUEAR
  |     |-- si
  |
  |-- Hay minimo 2 bloques visuales propios/autorizados?
  |     |-- no -> PEDIR_MAS_MATERIAL
  |     |-- si
  |
  |-- Hay riesgo de privacidad no resuelto?
  |     |-- si -> BLOQUEAR
  |     |-- no
  |
  |-- Storyboard evita slideshow, stock y placas largas?
  |     |-- no -> REESCRIBIR
  |     |-- si
  |
  |-- Audio/subtitulos/cierre/contacto decididos?
  |     |-- no -> HOLD_PRE_RENDER
  |     |-- si
  |
  |-- Contact sheet + preview 540x960 pasan gate?
        |-- no -> NO ENVIAR
        |-- si -> ORQUESTADOR_REVISA
```

## Tipos de plano propios

- Doctor a camara: autoridad humana y hook.
- Mano dibujando: explicacion sin placa.
- RM/TC anonima recortada: evidencia segura.
- Consultorio limpio: contexto y confianza.
- Pasillo/ingreso CMP: respiracion institucional.
- Instrumental preparado: medicina concreta.
- Campo/tecnica autorizado: momento tecnico, corto y contextualizado.
- Monitor sin datos: solo si aporta informacion nueva.
- Doctor revisando estudio: criterio medico.
- Detalle de escritura: preparacion/orden.
- Equipo/CMP trabajando: solvencia.
- Placa CMP final: contacto y marca.

## Texto

- Maximo 4-6 palabras por beat.
- Maximo 25-45 palabras en todo el reel, excluyendo contacto.
- Una idea por pantalla.
- No usar frases epicas, motivacionales ni promesas clinicas.
- Si una frase necesita coma larga, va al copy o a la voz, no a placa.

## Hard stops

- Renderizar sin idea, manifest y storyboard.
- Rehacer una pieza rechazada con la misma estructura.
- Compensar falta de imagen con mas texto.
- Usar stock, IA o anatomia generica como evidencia clinica.
- Slideshow de fotos/RM con zoom repetido.
- Monitor de pared repetido como eje del reel.
- Cierre tipo flyer o contacto chico.
- Publicar sin audio decidido o con silencio no aprobado.
- Aprobar sin contact sheet/preview 540x960.
- Abrir bibliotecas privadas completas.

## Proxima accion por defecto

Antes de editar un reel educativo, pedir pack minimo por REELS:

1. video vertical del Doctor de 12-18s;
2. mano/esquema;
3. RM anonima si aplica;
4. 1-2 planos CMP limpios;
5. nota de voz opcional.
