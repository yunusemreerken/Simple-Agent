"""
graph.py

Assembles the LangGraph StateGraph by registering all agent nodes and
defining the conditional edges that route between them based on detected intent.
"""

from langgraph.graph import StateGraph, END

from state import State
from agents.router import router_agent
from agents.support_agent import support_agent
from agents.freelance_agent import freelance_agent

# ---------------------------------------------------------------------------
# Conditional edge logic
# ---------------------------------------------------------------------------


def route_by_intent(state: State) -> str:
    """
    Maps the classified intent in state to the next graph node name.

    Args:
        state: The current shared graph state.

    Returns:
        The name of the next node to execute.
    """
    intent = state.get("intent", "unknown")

    routing_map = {
        "support": "support_agent",
        "freelance": "freelance_agent",
        "unknown": "support_agent",
    }

    return routing_map.get(intent, END)


# ---------------------------------------------------------------------------
# Graph construction
# ---------------------------------------------------------------------------


def build_graph() -> StateGraph:
    """
    Constructs and compiles the multi-agent LangGraph graph.

    Returns:
        A compiled LangGraph runnable ready for invocation.
    """
    builder = StateGraph(State)

    # Register nodes
    builder.add_node("router", router_agent)
    builder.add_node("support_agent", support_agent)
    builder.add_node("freelance_agent", freelance_agent)

    # Entry point
    builder.set_entry_point("router")

    # Conditional routing after the router node
    builder.add_conditional_edges(
        "router",
        route_by_intent,
        {
            "support_agent": "support_agent",
            "freelance_agent": "freelance_agent",
            END: END,
        },
    )

    # Terminal edges — agents finish and the graph ends
    builder.add_edge("support_agent", END)
    builder.add_edge("freelance_agent", END)

    return builder.compile()


# Module-level compiled graph (import and use directly)
graph = build_graph()
