from typing import Dict, Any, Optional

import streamlit as st

from app.llm.client import OPENAI_MODELS
from app.storage.session import SessionStorage
from rag.vector_store import VectorStore


def render_sidebar() -> Dict[str, Any]:
    storage = SessionStorage()
    action: Optional[str] = None
    action_data: Optional[Dict] = None

    with st.sidebar:
        st.title("🎓 AI Mentor")
        st.caption("Episodes 1 & 2 — Chat, Tools & RAG")

        st.divider()

        st.subheader("⚙️ Settings")
        model = st.selectbox("Model", OPENAI_MODELS, key="model_select")

        st.divider()

        st.subheader("💬 Sessions")
        col1, col2 = st.columns(2)

        with col1:
            if st.button("New Chat", use_container_width=True):
                st.session_state.messages = []
                st.session_state.session_id = storage.new_session_id()
                st.session_state.pop("show_sessions", None)
                st.rerun()

        with col2:
            sessions = storage.list_sessions()
            load_clicked = st.button(
                "Load Chat",
                use_container_width=True,
                disabled=len(sessions) == 0,
            )
            if load_clicked:
                st.session_state.show_sessions = True

        if st.session_state.get("show_sessions") and sessions:
            labels = {
                f"{s['updated_at'][:16]}  ({s['message_count']} msgs)  [{s['session_id']}]": s[
                    "session_id"
                ]
                for s in sessions[:10]
            }
            chosen_label = st.selectbox("Select a session:", list(labels.keys()))
            if st.button("Load", key="confirm_load"):
                loaded = storage.load_session(labels[chosen_label])
                if loaded:
                    st.session_state.messages = loaded["messages"]
                    st.session_state.session_id = loaded["session_id"]
                    st.session_state.pop("show_sessions", None)
                    st.rerun()

        if st.session_state.get("session_id"):
            msg_count = len(st.session_state.get("messages", []))
            st.caption(f"Session `{st.session_state.session_id}` · {msg_count} messages")

        st.divider()

        st.subheader("📚 Knowledge Base")
        store = VectorStore()
        if store.load() and store.chunks:
            sources = sorted({chunk["source"] for chunk in store.chunks})
            st.caption(f"{len(store.chunks)} chunks indexed from {len(sources)} document(s)")
            with st.expander("Indexed documents"):
                for source in sources:
                    st.caption(f"- {source}")
        else:
            st.caption("No knowledge base indexed yet.")
            st.caption("Run `python -m rag.build_index` to index `rag/documents/`.")

        st.divider()

        st.subheader("🚀 Special Features")

        with st.expander("📍 Generate Roadmap"):
            topic = st.text_input(
                "Topic", placeholder="e.g. Machine Learning", key="rm_topic"
            )
            level = st.selectbox(
                "Your current level",
                ["Beginner", "Intermediate", "Advanced"],
                key="rm_level",
            )
            goal = st.text_input(
                "Your goal",
                placeholder="e.g. Get a job as an ML engineer",
                key="rm_goal",
            )
            hours = st.slider("Hours per week", 1, 40, 10, key="rm_hours")
            if st.button("Generate Roadmap ✨", key="btn_roadmap"):
                if topic.strip():
                    action = "roadmap"
                    action_data = {
                        "topic": topic,
                        "level": level,
                        "goal": goal or "Master the topic",
                        "time_per_week": hours,
                    }
                else:
                    st.warning("Please enter a topic first.")

        with st.expander("💡 Explain a Concept"):
            concept = st.text_input(
                "Concept",
                placeholder="e.g. Attention mechanism",
                key="cp_concept",
            )
            cp_level = st.selectbox(
                "Your level",
                ["Beginner", "Intermediate", "Advanced"],
                key="cp_level",
            )
            if st.button("Explain ✨", key="btn_concept"):
                if concept.strip():
                    action = "concept"
                    action_data = {"concept": concept, "level": cp_level}
                else:
                    st.warning("Please enter a concept first.")

        with st.expander("🛠️ Recommend Projects"):
            pj_topic = st.text_input(
                "Topic", placeholder="e.g. NLP", key="pj_topic"
            )
            pj_level = st.selectbox(
                "Your level",
                ["Beginner", "Intermediate", "Advanced"],
                key="pj_level",
            )
            pj_goal = st.text_input(
                "Your goal",
                placeholder="e.g. Build a strong portfolio",
                key="pj_goal",
            )
            if st.button("Get Projects ✨", key="btn_projects"):
                if pj_topic.strip():
                    action = "projects"
                    action_data = {
                        "topic": pj_topic,
                        "level": pj_level,
                        "goal": pj_goal or "Build hands-on skills",
                    }
                else:
                    st.warning("Please enter a topic first.")

        st.divider()
        st.caption("Episodes coming soon:")
        st.caption("Ep 3 · Memory  |  Ep 4 · LangGraph")
        st.caption("Ep 5 · MCP  |  Ep 6 · Observability")

    return {
        "model": model,
        "action": action,
        "action_data": action_data,
    }
