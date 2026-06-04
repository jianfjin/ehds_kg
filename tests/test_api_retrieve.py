#!/usr/bin/env python3
"""Tests for ehds_api_server.py /api/retrieve endpoint.

Usage:
    cd ~/projects/ehds_kg
    python3 -m pytest tests/test_api_retrieve.py -v
"""

import json
import os
import sys
import time
import threading
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path

# ---------------------------------------------------------------------------
# Path setup: ensure src/ is on sys.path so the server can import its modules
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_DIR))

# Change to project root so relative data paths work
os.chdir(str(PROJECT_ROOT))

TEST_PORT = 8081
BASE_URL = f"http://localhost:{TEST_PORT}"
SERVER_START_WAIT = 10  # max seconds to wait for server readiness


class TestRetrieveAPI(unittest.TestCase):
    """Integration tests for /api/retrieve running on a dedicated test port."""

    server = None
    server_thread = None

    @classmethod
    def setUpClass(cls):
        """Start the HTTP server on TEST_PORT in a background thread."""
        import ehds_api_server  # noqa: F811 — now on sys.path

        cls.server = ThreadingHTTPServer(
            ("0.0.0.0", TEST_PORT),
            ehds_api_server.Handler,
        )
        cls.server_thread = threading.Thread(
            target=cls.server.serve_forever,
            daemon=True,
        )
        cls.server_thread.start()

        # Wait until /api/health responds or timeout
        deadline = time.monotonic() + SERVER_START_WAIT
        while time.monotonic() < deadline:
            try:
                req = urllib.request.urlopen(
                    f"{BASE_URL}/api/health", timeout=2
                )
                if req.status == 200:
                    return
            except Exception:
                time.sleep(0.3)
        raise RuntimeError(
            f"Server did not become ready on port {TEST_PORT} "
            f"within {SERVER_START_WAIT}s"
        )

    @classmethod
    def tearDownClass(cls):
        """Shut down the test server gracefully."""
        if cls.server is not None:
            cls.server.shutdown()
            cls.server.server_close()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _get(self, path: str) -> dict:
        """Send a GET request and return the parsed JSON body.

        Raises AssertionError on non-200 responses.
        """
        with urllib.request.urlopen(
            f"{BASE_URL}{path}", timeout=10
        ) as resp:
            self.assertEqual(
                resp.status,
                200,
                f"GET {path} returned HTTP {resp.status}",
            )
            body = resp.read().decode("utf-8")
            return json.loads(body)

    # ------------------------------------------------------------------
    # Test cases
    # ------------------------------------------------------------------

    def test_health(self):
        """/api/health returns {"status": "healthy"}"""
        data = self._get("/api/health")
        self.assertEqual(data["status"], "healthy")
        self.assertIn("layers", data)
        self.assertIsInstance(data["layers"], list)

    def test_retrieve_depth0_returns_results(self):
        """/api/retrieve ?q=health+data &depth=0 returns >=1 result"""
        data = self._get("/api/retrieve?q=health+data&depth=0")
        self.assertGreater(
            data["result_count"],
            0,
            "Expected at least 1 index result for 'health data'",
        )
        self.assertEqual(data["depth"], 0)
        self.assertEqual(data["query"], "health data")

    def test_retrieve_depth1_returns_results(self):
        """/api/retrieve ?q=electronic+health+data+space &depth=1 returns results

        NOTE: depth=1 activates TF-IDF semantic search on top of keyword
        index lookup.  If the TF-IDF cache is missing (e.g. first run),
        the semantic branch degrades gracefully — the test still gets
        results from the depth=0 keyword fallback.
        """
        data = self._get(
            "/api/retrieve?q=electronic+health+data+space&depth=1"
        )
        self.assertGreater(
            data["result_count"],
            0,
            "Expected at least 1 result for depth=1 search",
        )
        self.assertEqual(data["depth"], 1)

    def test_retrieve_depth0_result_fields(self):
        """Every result entry contains layer, document, section, text,
        source_path."""
        data = self._get("/api/retrieve?q=health+data&depth=0")
        self.assertGreater(data["result_count"], 0)
        for idx, r in enumerate(data["results"]):
            with self.subTest(result_index=idx):
                self.assertIn("layer", r, f"result[{idx}] missing 'layer'")
                self.assertIn(
                    "document", r, f"result[{idx}] missing 'document'"
                )
                self.assertIn(
                    "section", r, f"result[{idx}] missing 'section'"
                )
                self.assertIn("text", r, f"result[{idx}] missing 'text'")
                self.assertIn(
                    "source_path", r, f"result[{idx}] missing 'source_path'"
                )

    def test_retrieve_depth1_result_fields(self):
        """depth=1 results also contain the required fields (some may also
        include 'similarity' or 'article')."""
        data = self._get(
            "/api/retrieve?q=electronic+health+data+space&depth=1"
        )
        self.assertGreater(data["result_count"], 0)
        for idx, r in enumerate(data["results"]):
            with self.subTest(result_index=idx):
                self.assertIn("layer", r)
                self.assertIn("document", r)
                self.assertIn("section", r)
                self.assertIn("text", r)
                self.assertIn("source_path", r)

    def test_empty_query_returns_error(self):
        """Empty q= query returns HTTP 400 with an error object."""
        with self.assertRaises(urllib.error.HTTPError) as ctx:
            urllib.request.urlopen(
                f"{BASE_URL}/api/retrieve?q=&depth=0", timeout=10
            )
        self.assertEqual(ctx.exception.code, 400)
        err_body = ctx.exception.read().decode("utf-8")
        err_data = json.loads(err_body)
        self.assertIn("error", err_data)

    def test_no_query_returns_error(self):
        """Missing q= parameter returns HTTP 400 with an error object."""
        with self.assertRaises(urllib.error.HTTPError) as ctx:
            urllib.request.urlopen(
                f"{BASE_URL}/api/retrieve?depth=0", timeout=10
            )
        self.assertEqual(ctx.exception.code, 400)
        err_body = ctx.exception.read().decode("utf-8")
        err_data = json.loads(err_body)
        self.assertIn("error", err_data)


if __name__ == "__main__":
    unittest.main()
