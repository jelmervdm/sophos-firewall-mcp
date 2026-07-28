"""Unit tests for FastMCP server initialization, tool count, and registration."""

import pytest
from sophos_firewall_mcp.server import call_routed_tool, mcp, route_tools


def test_server_tool_registration():
    tm = mcp._tool_manager  # type: ignore[attr-defined]
    tools = list(tm._tools.keys())

    # Assert key tools are registered
    assert "sophos_raw_api_request" in tools
    assert "sophos_get_system_info" in tools
    assert "sophos_get_interface_list" in tools
    assert "sophos_list_firewall_rules" in tools
    assert "sophos_create_firewall_rule" in tools
    assert "sophos_update_firewall_rule" in tools
    assert "sophos_list_ip_hosts" in tools
    assert "sophos_create_ip_host" in tools
    assert "sophos_delete_ip_host_group" in tools
    assert "sophos_delete_fqdn_host" in tools
    assert "sophos_list_services" in tools
    assert "sophos_delete_service" in tools
    assert "sophos_create_service_group" in tools
    assert "sophos_delete_service_group" in tools
    assert "sophos_list_nat_rules" in tools
    assert "sophos_create_nat_rule" in tools
    assert "sophos_update_nat_rule" in tools
    assert "sophos_delete_nat_rule" in tools
    assert "sophos_list_users" in tools
    assert "sophos_delete_user" in tools
    assert "sophos_list_ipsec_vpns" in tools

    raw_tool = tm._tools["sophos_raw_api_request"]
    assert raw_tool.annotations.destructiveHint is True


@pytest.mark.asyncio
async def test_route_tools_disabled():
    res = await route_tools("show system status")
    assert "Tool routing is not enabled" in res


@pytest.mark.asyncio
async def test_call_routed_tool_disabled():
    res = await call_routed_tool("sophos_get_system_info")
    assert "Tool routing is not enabled" in res
