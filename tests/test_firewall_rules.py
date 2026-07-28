"""Unit tests for firewall rule tools."""

import pytest
from sophos_firewall_mcp.tools.firewall_rules import (
    sophos_create_firewall_rule,
    sophos_delete_firewall_rule,
    sophos_get_firewall_rule,
    sophos_list_firewall_rules,
    sophos_update_firewall_rule,
    sophos_update_firewall_rule_status,
)


@pytest.mark.asyncio
async def test_sophos_list_firewall_rules(mock_client):
    mock_client.send_request.return_value = {
        "FirewallRule": [{"Name": "Rule1"}, {"Name": "Rule2"}]
    }
    res = await sophos_list_firewall_rules(client=mock_client)
    assert len(res) == 2
    assert res[0]["Name"] == "Rule1"


@pytest.mark.asyncio
async def test_sophos_get_firewall_rule(mock_client):
    mock_client.send_request.return_value = {
        "FirewallRule": {"Name": "Rule1", "Status": "Enable"}
    }
    res = await sophos_get_firewall_rule(name="Rule1", client=mock_client)
    assert res["Name"] == "Rule1"


@pytest.mark.asyncio
async def test_sophos_create_firewall_rule(mock_client):
    mock_client.send_request.return_value = {
        "Status": {"#text": "Configuration applied successfully."}
    }
    res = await sophos_create_firewall_rule(
        name="Allow_Web",
        action="Accept",
        source_zones=["LAN"],
        destination_zones=["WAN"],
        client=mock_client,
    )
    assert "Status" in res
    mock_client.send_request.assert_called_once()
    args, kwargs = mock_client.send_request.call_args
    assert args[0] == "Set"
    assert args[1] == "FirewallRule"
    payload = args[2]
    assert payload["Name"] == "Allow_Web"
    assert payload["PolicyType"] == "Network"
    assert payload["IPFamily"] == "IPv4"


@pytest.mark.asyncio
async def test_sophos_update_firewall_rule(mock_client):
    mock_client.send_request.side_effect = [
        # Response for GET
        {"FirewallRule": {"Name": "Rule1", "Status": "Enable", "NetworkPolicy": {"Action": "Accept"}}},
        # Response for SET
        {"Status": {"#text": "Configuration applied successfully."}},
    ]
    res = await sophos_update_firewall_rule(
        name="Rule1",
        log_traffic="Enable",
        action="Drop",
        client=mock_client,
    )
    assert "Status" in res
    assert mock_client.send_request.call_count == 2
    set_args, _ = mock_client.send_request.call_args_list[1]
    assert set_args[0] == "Set"
    assert set_args[1] == "FirewallRule"
    updated_payload = set_args[2]
    assert updated_payload["NetworkPolicy"]["LogTraffic"] == "Enable"
    assert updated_payload["NetworkPolicy"]["Action"] == "Drop"
    assert updated_payload["PolicyType"] == "Network"


@pytest.mark.asyncio
async def test_sophos_update_firewall_rule_not_found(mock_client):
    mock_client.send_request.return_value = {"FirewallRule": []}
    res = await sophos_update_firewall_rule(name="NonExistent", log_traffic="Enable", client=mock_client)
    assert "error" in res


@pytest.mark.asyncio
async def test_sophos_update_firewall_rule_status(mock_client):
    mock_client.send_request.return_value = {
        "Status": {"#text": "Configuration applied successfully."}
    }
    res = await sophos_update_firewall_rule_status(name="Rule1", status="Disable", client=mock_client)
    assert "Status" in res


@pytest.mark.asyncio
async def test_sophos_delete_firewall_rule(mock_client):
    mock_client.send_request.return_value = {
        "Status": {"#text": "Configuration applied successfully."}
    }
    res = await sophos_delete_firewall_rule(name="Rule1", client=mock_client)
    assert "Status" in res
    mock_client.send_request.assert_called_once_with("Remove", "FirewallRule", {"Name": "Rule1"})
