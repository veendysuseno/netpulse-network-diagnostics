#!/usr/bin/env python3
"""NetPulse: small network diagnostics CLI."""

import argparse
import platform
import socket
import subprocess
import sys


def resolve_host(host: str) -> list[str]:
    """Return unique IPv4 addresses for a hostname."""
    results = socket.getaddrinfo(host, None, socket.AF_INET, socket.SOCK_STREAM)
    return sorted({item[4][0] for item in results})


def check_tcp(host: str, port: int, timeout: float = 3.0) -> bool:
    """Return True if a TCP connection can be established."""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except (OSError, TimeoutError):
        return False


def ping_host(host: str, timeout: int = 4) -> int:
    """Run one ping; return the operating system process exit code."""
    flag = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", flag, "1", host]
    try:
        completed = subprocess.run(
            command, capture_output=True, text=True, timeout=timeout, check=False
        )
        output = completed.stdout.strip() or completed.stderr.strip()
        if output:
            print(output)
        return completed.returncode
    except FileNotFoundError:
        print("[-] ping utility was not found on this system.")
        return 127
    except subprocess.TimeoutExpired:
        print("[-] Ping timed out.")
        return 124


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="netpulse",
        description="Basic DNS, TCP, and ping diagnostics."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    dns_parser = subparsers.add_parser("dns", help="Resolve a hostname")
    dns_parser.add_argument("host")

    tcp_parser = subparsers.add_parser("tcp", help="Test a TCP port")
    tcp_parser.add_argument("host")
    tcp_parser.add_argument("port", type=int)
    tcp_parser.add_argument("--timeout", type=float, default=3.0)

    ping_parser = subparsers.add_parser("ping", help="Ping a host once")
    ping_parser.add_argument("host")
    ping_parser.add_argument("--timeout", type=int, default=4)

    return parser


def main() -> int:
    args = build_parser().parse_args()

    if args.command == "dns":
        print(f"[+] DNS lookup: {args.host}")
        try:
            addresses = resolve_host(args.host)
            for address in addresses:
                print(f"[+] IPv4: {address}")
            return 0
        except socket.gaierror as exc:
            print(f"[-] DNS lookup failed: {exc}")
            return 1

    if args.command == "tcp":
        if not 1 <= args.port <= 65535:
            print("[-] Port must be between 1 and 65535.")
            return 2
        print(f"[*] Checking {args.host}:{args.port} ...")
        if check_tcp(args.host, args.port, args.timeout):
            print(f"[+] TCP port {args.port} is reachable.")
            return 0
        print(f"[-] TCP port {args.port} is not reachable.")
        return 1

    if args.command == "ping":
        print(f"[*] Pinging {args.host} ...")
        return ping_host(args.host, args.timeout)

    return 2


if __name__ == "__main__":
    sys.exit(main())
