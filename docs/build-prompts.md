# Agentic AI Projesi — Build Prompts

Her milestone bağımsız bir sohbette çalışır.  
Sırayla ilerle. Bir önceki milestone çalışmadan sonrakine geçme.

---

## Milestone 1 — Proje İskeleti

> **Bu prompt'u yeni bir sohbette kullan.**

```
You are an expert Python developer specializing in AI agent systems.

Create a clean Python project skeleton for a multi-agent system with the following structure:

proje/
├── agents/
│   ├── __init__.py
│   ├── router.py
│   ├── support_agent.py
│   └── freelance_agent.py
├── tools/
│   ├── __init__.py
│   └── web_search.py
├── state.py
├── graph.py
├── main.py
├── .env.example
├── .gitignore
└── requirements.txt

Requirements:
- Python 3.11+
- LangGraph for agent orchestration
- LangChain for LLM integration
- python-dotenv for environment management
- Use Claude (Anthropic) as the LLM

Rules:
- Every file must have correct imports and placeholder implementations
- state.py must define the shared State TypedDict with fields: messages, intent, user_info, proposal_draft
- requirements.txt must include exact package versions
- .gitignore must exclude .env and __pycache__
- .env.example must show all required keys without values
- Add a brief docstring to every file explaining its purpose

Do not implement business logic yet. Only the skeleton.
Output every file completely. Do not truncate.
```

---

## Milestone 2 — State & Router Agent

> **Bu prompt'u yeni bir sohbette kullan.**  
> Milestone 1 dosyaları elinizde olmalı. İlgili dosyaları prompt'a yapıştır.

```
You are an expert Python developer specializing in LangGraph multi-agent systems.

I have a Python project skeleton. Now implement the State definition and Router Agent.

CURRENT state.py:
[state.py içeriğini buraya yapıştır]

CURRENT agents/router.py:
[router.py içeriğini buraya yapıştır]

TASK 1 — state.py:
Implement the shared State TypedDict:
- messages: Annotated[list, add_messages]  (LangGraph message reducer)
- intent: str  (router decision: "support", "freelance", "unknown")
- user_info: dict  (extracted user context)
- proposal_draft: str  (freelance agent output)

TASK 2 — agents/router.py:
Implement a Router Agent that:
- Receives the State
- Calls Claude claude-sonnet-4-20250514 with a system prompt that classifies user intent
- Classifies intent into exactly: "support", "freelance", or "unknown"
- Returns updated state with intent field set
- Uses structured output (respond only with the intent string)

System prompt for classification must handle:
- Support: questions, complaints, help requests
- Freelance: proposal writing, job analysis, bid requests
- Unknown: anything else → route to support as fallback

Rules:
- Use ANTHROPIC_API_KEY from environment
- Add clear comments explaining each step
- Include a simple test at the bottom under if __name__ == "__main__"

Output both files completely.
```

---

## Milestone 3 — Freelance Agent

> **Bu prompt'u yeni bir sohbette kullan.**  
> Milestone 2 dosyaları elinizde olmalı.

```
You are an expert Python developer specializing in LangGraph and AI agents.

I am building a freelancer assistant agent. Implement the Freelance Agent.

CURRENT state.py:
[state.py içeriğini buraya yapıştır]

CURRENT agents/freelance_agent.py:
[freelance_agent.py içeriğini buraya yapıştır]

TASK — agents/freelance_agent.py:
Implement a Freelance Agent that:
- Reads the user's message from state["messages"]
- Reads user_info from state if available
- Calls Claude claude-sonnet-4-20250514 to generate a professional freelance proposal
- The proposal must include: opening hook, relevant experience summary, approach to the project, call to action
- Returns updated state with proposal_draft field set

System prompt requirements:
- Tone: professional but personable
- Length: 150-250 words
- Do NOT use generic filler phrases like "I am writing to express my interest"
- Start with a direct reference to the client's specific problem
- End with a clear next step

Rules:
- Agent must be a plain function: def freelance_agent(state: State) -> dict
- Use ANTHROPIC_API_KEY from environment
- Add a test under if __name__ == "__main__" that runs with a sample job description

Output the complete file.
```

---

## Milestone 4 — Support Agent

> **Bu prompt'u yeni bir sohbette kullan.**  
> Milestone 2 dosyaları elinizde olmalı.

```
You are an expert Python developer specializing in LangGraph and AI agents.

Implement the Support Agent for a customer support system.

CURRENT state.py:
[state.py içeriğini buraya yapıştır]

CURRENT agents/support_agent.py:
[support_agent.py içeriğini buraya yapıştır]

TASK — agents/support_agent.py:
Implement a Support Agent that:
- Reads the user's message from state["messages"]
- Calls Claude claude-sonnet-4-20250514 to generate a helpful support response
- Handles three response types automatically:
  1. Direct answer — if the question can be answered immediately
  2. Clarification needed — if more information is required
  3. Escalation — if the issue is complex and needs human review
- Returns updated state with the assistant's response appended to messages

System prompt requirements:
- Tone: friendly, concise, solution-focused
- Always acknowledge the user's problem first
- Never say "I cannot help with that" — always offer an alternative
- For escalation cases, tell the user a human will follow up

Rules:
- Agent must be a plain function: def support_agent(state: State) -> dict
- Use ANTHROPIC_API_KEY from environment
- Add a test under if __name__ == "__main__"

Output the complete file.
```

---

## Milestone 5 — LangGraph Graph Kurulumu

> **Bu prompt'u yeni bir sohbette kullan.**  
> Tüm agent dosyaları elinizde olmalı.

```
You are an expert Python developer specializing in LangGraph.

Wire together all agents into a LangGraph StateGraph.

CURRENT files — paste each:
[state.py içeriğini buraya yapıştır]
[agents/router.py içeriğini buraya yapıştır]
[agents/freelance_agent.py içeriğini buraya yapıştır]
[agents/support_agent.py içeriğini buraya yapıştır]

TASK — graph.py:
Build the LangGraph StateGraph:

1. Nodes:
   - "router" → router_agent function
   - "freelance" → freelance_agent function
   - "support" → support_agent function

2. Edges:
   - START → "router"
   - "router" → conditional edge based on state["intent"]:
     - "freelance" → "freelance" node
     - "support" → "support" node
     - "unknown" → "support" node (fallback)
   - "freelance" → END
   - "support" → END

3. Compile the graph and export as: app = graph.compile()

TASK — main.py:
Implement a simple CLI loop:
- Print "Agent hazır. Çıkmak için 'q' yaz."
- Read user input
- Invoke the graph with the message
- Print the response
- Loop until user types "q"

Rules:
- Import app from graph.py
- Handle keyboard interrupt gracefully
- Print which agent handled the request (router intent)

Output both files completely.
```

---

## Milestone 6 — Web Search Tool

> **Bu prompt'u yeni bir sohbette kullan.**  
> Graph çalışıyor olmalı.

```
You are an expert Python developer specializing in LangChain tools and AI agents.

Add a web search tool to the freelance agent.

CURRENT files — paste each:
[tools/web_search.py içeriğini buraya yapıştır]
[agents/freelance_agent.py içeriğini buraya yapıştır]

TASK 1 — tools/web_search.py:
Implement a web search tool using DuckDuckGo (duckduckgo-search package, no API key needed):
- Function signature: def web_search(query: str, max_results: int = 3) -> list[dict]
- Returns list of: {"title": str, "url": str, "snippet": str}
- Handle errors gracefully, return empty list on failure
- Add result caching with functools.lru_cache (maxsize=32)

TASK 2 — agents/freelance_agent.py:
Update the Freelance Agent to:
- Before generating the proposal, search for context about the job/industry
- Use web_search to find 2-3 relevant results based on key terms from the user's message
- Include relevant context in the Claude prompt (as background research)
- Still return proposal_draft in state

Rules:
- Keep the agent function signature unchanged: def freelance_agent(state: State) -> dict
- Search should not break the agent if it fails (try/except)
- Add duckduckgo-search to requirements.txt

Output both files completely.
```

---

## Milestone 7 — End-to-End Test & Hata Yönetimi

> **Bu prompt'u yeni bir sohbette kullan.**  
> Tüm milestone'lar tamamlanmış olmalı.

```
You are an expert Python developer and QA engineer.

Add error handling and a basic test suite to the multi-agent project.

CURRENT files — paste each:
[graph.py içeriğini buraya yapıştır]
[main.py içeriğini buraya yapıştır]
[agents/router.py içeriğini buraya yapıştır]

TASK 1 — Error handling in graph.py:
- Wrap each node execution in try/except
- On agent failure: log the error, set intent to "support", route to support agent as fallback
- Never let an unhandled exception crash the CLI

TASK 2 — Create tests/test_agents.py:
Write pytest tests covering:
- test_router_classifies_freelance: message about writing a proposal → intent == "freelance"
- test_router_classifies_support: message about a complaint → intent == "support"
- test_router_unknown_falls_back: nonsense message → routes to support
- test_freelance_agent_returns_draft: freelance agent returns non-empty proposal_draft
- test_support_agent_returns_message: support agent appends a message to state

Rules:
- Use pytest
- Mock the Anthropic API calls with pytest-mock (do not make real API calls in tests)
- Each test must be independent (no shared state)
- Add pytest and pytest-mock to requirements.txt

Output all modified and new files completely.
```

---

## Notlar

- Her milestone tek bir sohbette tamamlanır.
- Bir sonraki milestone'a geçmeden önce mevcut milestone'un testini çalıştır.
- Dosyaları bir sonraki prompt'a yapıştırırken tüm içeriği ekle, kısaltma.
- API key olmadan test etmek istersen Milestone 7'deki mock testlerini önce çalıştır.
