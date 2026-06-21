"""
main.py

Entry point for the multi-agent system. Loads environment variables,
initialises the LangGraph graph, and runs an interactive CLI loop.
"""

import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

# Load .env before importing modules that read HuggingFace settings.
load_dotenv()

from graph import graph  # noqa: E402  (import after env is loaded)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _validate_env() -> None:
    """Raises EnvironmentError if required environment variables are missing."""
    required = ["HF_MODEL_NAME"]
    missing = [key for key in required if not os.getenv(key)]
    if missing:
        raise EnvironmentError(
            f"Missing required environment variables: {', '.join(missing)}\n"
            "Copy .env.example to .env and fill in the values."
        )


def run_cli() -> None:
    """
    Starts a simple REPL that feeds user input through the multi-agent graph
    and prints the assistant's response to stdout.
    """
    print("Multi-Agent System — type 'quit' or 'exit' to stop.\n")

    # Maintain conversation history across turns
    # TODO: persist history with LangGraph checkpointer for true multi-turn memory
    conversation_messages: list = []

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if user_input.lower() in {"quit", "exit", "q"}:
            print("Goodbye!")
            break

        if not user_input:
            continue

        conversation_messages.append(HumanMessage(content=user_input))

        initial_state = {
            "messages": conversation_messages,
            "intent": None,
            "user_info": None,
            "proposal_draft": None,
        }

        # Invoke the graph synchronously
        result = graph.invoke(initial_state)

        # Extract the last AI message
        ai_messages = [
            m for m in result["messages"] if m.type == "ai"
        ]
        if ai_messages:
            reply = ai_messages[-1].content
            print(f"\nAssistant: {reply}\n")
            conversation_messages.append(ai_messages[-1])
        else:
            print("\nAssistant: (no response generated)\n")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    _validate_env()
    run_cli()
