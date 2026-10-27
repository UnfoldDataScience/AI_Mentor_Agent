# AI Mentor — Episodes 1–5

A conversational AI tutor for learning Artificial Intelligence, Machine Learning, and Data Science.

Built with **Python**, **Streamlit**, and the **OpenAI API** as part of a 6-episode YouTube series.

---

## What this app can do

**Episode 1 — Agentic chat + tools**
- Chats with you about AI/ML topics
- Automatically decides which tool to use based on your question (agentic behaviour)
- Generates structured learning roadmaps
- Explains concepts with analogies and code examples
- Recommends hands-on projects for your level
- Saves every conversation to a JSON file

**Episode 2 — RAG (your own knowledge base)**
- A fourth tool, `search_knowledge_base`, lets the agent search your own notes/documents
- Retrieval is transparent — every answer that uses your notes shows which sources and similarity scores were used
- Build or refresh the knowledge base with one command: `python -m rag.build_index`

**Episode 3 — Memory (remembers you across sessions)**
- A fifth tool, `remember_about_user`, lets the agent save lasting facts about you — background, goals, level, deadlines, preferences
- Unlike a session (one conversation) or the knowledge base (your documents), memory is global to *you* and persists across every future session
- Every chat is automatically given access to what's been remembered — no need to repeat yourself
- The sidebar's **🧠 Memory** panel shows everything remembered, with a delete button per fact

**Episode 4 — LangGraph (multi-step reasoning)**
- The agentic loop is rebuilt on **LangGraph** as a graph: an `agent` node (decides what to do) and a `tools` node (executes it), looping until the model has everything it needs
- The agent can now call **multiple tools in one turn**, one after another, and weave the results into a single combined answer — e.g. explain a concept, then recommend a project for it, in one reply
- The `🔧 Agent used tool(s)` caption now shows the full chain, e.g. `explain_concept → recommend_projects`
- A hard `recursion_limit` on the graph keeps the loop from running away

**Episode 5 — MCP (external tools)**
- A separate **MCP server** (`tools/server.py`) runs in its own process and exposes two tools that call live APIs: `search_arxiv_papers` (real research papers) and `search_github_repos` (real open-source repos)
- An **MCP client** (`tools/client.py`) discovers those tools at startup over stdio and converts them into the same OpenAI tool format the built-in tools use — no hand-written schemas
- The LangGraph loop is unchanged: external tools sit alongside the five built-in ones, so the agent can chain them, e.g. `explain_concept → 🔌 search_github_repos`
- External tools are marked with 🔌 in the tool caption, and the sidebar's **🔌 MCP Tools** panel shows the connected server and its tools
- A failing tool (bad arguments, API down) no longer crashes the app — the error is handed back to the agent as the tool's result

---

## Series overview

| Episode | What you build |
|---|---|
| 1 | Agentic chat with tool use + session storage |
| 2 | RAG — ask questions over your own documents |
| 3 | Memory — remember things across sessions |
| 4 | LangGraph — multi-step reasoning chains |
| **5 — This episode** | MCP — plug in external tools |
| 6 | Observability — trace and monitor everything |

---

## Setup

### Prerequisites
- Python 3.10+
- An [OpenAI API key](https://platform.openai.com/api-keys)

### 1. Clone / navigate to the project

```bash
cd AITutor
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set your API key

```bash
cp .env.example .env
```

Open `.env` and add your key:

```
OPENAI_API_KEY=sk-...your-key-here...
```

### 5. Run the app

```bash
streamlit run app.py
```

Opens at `http://localhost:8501`.

---

## How to use it

### Chat (agentic mode)
Just type naturally — the AI decides which tool to call.

| Try typing... | What happens |
|---|---|
| *"I want to learn NLP from scratch"* | Agent calls the roadmap tool |
| *"What is a transformer model?"* | Agent calls the concept explainer |
| *"What projects should I build for computer vision?"* | Agent calls the project recommender |
| *"Check my notes — what's cosine similarity?"* | Agent calls `search_knowledge_base` |
| *"I'm a backend dev trying to break into ML by December"* | Agent calls `remember_about_user` |
| *"Explain attention, then recommend a project to practice it"* | Agent chains `explain_concept` → `recommend_projects` in one turn |
| *"Find me the key research papers on diffusion models"* | Agent calls 🔌 `search_arxiv_papers` via MCP |
| *"Explain RAG, then show me popular GitHub repos to learn it"* | Agent chains `explain_concept` → 🔌 `search_github_repos` |
| *"What's the difference between AI and ML?"* | Agent answers directly |

When a tool fires, you'll see `🔧 Agent used tool: <name>` above the response — or, for a chain,
`🔧 Agent used tools: <name> → <name>`.

### Knowledge base (RAG)
1. Drop `.md` / `.txt` files into `rag/documents/` — a few sample docs are included to get started
2. Run `python -m rag.build_index` to (re)build the index whenever your documents change
3. The sidebar shows how many chunks/documents are currently indexed
4. When the agent answers from your notes, it cites them inline (`[1]`, `[2]`, ...) and shows a **"📚 Sources retrieved"** panel with the source file and similarity score for each chunk used
5. If your notes don't cover the question, the agent says so and falls back to general knowledge

### Memory (long-term, across sessions)
1. Mention something lasting about yourself in chat (goal, level, background, deadline) — the agent decides whether it's worth remembering and calls `remember_about_user`
2. Every future chat — even in a brand new session — automatically gets this context, so the agent doesn't need to be reminded
3. The sidebar's **🧠 Memory** panel lists every remembered fact; click 🗑️ next to any of them to forget it

### Multi-step reasoning (LangGraph)
1. Ask for more than one thing in a single message — e.g. *"Explain transformers, then suggest a beginner project for them"*
2. The agent runs a loop: think → call a tool → look at the result → decide whether it needs another tool → repeat, until it has everything it needs
3. It combines every tool result into one coherent final answer, instead of stopping after the first tool call
4. The caption above the response shows the full chain of tools used, in order

### External tools (MCP)
1. Nothing to set up — when the app starts, it launches the MCP server (`tools/server.py`) as a subprocess and asks it which tools it offers
2. Ask for real papers or repos — the agent calls the external tool, which hits the live arXiv / GitHub API and returns real titles and links
3. The sidebar's **🔌 MCP Tools** panel shows whether the server connected and which tools it exposes
4. To add a new external tool, add a function with `@server.tool(...)` in `tools/server.py` and restart the app — the client discovers it automatically

The GitHub search API allows ~10 unauthenticated requests per minute; arXiv needs no key either.

### Sidebar — explicit controls
Use the sidebar forms when you want to set exact parameters (topic, level, hours/week, goal) without relying on the agent to infer them.

### Session management
- **New Chat** — fresh conversation
- **Load Chat** — restore any previous session
- Sessions auto-save to `sessions/` after every message

---

## Project structure

```
AITutor/
├── app.py                  ← entry point
├── app/
│   ├── llm/client.py       ← OpenAI wrapper (single-shot chat calls)
│   ├── tools/definitions.py← tool schemas (OpenAI function calling format)
│   ├── services/tutor.py   ← orchestrates the graph + tools
│   ├── prompts/tutor.py    ← all prompt strings
│   ├── storage/session.py  ← saves/loads JSON sessions
│   └── ui/                 ← Streamlit components
├── rag/                    ← Episode 2
│   ├── documents/          ← your notes (.md / .txt) — knowledge base source
│   ├── loader.py           ← reads documents/
│   ├── chunker.py          ← splits text into overlapping chunks
│   ├── embeddings.py       ← OpenAI embeddings client
│   ├── vector_store.py     ← cosine-similarity search over embeddings (numpy)
│   ├── build_index.py      ← CLI: python -m rag.build_index
│   └── index/              ← generated index (gitignored)
├── memory/                 ← Episode 3
│   └── store.py            ← MemoryStore — reads/writes user_memory.json (gitignored)
├── agents/                 ← Episode 4
│   └── graph.py            ← TutorGraph — LangGraph agent/tools loop, multi-step reasoning
├── tools/                  ← Episode 5
│   ├── server.py           ← MCP server (separate process) — arXiv + GitHub tools
│   └── client.py           ← MCPClient — discovers + calls MCP tools over stdio
└── observability/          ← Episode 6 (empty)
```

---

## Key agentic concepts introduced

| Term | What it means |
|---|---|
| **Tool** | A function the model can choose to call |
| **Tool schema** | JSON spec describing the tool's name and parameters |
| **Tool call** | The model returning a structured call instead of plain text |
| **Agentic loop** | Think → decide → act → return result |

| Term | What it means |
|---|---|
| **Memory** | Facts about the *learner* that persist across every session — distinct from RAG (your documents) and from a session (one conversation) |
| **Always-on context** | Memories are injected into the system prompt on every call, so the agent doesn't need to "search" for them like it does with `search_knowledge_base` |

| Term | What it means |
|---|---|
| **Graph** | The agentic loop expressed as nodes (`agent`, `tools`) and edges, instead of one hardcoded round of "call the model, maybe call one tool, done" |
| **State** | The running list of messages (`AgentState`) that flows through every node and accumulates as the loop progresses |
| **Multi-step reasoning** | The model can call a tool, see its result, and decide to call *another* tool before answering — instead of being limited to one tool per message |
| **Recursion limit** | A hard cap on how many times the graph can loop `agent ↔ tools`, so a confused model can't loop forever |

Episodes 1–3 used a **single-step loop** (at most one tool per message). Episode 4 replaces
that loop with a LangGraph graph, so the agent can chain several tools together in one turn.

| Term | What it means |
|---|---|
| **MCP (Model Context Protocol)** | A standard protocol for exposing tools to an AI app, so tools can live outside the app and be reused by any MCP client |
| **MCP server** | A separate process that offers tools — here `tools/server.py`, talking over stdin/stdout (stdio) |
| **MCP client** | The part of our app that connects to a server, lists its tools, and calls them — here `tools/client.py` |
| **Tool discovery** | The client asks the server which tools it has (`list_tools`) at runtime, instead of us hardcoding their schemas |

Episodes 1–4 defined every tool inside the app. Episode 5 adds tools the app *discovers*
from a separate MCP server, and the agent uses them exactly like its built-in tools.
