"""Unit tests for services tools."""

import pytest
from sophos_firewall_mcp.tools.services_objects import (
    sophos_create_service,
    sophos_create_service_group,
    sophos_delete_service,
    sophos_delete_service_group,
    sophos_get_service,
    sophos_list_service_groups,
    sophos_list_services,
)


@pytest.mark.asyncio
async def test_sophos_list_services(mock_client):
    mock_client.send_request.return_value = {"Services": {"Name": "HTTP", "Type": "TCP/UDP"}}
    res = await sophos_list_services(client=mock_client)
    assert res["Name"] == "HTTP"


@pytest.mark.asyncio
async def test_sophos_get_service(mock_client):
    mock_client.send_request.return_value = {"Services": {"Name": "HTTP", "Type": "TCP/UDP"}}
    res = await sophos_get_service(name="HTTP", client=mock_client)
    assert res["Name"] == "HTTP"


@pytest.mark.asyncio
async def test_sophos_create_service(mock_client):
    mock_client.send_request.return_value = {"Status": {"#text": "Applied"}}
    res = await sophos_create_service(
        name="Custom_8080", protocol="TCP", destination_port="8080", client=mock_client
    )
    assert "Status" in res


@pytest.mark.asyncio
async def test_sophos_delete_service(mock_client):
    mock_client.send_request.return_value = {"Status": {"#text": "Applied"}}
    res = await sophos_delete_service(name="Custom_8080", client=mock_client)
    assert "Status" in res


@pytest.mark.asyncio
async def test_sophos_list_service_groups(mock_client):
    mock_client.send_request.return_value = {"ServiceGroup": {"Name": "Group1"}}
    res = await sophos_list_service_groups(client=mock_client)
    assert res["Name"] == "Group1"


@pytest.mark.asyncio
async def test_sophos_create_service_group(mock_client):
    mock_client.send_request.return_value = {"Status": {"#text": "Applied"}}
    res = await sophos_create_service_group(
        name="WebServices", service_list=["HTTP", "HTTPS"], client=mock_client
    )
    assert "Status" in res


@pytest.mark.asyncio
async def test_sophos_delete_service_group(mock_client):
    mock_client.send_request.return_value = {"Status": {"#text": "Applied"}}
    res = await sophos_delete_service_group(name="WebServices", client=mock_client)
    assert "Status" in res
