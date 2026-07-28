"""Unit tests for low-level generic raw XML API tool."""

import pytest
from sophos_firewall_mcp.tools.raw_api import sophos_raw_api_request


@pytest.mark.asyncio
async def test_sophos_raw_api_request_get(mock_client):
    mock_client.send_request.return_value = {"Interface": [{"Name": "Port1"}]}
    res = await sophos_raw_api_request(
        operation="Get",
        tag="Interface",
        params=None,
        client=mock_client,
    )
    assert "Interface" in res
    mock_client.send_request.assert_called_once_with(operation="Get", tag="Interface", params=None)


@pytest.mark.asyncio
async def test_sophos_raw_api_request_set(mock_client):
    mock_client.send_request.return_value = {"Status": {"#text": "Configuration applied successfully."}}
    res = await sophos_raw_api_request(
        operation="Set",
        tag="DnsSetting",
        params={"PrimaryDNS": "1.1.1.1"},
        client=mock_client,
    )
    assert "Status" in res
    mock_client.send_request.assert_called_once_with(
        operation="Set", tag="DnsSetting", params={"PrimaryDNS": "1.1.1.1"}
    )
