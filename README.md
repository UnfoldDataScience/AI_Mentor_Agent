# AI Mentor — Episode 1

A conversational AI tutor for learning Artificial Intelligence, Machine Learning, and Data Science.

Built with **Python**, **Streamlit**, and the **OpenAI API** as part of a 6-episode YouTube series.

---

## What you'll build in this episode

A working AI Mentor app that:
- Chats with you about AI/ML topics
- Automatically decides which tool to use based on your question (agentic behaviour)
- Generates structured learning roadmaps
- Explains concepts with analogies and code examples
- Recommends hands-on projects for your level
- Saves every conversation to a JSON file

---

## Series overview

| Episode | What you build |
|---|---|
| **1 — This episode** | Agentic chat with tool use + session storage |
| 2 | RAG — ask questions over your own documents |
| 3 | Memory — remember things across sessions |
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
| *"What's the difference between AI and ML?"* | Agent answers directly |

When a tool fires, you'll see `🔧 Agent used tool: <name>` above the response.

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
├── rag/                    ← Episode 2 (empty)
├── memory/                 ← Episode 3 (empty)
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
