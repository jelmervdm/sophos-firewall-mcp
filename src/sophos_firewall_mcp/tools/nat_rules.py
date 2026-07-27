"""NAT and port forwarding rule tools for Sophos Firewall."""

from typing import Annotated, Any, Dict, List, Optional, Union, cast
from pydantic import Field
from sophos_firewall_mcp.client import SophosFirewallClient


async def sophos_list_nat_rules(
    name: Annotated[
        Optional[str],
        Field(description="Optional NAT rule name filter."),
    ] = None,
    client: Any = None,
) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    """List NAT and DNAT port-forwarding rules on Sophos Firewall.

    Use when reviewing Network Address Translation rules and port forwarding.

    Args:
        name: Optional NAT rule name filter.
        client: Optional SophosFirewallClient instance.

    Returns:
        List or dict of NAT rules.
    """
    close_client = False
    if client is None:
        client = SophosFirewallClient()
        close_client = True

    try:
        filter_crit = None
        if name:
            filter_crit = {"key": {"@name": "Name", "@operation": "=", "#text": name}}
        res = await client.get_tag("NATRule", filter_crit)
        return cast(Union[Dict[str, Any], List[Dict[str, Any]]], res)
    finally:
        if close_client:
            await client.close()


async def sophos_get_nat_rule(
    name: Annotated[
        str,
        Field(description="Name of the NAT rule to retrieve."),
    ],
    client: Any = None,
) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    """Retrieve detailed configuration of a specific NAT rule.

    Use when auditing original/translated source, destination, and service parameters.

    Args:
        name: Name of the NAT rule.
        client: Optional SophosFirewallClient instance.

    Returns:
        NAT rule configuration details.
    """
    return await sophos_list_nat_rules(name=name, client=client)
