"""Unit tests for ToolRouter."""

from sophos_firewall_mcp.router import get_router


def test_get_router_disabled(monkeypatch):
    monkeypatch.delenv("USE_ROUTER", raising=False)
    monkeypatch.delenv("TOOL_ROUTING", raising=False)
    assert get_router() is None
