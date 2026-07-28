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


async def sophos_create_nat_rule(
    name: Annotated[
        str,
        Field(description="Unique name for the NAT rule."),
    ],
    status: Annotated[
        str,
        Field(description="Rule status: 'Enable' or 'Disable'."),
    ] = "Enable",
    original_source: Annotated[
        Optional[List[str]],
        Field(description="Original source host/network object names (e.g. ['Any'])."),
    ] = None,
    original_destination: Annotated[
        Optional[List[str]],
        Field(description="Original destination host/network object names (e.g. ['WAN_IP'])."),
    ] = None,
    original_service: Annotated[
        Optional[List[str]],
        Field(description="Original service object names (e.g. ['HTTP'])."),
    ] = None,
    translated_source: Annotated[
        Optional[str],
        Field(description="Translated source object or 'MASQUERADE' / 'Original'."),
    ] = "Original",
    translated_destination: Annotated[
        Optional[str],
        Field(description="Translated destination host/network object name."),
    ] = "Original",
    translated_service: Annotated[
        Optional[str],
        Field(description="Translated service object name."),
    ] = "Original",
    client: Any = None,
) -> Dict[str, Any]:
    """Create a Network Address Translation (NAT or DNAT) rule.

    Use when defining port forwarding, SNAT masquerading, or DNAT inbound translation rules.

    Args:
        name: Unique name for the NAT rule.
        status: Rule status ('Enable' or 'Disable'). Default is 'Enable'.
        original_source: Original source host/network object names.
        original_destination: Original destination host/network object names.
        original_service: Original service object names.
        translated_source: Translated source object ('MASQUERADE', 'Original', etc.).
        translated_destination: Translated destination host/network object.
        translated_service: Translated service object name.
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
        "Status": status,
        "OriginalSource": {"Host": original_source or ["Any"]},
        "OriginalDestination": {"Host": original_destination or ["Any"]},
        "OriginalService": {"Service": original_service or ["Any"]},
        "TranslatedSource": translated_source or "Original",
        "TranslatedDestination": translated_destination or "Original",
        "TranslatedService": translated_service or "Original",
    }

    try:
        res = await client.set_tag("NATRule", payload)
        return cast(Dict[str, Any], res)
    finally:
        if close_client:
            await client.close()


async def sophos_update_nat_rule(
    name: Annotated[
        str,
        Field(description="Name of the NAT rule to update."),
    ],
    status: Annotated[
        Optional[str],
        Field(description="Optional new status: 'Enable' or 'Disable'."),
    ] = None,
    translated_source: Annotated[
        Optional[str],
        Field(description="Optional new translated source object."),
    ] = None,
    translated_destination: Annotated[
        Optional[str],
        Field(description="Optional new translated destination object."),
    ] = None,
    translated_service: Annotated[
        Optional[str],
        Field(description="Optional new translated service object."),
    ] = None,
    client: Any = None,
) -> Dict[str, Any]:
    """Update fields on an existing NAT rule.

    Use when updating status or target translation parameters on an existing NAT or port-forwarding rule.

    Args:
        name: Name of the NAT rule to update.
        status: Optional new status ('Enable' or 'Disable').
        translated_source: Optional new translated source object.
        translated_destination: Optional new translated destination object.
        translated_service: Optional new translated service object.
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
        rules = await client.get_tag("NATRule", filter_crit)

        target_rule: Optional[Dict[str, Any]] = None
        if isinstance(rules, dict):
            if rules.get("Name") == name or "Name" in rules:
                target_rule = rules
            elif "NATRule" in rules:
                sub = rules["NATRule"]
                if isinstance(sub, list):
                    target_rule = next((r for r in sub if isinstance(r, dict) and r.get("Name") == name), None)
                elif isinstance(sub, dict) and sub.get("Name") == name:
                    target_rule = sub
        elif isinstance(rules, list):
            target_rule = next((r for r in rules if isinstance(r, dict) and r.get("Name") == name), None)

        if not target_rule:
            return {"error": f"NAT rule '{name}' not found."}

        if status is not None:
            target_rule["Status"] = status
        if translated_source is not None:
            target_rule["TranslatedSource"] = translated_source
        if translated_destination is not None:
            target_rule["TranslatedDestination"] = translated_destination
        if translated_service is not None:
            target_rule["TranslatedService"] = translated_service

        target_rule.pop("@transactionid", None)

        res = await client.set_tag("NATRule", target_rule)
        return cast(Dict[str, Any], res)
    finally:
        if close_client:
            await client.close()


async def sophos_delete_nat_rule(
    name: Annotated[
        str,
        Field(description="Name of the NAT rule to delete."),
    ],
    client: Any = None,
) -> Dict[str, Any]:
    """Delete a NAT rule by name.

    Use when permanently removing a NAT or port-forwarding policy.

    Args:
        name: Name of the NAT rule to remove.
        client: Optional SophosFirewallClient instance.

    Returns:
        API response status dictionary.
    """
    close_client = False
    if client is None:
        client = SophosFirewallClient()
        close_client = True

    try:
        res = await client.remove_tag("NATRule", name)
        return cast(Dict[str, Any], res)
    finally:
        if close_client:
            await client.close()
