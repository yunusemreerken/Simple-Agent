"""
tools/__init__.py

Exposes all LangChain-compatible tool objects for use by agents.
"""

from tools.web_search import web_search_tool

__all__ = ["web_search_tool"]