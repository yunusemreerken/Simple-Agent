# Architecture Discussion — Agentic AI Project

Date: May 2026
Topic: Multi-agent architecture decisions, LangGraph, security, starting strategy

---

## Project Definition

**Application type:** Customer support / chatbot + Business process automation + Freelancer bot (proposal writing)
**Language:** Python
**Architecture decision:** Multi-agent (LangGraph)

---

## What Is a Tool?

Any function an agent can call outside of the LLM itself is a "tool".

Examples:
- `web_search()` → search Google
- `write_docx()` → create a Word file
- `send_email()` → send an email
- `query_db()` → query a database

The agent thinks → decides which tool to call → tool runs → receives the result → continues.

---

## Why Multi-Agent?

Specialized agents instead of one "do-everything" agent:

```
User message
      ↓
Router Agent  ← "What kind of request is this?"
   /      \
Support   Freelance
Agent     Agent
```

Each agent works with its own tools. Adding a new agent or tool → just a new node.

---

## Why LangGraph?

| Feature | LangGraph |
|---|---|
| Adding tools | Very easy |
| Multi-agent | Native support |
| State management | Powerful |
| Error handling | Via graph flow |

---

## Adding an Agent — How It Works

Adding a new agent in LangGraph is 3 steps:

```python
# 1. New agent function
def seo_agent(state):
    return {"result": "..."}

# 2. Add node to graph
graph.add_node("seo", seo_agent)

# 3. Add new route to router
if intent == "seo":
    return "seo"
```

Existing agents are not affected by this change.

---

## Inter-Agent Communication

All agents communicate through a shared `State` object:

```python
class State(TypedDict):
    messages: list        # conversation history
    intent: str           # router decision
    user_info: dict       # readable by all agents
    proposal_draft: str   # written by freelance agent, read by others
```

New agent → add a new field to state → backward compatibility is automatic.

---

## Security — Priority Order

**Immediately (at project start):**
- Store API keys in `.env`
- Each agent should only access its own tools

**Once the first prototype is running:**
- Rate limiting
- Input validation
- Prompt injection protection

**Before going to production:**
- Log all actions (LangSmith)
- Approval step for hard-to-reverse operations
- LangSmith monitoring integration

---

## Starting Strategy

Decision: Start with the real project instead of an empty "hello world" agent.

**Rationale:** Mistakes made while solving a real problem teach permanently.
Abstract examples don't.

**Order:**
1. Get Router + Freelance Agent working (MVP)
2. Add Support Agent
3. Expand tools
4. RAG system
5. Security layer

---

## Learning Roadmap

| Week | Topic |
|---|---|
| 1 | LLM Huggeng Face, Tool Calling, Agent loop (ReAct) |
| 2 | LangGraph — Node, Edge, State, Conditional routing |
| 3 | Router + 2 Agent setup (project architecture) |
| 4 | RAG system, Vector DB, Agent memory |

---

## Next Step

Code the first working agent:
Router Agent + Freelance Agent (minimal, working version).