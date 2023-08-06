import json
from unittest import TestCase
try:
    from unittest import mock
except ImportError:
    from mock import mock

from ethermine_monitor.app import worker_monitor


WORKING = json.loads("""
{"status":"OK","data":[{"worker":"nc1","time":1513804800,"lastSeen":1513804673,"reportedHashrate":148926506,"currentHashrate":85166666.66666667,"validShares":76,"invalidShares":0,"staleShares":1,"averageHashrate":142177469.1358024}]}
""")
BROKEN = json.loads("""
{"status":"OK","data":[{"worker":"nc1","time":1513804200,"lastSeen":1513802783,"reportedHashrate":0,"currentHashrate":100722222.22222222,"validShares":90,"invalidShares":0,"staleShares":1,"averageHashrate":142973765.4320987}]}
""")


class TestResults(TestCase):
    def test_response_simple(self):
        with mock.patch('ethermine_monitor.app.request_worker_data', side_effect=lambda: WORKING['data']):
            for result in worker_monitor():
                self.assertTrue(result)
        with mock.patch('ethermine_monitor.app.request_worker_data', side_effect=lambda: BROKEN['data']):
            for result in worker_monitor():
                self.assertFalse(result)
