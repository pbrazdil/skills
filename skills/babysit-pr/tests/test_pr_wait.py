"""Check readiness against repository requirements without vendor dependencies."""
import runpy
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

Watcher = runpy.run_path(str(Path(__file__).parents[1] / 'scripts/pr-wait'))['Watcher']


class ReadinessTests(unittest.TestCase):
    def poll_result(self, *, required=(), checks=None, **fields):
        with tempfile.TemporaryDirectory() as directory:
            with patch.dict(Watcher.__init__.__globals__, STATE_DIR=Path(directory)):
                watcher = Watcher('owner/repo', 1, 'ready', 20)
            watcher.required = set(required)
            pr = dict(state='OPEN', url='https://github.com/owner/repo/pull/1',
                      baseRefName='main', headRefOid='abcdef123', viewer='owner',
                      author={'login': 'owner'}, comments={'nodes': []},
                      reviews={'nodes': []}, reviewThreads={'nodes': []},
                      mergeStateStatus='CLEAN', mergeable='MERGEABLE',
                      reviewDecision=None, isDraft=False)
            pr.update(fields)
            watcher.fetch_pr = lambda: pr
            watcher.fetch_checks = lambda: checks or {}
            with patch.object(watcher, 'say'):
                try:
                    watcher.poll()
                    watcher.poll()
                except SystemExit as result:
                    return result.code
            return None

    def test_ready_without_bots_or_checks(self):
        self.assertEqual(self.poll_result(), 0)

    def test_green_ci_without_review_bots(self):
        self.assertEqual(self.poll_result(required=['CI'], checks={
            'CI': {'bucket': 'pass', 'link': ''}}), 0)

    def test_missing_required_check_waits(self):
        self.assertIsNone(self.poll_result(required=['CI']))

    def test_failed_required_check_blocks(self):
        self.assertEqual(self.poll_result(required=['CI'], checks={
            'CI': {'bucket': 'fail', 'link': ''}}), 1)

    def test_repository_review_requirements_block(self):
        for decision in ('REVIEW_REQUIRED', 'CHANGES_REQUESTED'):
            with self.subTest(decision=decision):
                self.assertEqual(self.poll_result(reviewDecision=decision), 1)

    def test_unresolved_thread_blocks(self):
        self.assertEqual(self.poll_result(reviewThreads={'nodes': [{
            'isResolved': False, 'path': 'app.py', 'line': 1,
            'comments': {'nodes': [{'id': '1', 'url': 'https://example.com',
                                   'body': 'Fix this', 'author': {'login': 'owner'}}]}}]}), 1)

    def test_unknown_mergeability_waits(self):
        self.assertIsNone(self.poll_result(mergeable='UNKNOWN'))

    def test_unready_pr_blocks(self):
        for fields in ({'isDraft': True}, {'mergeStateStatus': 'BLOCKED'},
                       {'mergeStateStatus': 'BEHIND'}, {'mergeStateStatus': 'DIRTY'}):
            with self.subTest(fields=fields):
                self.assertEqual(self.poll_result(**fields), 1)


if __name__ == '__main__':
    unittest.main()
