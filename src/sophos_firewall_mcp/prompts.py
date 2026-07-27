"""FastMCP prompt templates for Sophos Firewall diagnostics and security tasks."""

from mcp.server.fastmcp import FastMCP


def register(mcp: FastMCP) -> None:
    """Register diagnostic and security audit prompt templates."""

    @mcp.prompt()
    def audit_firewall_rules(focus_zone: str = "WAN") -> str:
        """Prompt template for conducting a security audit of firewall rules.

        Args:
            focus_zone: Network zone to audit (e.g. 'WAN', 'LAN', 'DMZ'). Default is 'WAN'.
        """
        return f"""You are a certified Sophos Network Security Auditor.
Your task is to conduct a thorough security audit of firewall rules facing the '{focus_zone}' zone.

Steps to perform:
1. Call `sophos_list_firewall_rules()` to inspect all active security policies.
2. Identify rules with permissive source/destination settings ('Any' -> 'Any').
3. Verify that dangerous protocols (Telnet, unencrypted HTTP, SMB) are properly blocked or restricted.
4. Flag disabled rules or duplicate policies that may cause security vulnerabilities.
5. Provide actionable security recommendations in structured Markdown format.
"""

    @mcp.prompt()
    def troubleshoot_connectivity(source_ip: str, destination_ip: str) -> str:
        """Prompt template for troubleshooting network connectivity issues between hosts.

        Args:
            source_ip: IP address or host name attempting connection.
            destination_ip: Target destination IP address or service.
        """
        return f"""You are a Sophos Firewall Network Administrator troubleshooting traffic flow.

Source IP: {source_ip}
Destination IP: {destination_ip}

Instructions:
1. Call `sophos_get_interface_list()` to verify network interface configurations and subnets.
2. Call `sophos_list_ip_hosts()` to locate corresponding IP host objects.
3. Call `sophos_list_firewall_rules()` to trace active policy matches between source and destination.
4. Check NAT rules using `sophos_list_nat_rules()` to verify translation policies.
5. Summarize potential root causes (e.g. dropped by policy, missing NAT rule, disabled service).
"""
