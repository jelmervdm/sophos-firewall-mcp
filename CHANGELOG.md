# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-07-27

### Added
- **Initial release** of `sophos-firewall-mcp-server`.
- **Async API Client (`client.py`)**: Built on `httpx.AsyncClient` with XML API request generation and `xmltodict` parsing for Sophos SFOS endpoints (`/webconsole/APIController`).
- **7 Modular Tool Domains (28 Tools)**:
  - System diagnostics, service state, network interfaces (`system.py`).
  - Firewall security policies CRUD and status toggling (`firewall_rules.py`).
  - IP host definitions, network subnets, host groups, FQDN objects (`hosts_objects.py`).
  - TCP/UDP service definitions and service groups (`services_objects.py`).
  - SNAT and DNAT port-forwarding inspection (`nat_rules.py`).
  - User accounts and live session monitoring (`users_auth.py`).
  - IPsec site-to-site tunnels and SSL VPN remote access policies (`vpn.py`).
- **FastMCP Resources & Prompts**: Read-only URIs (`sophos://system/info`, `sophos://interfaces`) and diagnostic prompts (`audit_firewall_rules`, `troubleshoot_connectivity`).
- **Semantic Tool Routing (`router.py`)**: FastEmbed embedding-based tool discovery (`USE_ROUTER=true`).
- **Tier A+ Quality Score**: 100% parameter descriptions, full `ToolAnnotations` safety metadata, and 100% test pass rate audited against the [glama-ai TDQS framework](https://github.com/glama-ai/tool-definition-quality-score).
- **Automated CI/CD & Security Pipelines**: GitHub Actions workflows for testing, linting, SAST security (pip-audit, Semgrep), Dependabot auto-merging, and container publishing to GHCR.
