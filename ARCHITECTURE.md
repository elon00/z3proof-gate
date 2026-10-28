# Z3proof Gate — verified scope and architecture

**Canonical ID:** QMOOSA-0765  
**Role:** Tests / SMT verification gate  
**Readiness:** Development only; security approval and deployment readiness not established.

## Implemented boundary

`tools/z3_gate.py` parses bounded SMT-LIB2 assertions using the actual pinned `z3-solver` Python package. It checks SAT or UNSAT with finite timeout and resource bounds, fails closed for UNKNOWN/parse errors, and exposes an explicit expected-result CLI. `tests/test_z3_gate.py` exercises satisfiable, contradictory, malformed, oversized and unexpected-result inputs using a real solver.

## Not implemented or independently verified

- A sound and complete formal model for any specific blockchain or cryptographic protocol.
- Production-grade cryptography, FIPS conformance, PQC, QuickNode RPC, x402, Conway automata, agentics, or settlement.
- Cross-process AES-GCM nonce safety in the separate Batch 14 TLS engine.
- Any production certification, deployment readiness, or 100/100 portfolio score.

The legacy Rust executable is deliberately fail-closed and does not claim verification. Only the Python Z3 gate is in scope. No remote service, secrets, gas, or cycles are used. Security approval requires a separate model review and independent assessment.
