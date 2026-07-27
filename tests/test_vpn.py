"""Unit tests for VPN tools."""

import pytest
from sophos_firewall_mcp.tools.vpn import sophos_list_ipsec_vpns, sophos_list_sslvpn_policies


@pytest.mark.asyncio
async def test_sophos_list_ipsec_vpns(mock_client):
    mock_client.send_request.return_value = {"IPsecVpn": {"Name": "Tunnel1", "Status": "Active"}}
    res = await sophos_list_ipsec_vpns(client=mock_client)
    assert res["Name"] == "Tunnel1"


@pytest.mark.asyncio
async def test_sophos_list_sslvpn_policies(mock_client):
    mock_client.send_request.return_value = {"SSLVPNPolicy": {"Name": "RemoteAccess"}}
    res = await sophos_list_sslvpn_policies(client=mock_client)
    assert res["Name"] == "RemoteAccess"
