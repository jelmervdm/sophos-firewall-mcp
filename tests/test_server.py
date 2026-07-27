"""Unit tests for FastMCP server initialization, tool count, and registration."""

import pytest
from sophos_firewall_mcp.server import call_routed_tool, mcp, route_tools


def test_server_tool_registration():
    tm = mcp._tool_manager  # type: ignore[attr-defined]
    tools = list(tm._tools.keys())

    # Assert key tools are registered
    assert "sophos_get_system_info" in tools
    assert "sophos_get_interface_list" in tools
    assert "sophos_list_firewall_rules" in tools
    assert "sophos_create_firewall_rule" in tools
    assert "sophos_list_ip_hosts" in tools
    assert "sophos_create_ip_host" in tools
    assert "sophos_list_services" in tools
    assert "sophos_list_nat_rules" in tools
    assert "sophos_list_users" in tools
    assert "sophos_list_ipsec_vpns" in tools


def test_route_tools_disabled():
    res = route_tools("show system status")
    assert "Tool routing is not enabled" in res


@pytest.mark.asyncio
async def test_call_routed_tool_disabled():
    res = await call_routed_tool("sophos_get_system_info")
    assert "Tool routing is not enabled" in res
