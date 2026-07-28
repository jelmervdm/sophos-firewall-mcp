"""Unit tests for user authentication tools."""

import pytest
from sophos_firewall_mcp.tools.users_auth import (
    sophos_create_user,
    sophos_delete_user,
    sophos_get_user,
    sophos_list_live_users,
    sophos_list_users,
)


@pytest.mark.asyncio
async def test_sophos_list_users(mock_client):
    mock_client.send_request.return_value = {"User": {"Username": "admin", "Name": "Administrator"}}
    res = await sophos_list_users(client=mock_client)
    assert res["Username"] == "admin"


@pytest.mark.asyncio
async def test_sophos_get_user(mock_client):
    mock_client.send_request.return_value = {"User": {"Username": "jdoe", "Name": "John"}}
    res = await sophos_get_user(username="jdoe", client=mock_client)
    assert res["Username"] == "jdoe"


@pytest.mark.asyncio
async def test_sophos_create_user(mock_client):
    mock_client.send_request.return_value = {"Status": {"#text": "Applied"}}
    res = await sophos_create_user(
        username="jdoe", name="John Doe", password="Password123!", client=mock_client
    )
    assert "Status" in res


@pytest.mark.asyncio
async def test_sophos_delete_user(mock_client):
    mock_client.send_request.return_value = {"Status": {"#text": "Applied"}}
    res = await sophos_delete_user(username="jdoe", client=mock_client)
    assert "Status" in res


@pytest.mark.asyncio
async def test_sophos_list_live_users(mock_client):
    mock_client.send_request.return_value = {"LiveUser": [{"Username": "jdoe"}]}
    res = await sophos_list_live_users(client=mock_client)
    assert len(res) == 1
