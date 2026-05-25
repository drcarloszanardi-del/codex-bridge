# deterministic gates pseudodiff

```diff
+ gates.noInventarTopografia(input, output)
+ gates.extraforaminalNoInterlaminar(input, parte)
+ gates.sinDescompresionDirecta(input, parte)
+ gates.artrodesisSinLateralidad(procedimiento, parte)
+ gates.hemostasiaRecuentoAntesCierre(parte)
+ gates.noDuplicarTecnica(parte, ["PLIF", "TLIF", "parche dural"])
```

## reglas

- Si el input no explicita topografia de hernia, output no puede inventarla.
- Hernia extraforaminal exige abordaje foraminal/extraforaminal/Wiltse y bloquea interlaminar/flavectomia como secuencia principal.
- Si el input dice "sin descompresion directa", bloquear laminectomia, flavectomia y liberacion radicular.
- Artrodesis/fijacion por nivel no lleva lateralidad; la lateralidad puede pertenecer al abordaje.
- Hemostasia y recuento deben preceder el cierre.
