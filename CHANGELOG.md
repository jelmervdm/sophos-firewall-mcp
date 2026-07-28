# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-07-27

### Changed
- **Secure Default SSL Verification (`client.py`)**: Updated `SophosFirewallClient` to default `verify_ssl` to `True` (`SOPHOS_VERIFY_SSL` defaults to `"true"`). Ensures TLS certificate validation by default, allowing explicit override (`SOPHOS_VERIFY_SSL=false`) for lab/testing environments.
- **Destructive Tool Safety Metadata (`server.py`)**: Set `destructiveHint=True` on `sophos_raw_api_request` tool annotation to ensure MCP client UIs request explicit user confirmation before running raw XML mutations.

### Fixed
- **Module Import Event Loop Safety (`server.py`)**: Refactored semantic tool router initialization to lazy async loading (`get_initialized_router()`). Resolves `RuntimeError: asyncio.run() cannot be called from a running event loop` when importing the server module within an existing event loop.
- **Code Cleanliness (`client.py`)**: Removed unreachable duplicate `return` statement in `send_request()`.

## [0.1.5] - 2026-07-27

### Added
- **Generic Low-Level API Tool (`raw_api.py`, `server.py`)**: Added `sophos_raw_api_request` to allow LLMs to execute low-level `Get`, `Set`, or `Remove` SFOS XML operations for any tag (e.g. `Interface`, `DNS`, `DHCP`, `WebFilterPolicy`, `Route`, `Zone`) with arbitrary parameters.
- **NAT Rule Management (`nat_rules.py`)**: Added `sophos_create_nat_rule`, `sophos_update_nat_rule`, and `sophos_delete_nat_rule` tools.
- **Service Object CRUD (`services_objects.py`)**: Added `sophos_delete_service`, `sophos_create_service_group`, and `sophos_delete_service_group` tools.
- **Host Object Deletions (`hosts_objects.py`)**: Added `sophos_delete_ip_host_group` and `sophos_delete_fqdn_host` tools.
- **User Account Deletion (`users_auth.py`)**: Added `sophos_delete_user` tool.

## [0.1.4] - 2026-07-27

### Fixed
- **Tool Router Event Loop (`server.py`)**: Converted `route_tools` to `async def` and replaced `asyncio.run(mcp.list_tools())` with `await mcp.list_tools()`. Fixes `asyncio.run() cannot be called from a running event loop` when tool routing is enabled.
- **Firewall Rule XML Schema (`firewall_rules.py`)**: Included mandatory `PolicyType` (`"Network"`) and `IPFamily` (`"IPv4"`) in top-level `sophos_create_firewall_rule` payload dictionary. Fixes Sophos SFOS API Error `Status 501: Configuration parameters validation failed. InvalidParams: /FirewallRule/PolicyType`.

### Added
- **General Firewall Rule Modification Tool (`firewall_rules.py`, `server.py`)**: Added `sophos_update_firewall_rule` tool to fetch existing rule configuration, update specified properties (e.g. `action`, `log_traffic`, `source_zones`, `destination_zones`, `source_networks`, `destination_networks`, `services`, `status`), clean transaction IDs, and apply updates to Sophos SFOS via `set_tag`.

## [0.1.3] - 2026-07-27

### Fixed
- **Pre-download FastEmbed Model (`Dockerfile`)**: Pre-downloads embedding model weights (`BAAI/bge-small-en-v1.5`) directly into the container image during Docker build step. Eliminates runtime startup downloads over HuggingFace Hub, preventing client connection timeouts (`context canceled`).
- **Log Noise & Startup Resilience (`router.py`)**: Suppressed verbose `httpx`, `httpcore`, and `huggingface_hub` HTTP request log spam during model load. Updated `get_router()` error handling to catch all initialization exceptions and fall back gracefully to standard tool mode.

## [0.1.2] - 2026-07-27

### Fixed
- **Configurable API Version (`client.py`)**: Updated `SophosFirewallClient` to accept an `api_version` parameter (defaulting to `2200.1` for SFOS v22+ compatibility or reading from `SOPHOS_API_VERSION` env var). Fixes Sophos API Error 529 ("There is no API Version").
- **System Information Error Handling (`system.py`, `resources.py`)**: Added graceful handling for error code 529 ("Input request module is Invalid") in `sophos_get_system_info` and `sophos://system/info` when querying unsupported `<SystemInformation>` tags on SFOS appliances.
- **Environment & Deployments (`.env.example`, `docker-compose.yml`, `README.md`)**: Documented and passed `SOPHOS_API_VERSION` across container definitions and configuration files.

## [0.1.1] - 2026-07-27

### Fixed
- **Graceful Optional Dependency Fallback (`router.py`)**: Added `try...except (ImportError, ModuleNotFoundError)` to `get_router()` to catch missing `fastembed` / `numpy` dependencies when `USE_ROUTER=true` is enabled. Instead of crashing server initialization with `ModuleNotFoundError`, it logs a warning and gracefully disables tool routing while serving all 28 standard tools.
- **Dockerfile Package Installation (`Dockerfile`)**: Updated container build to `pip install .[router]` so official Docker images include `fastembed` and `numpy` out of the box for router compatibility.
- **Unit Test Coverage (`tests/test_router.py`)**: Added unit test `test_get_router_missing_fastembed` verifying graceful fallback behavior.
- **Documentation (`README.md`)**: Updated semantic tool routing documentation with explicit instructions for `pip`, `uv`, and `uvx` when using router extras.

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
