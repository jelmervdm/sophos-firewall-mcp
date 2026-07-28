"""Service definitions and service group management tools."""

from typing import Annotated, Any, Dict, List, Optional, Union, cast
from pydantic import Field
from sophos_firewall_mcp.client import SophosFirewallClient


async def sophos_list_services(
    name: Annotated[
        Optional[str],
        Field(description="Optional service definition name filter."),
    ] = None,
    client: Any = None,
) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    """List service objects (TCP, UDP, ICMP, IP protocol definitions).

    Use when inspecting custom or predefined port and protocol definitions.

    Args:
        name: Optional service name filter.
        client: Optional SophosFirewallClient instance.

    Returns:
        List or dict of service definitions.
    """
    close_client = False
    if client is None:
        client = SophosFirewallClient()
        close_client = True

    try:
        filter_crit = None
        if name:
            filter_crit = {"key": {"@name": "Name", "@operation": "=", "#text": name}}
        res = await client.get_tag("Services", filter_crit)
        return cast(Union[Dict[str, Any], List[Dict[str, Any]]], res)
    finally:
        if close_client:
            await client.close()


async def sophos_get_service(
    name: Annotated[
        str,
        Field(description="Name of the service object to retrieve."),
    ],
    client: Any = None,
) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    """Retrieve details of a specific service definition.

    Use when verifying target port ranges or protocol parameters for a service.

    Args:
        name: Name of the service object.
        client: Optional SophosFirewallClient instance.

    Returns:
        Service definition configuration.
    """
    return await sophos_list_services(name=name, client=client)


async def sophos_create_service(
    name: Annotated[
        str,
        Field(description="Unique name for the service definition."),
    ],
    protocol: Annotated[
        str,
        Field(description="Protocol type: 'TCP', 'UDP', 'TCP/UDP', or 'ICMP'."),
    ] = "TCP",
    source_port: Annotated[
        str,
        Field(description="Source port range (e.g. '1:65535')."),
    ] = "1:65535",
    destination_port: Annotated[
        str,
        Field(description="Destination port or port range (e.g. '8080' or '8000:8080')."),
    ] = "8080",
    client: Any = None,
) -> Dict[str, Any]:
    """Create a custom TCP/UDP service definition.

    Use when adding new port or protocol definitions for firewall rules.

    Args:
        name: Unique name for the service definition.
        protocol: Protocol type ('TCP', 'UDP', 'TCP/UDP', or 'ICMP'). Default is 'TCP'.
        source_port: Source port range (e.g. '1:65535'). Default is '1:65535'.
        destination_port: Destination port or port range (e.g. '8080' or '8000:8080').
        client: Optional SophosFirewallClient instance.

    Returns:
        API response status dictionary.
    """
    close_client = False
    if client is None:
        client = SophosFirewallClient()
        close_client = True

    payload = {
        "Name": name,
        "Type": "TCP/UDP",
        "ServiceDetail": {
            "Protocol": protocol,
            "SourcePort": source_port,
            "DestinationPort": destination_port,
        },
    }

    try:
        res = await client.set_tag("Services", payload)
        return cast(Dict[str, Any], res)
    finally:
        if close_client:
            await client.close()


async def sophos_list_service_groups(
    name: Annotated[
        Optional[str],
        Field(description="Optional service group name filter."),
    ] = None,
    client: Any = None,
) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    """List service group objects configured on Sophos Firewall.

    Use when browsing bundled groups of services used in rule policies.

    Args:
        name: Optional service group name filter.
        client: Optional SophosFirewallClient instance.

    Returns:
        List or dict of service groups.
    """
    close_client = False
    if client is None:
        client = SophosFirewallClient()
        close_client = True

    try:
        filter_crit = None
        if name:
            filter_crit = {"key": {"@name": "Name", "@operation": "=", "#text": name}}
        res = await client.get_tag("ServiceGroup", filter_crit)
        return cast(Union[Dict[str, Any], List[Dict[str, Any]]], res)
    finally:
        if close_client:
            await client.close()


async def sophos_delete_service(
    name: Annotated[
        str,
        Field(description="Name of the custom service object to remove."),
    ],
    client: Any = None,
) -> Dict[str, Any]:
    """Delete a custom service definition object by name.

    Use when deleting obsolete service port definitions from Sophos Firewall.

    Args:
        name: Name of the service object to delete.
        client: Optional SophosFirewallClient instance.

    Returns:
        API response status dictionary.
    """
    close_client = False
    if client is None:
        client = SophosFirewallClient()
        close_client = True

    try:
        res = await client.remove_tag("Services", name)
        return cast(Dict[str, Any], res)
    finally:
        if close_client:
            await client.close()


async def sophos_create_service_group(
    name: Annotated[
        str,
        Field(description="Unique name for the service group."),
    ],
    service_list: Annotated[
        List[str],
        Field(description="List of service object names to group together (e.g. ['HTTP', 'HTTPS'])."),
    ],
    client: Any = None,
) -> Dict[str, Any]:
    """Create a new service group object.

    Use when bundling multiple service port definitions into a single named group for security rules.

    Args:
        name: Unique name for the service group.
        service_list: List of service object names to include in the group.
        client: Optional SophosFirewallClient instance.

    Returns:
        API response status dictionary.
    """
    close_client = False
    if client is None:
        client = SophosFirewallClient()
        close_client = True

    payload = {
        "Name": name,
        "ServiceList": {"Service": service_list},
    }

    try:
        res = await client.set_tag("ServiceGroup", payload)
        return cast(Dict[str, Any], res)
    finally:
        if close_client:
            await client.close()


async def sophos_delete_service_group(
    name: Annotated[
        str,
        Field(description="Name of the service group to remove."),
    ],
    client: Any = None,
) -> Dict[str, Any]:
    """Delete a service group object by name.

    Use when removing an obsolete service group definition from Sophos Firewall.

    Args:
        name: Name of the service group to remove.
        client: Optional SophosFirewallClient instance.

    Returns:
        API response status dictionary.
    """
    close_client = False
    if client is None:
        client = SophosFirewallClient()
        close_client = True

    try:
        res = await client.remove_tag("ServiceGroup", name)
        return cast(Dict[str, Any], res)
    finally:
        if close_client:
            await client.close()
