"""Offline regression tests for the bounded REA Hackingtool app."""
import contextlib
import io
import json
import unittest
from unittest.mock import patch

import rea_safe_app


class SafeAppTests(unittest.TestCase):
    def test_localhost_success(self):
        with patch.object(rea_safe_app.socket, "gethostbyname", return_value="127.0.0.1") as resolver:
            self.assertEqual(rea_safe_app.resolve_localhost("localhost")["address"], "127.0.0.1")
            resolver.assert_called_once_with("localhost")

    def test_disallowed_host_never_reaches_network(self):
        with patch.object(rea_safe_app.socket, "gethostbyname") as resolver:
            with self.assertRaises(ValueError):
                rea_safe_app.resolve_localhost("example.com")
            resolver.assert_not_called()

    def test_non_loopback_dns_result_fails_closed(self):
        with patch.object(rea_safe_app.socket, "gethostbyname", return_value="8.8.8.8"):
            with self.assertRaises(RuntimeError):
                rea_safe_app.resolve_localhost("localhost")

    def test_list_outputs_stable_json(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(rea_safe_app.main(["list"]), 0)
        self.assertEqual(json.loads(output.getvalue())["safe_tools"][0]["name"], "Host2IP")

    def test_cli_rejects_external_target(self):
        with patch.object(rea_safe_app.socket, "gethostbyname") as resolver:
            with contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as exit_result:
                    rea_safe_app.main(["host-to-ip", "example.com"])
            self.assertEqual(exit_result.exception.code, 2)
            resolver.assert_not_called()

    def test_cli_localhost_end_to_end(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(rea_safe_app.main(["host-to-ip", "localhost"]), 0)
        result = json.loads(output.getvalue())
        self.assertEqual(result["hostname"], "localhost")
        self.assertTrue(result["address"].startswith("127."))


if __name__ == "__main__":
    unittest.main()
