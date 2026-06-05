"""
agents/freelance_agent.py

Freelance agent that gathers project requirements from the user and generates
a structured project proposal, storing the draft in the shared state.
"""

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage
from state import State

# ---------------------------------------------------------------------------
# LLM initialisation
# ---------------------------------------------------------------------------

_llm = ChatAnthropic(model="claude-opus-4-5", temperature=0.3)

# ---------------------------------------------------------------------------
# System prompt
# ---------------------------------------------------------------------------

FREELANCE_SYSTEM_PROMPT = """You are an expert freelance project consultant.
Your goals:
1. Gather key project details: scope, timeline, budget, and deliverables.
2. Ask clarifying questions one at a time until you have enough information.
3. When sufficient detail is available, produce a professional project proposal
   in Markdown format that includes:
   - Executive Summary
   - Scope of Work
   - Timeline & Milestones
   - Pricing Breakdown
   - Terms & Conditions placeholder

Store the final proposal in your response so it can be captured as a draft."""

# ---------------------------------------------------------------------------
# Agent node
# ---------------------------------------------------------------------------


def freelance_agent(state: State) -> dict:
    """
    Drives a requirements-gathering conversation and produces a proposal draft.

    Args:
        state: The current shared graph state.

    Returns:
        A partial state update dict with updated ``messages`` and,
        once ready, a ``proposal_draft`` string.
    """
    # TODO: implement multi-turn requirements gathering and proposal generation
    messages = [SystemMessage(content=FREELANCE_SYSTEM_PROMPT)] + state["messages"]
    response = _llm.invoke(messages)

    # Placeholder: treat every response as a draft until business logic is added
    proposal_draft = state.get("proposal_draft", "") or ""

    return {
        "messages": [response],
        "proposal_draft": proposal_draft,
    }