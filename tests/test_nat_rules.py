"""Unit tests for NAT rule tools."""

import pytest
from sophos_firewall_mcp.tools.nat_rules import (
    sophos_create_nat_rule,
    sophos_delete_nat_rule,
    sophos_get_nat_rule,
    sophos_list_nat_rules,
    sophos_update_nat_rule,
)


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


@pytest.mark.asyncio
async def test_sophos_create_nat_rule(mock_client):
    mock_client.send_request.return_value = {"Status": {"#text": "Configuration applied successfully."}}
    res = await sophos_create_nat_rule(
        name="NAT_Web",
        translated_source="MASQUERADE",
        client=mock_client,
    )
    assert "Status" in res
    mock_client.send_request.assert_called_once()


@pytest.mark.asyncio
async def test_sophos_update_nat_rule(mock_client):
    mock_client.send_request.side_effect = [
        {"NATRule": {"Name": "NAT1", "Status": "Enable"}},
        {"Status": {"#text": "Configuration applied successfully."}},
    ]
    res = await sophos_update_nat_rule(name="NAT1", status="Disable", client=mock_client)
    assert "Status" in res


@pytest.mark.asyncio
async def test_sophos_delete_nat_rule(mock_client):
    mock_client.send_request.return_value = {"Status": {"#text": "Configuration applied successfully."}}
    res = await sophos_delete_nat_rule(name="NAT1", client=mock_client)
    assert "Status" in res
