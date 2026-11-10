import socket
import unittest
from unittest.mock import patch

from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from netpulse import check_tcp, resolve_host


class NetPulseTests(unittest.TestCase):
    @patch("netpulse.socket.getaddrinfo")
    def test_resolve_host_returns_unique_ipv4(self, mock_getaddrinfo):
        mock_getaddrinfo.return_value = [
            (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("192.0.2.10", 0)),
            (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("192.0.2.10", 0)),
            (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("192.0.2.11", 0)),
        ]
        self.assertEqual(
            resolve_host("example.test"), ["192.0.2.10", "192.0.2.11"]
        )

    @patch("netpulse.socket.create_connection")
    def test_tcp_check_success(self, mock_connect):
        mock_connect.return_value.__enter__.return_value = None
        self.assertTrue(check_tcp("example.test", 443))

    @patch("netpulse.socket.create_connection", side_effect=OSError("refused"))
    def test_tcp_check_failure(self, _mock_connect):
        self.assertFalse(check_tcp("example.test", 443))


if __name__ == "__main__":
    unittest.main()
