"""
tools/web_search.py

Provides a LangChain Tool wrapper around the Tavily search backend.
Agents can call this tool to retrieve up-to-date information from the internet.

Setup:
    pip install langchain-tavily
    Add TAVILY_API_KEY to your .env file (free tier: tavily.com)
"""

import os
from langchain_core.tools import tool

# ---------------------------------------------------------------------------
# Provider check
# ---------------------------------------------------------------------------

_TAVILY_KEY = os.getenv("TAVILY_API_KEY")
_tavily_search = None

if _TAVILY_KEY:
    try:
        from langchain_tavily import TavilySearch
        _tavily_search = TavilySearch(max_results=3)
    except ImportError:
        pass  # langchain-tavily not installed — tool will return helpful message

# ---------------------------------------------------------------------------
# Tool definition
# ---------------------------------------------------------------------------


@tool
def web_search_tool(query: str) -> str:
    """
    Search the web for current information about a given query.

    Args:
        query: A natural-language search query string.

    Returns:
        A plain-text summary of the top search results.
    """
    if _tavily_search is None:
        return (
            "Web search is not available. "
            "Add TAVILY_API_KEY to your .env file and run: "
            "pip install langchain-tavily"
        )

    try:
        results = _tavily_search.invoke(query)
        if isinstance(results, list):
            return "\n\n".join(
                r.get("content", "") for r in results if r.get("content")
            )
        return str(results)
    except Exception as exc:
        return f"Search failed: {exc}"