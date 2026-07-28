"""Firewall security policy tools for Sophos Firewall."""

from typing import Annotated, Any, Dict, List, Optional, Union, cast
from pydantic import Field
from sophos_firewall_mcp.client import SophosFirewallClient


async def sophos_list_firewall_rules(
    name: Annotated[
        Optional[str],
        Field(description="Optional firewall rule name filter."),
    ] = None,
    client: Any = None,
) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    """List firewall security rules configured on the appliance.

    Use when browsing security policies or searching for rules matching a specific name.

    Args:
        name: Optional firewall rule name filter.
        client: Optional SophosFirewallClient instance.

    Returns:
        List or dict of firewall rule configurations.
    """
    close_client = False
    if client is None:
        client = SophosFirewallClient()
        close_client = True

    try:
        filter_crit = None
        if name:
            filter_crit = {"key": {"@name": "Name", "@operation": "=", "#text": name}}
        res = await client.get_tag("FirewallRule", filter_crit)
        return cast(Union[Dict[str, Any], List[Dict[str, Any]]], res)
    finally:
        if close_client:
            await client.close()


async def sophos_get_firewall_rule(
    name: Annotated[
        str,
        Field(description="Name of the firewall rule to retrieve."),
    ],
    client: Any = None,
) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    """Retrieve details for a specific firewall rule by name.

    Use when inspecting full policy configuration for a single firewall rule.

    Args:
        name: Name of the firewall rule.
        client: Optional SophosFirewallClient instance.

    Returns:
        Firewall rule configuration.
    """
    return await sophos_list_firewall_rules(name=name, client=client)


async def sophos_create_firewall_rule(
    name: Annotated[
        str,
        Field(description="Unique name for the firewall rule."),
    ],
    action: Annotated[
        str,
        Field(description="Rule policy action: 'Accept', 'Drop', or 'Reject'."),
    ] = "Accept",
    source_zones: Annotated[
        Optional[List[str]],
        Field(description="List of source network zone names (e.g. ['LAN'])."),
    ] = None,
    destination_zones: Annotated[
        Optional[List[str]],
        Field(description="List of destination network zone names (e.g. ['WAN'])."),
    ] = None,
    source_networks: Annotated[
        Optional[List[str]],
        Field(description="List of source host/network object names (e.g. ['Any'])."),
    ] = None,
    destination_networks: Annotated[
        Optional[List[str]],
        Field(description="List of destination host/network object names (e.g. ['Any'])."),
    ] = None,
    services: Annotated[
        Optional[List[str]],
        Field(description="List of service object names (e.g. ['HTTP', 'HTTPS'])."),
    ] = None,
    status: Annotated[
        str,
        Field(description="Rule status: 'Enable' or 'Disable'."),
    ] = "Enable",
    client: Any = None,
) -> Dict[str, Any]:
    """Create a new IPv4 firewall security rule.

    Use when defining new network access control policies between zones and host objects.

    Args:
        name: Unique name for the firewall rule.
        action: Rule policy action ('Accept', 'Drop', or 'Reject'). Default is 'Accept'.
        source_zones: List of source network zone names (e.g. ['LAN']).
        destination_zones: List of destination network zone names (e.g. ['WAN']).
        source_networks: List of source host/network object names (e.g. ['Any']).
        destination_networks: List of destination host/network object names (e.g. ['Any']).
        services: List of service object names (e.g. ['HTTP', 'HTTPS']).
        status: Rule status ('Enable' or 'Disable'). Default is 'Enable'.
        client: Optional SophosFirewallClient instance.

    Returns:
        API response status dictionary.
    """
    close_client = False
    if client is None:
        client = SophosFirewallClient()
        close_client = True

    payload: Dict[str, Any] = {
        "Name": name,
        "IPFamily": "IPv4",
        "Status": status,
        "PolicyType": "Network",
        "NetworkPolicy": {
            "Action": action,
            "SourceZones": {"Zone": source_zones or ["LAN"]},
            "DestinationZones": {"Zone": destination_zones or ["WAN"]},
            "SourceNetworks": {"Network": source_networks or ["Any"]},
            "DestinationNetworks": {"Network": destination_networks or ["Any"]},
            "Services": {"Service": services or ["Any"]},
        },
    }

    try:
        res = await client.set_tag("FirewallRule", payload)
        return cast(Dict[str, Any], res)
    finally:
        if close_client:
            await client.close()


async def sophos_update_firewall_rule(
    name: Annotated[
        str,
        Field(description="Name of the firewall rule to update."),
    ],
    action: Annotated[
        Optional[str],
        Field(description="Rule policy action: 'Accept', 'Drop', or 'Reject'."),
    ] = None,
    source_zones: Annotated[
        Optional[List[str]],
        Field(description="List of source network zone names (e.g. ['LAN'])."),
    ] = None,
    destination_zones: Annotated[
        Optional[List[str]],
        Field(description="List of destination network zone names (e.g. ['WAN'])."),
    ] = None,
    source_networks: Annotated[
        Optional[List[str]],
        Field(description="List of source host/network object names (e.g. ['Any'])."),
    ] = None,
    destination_networks: Annotated[
        Optional[List[str]],
        Field(description="List of destination host/network object names (e.g. ['Any'])."),
    ] = None,
    services: Annotated[
        Optional[List[str]],
        Field(description="List of service object names (e.g. ['HTTP', 'HTTPS'])."),
    ] = None,
    log_traffic: Annotated[
        Optional[str],
        Field(description="Enable or disable logging: 'Enable' or 'Disable'."),
    ] = None,
    status: Annotated[
        Optional[str],
        Field(description="Rule status: 'Enable' or 'Disable'."),
    ] = None,
    client: Any = None,
) -> Dict[str, Any]:
    """Update configuration fields on an existing firewall rule.

    Use when modifying parameters such as logging, action, zones, host objects, or status on an existing security policy.

    Args:
        name: Name of the firewall rule to update.
        action: Optional new rule policy action ('Accept', 'Drop', or 'Reject').
        source_zones: Optional list of source network zone names.
        destination_zones: Optional list of destination network zone names.
        source_networks: Optional list of source host/network object names.
        destination_networks: Optional list of destination host/network object names.
        services: Optional list of service object names.
        log_traffic: Optional logging setting ('Enable' or 'Disable').
        status: Optional rule status ('Enable' or 'Disable').
        client: Optional SophosFirewallClient instance.

    Returns:
        API response status dictionary.
    """
    close_client = False
    if client is None:
        client = SophosFirewallClient()
        close_client = True

    try:
        filter_crit = {"key": {"@name": "Name", "@operation": "=", "#text": name}}
        rules = await client.get_tag("FirewallRule", filter_crit)

        target_rule: Optional[Dict[str, Any]] = None
        if isinstance(rules, dict):
            if rules.get("Name") == name or "Name" in rules:
                target_rule = rules
            elif "FirewallRule" in rules:
                sub = rules["FirewallRule"]
                if isinstance(sub, list):
                    target_rule = next((r for r in sub if isinstance(r, dict) and r.get("Name") == name), None)
                elif isinstance(sub, dict) and sub.get("Name") == name:
                    target_rule = sub
        elif isinstance(rules, list):
            target_rule = next((r for r in rules if isinstance(r, dict) and r.get("Name") == name), None)

        if not target_rule:
            return {"error": f"Firewall rule '{name}' not found."}

        if status is not None:
            target_rule["Status"] = status

        target_rule.setdefault("IPFamily", "IPv4")
        target_rule.setdefault("PolicyType", "Network")

        net_policy = target_rule.get("NetworkPolicy")
        if not isinstance(net_policy, dict):
            net_policy = {}
            target_rule["NetworkPolicy"] = net_policy

        if action is not None:
            net_policy["Action"] = action
        if log_traffic is not None:
            net_policy["LogTraffic"] = log_traffic

        if source_zones is not None:
            net_policy["SourceZones"] = {"Zone": source_zones}
        if destination_zones is not None:
            net_policy["DestinationZones"] = {"Zone": destination_zones}
        if source_networks is not None:
            net_policy["SourceNetworks"] = {"Network": source_networks}
        if destination_networks is not None:
            net_policy["DestinationNetworks"] = {"Network": destination_networks}
        if services is not None:
            net_policy["Services"] = {"Service": services}

        target_rule.pop("@transactionid", None)

        res = await client.set_tag("FirewallRule", target_rule)
        return cast(Dict[str, Any], res)
    finally:
        if close_client:
            await client.close()


async def sophos_update_firewall_rule_status(
    name: Annotated[
        str,
        Field(description="Name of the firewall rule to update."),
    ],
    status: Annotated[
        str,
        Field(description="Desired status: 'Enable' or 'Disable'."),
    ],
    client: Any = None,
) -> Dict[str, Any]:
    """Enable or disable an existing firewall rule.

    Use when toggling a security policy active state without deleting the rule.

    Args:
        name: Name of the firewall rule.
        status: Desired state ('Enable' or 'Disable').
        client: Optional SophosFirewallClient instance.

    Returns:
        API response status dictionary.
    """
    close_client = False
    if client is None:
        client = SophosFirewallClient()
        close_client = True

    payload = {"Name": name, "Status": status}
    try:
        res = await client.set_tag("FirewallRule", payload)
        return cast(Dict[str, Any], res)
    finally:
        if close_client:
            await client.close()


async def sophos_delete_firewall_rule(
    name: Annotated[
        str,
        Field(description="Name of the firewall rule to delete."),
    ],
    client: Any = None,
) -> Dict[str, Any]:
    """Delete a firewall rule by name.

    Use when permanently removing an obsolete security policy.

    Args:
        name: Name of the firewall rule to delete.
        client: Optional SophosFirewallClient instance.

    Returns:
        API response status dictionary.
    """
    close_client = False
    if client is None:
        client = SophosFirewallClient()
        close_client = True

    try:
        res = await client.remove_tag("FirewallRule", name)
        return cast(Dict[str, Any], res)
    finally:
        if close_client:
            await client.close()
