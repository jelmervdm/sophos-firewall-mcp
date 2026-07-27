# Sophos Firewall MCP Server (`sophos-firewall-mcp`)

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue)](pyproject.toml)

An asynchronous [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server for Sophos Firewall (SFOS), enabling AI assistants (such as Antigravity, Claude, and VS Code) to manage, audit, and troubleshoot Sophos Firewall network security infrastructure.

---

## 🌟 Key Features

* **Async XML API Integration:** Built on `httpx.AsyncClient` for high-throughput, non-blocking IO with Sophos SFOS XML API endpoints.
* **7 Comprehensive Tool Domains:**
  * **System & Status:** System version, serial number, uptime, service operational state, and network interface configurations.
  * **Firewall Rules:** Security policies listing, creation, status toggling, and rule deletion.
  * **Host & Network Objects:** IP host definitions, network subnets, IP host groups, and FQDN objects.
  * **Services:** Custom TCP/UDP service objects, port ranges, and service groups.
  * **NAT Rules:** SNAT and DNAT port-forwarding rule inspection.
  * **User Management:** Local user account configuration and live user session monitoring.
  * **VPN Management:** IPsec site-to-site tunnels and SSL VPN remote access policies.
* **FastMCP Resources:** Read-only system state via URIs (`sophos://system/info`, `sophos://interfaces`, `sophos://services/status`).
* **Guided Prompts:** Contextual security audits (`audit_firewall_rules`) and traffic troubleshooting (`troubleshoot_connectivity`).
* **Optional Semantic Tool Router:** FastEmbed text embedding router for intelligent tool selection.

---

## 🔧 Environment Variables

| Variable | Default | Description |
| :--- | :--- | :--- |
| `SOPHOS_HOST` | `192.168.1.1` | Sophos Firewall IP address or FQDN |
| `SOPHOS_PORT` | `4444` | Web Console API port (default `4444`) |
| `SOPHOS_USERNAME` | `admin` | API Administrator Username |
| `SOPHOS_PASSWORD` | *Required* | API Administrator Password |
| `SOPHOS_VERIFY_SSL` | `false` | Verify SSL/TLS certificates (set `false` for self-signed certificates) |
| `SOPHOS_TIMEOUT` | `30.0` | API request timeout in seconds |
| `USE_ROUTER` | `false` | Enable semantic tool routing via FastEmbed |

---

## 🚀 Quick Start & Installation

### Option 1: Local Virtual Environment with `uv` or `pip`

```bash
# Clone repository
git clone https://github.com/jelmervdm/sophos-firewall-mcp.git
cd sophos-firewall-mcp

# Create virtual environment & install package
python -m venv .venv
source .venv/bin/activate
pip install -e ".[router]" -r requirements-dev.txt

# Run server via stdio
sophos-firewall-mcp-server
```

---

## 🛠 MCP Client Configuration

### Antigravity IDE / VS Code / Claude Desktop (`mcpServers`)

Add the following to your MCP client configuration (`mcp_config.json`):

```json
{
  "mcpServers": {
    "sophos-firewall": {
      "command": "uv",
      "args": [
        "--directory",
        "/home/jelmer/github-public/sophos-firewall-mcp",
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

---

## 🐳 Docker Deployment

### Docker Compose

```bash
docker-compose up -d
```

### Docker CLI

```bash
docker build -t sophos-firewall-mcp:latest .
docker run -i --rm \
  -e SOPHOS_HOST="192.168.1.1" \
  -e SOPHOS_PORT="4444" \
  -e SOPHOS_USERNAME="admin" \
  -e SOPHOS_PASSWORD="your_password" \
  -e SOPHOS_VERIFY_SSL="false" \
  sophos-firewall-mcp:latest
```

---

## 🧪 Testing & Quality Assurance

Run the test suite, linting, and type verification:

```bash
# Run pytest unit tests
pytest -v

# Run type checker
mypy src

# Run linter & formatter checks
flake8 src tests
black --check src tests
```

---

## 📄 License

Distributed under the Apache 2.0 License. See [LICENSE](LICENSE) for details.
