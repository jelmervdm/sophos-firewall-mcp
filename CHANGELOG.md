# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-07-27

### Added
- Initial release of `sophos-firewall-mcp-server`.
- Asynchronous `SophosFirewallClient` with XML API payload generation, XML parsing, and SSL verification options.
- 7 modular tool domains:
  - System info, service status, network interfaces (`system.py`).
  - Firewall rules and security policies (`firewall_rules.py`).
  - IP hosts, host groups, FQDNs (`hosts_objects.py`).
  - Service objects and service groups (`services_objects.py`).
  - NAT and port forwarding rules (`nat_rules.py`).
  - Local users and live session monitoring (`users_auth.py`).
  - IPsec site-to-site & SSL VPN status (`vpn.py`).
- FastMCP Resources (`sophos://system/info`, `sophos://interfaces`) and diagnostic Prompts (`audit_firewall_rules`, `troubleshoot_connectivity`).
- Optional semantic tool router (`router.py`) using FastEmbed.
- Comprehensive unit test suite with mock XML responses.
- Containerization support with Docker, Docker Compose, and entrypoint script.
