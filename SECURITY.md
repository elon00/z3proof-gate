# Security and verification policy

This repository is a **development-stage SMT verification test component**, not a certified cryptographic product. It has no demonstrated NIST FIPS validation, authenticated RPC integration, or production-readiness evidence.

The solver is bounded to 16 KiB SMT-LIB2 input, a maximum 10-second solver timeout and a resource limit. Unknown results, parsing errors and mismatched expectations are treated as failures. The solver result does **not** establish that a model faithfully represents a real system.

Do not submit secrets, credentials, private keys or sensitive production artifacts. For a sensitive vulnerability, use GitHub's private vulnerability reporting mechanism if available rather than posting exploit details publicly. No bounty eligibility or compensation is promised.

Acceptance requires real CI on the exact PR head, adversarial negative tests, model validation and independent security review. Never treat a green CodeQL check alone as security approval.
