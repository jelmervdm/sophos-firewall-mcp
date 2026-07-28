"""IP hosts, networks, host groups, and FQDN object management tools."""

from typing import Annotated, Any, Dict, List, Optional, Union, cast
from pydantic import Field
from sophos_firewall_mcp.client import SophosFirewallClient


async def sophos_list_ip_hosts(
    name: Annotated[
        Optional[str],
        Field(description="Optional IP host object name filter."),
    ] = None,
    client: Any = None,
) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    """List IP host objects defined on Sophos Firewall.

    Use when browsing IP address, network subnet, or IP range objects.

    Args:
        name: Optional IP host name filter.
        client: Optional SophosFirewallClient instance.

    Returns:
        List or dict of IP host objects.
    """
    close_client = False
    if client is None:
        client = SophosFirewallClient()
        close_client = True

    try:
        filter_crit = None
        if name:
            filter_crit = {"key": {"@name": "Name", "@operation": "=", "#text": name}}
        res = await client.get_tag("IPHost", filter_crit)
        return cast(Union[Dict[str, Any], List[Dict[str, Any]]], res)
    finally:
        if close_client:
            await client.close()


async def sophos_get_ip_host(
    name: Annotated[
        str,
        Field(description="Name of the IP host object to retrieve."),
    ],
    client: Any = None,
) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    """Retrieve configuration details for a specific IP host object.

    Use when inspecting target IP address or subnet definition for an object.

    Args:
        name: Name of the IP host object.
        client: Optional SophosFirewallClient instance.

    Returns:
        IP host configuration.
    """
    return await sophos_list_ip_hosts(name=name, client=client)


async def sophos_create_ip_host(
    name: Annotated[
        str,
        Field(description="Unique name for the host object."),
    ],
    host_type: Annotated[
        str,
        Field(description="Type of host object: 'IP', 'Network', 'IPRange', or 'IPList'."),
    ] = "IP",
    ip_address: Annotated[
        str,
        Field(description="IP address or network prefix (e.g. '192.168.1.100')."),
    ] = "192.168.1.100",
    subnet_mask: Annotated[
        Optional[str],
        Field(description="Subnet mask if host_type is 'Network' (e.g. '255.255.255.0' or '24')."),
    ] = None,
    ip_family: Annotated[
        str,
        Field(description="IP protocol family: 'IPv4' or 'IPv6'."),
    ] = "IPv4",
    client: Any = None,
) -> Dict[str, Any]:
    """Create a new IP host object (IP Address, Network, IP Range, or IP List).

    Use when registering host IP or network subnet definitions for firewall policies.

    Args:
        name: Unique name for the host object.
        host_type: Type of host object ('IP', 'Network', 'IPRange', or 'IPList'). Default is 'IP'.
        ip_address: IP address or starting IP address/subnet.
        subnet_mask: Subnet mask if host_type is 'Network' (e.g. '255.255.255.0' or '24').
        ip_family: IP protocol family ('IPv4' or 'IPv6'). Default is 'IPv4'.
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
        "IPFamily": ip_family,
        "HostType": host_type,
        "IPAddress": ip_address,
    }
    if subnet_mask:
        payload["Subnet"] = subnet_mask

    try:
        res = await client.set_tag("IPHost", payload)
        return cast(Dict[str, Any], res)
    finally:
        if close_client:
            await client.close()


async def sophos_delete_ip_host(
    name: Annotated[
        str,
        Field(description="Name of the IP host object to remove."),
    ],
    client: Any = None,
) -> Dict[str, Any]:
    """Delete an IP host object by name.

    Use when deleting unused IP host objects from the firewall database.

    Args:
        name: Name of the IP host to remove.
        client: Optional SophosFirewallClient instance.

    Returns:
        API response status dictionary.
    """
    close_client = False
    if client is None:
        client = SophosFirewallClient()
        close_client = True

    try:
        res = await client.remove_tag("IPHost", name)
        return cast(Dict[str, Any], res)
    finally:
        if close_client:
            await client.close()


async def sophos_list_ip_host_groups(
    name: Annotated[
        Optional[str],
        Field(description="Optional IP host group name filter."),
    ] = None,
    client: Any = None,
) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    """List IP host groups configured on Sophos Firewall.

    Use when viewing grouped IP host definitions used in rule sets.

    Args:
        name: Optional group name filter.
        client: Optional SophosFirewallClient instance.

    Returns:
        List or dict of IP host groups.
    """
    close_client = False
    if client is None:
        client = SophosFirewallClient()
        close_client = True

    try:
        filter_crit = None
        if name:
            filter_crit = {"key": {"@name": "Name", "@operation": "=", "#text": name}}
        res = await client.get_tag("IPHostGroup", filter_crit)
        return cast(Union[Dict[str, Any], List[Dict[str, Any]]], res)
    finally:
        if close_client:
            await client.close()


async def sophos_create_ip_host_group(
    name: Annotated[
        str,
        Field(description="Unique name for the host group."),
    ],
    host_list: Annotated[
        List[str],
        Field(description="List of IP host object names to include in the group."),
    ],
    client: Any = None,
) -> Dict[str, Any]:
    """Create an IP host group containing multiple IP host objects.

    Use when bundling multiple IP host objects together for unified security policies.

    Args:
        name: Unique name for the host group.
        host_list: List of IP host object names to include in the group.
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
        "HostList": {"Host": host_list},
    }

    try:
        res = await client.set_tag("IPHostGroup", payload)
        return cast(Dict[str, Any], res)
    finally:
        if close_client:
            await client.close()


async def sophos_list_fqdn_hosts(
    name: Annotated[
        Optional[str],
        Field(description="Optional FQDN host object name filter."),
    ] = None,
    client: Any = None,
) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    """List FQDN (Fully Qualified Domain Name) host objects.

    Use when inspecting domain-based network host objects.

    Args:
        name: Optional FQDN host name filter.
        client: Optional SophosFirewallClient instance.

    Returns:
        List or dict of FQDN host objects.
    """
    close_client = False
    if client is None:
        client = SophosFirewallClient()
        close_client = True

    try:
        filter_crit = None
        if name:
            filter_crit = {"key": {"@name": "Name", "@operation": "=", "#text": name}}
        res = await client.get_tag("FQDNHost", filter_crit)
        return cast(Union[Dict[str, Any], List[Dict[str, Any]]], res)
    finally:
        if close_client:
            await client.close()


async def sophos_create_fqdn_host(
    name: Annotated[
        str,
        Field(description="Unique name for the FQDN host object."),
    ],
    fqdn: Annotated[
        str,
        Field(description="Fully qualified domain name (e.g. 'api.example.com')."),
    ],
    client: Any = None,
) -> Dict[str, Any]:
    """Create a new FQDN host object.

    Use when defining domain name target objects for firewall or NAT rules.

    Args:
        name: Unique name for the FQDN host object.
        fqdn: Fully qualified domain name (e.g. 'api.example.com').
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
        "FQDN": fqdn,
    }

    try:
        res = await client.set_tag("FQDNHost", payload)
        return cast(Dict[str, Any], res)
    finally:
        if close_client:
            await client.close()


async def sophos_delete_ip_host_group(
    name: Annotated[
        str,
        Field(description="Name of the IP host group to remove."),
    ],
    client: Any = None,
) -> Dict[str, Any]:
    """Delete an IP host group by name.

    Use when deleting an obsolete host group object from Sophos Firewall.

    Args:
        name: Name of the host group to remove.
        client: Optional SophosFirewallClient instance.

    Returns:
        API response status dictionary.
    """
    close_client = False
    if client is None:
        client = SophosFirewallClient()
        close_client = True

    try:
        res = await client.remove_tag("IPHostGroup", name)
        return cast(Dict[str, Any], res)
    finally:
        if close_client:
            await client.close()


async def sophos_delete_fqdn_host(
    name: Annotated[
        str,
        Field(description="Name of the FQDN host object to remove."),
    ],
    client: Any = None,
) -> Dict[str, Any]:
    """Delete an FQDN host object by name.

    Use when deleting domain-based host objects from Sophos Firewall.

    Args:
        name: Name of the FQDN host object to remove.
        client: Optional SophosFirewallClient instance.

    Returns:
        API response status dictionary.
    """
    close_client = False
    if client is None:
        client = SophosFirewallClient()
        close_client = True

    try:
        res = await client.remove_tag("FQDNHost", name)
        return cast(Dict[str, Any], res)
    finally:
        if close_client:
            await client.close()
