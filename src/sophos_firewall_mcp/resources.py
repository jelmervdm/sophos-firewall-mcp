"""FastMCP resources providing static/read-only access to Sophos Firewall data."""

import json
from mcp.server.fastmcp import FastMCP
from sophos_firewall_mcp.client import SophosFirewallClient


def register(mcp: FastMCP) -> None:
    """Register Sophos Firewall resources on FastMCP server instance."""

    @mcp.resource("sophos://system/info")
    async def get_system_info_resource() -> str:
        """Resource providing system details, appliance model, serial number, and firmware version."""
        async with SophosFirewallClient() as client:
            info = await client.get_tag("SystemInformation")
        return json.dumps(info, indent=2)

    @mcp.resource("sophos://interfaces")
    async def get_interfaces_resource() -> str:
        """Resource providing network interface configuration, zones, and link state."""
        async with SophosFirewallClient() as client:
            interfaces = await client.get_tag("Interface")
        return json.dumps(interfaces, indent=2)

    @mcp.resource("sophos://services/status")
    async def get_service_status_resource() -> str:
        """Resource providing operational status of core firewall background services."""
        async with SophosFirewallClient() as client:
            services = await client.get_tag("Services")
        return json.dumps(services, indent=2)
