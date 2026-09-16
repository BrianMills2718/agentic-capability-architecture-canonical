# DIGIMON governed evidence provider

This capability is an ACA discovery/binding descriptor for the provider-owned DIGIMON governed-evidence search action. It does **not** copy DIGIMON execution or domain semantics into ACA.

The machine-readable `provider_operability` block pins one exact DIGIMON revision and names the HTTP action selector, request/result contracts, bearer-auth boundary, health/trace/failure evidence, idempotency surface, and provider-owned recovery references.

ACA may use this metadata to understand and select the provider. DIGIMON remains responsible for executing the call, enforcing authorization, retaining traces/results, retry/idempotency behavior, and recovery guidance.
