"""Offline contract checks. No external API or brokerage calls."""
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
import json
import tempfile
import unittest
from unittest.mock import patch

import arena_review as ar


class V09CouncilTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.directory = Path(temp.name)

    def test_twelve_teams_and_review_graph(self):
        teams, incoming = ar.council()
        self.assertEqual(len(teams), 12)
        self.assertEqual(sum(len(t["reviewTargets"]) for t in teams), 24)
        self.assertTrue(all(len(v) == 2 for v in incoming.values()))
        self.assertTrue(all(r != t for t, reviewers in incoming.items() for r in reviewers))

    def test_proposals_do_not_receive_other_teams_drafts(self):
        teams, incoming = ar.council()
        foreign_marker = "FOREIGN_SECRET_MARKER_NOT_FOR_T01"
        ar.write_atomic(ar.path_for(self.directory, "propose", "T02"), foreign_marker)
        system, user = ar.build_prompt("propose", "T01", "", self.directory, teams, incoming)
        self.assertNotIn(foreign_marker, system + user)
        self.assertIn("T01", user)
        self.assertIn("Critical", user)

    def test_paid_calls_are_blocked_without_opt_in(self):
        sink = StringIO()
        with redirect_stdout(sink), self.assertRaises(SystemExit) as caught:
            ar.main(["propose", "--run-dir", str(self.directory), "--model", "test-model"])
        self.assertEqual(caught.exception.code, 2)
        self.assertFalse((self.directory / "propose").exists())

    def test_dry_run_does_not_require_api_token(self):
        with redirect_stdout(StringIO()):
            self.assertEqual(ar.main(["propose", "--run-dir", str(self.directory),
                                      "--max-calls", "3", "--dry-run"]), 0)
        self.assertFalse((self.directory / "propose").exists())

    def test_missing_prerequisite_prevents_review(self):
        teams, _ = ar.council()
        with self.assertRaisesRegex(ValueError, "Complete all propose"):
            ar.stage_ready("review", self.directory, teams)

    def fake_artifact(self, phase, team, target=""):
        p = ar.path_for(self.directory, phase, team, target)
        content = "# Independent documented review\n" + ("Evidence and limitations. " * 15)
        ar.write_atomic(p, content)
        ar.write_atomic(p.with_suffix(".meta.json"), json.dumps({
            "phase": phase, "team": team, "target": target or None,
            "api_response_id": "resp_sample_abc", "output_sha256": ar.sha(content),
        }))

    def test_49_artifact_complete_and_tamper_detection(self):
        teams, _ = ar.council()
        jobs = ar.all_jobs(teams)
        for phase in ar.PHASES:
            for team, target in jobs[phase]:
                self.fake_artifact(phase, team, target)
        report = ar.audit(self.directory, teams)
        self.assertTrue(report["design_ready"])
        self.assertEqual(sum(report[p]["completed"] for p in ar.PHASES), 49)
        victim = ar.path_for(self.directory, "review", "T01", "T02")
        victim.write_text(victim.read_text() + "MUTATED", encoding="utf-8")
        tampered = ar.audit(self.directory, teams)
        self.assertFalse(tampered["design_ready"])
        self.assertEqual(tampered["review"]["completed"], 23)

    def test_two_unique_reviewers_for_each_team(self):
        _, incoming = ar.council()
        self.assertEqual(incoming["T01"], ["T08", "T12"])
        self.assertEqual(incoming["T05"], ["T04", "T12"])

    def test_actual_invocations_are_separate_and_resumable(self):
        with redirect_stdout(StringIO()), patch.dict("os.environ", {"OPENAI_API_KEY": "test-not-real-key"}), \
             patch.object(ar, "api_call", return_value=(
                 {"id": "resp_offline_test", "status": "completed", "usage": {"total_tokens": 1}},
                 "Offline independent proposal with explicit assumptions. " * 10
             )) as request:
            ar.main(["propose", "--run-dir", str(self.directory), "--model", "test-only",
                     "--max-calls", "2", "--confirm-api-spend"])
            self.assertEqual(request.call_count, 2)
            ar.main(["propose", "--run-dir", str(self.directory), "--model", "test-only",
                     "--max-calls", "2", "--confirm-api-spend"])
            self.assertEqual(request.call_count, 4)
        self.assertEqual(ar.audit(self.directory, ar.council()[0])["propose"]["completed"], 4)


if __name__ == "__main__":
    unittest.main()
