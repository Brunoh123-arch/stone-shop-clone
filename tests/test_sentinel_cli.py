import unittest
from unittest.mock import patch, MagicMock
import os
import json
import urllib.error

# Adiciona scripts ao path
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))

import catbox_sentinel

class TestSentinelCli(unittest.TestCase):
    def test_probe_url_healthy_206(self):
        mock_resp = MagicMock()
        mock_resp.status = 206
        mock_resp.headers = {'Content-Range': 'bytes 0-10/5000000'}

        with patch('urllib.request.urlopen', return_value=mock_resp):
            item = {
                "namespace": "teste",
                "product_id": "1",
                "video_id": "vid1",
                "original_path": "vid1.mp4",
                "catbox_url": "https://files.catbox.moe/abc123.mp4",
                "poster_path": "poster.jpg"
            }
            res = catbox_sentinel.probe_single_video(item, timeout=5)
            self.assertEqual(res['status_code'], 206)
            self.assertEqual(res['state'], 'HEALTHY')
            self.assertEqual(res['total_bytes'], 5000000)
            self.assertGreaterEqual(res['latency_ms'], 0)

    def test_probe_url_404_dead(self):
        err = urllib.error.HTTPError("https://files.catbox.moe/dead.mp4", 404, "Not Found", {}, None)
        with patch('urllib.request.urlopen', side_effect=err):
            item = {
                "namespace": "teste",
                "product_id": "1",
                "video_id": "dead",
                "original_path": "dead.mp4",
                "catbox_url": "https://files.catbox.moe/dead.mp4",
                "poster_path": "poster.jpg"
            }
            res = catbox_sentinel.probe_single_video(item, timeout=5)
            self.assertEqual(res['status_code'], 404)
            self.assertEqual(res['state'], 'DEAD')

    def test_report_schema_compliance_if_exists(self):
        report_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'sentinel_health_report.json')
        if os.path.exists(report_path):
            with open(report_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.assertIn('summary', data)
            self.assertIn('results', data)
            self.assertIn('total_checked', data['summary'])
            self.assertIn('healthy_count', data['summary'])
            self.assertIn('success_rate_percent', data['summary'])
            self.assertIn('avg_latency_ms', data['summary'])

            for r in data['results']:
                self.assertIn('catbox_url', r)
                self.assertIn('status_code', r)
                self.assertIn('state', r)
                self.assertIn('latency_ms', r)

if __name__ == '__main__':
    unittest.main()
