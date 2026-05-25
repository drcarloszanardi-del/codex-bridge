# route guard pseudodiff

## objetivo

Impedir que generadores no canonicos produzcan documentos enviables.

```diff
+ const CANONICAL_CLINICA_ROUTE = {
+   app: "app/product.html",
+   wrapper: "scripts/jarvis/clinical_document_handoff.js",
+   required_gates: ["redaction_shield", "clinical_send_gate", "route_manifest"]
+ };
+
+ function assertCanonicalRoute(route) {
+   if (route.app !== CANONICAL_CLINICA_ROUTE.app) throw new Error("non_canonical_route");
+   if (!route.gates.includes("redaction_shield")) throw new Error("missing_redaction_shield");
+   if (!route.gates.includes("clinical_send_gate")) throw new Error("missing_send_gate");
+ }
+
+ // app/app.js debe quedar demo-only o pasar por assertCanonicalRoute antes de exportar/enviar.
```

## tests

- `validate_clinica_route_guard.js` debe fallar si `app/app.js` exporta sin route manifest.
- Todo PDF/documento debe registrar `route_id`, `gate_version`, `manifest_hash`.
