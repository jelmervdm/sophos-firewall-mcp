"""Unit tests for SophosFirewallClient and XML payload handling."""

import pytest
import respx
from httpx import Response
from sophos_firewall_mcp.client import (
    SophosAuthenticationError,
    SophosFirewallClient,
    SophosResponseError,
)
from tests.conftest import (
    MOCK_FAILED_LOGIN_XML,
    MOCK_SUCCESS_LOGIN_XML,
    MOCK_SYSTEM_INFO_XML,
)


def test_client_init_defaults(monkeypatch):
    monkeypatch.setenv("SOPHOS_HOST", "10.0.0.1")
    monkeypatch.setenv("SOPHOS_PORT", "8443")
    monkeypatch.setenv("SOPHOS_USERNAME", "sysadmin")
    monkeypatch.setenv("SOPHOS_PASSWORD", "pass123")
    monkeypatch.setenv("SOPHOS_API_VERSION", "2200.1")
    monkeypatch.setenv("SOPHOS_VERIFY_SSL", "true")

    client = SophosFirewallClient()
    assert client.host == "10.0.0.1"
    assert client.port == 8443
    assert client.username == "sysadmin"
    assert client.password == "pass123"
    assert client.api_version == "2200.1"
    assert client.verify_ssl is True
    assert client.endpoint_url == "https://10.0.0.1:8443/webconsole/APIController"


def test_client_fallback_defaults():
    client = SophosFirewallClient()
    assert client.host == "172.16.16.16"
    assert client.port == 4444
    assert client.api_version == "2200.1"


def test_client_custom_api_version(monkeypatch):
    monkeypatch.delenv("SOPHOS_API_VERSION", raising=False)
    client_custom = SophosFirewallClient(api_version="1900.1")
    assert client_custom.api_version == "1900.1"


def test_build_xml_request():
    client = SophosFirewallClient(username="testuser", password="testpass", api_version="2200.1")
    xml_str = client.build_xml_request("Get", "SystemInformation")
    assert 'APIVersion="2200.1"' in xml_str
    assert "<Username>testuser</Username>" in xml_str
    assert "<Password>testpass</Password>" in xml_str
    assert "<Get>" in xml_str
    assert "<SystemInformation>" in xml_str or "<SystemInformation/>" in xml_str


@pytest.mark.asyncio
@respx.mock
async def test_send_request_success():
    client = SophosFirewallClient(host="192.168.1.1", port=4444)
    respx.post("https://192.168.1.1:4444/webconsole/APIController").mock(
        return_value=Response(200, text=MOCK_SYSTEM_INFO_XML)
    )

    res = await client.send_request("Get", "SystemInformation")
    assert res["SystemInformation"]["Model"] == "XGS2100"
    assert res["SystemInformation"]["Version"] == "19.5.3 MR-3"
    await client.close()


@pytest.mark.asyncio
@respx.mock
async def test_send_request_auth_failure():
    client = SophosFirewallClient(host="192.168.1.1", port=4444)
    respx.post("https://192.168.1.1:4444/webconsole/APIController").mock(
        return_value=Response(200, text=MOCK_FAILED_LOGIN_XML)
    )

    with pytest.raises(SophosAuthenticationError):
        await client.send_request("Get", "SystemInformation")
    await client.close()


@pytest.mark.asyncio
@respx.mock
async def test_send_request_response_error():
    client = SophosFirewallClient(host="192.168.1.1", port=4444)
    err_xml = '<Response><Status code="501">Operation failed.</Status></Response>'
    respx.post("https://192.168.1.1:4444/webconsole/APIController").mock(
        return_value=Response(200, text=err_xml)
    )

    with pytest.raises(SophosResponseError):
        await client.send_request("Get", "SystemInformation")
    await client.close()


@pytest.mark.asyncio
@respx.mock
async def test_get_tag():
    client = SophosFirewallClient(host="192.168.1.1", port=4444)
    respx.post("https://192.168.1.1:4444/webconsole/APIController").mock(
        return_value=Response(200, text=MOCK_SYSTEM_INFO_XML)
    )

    res = await client.get_tag("SystemInformation")
    assert res["Model"] == "XGS2100"
    await client.close()


@pytest.mark.asyncio
@respx.mock
async def test_set_tag():
    client = SophosFirewallClient(host="192.168.1.1", port=4444)
    respx.post("https://192.168.1.1:4444/webconsole/APIController").mock(
        return_value=Response(200, text=MOCK_SUCCESS_LOGIN_XML)
    )

    res = await client.set_tag("IPHost", {"Name": "TestHost", "IPAddress": "1.1.1.1"})
    assert res["Status"]["#text"] == "Configuration applied successfully."
    await client.close()


@pytest.mark.asyncio
@respx.mock
async def test_remove_tag():
    client = SophosFirewallClient(host="192.168.1.1", port=4444)
    respx.post("https://192.168.1.1:4444/webconsole/APIController").mock(
        return_value=Response(200, text=MOCK_SUCCESS_LOGIN_XML)
    )

    res = await client.remove_tag("IPHost", "TestHost")
    assert "Response" in res or "Status" in res
    await client.close()
