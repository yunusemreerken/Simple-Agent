"""
agents/router.py

Classifies the user's intent and writes it to state.intent.
The graph uses state.intent to route to the correct downstream agent.

Supported intents:
    "freelance"  → user wants a proposal written
    "unknown"    → cannot classify → graph ends gracefully

Uses the local HuggingFace model via model.loader.get_llm().
"""

import logging
import re
from langchain_core.messages import HumanMessage, SystemMessage
from state import State
from model.loader import get_llm

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Prompt
# ---------------------------------------------------------------------------

ROUTER_SYSTEM_PROMPT = """You are an intent classifier for a freelance proposal assistant.

Your only job is to read the user's message and output a single word — the intent.

Rules:
- If the user wants help writing a freelance proposal, cover letter, or bid for a job → output: freelance
- For anything else → output: unknown

Output ONLY the single intent word. No explanation, no punctuation, no extra text.

Examples:
User: "Write a proposal for this Python job on Upwork"  → freelance
User: "I need a cover letter for a data science gig"    → freelance
User: "Help me bid on this React project"               → freelance
User: "What is the weather today?"                      → unknown
"""

# ---------------------------------------------------------------------------
# Intent extraction
# ---------------------------------------------------------------------------

VALID_INTENTS = {"freelance", "unknown"}


def _extract_intent(raw_output: str) -> str:
    """
    Parses the model's raw output and returns a valid intent string.
    Falls back to 'unknown' if output is unrecognised.
    """
    # Strip whitespace, lowercase, take only the first word
    cleaned = raw_output.strip().lower()
    first_word = re.split(r"[\s\n,.]", cleaned)[0]

    if first_word in VALID_INTENTS:
        return first_word

    logger.warning(
        "Router received unexpected intent '%s'. Defaulting to 'unknown'.", first_word
    )
    return "unknown"


# ---------------------------------------------------------------------------
# Agent node
# ---------------------------------------------------------------------------

def router_agent(state: State) -> dict:
    """
    LangGraph node: classifies the user's intent.

    Reads the last HumanMessage from state.messages, calls the local LLM,
    and returns {"intent": <classified_intent>}.

    Args:
        state: The current shared graph state.

    Returns:
        dict with "intent" key to be merged into state.
    """
    # Extract the latest user message
    messages = state.get("messages", [])
    user_message = ""
    for msg in reversed(messages):
        if isinstance(msg, HumanMessage):
            user_message = msg.content
            break

    if not user_message:
        logger.warning("Router: no HumanMessage found in state. Defaulting to 'unknown'.")
        return {"intent": "unknown"}

    logger.debug("Router classifying message: %s", user_message[:120])

    # Call the local LLM
    llm = get_llm()
    prompt = [
        SystemMessage(content=ROUTER_SYSTEM_PROMPT),
        HumanMessage(content=user_message),
    ]

    try:
        response = llm.invoke(prompt)
        raw_output = response.content if hasattr(response, "content") else str(response)
    except Exception as exc:
        logger.error("Router LLM call failed: %s", exc)
        return {"intent": "unknown"}

    intent = _extract_intent(raw_output)
    logger.info("Router classified intent: '%s'", intent)

    return {"intent": intent}