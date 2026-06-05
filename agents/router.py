"""
agents/router.py

Router agent responsible for classifying the user's intent and directing
the conversation to the appropriate downstream agent (support or freelance).
"""

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage
from state import State

# ---------------------------------------------------------------------------
# LLM initialisation
# ---------------------------------------------------------------------------

_llm = ChatAnthropic(model="claude-opus-4-5", temperature=0)

# ---------------------------------------------------------------------------
# System prompt
# ---------------------------------------------------------------------------

ROUTER_SYSTEM_PROMPT = """You are a routing assistant. Your only job is to classify 
the user's message into one of the following intents:

- "support"   : The user needs technical help, has a bug report, or a general question.
- "freelance" : The user wants to hire a freelancer or receive a project proposal.
- "unknown"   : The intent is unclear.

Respond with exactly one word: support, freelance, or unknown."""

# ---------------------------------------------------------------------------
# Agent node
# ---------------------------------------------------------------------------


def router_agent(state: State) -> dict:
    """
    Classifies the latest user message and writes the detected intent into state.

    Args:
        state: The current shared graph state.

    Returns:
        A partial state update dict containing the detected ``intent``.
    """
    # TODO: implement intent classification logic
    messages = [SystemMessage(content=ROUTER_SYSTEM_PROMPT)] + state["messages"]
    response = _llm.invoke(messages)

    intent = response.content.strip().lower()
    if intent not in {"support", "freelance"}:
        intent = "unknown"

    return {"intent": intent}