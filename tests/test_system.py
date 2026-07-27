"""Unit tests for system tools."""

import pytest
from sophos_firewall_mcp.tools.system import (
    sophos_get_interface_list,
    sophos_get_service_status,
    sophos_get_system_info,
)


@pytest.mark.asyncio
async def test_sophos_get_system_info(mock_client):
    mock_client.send_request.return_value = {
        "SystemInformation": {
            "Model": "XGS2100",
            "Version": "19.5.3",
        }
    }
    res = await sophos_get_system_info(client=mock_client)
    assert res["Model"] == "XGS2100"
    mock_client.send_request.assert_called_once_with("Get", "SystemInformation", None)


@pytest.mark.asyncio
async def test_sophos_get_service_status(mock_client):
    mock_client.send_request.return_value = {
        "Services": {"DNS": "Running", "IPS": "Running"}
    }
    res = await sophos_get_service_status(client=mock_client)
    assert res["DNS"] == "Running"
    mock_client.send_request.assert_called_once_with("Get", "Services", None)


@pytest.mark.asyncio
async def test_sophos_get_interface_list(mock_client):
    mock_client.send_request.return_value = {
        "Interface": {"Name": "Port1", "Zone": "LAN"}
    }
    res = await sophos_get_interface_list(client=mock_client)
    assert res["Name"] == "Port1"
    mock_client.send_request.assert_called_once_with("Get", "Interface", None)
