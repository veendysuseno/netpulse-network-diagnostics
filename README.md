# NetPulse — Lightweight Network Diagnostics

A beginner-friendly Python CLI for basic network troubleshooting. NetPulse checks DNS resolution, tests TCP connectivity, and reports basic host reachability.

> Built as a small portfolio project for learning Python, networking, and Git/GitHub workflows.

## Project Goals

- **Learning & Skill Building**: Practice core Python programming concepts, standard library usage, and clean code principles.
- **Networking Foundations**: Understand basic networking protocols (DNS, TCP, ICMP ping) through hands-on CLI implementation.
- **Developer Workflow**: Apply Git/GitHub best practices, modular project structure, and unit testing.
- **Lightweight Tooling**: Provide a simple, zero-dependency network diagnostic utility for daily command-line use.

## Features

- Resolve a hostname to IPv4 addresses
- Test TCP connectivity to a host and port
- Run a basic ping check using the operating system's ping utility
- Clear, readable terminal output
- Unit tests for core helper functions

## Requirements

- Python 3.10+
- No third-party Python packages required
- `ping` utility available on your operating system (only needed for the ping command)

## Run

```bash
python src/netpulse.py dns example.com
python src/netpulse.py tcp example.com 443
python src/netpulse.py ping 1.1.1.1
```

## Example output

```text
$ python src/netpulse.py dns example.com
[+] DNS lookup: example.com
[+] IPv4: 93.184.216.34
```

Actual IP addresses and results depend on your network and DNS provider.

## Run tests

```bash
python -m unittest discover -s tests -v
```

## Project structure

```text
netpulse/
├── README.md
├── LICENSE
├── .gitignore
├── src/
│   └── netpulse.py
└── tests/
    └── test_netpulse.py
```

## Safety

Only test systems and networks you own or have explicit permission to assess. NetPulse performs basic DNS, ping, and TCP connection checks; it is not a vulnerability scanner.

## Roadmap

- [ ] Add latency measurement summary
- [ ] Export diagnostic results to JSON
- [ ] Add configurable connection timeout
- [ ] Add support for checking multiple hosts from a file

## License

MIT
