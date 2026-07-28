"""Low-level generic XML API request tool for Sophos Firewall."""

from typing import Annotated, Any, Dict, Optional, Union, cast
from pydantic import Field
from sophos_firewall_mcp.client import SophosFirewallClient


async def sophos_raw_api_request(
    operation: Annotated[
        str,
        Field(description="SFOS XML API operation tag: 'Get', 'Set', or 'Remove'."),
    ],
    tag: Annotated[
        str,
        Field(description="Target Sophos XML entity tag (e.g. 'FirewallRule', 'IPHost', 'Interface', 'DNS', 'DHCP')."),
    ],
    params: Annotated[
        Optional[Dict[str, Any]],
        Field(description="Optional child parameters, payload dictionary, or XML search filter criteria."),
    ] = None,
    client: Any = None,
) -> Union[Dict[str, Any], list]:
    """Execute a low-level, generic Sophos Firewall XML API operation.

    Use when executing custom or low-level SFOS XML API calls for tags or configuration settings not supported by dedicated high-level tools.

    Args:
        operation: API operation type ('Get', 'Set', or 'Remove').
        tag: Target Sophos XML entity tag.
        params: Optional payload dictionary or search filter criteria.
        client: Optional SophosFirewallClient instance.

    Returns:
        Parsed API response dictionary or object list.
    """
    close_client = False
    if client is None:
        client = SophosFirewallClient()
        close_client = True

    try:
        res = await client.send_request(operation=operation, tag=tag, params=params)
        return cast(Union[Dict[str, Any], list], res)
    finally:
        if close_client:
            await client.close()
