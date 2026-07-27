"""Unit tests for NAT rule tools."""

import pytest
from sophos_firewall_mcp.tools.nat_rules import sophos_get_nat_rule, sophos_list_nat_rules


@pytest.mark.asyncio
async def test_sophos_list_nat_rules(mock_client):
    mock_client.send_request.return_value = {"NATRule": {"Name": "NAT1", "OriginalService": "HTTP"}}
    res = await sophos_list_nat_rules(client=mock_client)
    assert res["Name"] == "NAT1"


@pytest.mark.asyncio
async def test_sophos_get_nat_rule(mock_client):
    mock_client.send_request.return_value = {"NATRule": {"Name": "NAT1", "OriginalService": "HTTP"}}
    res = await sophos_get_nat_rule(name="NAT1", client=mock_client)
    assert res["Name"] == "NAT1"
