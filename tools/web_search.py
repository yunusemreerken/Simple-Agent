
"""
tools/web_search.py

Provides a LangChain Tool wrapper around a web-search backend.
Agents can call this tool to retrieve up-to-date information from the internet.
"""

from langchain_core.tools import tool

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
    # TODO: integrate a real search provider (e.g. Tavily, SerpAPI, Brave Search)
    # Example with Tavily:
    #   from langchain_community.tools.tavily_search import TavilySearchResults
    #   search = TavilySearchResults(max_results=3)
    #   results = search.invoke(query)
    #   return "\n".join(r["content"] for r in results)

    raise NotImplementedError(
        "web_search_tool is not yet implemented. "
        "Configure a search provider and replace this placeholder."
    )