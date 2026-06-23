# AI Mentor — Episodes 1, 2 & 3

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

---

## Series overview

| Episode | What you build |
|---|---|
| 1 | Agentic chat with tool use + session storage |
| 2 | RAG — ask questions over your own documents |
| **3 — This episode** | Memory — remember things across sessions |
| 4 | LangGraph — multi-step reasoning chains |
| 5 | MCP — plug in external tools |
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
| *"What's the difference between AI and ML?"* | Agent answers directly |

When a tool fires, you'll see `🔧 Agent used tool: <name>` above the response.

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
│   ├── llm/client.py       ← OpenAI wrapper (chat + agentic loop)
│   ├── tools/definitions.py← tool schemas (OpenAI function calling format)
│   ├── services/tutor.py   ← orchestrates LLM + tools
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
├── agents/                 ← Episode 4 (empty)
├── tools/                  ← Episode 5 (empty)
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

This episode uses a **single-step loop** (one tool per message). Multi-step chains come in Episode 4.

| Term | What it means |
|---|---|
| **Memory** | Facts about the *learner* that persist across every session — distinct from RAG (your documents) and from a session (one conversation) |
| **Always-on context** | Memories are injected into the system prompt on every call, so the agent doesn't need to "search" for them like it does with `search_knowledge_base` |
