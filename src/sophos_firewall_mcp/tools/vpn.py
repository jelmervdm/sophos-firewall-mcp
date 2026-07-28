"""IPsec site-to-site and SSL VPN management tools."""

from typing import Any, Dict, List, Optional, Union, cast
from sophos_firewall_mcp.client import SophosFirewallClient


async def sophos_list_ipsec_vpns(
    client: Any = None,
) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    """List IPsec site-to-site VPN connection configurations and status.

    Use when inspecting site-to-site IPsec tunnel states and gateway parameters.

    Args:
        client: Optional SophosFirewallClient instance.

    Returns:
        List or dict of IPsec VPN connections.
    """
    close_client = False
    if client is None:
        client = SophosFirewallClient()
        close_client = True

    try:
        res = await client.get_tag("IPsecVpn")
        return cast(Union[Dict[str, Any], List[Dict[str, Any]]], res)
    finally:
        if close_client:
            await client.close()


async def sophos_list_sslvpn_policies(
    client: Any = None,
) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    """List SSL VPN remote access policies configured on Sophos Firewall.

    Use when viewing user access policies, SSL VPN IP pools, and permitted networks.

    Args:
        client: Optional SophosFirewallClient instance.

    Returns:
        List or dict of SSL VPN remote access policies.
    """
    close_client = False
    if client is None:
        client = SophosFirewallClient()
        close_client = True

    try:
        res = await client.get_tag("SSLVPNPolicy")
        return cast(Union[Dict[str, Any], List[Dict[str, Any]]], res)
    finally:
        if close_client:
            await client.close()
