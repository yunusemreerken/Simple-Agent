"""
agents/support_agent.py

Support agent that handles technical questions, bug reports, and general
customer-service interactions. Has access to the web_search tool.
"""

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage, AIMessage
from state import State
from tools.web_search import web_search_tool

# ---------------------------------------------------------------------------
# LLM initialisation
# ---------------------------------------------------------------------------

_llm = ChatAnthropic(model="claude-opus-4-5", temperature=0).bind_tools(
    [web_search_tool]
)

# ---------------------------------------------------------------------------
# System prompt
# ---------------------------------------------------------------------------

SUPPORT_SYSTEM_PROMPT = """You are a knowledgeable and empathetic customer support agent.
Your goals:
1. Understand the user's problem clearly.
2. Provide accurate, step-by-step solutions.
3. Use the web_search tool when you need up-to-date information.
4. Escalate gracefully if the issue is beyond your scope.

Always be polite and concise."""

# ---------------------------------------------------------------------------
# Agent node
# ---------------------------------------------------------------------------


def support_agent(state: State) -> dict:
    """
    Handles support-related conversations and appends an AI reply to messages.

    Args:
        state: The current shared graph state.

    Returns:
        A partial state update dict containing the updated ``messages`` list.
    """
    # TODO: add tool-call loop (ReAct pattern) and memory integration
    messages = [SystemMessage(content=SUPPORT_SYSTEM_PROMPT)] + state["messages"]
    response = _llm.invoke(messages)

    return {"messages": [response]}