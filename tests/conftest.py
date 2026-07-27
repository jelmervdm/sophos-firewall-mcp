"""Shared fixtures and XML response mocks for sophos-firewall-mcp tests."""

import pytest
from unittest.mock import AsyncMock
from sophos_firewall_mcp.client import SophosFirewallClient

# Mock XML Responses from SFOS XML API
MOCK_SUCCESS_LOGIN_XML = """<?xml version="1.0" encoding="UTF-8"?>
<Response APIVersion="1900.1">
    <Login>
        <status>Authentication Successful</status>
    </Login>
    <Status code="200">Configuration applied successfully.</Status>
</Response>
"""

MOCK_FAILED_LOGIN_XML = """<?xml version="1.0" encoding="UTF-8"?>
<Response APIVersion="1900.1">
    <Login>
        <status>Authentication Failed</status>
    </Login>
</Response>
"""

MOCK_SYSTEM_INFO_XML = """<?xml version="1.0" encoding="UTF-8"?>
<Response APIVersion="1900.1">
    <Login>
        <status>Authentication Successful</status>
    </Login>
    <SystemInformation>
        <Model>XGS2100</Model>
        <Version>19.5.3 MR-3</Version>
        <SerialNumber>C12345678901</SerialNumber>
        <Uptime>15 days, 4 hours</Uptime>
        <CpuUsage>12%</CpuUsage>
        <MemoryUsage>45%</MemoryUsage>
    </SystemInformation>
    <Status code="200">Configuration applied successfully.</Status>
</Response>
"""

MOCK_INTERFACE_XML = """<?xml version="1.0" encoding="UTF-8"?>
<Response APIVersion="1900.1">
    <Login>
        <status>Authentication Successful</status>
    </Login>
    <Interface>
        <Name>Port1</Name>
        <Hardware>Ethernet</Hardware>
        <Zone>LAN</Zone>
        <IPAddress>192.168.1.1</IPAddress>
        <Netmask>255.255.255.0</Netmask>
        <LinkStatus>Connected</LinkStatus>
    </Interface>
    <Status code="200">Configuration applied successfully.</Status>
</Response>
"""

MOCK_FIREWALL_RULE_XML = """<?xml version="1.0" encoding="UTF-8"?>
<Response APIVersion="1900.1">
    <Login>
        <status>Authentication Successful</status>
    </Login>
    <FirewallRule>
        <Name>Allow_LAN_to_WAN</Name>
        <Status>Enable</Status>
        <NetworkPolicy>
            <Action>Accept</Action>
            <SourceZones><Zone>LAN</Zone></SourceZones>
            <DestinationZones><Zone>WAN</Zone></DestinationZones>
            <SourceNetworks><Network>Any</Network></SourceNetworks>
            <DestinationNetworks><Network>Any</Network></DestinationNetworks>
            <Services><Service>Any</Service></Services>
        </NetworkPolicy>
    </FirewallRule>
    <Status code="200">Configuration applied successfully.</Status>
</Response>
"""

MOCK_IP_HOST_XML = """<?xml version="1.0" encoding="UTF-8"?>
<Response APIVersion="1900.1">
    <Login>
        <status>Authentication Successful</status>
    </Login>
    <IPHost>
        <Name>Server_Web01</Name>
        <IPFamily>IPv4</IPFamily>
        <HostType>IP</HostType>
        <IPAddress>192.168.1.50</IPAddress>
    </IPHost>
    <Status code="200">Configuration applied successfully.</Status>
</Response>
"""

MOCK_SERVICES_XML = """<?xml version="1.0" encoding="UTF-8"?>
<Response APIVersion="1900.1">
    <Login>
        <status>Authentication Successful</status>
    </Login>
    <Services>
        <Name>Custom_HTTP_8080</Name>
        <Type>TCP/UDP</Type>
        <ServiceDetail>
            <Protocol>TCP</Protocol>
            <SourcePort>1:65535</SourcePort>
            <DestinationPort>8080</DestinationPort>
        </ServiceDetail>
    </Services>
    <Status code="200">Configuration applied successfully.</Status>
</Response>
"""

MOCK_NAT_RULE_XML = """<?xml version="1.0" encoding="UTF-8"?>
<Response APIVersion="1900.1">
    <Login>
        <status>Authentication Successful</status>
    </Login>
    <NATRule>
        <Name>DNAT_Web_Server</Name>
        <Status>Enable</Status>
        <OriginalService>HTTP</OriginalService>
        <TranslatedService>HTTP</TranslatedService>
    </NATRule>
    <Status code="200">Configuration applied successfully.</Status>
</Response>
"""

MOCK_USER_XML = """<?xml version="1.0" encoding="UTF-8"?>
<Response APIVersion="1900.1">
    <Login>
        <status>Authentication Successful</status>
    </Login>
    <User>
        <Username>jdoe</Username>
        <Name>John Doe</Name>
        <Group>Open Group</Group>
        <Email>jdoe@example.com</Email>
    </User>
    <Status code="200">Configuration applied successfully.</Status>
</Response>
"""

MOCK_VPN_XML = """<?xml version="1.0" encoding="UTF-8"?>
<Response APIVersion="1900.1">
    <Login>
        <status>Authentication Successful</status>
    </Login>
    <IPsecVpn>
        <Name>Branch_Office_Tunnel</Name>
        <Status>Active</Status>
        <LocalGateway>1.2.3.4</LocalGateway>
        <RemoteGateway>5.6.7.8</RemoteGateway>
    </IPsecVpn>
    <Status code="200">Configuration applied successfully.</Status>
</Response>
"""


@pytest.fixture
def mock_client():
    """Return a mock SophosFirewallClient with AsyncMock responses."""
    client = SophosFirewallClient(
        host="192.168.1.1",
        port=4444,
        username="admin",
        password="secretpassword",
        verify_ssl=False,
    )
    client.send_request = AsyncMock()
    return client
