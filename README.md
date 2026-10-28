# Z3proof Gate — bounded offline SMT verification

Canonical ID: **QMOOSA-0765** (tests component). This repository contains a small, genuine Z3-based SAT/UNSAT verification gate; it is **not** a complete formal-verification platform or production-certified security system.

## Reproduce

Requires Python 3.11 and the actual Z3 solver binding (no mock solver):

```bash
python -m pip install --no-deps z3-solver==4.13.4.0
python -m tools.z3_gate --self-check
python -m unittest discover -s tests -p 'test_*.py' -v
```

To verify a safety property, encode its **negation** as SMT-LIB2 and require UNSAT:

```bash
python -m tools.z3_gate --file property-negation.smt2 --expect unsat
```

SAT, malformed input, solver UNKNOWN, timeouts, resource failures, missing Z3, and unexpected results must not be reported as a verified proof. The gate bounds input to 16 KiB and solver timeout to 10 seconds maximum. A passing UNSAT result only establishes unsatisfiability of the exact submitted constraints under Z3 semantics; it does not establish the completeness or correctness of the model.

## Scope and evidence

- Real Python Z3 solver integration and adversarial regressions are proposed in a draft PR, pending exact-HEAD GitHub Actions evidence and review.
- No PQC implementation, FIPS 203/204/205 validation, authenticated RPC, deployment, wallet, escrow, or tokenomics is verified here.
- SECURITY_APPROVED, DEPLOYMENT_READY, and production certification: **NOT VERIFIED**.
- This code is for local, offline analysis; do not use it to authorize transactions or bypass security controls.

See `ARCHITECTURE.md` and GitHub Actions for the actual verification boundary.
