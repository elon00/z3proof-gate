"""Real Z3 solver regression tests. No mock solver or network RPC."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tools.z3_gate import GateError, MAX_INPUT_BYTES, check_smt2


SAT = "(declare-const x Int)\n(assert (> x 0))"
UNSAT = SAT + "\n(assert (< x 0))"


class Z3GateTests(unittest.TestCase):
    def test_sat(self):
        self.assertEqual(check_smt2(SAT), "sat")

    def test_unsat(self):
        self.assertEqual(check_smt2(UNSAT), "unsat")

    def test_bounded_boolean_unsat(self):
        self.assertEqual(check_smt2("(declare-const p Bool)\n(assert p)\n(assert (not p))"), "unsat")

    def test_malformed_rejected(self):
        with self.assertRaises(GateError):
            check_smt2("(assert (= 1")

    def test_empty_rejected(self):
        with self.assertRaises(GateError):
            check_smt2(" ")

    def test_declarations_only_rejected(self):
        with self.assertRaises(GateError):
            check_smt2("(declare-const x Int)")

    def test_oversized_rejected(self):
        with self.assertRaises(GateError):
            check_smt2("(assert true)\n" + (" " * MAX_INPUT_BYTES))

    def test_invalid_timeout_rejected(self):
        for value in (0, -1, 10001):
            with self.subTest(value=value), self.assertRaises(GateError):
                check_smt2(SAT, timeout_ms=value)

    def test_nul_rejected(self):
        with self.assertRaises(GateError):
            check_smt2("(assert true)\x00")

    def _cli(self, text, expected):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "case.smt2"
            path.write_text(text, encoding="utf-8")
            return subprocess.run(
                [sys.executable, "-m", "tools.z3_gate", "--file", str(path), "--expect", expected],
                capture_output=True, text=True, check=False, timeout=15,
            )

    def test_cli_expected_unsat_passes(self):
        result = self._cli(UNSAT, "unsat")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('"outcome": "unsat"', result.stdout)

    def test_cli_sat_cannot_pass_unsat_gate(self):
        result = self._cli(SAT, "unsat")
        self.assertNotEqual(result.returncode, 0)

    def test_cli_malformed_fails_closed(self):
        result = self._cli("(assert (= 1", "unsat")
        self.assertNotEqual(result.returncode, 0)

    def test_real_solver_self_check(self):
        result = subprocess.run(
            [sys.executable, "-m", "tools.z3_gate", "--self-check"],
            capture_output=True, text=True, check=False, timeout=15,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('"self_check": "pass"', result.stdout)


if __name__ == "__main__":
    unittest.main()
