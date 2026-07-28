"""Main FastMCP server entrypoint for Sophos Firewall MCP."""

import asyncio
from typing import Any, List, Optional, Union
from mcp.server.fastmcp import FastMCP
from mcp.types import Tool, ToolAnnotations

from sophos_firewall_mcp import prompts, resources
from sophos_firewall_mcp.router import get_router
from sophos_firewall_mcp.tools import (
    firewall_rules,
    hosts_objects,
    nat_rules,
    raw_api,
    services_objects,
    system,
    users_auth,
    vpn,
)

# Initialize FastMCP Server
mcp = FastMCP(
    "Sophos Firewall MCP Server",
    instructions=(
        "Sophos Firewall MCP Server provides tools to monitor system status, "
        "manage firewall rules, host objects, service definitions, NAT rules, "
        "user accounts, and VPN policies on Sophos Firewall (SFOS) appliances."
    ),
)

# Register resources & diagnostic prompts
resources.register(mcp)
prompts.register(mcp)

# -----------------------------------------------------------------------------
# Register Domain Tools with ToolAnnotations
# -----------------------------------------------------------------------------

# Low-Level Generic API Tool
mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=True, idempotentHint=False))(
    raw_api.sophos_raw_api_request
)

# System & Status Tools
mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))(system.sophos_get_system_info)
mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))(system.sophos_get_service_status)
mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))(system.sophos_get_interface_list)

# Firewall Rules Tools
mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))(firewall_rules.sophos_list_firewall_rules)
mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))(firewall_rules.sophos_get_firewall_rule)
mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, idempotentHint=False))(
    firewall_rules.sophos_create_firewall_rule
)
mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, idempotentHint=True))(
    firewall_rules.sophos_update_firewall_rule
)
mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, idempotentHint=True))(
    firewall_rules.sophos_update_firewall_rule_status
)
mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=True, idempotentHint=True))(
    firewall_rules.sophos_delete_firewall_rule
)

# Host & Network Object Tools
mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))(hosts_objects.sophos_list_ip_hosts)
mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))(hosts_objects.sophos_get_ip_host)
mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, idempotentHint=False))(
    hosts_objects.sophos_create_ip_host
)
mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=True, idempotentHint=True))(
    hosts_objects.sophos_delete_ip_host
)
mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))(hosts_objects.sophos_list_ip_host_groups)
mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, idempotentHint=False))(
    hosts_objects.sophos_create_ip_host_group
)
mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=True, idempotentHint=True))(
    hosts_objects.sophos_delete_ip_host_group
)
mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))(hosts_objects.sophos_list_fqdn_hosts)
mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, idempotentHint=False))(
    hosts_objects.sophos_create_fqdn_host
)
mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=True, idempotentHint=True))(
    hosts_objects.sophos_delete_fqdn_host
)

# Service & Protocol Tools
mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))(services_objects.sophos_list_services)
mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))(services_objects.sophos_get_service)
mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, idempotentHint=False))(
    services_objects.sophos_create_service
)
mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=True, idempotentHint=True))(
    services_objects.sophos_delete_service
)
mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))(services_objects.sophos_list_service_groups)
mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, idempotentHint=False))(
    services_objects.sophos_create_service_group
)
mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=True, idempotentHint=True))(
    services_objects.sophos_delete_service_group
)

# NAT Rules Tools
mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))(nat_rules.sophos_list_nat_rules)
mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))(nat_rules.sophos_get_nat_rule)
mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, idempotentHint=False))(
    nat_rules.sophos_create_nat_rule
)
mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, idempotentHint=True))(
    nat_rules.sophos_update_nat_rule
)
mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=True, idempotentHint=True))(
    nat_rules.sophos_delete_nat_rule
)

# User Accounts & Auth Tools
mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))(users_auth.sophos_list_users)
mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))(users_auth.sophos_get_user)
mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, idempotentHint=False))(
    users_auth.sophos_create_user
)
mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=True, idempotentHint=True))(
    users_auth.sophos_delete_user
)
mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))(users_auth.sophos_list_live_users)

# VPN Management Tools
mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))(vpn.sophos_list_ipsec_vpns)
mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))(vpn.sophos_list_sslvpn_policies)

# Lazy Tool Router Initialization
_router: Optional[Any] = None
_router_initialized: bool = False


async def get_initialized_router() -> Optional[Any]:
    """Lazy initialize and index the semantic tool router if enabled."""
    global _router, _router_initialized
    if _router_initialized:
        return _router

    r = get_router()
    if r is not None:
        all_registered_tools = await mcp.list_tools()
        r.index([(t.name, t.description or "") for t in all_registered_tools])
        _router = r
    _router_initialized = True
    return _router


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
async def route_tools(
    query: str,
    top_k: int = 5,
) -> Union[List[Tool], str]:
    """Find relevant Sophos Firewall tools matching a natural language prompt.

    Args:
        query: Natural language task description or question.
        top_k: Number of relevant tools to return. Default is 5.

    Returns:
        List of matching tool schema definitions or status string.
    """
    router = await get_initialized_router()
    if router is None:
        return "Tool routing is not enabled."
    tool_names = router.search(query, top_k=top_k)
    all_tools = await mcp.list_tools()
    name_map = {t.name: t for t in all_tools}
    return [name_map[n] for n in tool_names if n in name_map]


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False))
async def call_routed_tool(
    tool_name: str,
    arguments: Optional[dict] = None,
) -> Any:
    """Dynamically execute a routed tool by name with arguments.

    Args:
        tool_name: Name of the registered tool to call.
        arguments: Optional dictionary of arguments to pass to the tool function.

    Returns:
        Result of the executed tool function.
    """
    router = await get_initialized_router()
    if router is None:
        return "Tool routing is not enabled."
    return await mcp.call_tool(tool_name, arguments or {})


def main() -> None:
    """Entry point for running the Sophos Firewall MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
