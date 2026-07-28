"""Unit tests for host objects tools."""

import pytest
from sophos_firewall_mcp.tools.hosts_objects import (
    sophos_create_fqdn_host,
    sophos_create_ip_host,
    sophos_create_ip_host_group,
    sophos_delete_fqdn_host,
    sophos_delete_ip_host,
    sophos_delete_ip_host_group,
    sophos_get_ip_host,
    sophos_list_fqdn_hosts,
    sophos_list_ip_host_groups,
    sophos_list_ip_hosts,
)


@pytest.mark.asyncio
async def test_sophos_list_ip_hosts(mock_client):
    mock_client.send_request.return_value = {"IPHost": {"Name": "Host1", "IPAddress": "1.1.1.1"}}
    res = await sophos_list_ip_hosts(client=mock_client)
    assert res["Name"] == "Host1"


@pytest.mark.asyncio
async def test_sophos_get_ip_host(mock_client):
    mock_client.send_request.return_value = {"IPHost": {"Name": "Host1", "IPAddress": "1.1.1.1"}}
    res = await sophos_get_ip_host(name="Host1", client=mock_client)
    assert res["Name"] == "Host1"


@pytest.mark.asyncio
async def test_sophos_create_ip_host(mock_client):
    mock_client.send_request.return_value = {"Status": {"#text": "Applied"}}
    res = await sophos_create_ip_host(name="Host1", ip_address="192.168.1.10", client=mock_client)
    assert "Status" in res


@pytest.mark.asyncio
async def test_sophos_delete_ip_host(mock_client):
    mock_client.send_request.return_value = {"Status": {"#text": "Applied"}}
    res = await sophos_delete_ip_host(name="Host1", client=mock_client)
    assert "Status" in res


@pytest.mark.asyncio
async def test_sophos_list_ip_host_groups(mock_client):
    mock_client.send_request.return_value = {"IPHostGroup": {"Name": "Group1"}}
    res = await sophos_list_ip_host_groups(client=mock_client)
    assert res["Name"] == "Group1"


@pytest.mark.asyncio
async def test_sophos_create_ip_host_group(mock_client):
    mock_client.send_request.return_value = {"Status": {"#text": "Applied"}}
    res = await sophos_create_ip_host_group(name="Group1", host_list=["Host1", "Host2"], client=mock_client)
    assert "Status" in res


@pytest.mark.asyncio
async def test_sophos_delete_ip_host_group(mock_client):
    mock_client.send_request.return_value = {"Status": {"#text": "Applied"}}
    res = await sophos_delete_ip_host_group(name="Group1", client=mock_client)
    assert "Status" in res


@pytest.mark.asyncio
async def test_sophos_list_fqdn_hosts(mock_client):
    mock_client.send_request.return_value = {"FQDNHost": {"Name": "FQDN1"}}
    res = await sophos_list_fqdn_hosts(client=mock_client)
    assert res["Name"] == "FQDN1"


@pytest.mark.asyncio
async def test_sophos_create_fqdn_host(mock_client):
    mock_client.send_request.return_value = {"Status": {"#text": "Applied"}}
    res = await sophos_create_fqdn_host(name="FQDN1", fqdn="test.example.com", client=mock_client)
    assert "Status" in res


@pytest.mark.asyncio
async def test_sophos_delete_fqdn_host(mock_client):
    mock_client.send_request.return_value = {"Status": {"#text": "Applied"}}
    res = await sophos_delete_fqdn_host(name="FQDN1", client=mock_client)
    assert "Status" in res
