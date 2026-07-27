"""Unit tests for ToolRouter."""

from sophos_firewall_mcp.router import get_router


def test_get_router_disabled(monkeypatch):
    monkeypatch.delenv("USE_ROUTER", raising=False)
    monkeypatch.delenv("TOOL_ROUTING", raising=False)
    assert get_router() is None


def test_get_router_missing_fastembed(monkeypatch):
    monkeypatch.setenv("USE_ROUTER", "true")

    def mock_init(self, *args, **kwargs):
        raise ModuleNotFoundError("No module named 'fastembed'")

    from sophos_firewall_mcp.router import ToolRouter
    import sophos_firewall_mcp.router as router_mod

    router_mod._router = None
    monkeypatch.setattr(ToolRouter, "__init__", mock_init)

    assert get_router() is None
