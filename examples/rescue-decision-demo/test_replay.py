"""Replay conformance and tampering checks, using only temporary source copies."""

import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch


HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("demo_replay", HERE / "replay.py")
replay = importlib.util.module_from_spec(spec)
spec.loader.exec_module(replay)


class ReplayTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="synthetic-replay-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in replay.SOURCE_PATHS:
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(replay.ROOT / name, target)
        self.bundle = replay.generate(self.root)

    def write_bundle(self):
        (self.root / replay.DEMO / "replay-results.json").write_text(json.dumps(self.bundle))

    def test_three_fixture_decisions_and_reason_codes(self):
        expected = [
            ("WORTHWHILE_BENEFIT_RULED_OUT", ["BENEFIT_UPPER_BELOW_DELTA"], True),
            ("DO_NOT_ADVANCE", ["DEATH_BOUND_FAILED", "SELECTION_DETECTED"], True),
            ("TECHNICALLY_INDETERMINATE", ["EXPOSURE_MEASUREMENT_UNQUALIFIED"], False),
        ]
        self.assertEqual(len(self.bundle["cases"]), 3)
        for case, (decision, reasons, permitted) in zip(self.bundle["cases"], expected):
            with self.subTest(case=case["id"]):
                output = json.loads(case["stdout_text"])
                row = output["contrasts"][0]
                self.assertEqual(row["decision"], decision)
                self.assertEqual(row["reason_codes"], reasons)
                self.assertEqual(row["criteria"]["biological_interpretation_permitted_by_declared_controls"], permitted)
                self.assertEqual(output["replication_candidate_ids"], [])
                self.assertTrue(output["input_valid"])
                self.assertEqual(case["exit_code"], 0)

    def test_portable_and_deterministic_replay(self):
        self.assertEqual(replay.verify(self.root), self.bundle)
        self.assertEqual(replay.generate(self.root), self.bundle)
        for case in self.bundle["cases"]:
            self.assertFalse(Path(case["input_path"]).is_absolute())
            self.assertNotIn(str(replay.ROOT), json.dumps(case))

    def test_changed_input_fails_before_execution(self):
        p = self.root / self.bundle["cases"][0]["input_path"]
        p.write_bytes(p.read_bytes() + b"\n")
        with patch.object(replay.subprocess, "run", side_effect=AssertionError("must not execute")):
            with self.assertRaisesRegex(replay.ReplayError, "Source SHA256 mismatch"):
                replay.verify(self.root)

    def test_changed_implementation_fails_before_execution(self):
        p = self.root / replay.IMPLEMENTATION
        p.write_bytes(p.read_bytes() + b"\n# test mutation\n")
        with patch.object(replay.subprocess, "run", side_effect=AssertionError("must not execute")):
            with self.assertRaisesRegex(replay.ReplayError, "Source SHA256 mismatch"):
                replay.verify(self.root)

    def test_altered_output_with_recomputed_hash_still_fails(self):
        case = self.bundle["cases"][0]
        output = json.loads(case["stdout_text"])
        output["contrasts"][0]["decision"] = "REPLICATION_CANDIDATE"
        case["stdout_text"] = json.dumps(output) + "\n"
        case["stdout_sha256"] = hashlib.sha256(case["stdout_text"].encode()).hexdigest()
        self.write_bundle()
        with self.assertRaisesRegex(replay.ReplayError, "actual decision.py rerun"):
            replay.verify(self.root)

    def test_embedded_input_tampering_fails(self):
        self.bundle["cases"][0]["input_text"] += "\n"
        self.write_bundle()
        with self.assertRaisesRegex(replay.ReplayError, "embedded input SHA256 mismatch"):
            replay.verify(self.root)

    def test_html_tampering_fails(self):
        p = self.root / replay.DEMO / "replay.html"
        p.write_bytes(p.read_bytes().replace(b"Actual recorded Python output", b"Altered display"))
        with self.assertRaisesRegex(replay.ReplayError, "HTML mismatch"):
            replay.verify(self.root)

    def test_changed_sources_during_execution_fail_closed(self):
        run = replay.subprocess.run
        def mutate_after_run(*args, **kwargs):
            result = run(*args, **kwargs)
            p = self.root / replay.IMPLEMENTATION
            p.write_bytes(p.read_bytes() + b"\n# concurrent test mutation\n")
            return result
        with patch.object(replay.subprocess, "run", side_effect=mutate_after_run):
            with self.assertRaisesRegex(replay.ReplayError, "Source changed during execution"):
                replay.collect(self.root)


if __name__ == "__main__":
    unittest.main()
