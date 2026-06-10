"""
agents/freelance_agent.py

Freelance agent that gathers project requirements from the user and generates
a structured project proposal, storing the draft in the shared state.

Uses the local HuggingFace model via model.loader.get_llm().
"""

from langchain_core.messages import SystemMessage, AIMessage
from state import State
from model.loader import get_llm

# ---------------------------------------------------------------------------
# System prompt
# ---------------------------------------------------------------------------

FREELANCE_SYSTEM_PROMPT = """You are an expert freelance proposal writer.
Your goals:
1. Read the job description provided by the user carefully.
2. Write a compelling, professional freelance proposal in Markdown format.

The proposal must include:
- Opening hook (1-2 sentences that show you understand the client's problem)
- Relevant experience (brief, specific to the job)
- Proposed approach (how you will solve their problem)
- Timeline & Milestones
- Pricing Breakdown
- Call to action (invite them to discuss further)

Be concise, confident, and client-focused. Write in first person."""

# ---------------------------------------------------------------------------
# Agent node
# ---------------------------------------------------------------------------


def freelance_agent(state: State) -> dict:
    """
    Generates a freelance proposal based on the conversation history.

    Reads all messages from state, calls the local HuggingFace model,
    and returns updated messages + proposal_draft.

    Args:
        state: The current shared graph state.

    Returns:
        A partial state update dict with updated messages and proposal_draft.
    """
    llm = get_llm()

    messages = [SystemMessage(content=FREELANCE_SYSTEM_PROMPT)] + state["messages"]

    try:
        response = llm.invoke(messages)
    except Exception as exc:
        error_text = f"Freelance agent error: {exc}"
        fallback = AIMessage(content=error_text)
        return {"messages": [fallback], "proposal_draft": ""}

    # Extract the proposal text from the response
    proposal_text = (
        response.content if hasattr(response, "content") else str(response)
    )

    return {
        "messages": [response],
        "proposal_draft": proposal_text,
    }