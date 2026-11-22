"""Bounded, fail-closed SMT-LIB2 verification using the real Z3 solver.

This component verifies only the submitted constraints. It does not certify
cryptography, protocol security, deployment readiness, or production systems.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from z3 import Context, Solver, Z3Exception, get_version_string, parse_smt2_string, sat, unsat

MAX_INPUT_BYTES = 16_384
MAX_TIMEOUT_MS = 10_000


class GateError(Exception):
    """An input, solver, or resource failure; never a successful proof."""


def check_smt2(text: str, timeout_ms: int = 2_000) -> str:
    if not isinstance(text, str):
        raise GateError("input must be UTF-8 text")
    if not 1 <= timeout_ms <= MAX_TIMEOUT_MS:
        raise GateError("timeout must be between 1 and 10000 milliseconds")
    if not text.strip() or len(text.encode("utf-8")) > MAX_INPUT_BYTES:
        raise GateError("empty or oversized SMT-LIB2 input")
    if "\x00" in text:
        raise GateError("NUL byte is not permitted")
    try:
        # A fresh context prevents malformed input from contaminating later parses.
        ctx = Context()
        constraints = parse_smt2_string(text, ctx=ctx)
        if len(constraints) == 0:
            raise GateError("at least one assertion is required")
        solver = Solver(ctx=ctx)
        solver.set(timeout=timeout_ms)
        solver.set(rlimit=500_000)
        solver.add(*constraints)
        result = solver.check()
    except Z3Exception as exc:
        raise GateError("Z3 rejected SMT-LIB2 input or failed") from exc
    if result == sat:
        return "sat"
    if result == unsat:
        return "unsat"
    raise GateError("Z3 returned unknown or exceeded resource limits: " + solver.reason_unknown())


def main() -> int:
    parser = argparse.ArgumentParser(description="Offline, bounded Z3 SMT-LIB2 check")
    parser.add_argument("--file", type=Path, help="SMT-LIB2 file")
    parser.add_argument("--expect", choices=("sat", "unsat"), help="Required outcome")
    parser.add_argument("--self-check", action="store_true", help="Check real SAT and UNSAT cases")
    args = parser.parse_args()
    try:
        if args.self_check:
            sat_case = "(declare-const x Int)\n(assert (> x 0))"
            unsat_case = "(declare-const x Int)\n(assert (> x 0))\n(assert (< x 0))"
            if check_smt2(sat_case) != "sat" or check_smt2(unsat_case) != "unsat":
                raise GateError("solver self-check failed")
            print(json.dumps({"self_check": "pass", "z3_version": get_version_string()}))
            return 0
        if args.file is None or args.expect is None:
            raise GateError("--file and --expect are required unless --self-check is used")
        with args.file.open("rb") as source:
            raw = source.read(MAX_INPUT_BYTES + 1)
        if len(raw) > MAX_INPUT_BYTES:
            raise GateError("oversized SMT-LIB2 file")
        outcome = check_smt2(raw.decode("utf-8", errors="strict"))
        print(json.dumps({"outcome": outcome, "expected": args.expect, "z3_version": get_version_string()}))
        if outcome != args.expect:
            raise GateError("solver result does not match required outcome")
        return 0
    except (GateError, OSError, UnicodeError) as exc:
        print("Z3 gate FAILED: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
