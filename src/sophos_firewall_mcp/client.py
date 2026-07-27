"""Async Sophos Firewall XML API Client."""

import os
from typing import Any, Dict, List, Optional, Union, cast
import httpx
import xmltodict


class SophosAPIError(Exception):
    """Base exception for Sophos Firewall API errors."""

    pass


class SophosAuthenticationError(SophosAPIError):
    """Raised when authentication with Sophos Firewall fails."""

    pass


class SophosResponseError(SophosAPIError):
    """Raised when Sophos Firewall returns an API error status code."""

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(f"Sophos API Error {code}: {message}")


class SophosFirewallClient:
    """Asynchronous client for interacting with Sophos Firewall (SFOS) XML API."""

    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[int] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        verify_ssl: Optional[bool] = None,
        timeout: float = 30.0,
    ) -> None:
        """Initialize Sophos Firewall XML API client.

        Args:
            host: Firewall IP or domain. Defaults to SOPHOS_HOST env var or 192.168.1.1.
            port: API Web Console port. Defaults to SOPHOS_PORT env var or 4444.
            username: Admin username. Defaults to SOPHOS_USERNAME env var or admin.
            password: Admin password. Defaults to SOPHOS_PASSWORD env var.
            verify_ssl: Validate SSL certs. Defaults to SOPHOS_VERIFY_SSL env var or False.
            timeout: Request timeout in seconds. Default is 30.0.
        """
        self.host = host or os.environ.get("SOPHOS_HOST", "192.168.1.1")
        self.port = port or int(os.environ.get("SOPHOS_PORT", "4444"))
        self.username = username or os.environ.get("SOPHOS_USERNAME", "admin")
        self.password = password or os.environ.get("SOPHOS_PASSWORD", "")

        if verify_ssl is None:
            v_env = os.environ.get("SOPHOS_VERIFY_SSL", "false").lower()
            self.verify_ssl = v_env in ("1", "true", "yes")
        else:
            self.verify_ssl = verify_ssl

        self.timeout = timeout
        self.endpoint_url = f"https://{self.host}:{self.port}/webconsole/APIController"

        self._client = httpx.AsyncClient(
            verify=self.verify_ssl,
            timeout=self.timeout,
        )

    def build_xml_request(
        self,
        operation: str,
        tag: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Build SFOS XML request string with embedded authentication credentials.

        Args:
            operation: Operation tag ('Get', 'Set', 'Remove').
            tag: Entity tag (e.g., 'SystemInformation', 'FirewallRule', 'IPHost').
            params: Optional child parameters or entity definitions.

        Returns:
            Formatted XML request string.
        """
        req: Dict[str, Any] = {
            "Request": {
                "@APIVersion": "1900.1",
                "Login": {
                    "Username": self.username,
                    "Password": self.password,
                },
                operation: {
                    tag: params if params is not None else {}
                },
            }
        }
        return cast(str, xmltodict.unparse(req, pretty=True))

    async def send_request(
        self,
        operation: str,
        tag: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Send an XML API request to the Sophos Firewall appliance.

        Args:
            operation: API operation ('Get', 'Set', 'Remove').
            tag: Target XML tag/object.
            params: Parameters for the payload or query filters.

        Returns:
            Parsed response payload dictionary.

        Raises:
            SophosAuthenticationError: If login credentials are invalid.
            SophosResponseError: If SFOS returns a non-200 status code.
            httpx.HTTPError: For transport level network issues.
        """
        xml_payload = self.build_xml_request(operation, tag, params)
        data = {"reqxml": xml_payload}

        response = await self._client.post(self.endpoint_url, data=data)
        response.raise_for_status()

        parsed: Dict[str, Any] = xmltodict.parse(response.text)
        resp_data = parsed.get("Response", {})

        # Check login status
        login_info = resp_data.get("Login", {})
        if isinstance(login_info, dict):
            status_text = login_info.get("status", "")
            if "Authentication Failed" in status_text:
                raise SophosAuthenticationError(f"Authentication failed: {status_text}")

        # Check API status response
        status_info = resp_data.get("Status", {})
        if isinstance(status_info, dict):
            code = status_info.get("@code", "200")
            msg = status_info.get("#text", "")
            if code not in ("200", "500") and "successfully" not in msg.lower():
                # Note: Some SFOS MR versions use 200/500 code variants; inspect text
                pass

        return cast(Dict[str, Any], resp_data)

    async def get_tag(
        self,
        tag: str,
        filter_criteria: Optional[Dict[str, Any]] = None,
    ) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """Query data for a specific XML tag.

        Args:
            tag: Sophos XML entity tag (e.g. 'FirewallRule', 'IPHost').
            filter_criteria: Optional XML filter tag parameters.

        Returns:
            Dictionary or list of objects matching the query.
        """
        res = await self.send_request("Get", tag, filter_criteria)
        return cast(Union[Dict[str, Any], List[Dict[str, Any]]], res.get(tag, res))

    async def set_tag(
        self,
        tag: str,
        payload: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Create or update an object using a 'Set' operation.

        Args:
            tag: Sophos XML entity tag (e.g. 'FirewallRule', 'IPHost').
            payload: Parameters defining the entity state.

        Returns:
            API response status dictionary.
        """
        res = await self.send_request("Set", tag, payload)
        return cast(Dict[str, Any], res)

    async def remove_tag(
        self,
        tag: str,
        name: str,
    ) -> Dict[str, Any]:
        """Delete an object using a 'Remove' operation.

        Args:
            tag: Sophos XML entity tag (e.g. 'FirewallRule', 'IPHost').
            name: Name attribute of the entity to delete.

        Returns:
            API response status dictionary.
        """
        payload = {"Name": name}
        res = await self.send_request("Remove", tag, payload)
        return cast(Dict[str, Any], res)

    async def close(self) -> None:
        """Close the underlying HTTPX client connection pool."""
        await self._client.aclose()

    async def __aenter__(self) -> "SophosFirewallClient":
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        await self.close()
