# Sophos Firewall MCP Server (`sophos-firewall-mcp`)

[![Docker Image](https://img.shields.io/badge/docker-ghcr.io-blue.svg)](https://github.com/jelmervdm/sophos-firewall-mcp)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13-blue.svg)](pyproject.toml)
[![TDQS Score](https://img.shields.io/badge/TDQS-5.00%2F5.00%20(Tier%20A%2B)-success.svg)](https://github.com/glama-ai/tool-definition-quality-score)

An asynchronous [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server for Sophos Firewall (SFOS), enabling AI assistants (such as Antigravity IDE, Claude Desktop, VS Code, and Cursor) to manage, audit, and troubleshoot Sophos Firewall network security infrastructure.

---

## 🌟 Key Features

* **Async XML API Integration:** Built on `httpx.AsyncClient` for high-throughput, non-blocking IO with Sophos SFOS XML API endpoints (`/webconsole/APIController`).
* **7 Comprehensive Tool Domains (28 Tools):**
  * **System & Status:** System version, serial number, uptime, service operational state, and network interface configurations.
  * **Firewall Rules:** Security policies listing, creation, status toggling, and rule deletion.
  * **Host & Network Objects:** IP host definitions, network subnets, IP host groups, and FQDN objects.
  * **Services:** Custom TCP/UDP service objects, port ranges, and service groups.
  * **NAT Rules:** SNAT and DNAT port-forwarding rule inspection.
  * **User Management:** Local user account configuration and live user session monitoring.
  * **VPN Management:** IPsec site-to-site tunnels and SSL VPN remote access policies.
* **FastMCP Resources:** Read-only system state via URIs (`sophos://system/info`, `sophos://interfaces`, `sophos://services/status`).
* **Guided Prompts:** Contextual security audits (`audit_firewall_rules`) and traffic troubleshooting (`troubleshoot_connectivity`).
* **Semantic Tool Router:** FastEmbed text embedding router for intelligent tool selection (`USE_ROUTER=true`).
* **Tier A+ Quality Score:** 100% parameter descriptions, full `ToolAnnotations` safety metadata, and 100% test coverage.

---

## 🏆 Tool Definition Quality Score (TDQS)

This server is audited against the **[Tool Definition Quality Score (TDQS)](https://github.com/glama-ai/tool-definition-quality-score)** framework to guarantee optimal function calling, type safety, and runtime safety for LLMs.

```text
================ TDQS EVALUATION REPORT ================
Total Registered Tools        : 28
Tools with Behavioral Anno     : 28 / 28 (100.0%)
Tools with 100% Param Descs    : 28 / 28 (100.0%)
Tools with Usage Guidelines    : 28 / 28 (100.0%)
Average Quality Score (TDQS)   : 5.00 / 5.00
TDQS Quality Tier              : Tier A+
========================================================
```

- **Behavioral Annotations (`ToolAnnotations`):** 100% of tools specify `readOnlyHint`, `destructiveHint`, and `idempotentHint` metadata.
- **Parameter Descriptions (`Annotated[..., Field(...)]`):** Every parameter includes explicit typing and human-readable descriptions.
- **Usage Guidelines:** Standardized docstrings detailing exact trigger conditions ("Use when...").

---

## 🔧 Environment Variables

| Variable | Description | Default |
| :--- | :--- | :--- |
| `SOPHOS_HOST` | Sophos Firewall IP address or FQDN | `192.168.1.1` |
| `SOPHOS_PORT` | Web Console API port | `4444` |
| `SOPHOS_USERNAME` | API Administrator Username | `admin` |
| `SOPHOS_PASSWORD` | API Administrator Password | *(Required)* |
| `SOPHOS_VERIFY_SSL` | Verify SSL/TLS certificates (set `false` for self-signed certs) | `false` |
| `SOPHOS_TIMEOUT` | API request timeout in seconds | `30.0` |
| `USE_ROUTER` | Set `true` to enable FastEmbed semantic tool routing | `false` |

---

## 🛠 Client Integration

Add the configuration snippet matching your environment to your MCP settings file (e.g. `.vscode/mcp.json` or `mcp_config.json` in Antigravity IDE, Claude Desktop, or VS Code).

### Option 1: Docker / Podman Drop-in Container Deployment

Podman is fully supported as a rootless drop-in replacement for Docker on Fedora/RHEL/Linux:

```json
{
  "mcpServers": {
    "sophos-firewall": {
      "command": "podman",
      "args": [
        "run",
        "-i",
        "--rm",
        "-e", "SOPHOS_HOST",
        "-e", "SOPHOS_PORT",
        "-e", "SOPHOS_USERNAME",
        "-e", "SOPHOS_PASSWORD",
        "-e", "SOPHOS_VERIFY_SSL",
        "-e", "USE_ROUTER",
        "ghcr.io/jelmervdm/sophos-firewall-mcp:latest"
      ],
      "env": {
        "SOPHOS_HOST": "172.16.16.16",
        "SOPHOS_PORT": "4444",
        "SOPHOS_USERNAME": "admin",
        "SOPHOS_PASSWORD": "your_secure_password_here",
        "SOPHOS_VERIFY_SSL": "false",
        "USE_ROUTER": "false"
      }
    }
  }
}
```

> **Tip for Docker vs Podman**: Replace `"command": "podman"` with `"command": "docker"` if using standard Docker. Ensure `-i` is retained and **never** use `-t` (TTY mode), as TTY mode injects carriage returns (`\r\n`) that disrupt stdio JSON-RPC protocol parsing.

---

### Option 2: Local Python Execution (without PyPI)

#### Via `uv` (Local Workspace Directory):
```json
{
  "mcpServers": {
    "sophos-firewall": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/sophos-firewall-mcp",
        "run",
        "sophos-firewall-mcp-server"
      ],
      "env": {
        "SOPHOS_HOST": "192.168.1.1",
        "SOPHOS_PORT": "4444",
        "SOPHOS_USERNAME": "admin",
        "SOPHOS_PASSWORD": "your_secure_password_here",
        "SOPHOS_VERIFY_SSL": "false"
      }
    }
  }
}
```

#### Via `python` (Editable Install `pip install -e .`):
```json
{
  "mcpServers": {
    "sophos-firewall": {
      "command": "python",
      "args": ["-m", "sophos_firewall_mcp.server"],
      "env": {
        "SOPHOS_HOST": "192.168.1.1",
        "SOPHOS_PORT": "4444",
        "SOPHOS_USERNAME": "admin",
        "SOPHOS_PASSWORD": "your_secure_password_here",
        "SOPHOS_VERIFY_SSL": "false"
      }
    }
  }
}
```

#### Via `uvx` directly from GitHub Repository:
```json
{
  "mcpServers": {
    "sophos-firewall": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/jelmervdm/sophos-firewall-mcp.git",
        "sophos-firewall-mcp-server"
      ],
      "env": {
        "SOPHOS_HOST": "192.168.1.1",
        "SOPHOS_PORT": "4444",
        "SOPHOS_USERNAME": "admin",
        "SOPHOS_PASSWORD": "your_secure_password_here",
        "SOPHOS_VERIFY_SSL": "false"
      }
    }
  }
}
```

---

## 🧠 Semantic Tool Routing

When connecting `sophos-firewall-mcp` to AI models with constrained context windows, set `USE_ROUTER=true` (or `TOOL_ROUTING=true`).

When enabled:
1. The server exposes only 2 meta-tools: `route_tools` and `call_routed_tool`.
2. `route_tools` uses local CPU embeddings (`fastembed` with `BAAI/bge-small-en-v1.5`) to search for matching firewall tools in 5-10ms.
3. `call_routed_tool` dynamically invokes the matching tool with parameters.

---

## 🧪 Testing & Quality Assurance

Run the comprehensive test suite, linting, mypy type checks, and TDQS audit:

```bash
# Evaluate Tool Definition Quality Score (TDQS)
uv run python scripts/check_tdqs.py

# Run pytest unit test suite (39 tests)
uv run pytest -v

# Code style and syntax linting
uv run flake8 src tests scripts

# Static type verification
uv run mypy src
```

---

## 📄 License

Distributed under the Apache 2.0 License. See [LICENSE](LICENSE) for details.
