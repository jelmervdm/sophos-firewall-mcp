"""Semantic tool router using FastEmbed embeddings."""

import logging
import os
from typing import Any, List, Optional, Tuple

logger = logging.getLogger(__name__)


class ToolRouter:
    """Routes user queries to relevant Sophos Firewall tools via embedding similarity."""

    def __init__(self, model_name: str = "BAAI/bge-small-en-v1.5") -> None:
        from fastembed import TextEmbedding

        logger.info("Loading embedding model %s ...", model_name)
        cache_dir = os.environ.get("FASTEMBED_CACHE_DIR")
        self._model = TextEmbedding(model_name, cache_dir=cache_dir)
        self._tool_names: List[str] = []
        self._tool_embeddings: Optional[Any] = None
        logger.info("Embedding model loaded")

    def index(self, tools: List[Tuple[str, str]]) -> None:
        """Build the tool embedding index.

        Args:
            tools: List of (name, description) pairs for registered tools.
        """
        import numpy as np

        self._tool_names = [name for name, _ in tools]
        texts = [f"{name}: {desc}" for name, desc in tools]
        self._tool_embeddings = np.array(list(self._model.embed(texts)))
        logger.info("Indexed %d tool embeddings", len(self._tool_names))

    def search(self, query: str, top_k: int = 15) -> List[str]:
        """Return the top-k most relevant tool names for query.

        Args:
            query: Natural-language description of desired action.
            top_k: Number of tool names to return.

        Returns:
            List of tool names ordered by relevance.
        """
        import numpy as np

        if self._tool_embeddings is None or len(self._tool_names) == 0:
            return []

        query_vec = np.array(list(self._model.embed([query])))[0]
        scores = self._tool_embeddings @ query_vec
        top_indices = np.argsort(scores)[::-1][:top_k]
        return [self._tool_names[i] for i in top_indices]


_router: Optional[ToolRouter] = None


def get_router() -> Optional[ToolRouter]:
    """Return the singleton router if TOOL_ROUTING=true or USE_ROUTER=true."""
    global _router
    if _router is not None:
        return _router

    enabled = os.environ.get("TOOL_ROUTING", os.environ.get("USE_ROUTER", "")).lower() in (
        "1",
        "true",
        "yes",
    )
    if not enabled:
        return None

    try:
        _router = ToolRouter()
        return _router
    except (ImportError, ModuleNotFoundError) as exc:
        logger.warning(
            "Tool routing is enabled (USE_ROUTER=true), but required optional dependencies "
            "are missing (%s). Install with `pip install sophos-firewall-mcp-server[router]` "
            "or `pip install fastembed numpy`. Disabling tool router.",
            exc,
        )
        return None
