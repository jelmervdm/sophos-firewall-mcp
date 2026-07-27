"""System information and status tools for Sophos Firewall."""

from typing import Any, Dict, List, Union, cast
from sophos_firewall_mcp.client import SophosFirewallClient


async def sophos_get_system_info(
    client: Any = None,
) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    """Retrieve system information including appliance model, firmware version, serial number, and uptime.

    Use when inspecting hardware/firmware details and overall system status.

    Args:
        client: Optional SophosFirewallClient instance.

    Returns:
        System information parameters from Sophos Firewall.
    """
    close_client = False
    if client is None:
        client = SophosFirewallClient()
        close_client = True

    try:
        res = await client.get_tag("SystemInformation")
        return cast(Union[Dict[str, Any], List[Dict[str, Any]]], res)
    finally:
        if close_client:
            await client.close()


async def sophos_get_service_status(
    client: Any = None,
) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    """Retrieve current operational status of system services (DNS, DHCP, IPS, Web Protection, AntiVirus).

    Use when monitoring background service health or diagnosing firewall subsystem failures.

    Args:
        client: Optional SophosFirewallClient instance.

    Returns:
        Status details of core firewall services.
    """
    close_client = False
    if client is None:
        client = SophosFirewallClient()
        close_client = True

    try:
        res = await client.get_tag("Services")
        return cast(Union[Dict[str, Any], List[Dict[str, Any]]], res)
    finally:
        if close_client:
            await client.close()


async def sophos_get_interface_list(
    client: Any = None,
) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    """List network interfaces with configuration, IP addresses, network zones, and link state.

    Use when inspecting physical or virtual interface configurations, subnets, and link states.

    Args:
        client: Optional SophosFirewallClient instance.

    Returns:
        List or dict of network interface configurations.
    """
    close_client = False
    if client is None:
        client = SophosFirewallClient()
        close_client = True

    try:
        res = await client.get_tag("Interface")
        return cast(Union[Dict[str, Any], List[Dict[str, Any]]], res)
    finally:
        if close_client:
            await client.close()
