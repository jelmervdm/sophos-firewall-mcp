"""User authentication, local accounts, and live session monitoring tools."""

from typing import Annotated, Any, Dict, List, Optional, Union, cast
from pydantic import Field
from sophos_firewall_mcp.client import SophosFirewallClient


async def sophos_list_users(
    username: Annotated[
        Optional[str],
        Field(description="Optional username filter."),
    ] = None,
    client: Any = None,
) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    """List local user accounts configured on Sophos Firewall.

    Use when browsing local user accounts and group memberships.

    Args:
        username: Optional username filter.
        client: Optional SophosFirewallClient instance.

    Returns:
        List or dict of user accounts.
    """
    close_client = False
    if client is None:
        client = SophosFirewallClient()
        close_client = True

    try:
        filter_crit = None
        if username:
            filter_crit = {"key": {"@name": "Username", "@operation": "=", "#text": username}}
        res = await client.get_tag("User", filter_crit)
        return cast(Union[Dict[str, Any], List[Dict[str, Any]]], res)
    finally:
        if close_client:
            await client.close()


async def sophos_get_user(
    username: Annotated[
        str,
        Field(description="Username of the user account to retrieve."),
    ],
    client: Any = None,
) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    """Retrieve details for a specific local user account.

    Use when inspecting permissions, email, or profile settings for a user.

    Args:
        username: Username of the user account.
        client: Optional SophosFirewallClient instance.

    Returns:
        User account details.
    """
    return await sophos_list_users(username=username, client=client)


async def sophos_create_user(
    username: Annotated[
        str,
        Field(description="Login username for the account."),
    ],
    name: Annotated[
        str,
        Field(description="Full display name of the user."),
    ],
    password: Annotated[
        str,
        Field(description="User login password."),
    ],
    group: Annotated[
        str,
        Field(description="User group name (e.g. 'Open Group' or 'Administrator')."),
    ] = "Open Group",
    email: Annotated[
        Optional[str],
        Field(description="Optional user email address."),
    ] = None,
    client: Any = None,
) -> Dict[str, Any]:
    """Create a new local user account on Sophos Firewall.

    Use when registering new local user accounts for VPN or portal access.

    Args:
        username: Login username for the account.
        name: Full display name of the user.
        password: User login password.
        group: User group name (e.g. 'Open Group' or 'Administrator'). Default is 'Open Group'.
        email: Optional user email address.
        client: Optional SophosFirewallClient instance.

    Returns:
        API response status dictionary.
    """
    close_client = False
    if client is None:
        client = SophosFirewallClient()
        close_client = True

    payload: Dict[str, Any] = {
        "Username": username,
        "Name": name,
        "Password": password,
        "Group": group,
    }
    if email:
        payload["Email"] = email

    try:
        res = await client.set_tag("User", payload)
        return cast(Dict[str, Any], res)
    finally:
        if close_client:
            await client.close()


async def sophos_list_live_users(
    client: Any = None,
) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    """List active logged-in user sessions on Sophos Firewall.

    Use when monitoring live user logins, active session counts, or connected users.

    Args:
        client: Optional SophosFirewallClient instance.

    Returns:
        List or dict of live user sessions.
    """
    close_client = False
    if client is None:
        client = SophosFirewallClient()
        close_client = True

    try:
        res = await client.get_tag("LiveUser")
        return cast(Union[Dict[str, Any], List[Dict[str, Any]]], res)
    finally:
        if close_client:
            await client.close()


async def sophos_delete_user(
    username: Annotated[
        str,
        Field(description="Username of the user account to remove."),
    ],
    client: Any = None,
) -> Dict[str, Any]:
    """Delete a local user account by username.

    Use when removing obsolete or revoked user accounts from Sophos Firewall.

    Args:
        username: Username of the account to delete.
        client: Optional SophosFirewallClient instance.

    Returns:
        API response status dictionary.
    """
    close_client = False
    if client is None:
        client = SophosFirewallClient()
        close_client = True

    try:
        res = await client.remove_tag("User", username)
        return cast(Dict[str, Any], res)
    finally:
        if close_client:
            await client.close()
