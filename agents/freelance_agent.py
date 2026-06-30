"""
agents/freelance_agent.py

Freelance agent that gathers project requirements from the user and generates
a structured project proposal, storing the draft in the shared state.

Uses the local HuggingFace model via model.loader.get_llm().
"""

import re

from langchain_core.messages import AIMessage, HumanMessage
from state import State
from model.loader import get_llm
from tools.file_writer import save_proposal

# ---------------------------------------------------------------------------
# System prompt
# ---------------------------------------------------------------------------

FREELANCE_PROMPT_TEMPLATE = """<|im_start|>system
You are a freelance proposal writer.
Write only a client-facing proposal letter.
Never write a hiring ad, job description, candidate profile, bullet list, numbered list, or section labels.
Use 2-3 short paragraphs, 120-180 words total.
Speak as "I" to the client as "you".
Mention the client's concrete need, relevant experience, approach, and a clear next step.
<|im_end|>
<|im_start|>user
Write a freelance proposal for this job:

{job_description}
<|im_end|>
<|im_start|>assistant
"""

FORBIDDEN_OUTPUT_MARKERS = (
    "job title",
    "responsibilities",
    "requirements",
    "skills",
    "benefits",
    "salary",
    "location",
    "duration",
)

# ---------------------------------------------------------------------------
# Agent node
# ---------------------------------------------------------------------------


def _looks_like_job_post(text: str) -> bool:
    """Returns True when the model drifted into job-posting format."""
    normalized = text.lower()
    marker_count = sum(marker in normalized for marker in FORBIDDEN_OUTPUT_MARKERS)
    numbered_lines = sum(
        line.strip()[:2].rstrip(".").isdigit()
        for line in text.splitlines()
        if line.strip()
    )
    return marker_count >= 2 or numbered_lines >= 3


def _clean_job_description(job_description: str) -> str:
    """Removes common command text so the fallback can reference the job cleanly."""
    cleaned = re.sub(
        r"^\s*write a proposal for (this )?job:\s*",
        "",
        job_description,
        flags=re.IGNORECASE,
    ).strip()
    return cleaned or job_description.strip()


def _fallback_proposal(job_description: str) -> str:
    """Deterministic fallback used when a small local model ignores format rules."""
    job_summary = _clean_job_description(job_description)
    return (
        f"Your project needs a reliable solution for this workflow: {job_summary}\n\n"
        "I can help build this with Python using a clear, maintainable approach: first "
        "reviewing the inputs and expected output, then creating the automation flow, "
        "adding validation for edge cases, and packaging the result so it is easy to run "
        "and maintain. I have experience with Python automation, data cleanup, file "
        "processing, and reporting workflows, so I would focus on making the process "
        "dependable rather than just producing a one-off script.\n\n"
        "If you can share a sample input, the desired output, and any current manual "
        "steps, I can outline the exact implementation plan and start with a first "
        "working version."
    )


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
    user_message = ""
    for message in reversed(state.get("messages", [])):
        if isinstance(message, HumanMessage):
            user_message = message.content
            break

    if not user_message:
        fallback = AIMessage(content="Please share the job description you want to respond to.")
        return {"messages": [fallback], "proposal_draft": ""}

    try:
        llm = get_llm()
        prompt = FREELANCE_PROMPT_TEMPLATE.format(job_description=user_message)
        response = llm.invoke(prompt)
    except Exception as exc:
        error_text = f"Freelance agent error: {exc}"
        fallback = AIMessage(content=error_text)
        return {"messages": [fallback], "proposal_draft": ""}

    # Extract the proposal text from the response
    proposal_text = (
        response.content if hasattr(response, "content") else str(response)
    )
    if _looks_like_job_post(proposal_text):
        proposal_text = _fallback_proposal(user_message)

    try:
        saved_path = save_proposal(proposal_text)
        response_text = f"{proposal_text}\n\nSaved to: {saved_path}"
    except Exception as exc:
        response_text = f"{proposal_text}\n\nCould not save proposal: {exc}"

    proposal_message = AIMessage(content=response_text)

    return {
        "messages": [proposal_message],
        "proposal_draft": proposal_text,
    }
