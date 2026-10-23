import importlib.util
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('canary', ROOT/'canary/run_canary.py')
c = importlib.util.module_from_spec(spec); spec.loader.exec_module(c)

class CanaryTests(unittest.TestCase):
    def setUp(self):
        self.rows=c.load_panel(); self.good=c.fixture(self.rows)
    def test_control_and_failure_injection(self):
        self.assertEqual(c.self_test(self.rows),0)
    def test_loss_channel_cannot_be_replaced_by_gain(self):
        bad=self.good.replace('0.0 0.9 0.0 0.0','0.9 0.0 0.0 0.0')
        self.assertTrue(c.evaluate(bad,self.rows))
    def test_negative_control_catches_everything_positive(self):
        bad=self.good.splitlines(); bad[-1]=bad[-1].replace('0.0 0.0 0.0 0.0 0.0','0.9 0.0 0.0 0.0 0.9')
        self.assertTrue(c.evaluate('\n'.join(bad),self.rows))
    def test_missing_reference_is_not_success(self):
        r=subprocess.run([sys.executable,str(ROOT/'canary/run_canary.py'),'--reference','/nonexistent/mva-test-reference'],capture_output=True,text=True)
        self.assertEqual(r.returncode,2); self.assertIn('NOT RUN',r.stderr)
    def test_mismatched_maximum_rejected(self):
        bad=self.good.replace('0.9 fixture','0.1 fixture')
        self.assertTrue(c.evaluate(bad,self.rows))

if __name__=='__main__': unittest.main()
