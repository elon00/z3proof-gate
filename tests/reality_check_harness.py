"""Legacy entry point: run a genuine, narrowly scoped Z3 solver self-check.

No RPC, PQC, escrow, FIPS, or production status is asserted here.
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.z3_gate import check_smt2  # noqa: E402


def main():
    sat_case = "(declare-const x Int)\n(assert (> x 0))"
    unsat_case = sat_case + "\n(assert (< x 0))"
    assert check_smt2(sat_case) == "sat"
    assert check_smt2(unsat_case) == "unsat"
    print("Real Z3 SAT/UNSAT self-check PASS; other security claims NOT VERIFIED")


if __name__ == "__main__":
    main()
