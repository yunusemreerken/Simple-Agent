"""
agents/support_agent.py

Support agent that handles technical questions and general customer-service
interactions. Web search is stubbed — enable when a provider is configured.

Uses the local HuggingFace model via model.loader.get_llm().
"""

from langchain_core.messages import SystemMessage, AIMessage
from state import State
from model.loader import get_llm

# ---------------------------------------------------------------------------
# System prompt
# ---------------------------------------------------------------------------

SUPPORT_SYSTEM_PROMPT = """You are a knowledgeable and empathetic support agent.
Your goals:
1. Understand the user's problem clearly.
2. Provide accurate, step-by-step solutions.
3. Escalate gracefully if the issue is beyond your scope.

Always be polite and concise."""

# ---------------------------------------------------------------------------
# Agent node
# ---------------------------------------------------------------------------


def support_agent(state: State) -> dict:
    """
    Handles support-related conversations and appends an AI reply to messages.

    Web search tool is disabled until a provider (Tavily, SerpAPI, etc.)
    is configured in tools/web_search.py.

    Args:
        state: The current shared graph state.

    Returns:
        A partial state update dict containing the updated messages list.
    """
    llm = get_llm()

    messages = [SystemMessage(content=SUPPORT_SYSTEM_PROMPT)] + state["messages"]

    try:
        response = llm.invoke(messages)
    except Exception as exc:
        error_text = f"Support agent error: {exc}"
        fallback = AIMessage(content=error_text)
        return {"messages": [fallback]}

    return {"messages": [response]}