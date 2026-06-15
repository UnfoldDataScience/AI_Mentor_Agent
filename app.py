import streamlit as st
from dotenv import load_dotenv

from app.services.tutor import TutorService
from app.storage.session import SessionStorage
from app.ui.chat import render_chat_history
from app.ui.sidebar import render_sidebar

load_dotenv()


def _init_session_state() -> None:
    storage = SessionStorage()
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "session_id" not in st.session_state:
        st.session_state.session_id = storage.new_session_id()


def _handle_special_action(
    action: str,
    data: dict,
    tutor: TutorService,
    storage: SessionStorage,
) -> None:
    with st.spinner("Generating response..."):
        if action == "roadmap":
            user_msg = (
                f"Generate a learning roadmap for **{data['topic']}**\n"
                f"- Level: {data['level']}\n"
                f"- Goal: {data['goal']}\n"
                f"- Time available: {data['time_per_week']} hours/week"
            )
            response = tutor.generate_roadmap(**data)

        elif action == "concept":
            user_msg = (
                f"Explain the concept: **{data['concept']}** "
                f"(Level: {data['level']})"
            )
            response = tutor.explain_concept(**data)

        elif action == "projects":
            user_msg = (
                f"Recommend projects for learning **{data['topic']}**\n"
                f"- Level: {data['level']}\n"
                f"- Goal: {data['goal']}"
            )
            response = tutor.recommend_projects(**data)

        else:
            return

    st.session_state.messages.append({"role": "user", "content": user_msg})
    st.session_state.messages.append({"role": "assistant", "content": response})
    storage.save_session(
        st.session_state.session_id,
        st.session_state.messages,
        metadata={"last_action": action},
    )
    st.rerun()


def main() -> None:
    st.set_page_config(
        page_title="AI Mentor",
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    _init_session_state()
    storage = SessionStorage()

    config = render_sidebar()
    tutor = TutorService(model=config["model"])

    if config["action"]:
        _handle_special_action(config["action"], config["action_data"], tutor, storage)
        return

    st.title("🎓 AI Mentor")
    st.caption(
        f"Episode 1 · Model: **{config['model']}** · "
        f"Session: `{st.session_state.session_id}`"
    )

    render_chat_history()

    if prompt := st.chat_input("Ask your AI Mentor anything..."):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response, tool_used = tutor.chat(st.session_state.messages)
            if tool_used:
                st.caption(f"🔧 Agent used tool: `{tool_used}`")
            st.markdown(response)

            if tool_used == "search_knowledge_base" and tutor.last_retrieved_chunks:
                with st.expander("📚 Sources retrieved"):
                    for i, chunk in enumerate(tutor.last_retrieved_chunks, start=1):
                        st.markdown(
                            f"**[{i}] {chunk['source']}** · similarity {chunk['score']:.2f}"
                        )
                        snippet = chunk["text"][:300]
                        if len(chunk["text"]) > 300:
                            snippet += "..."
                        st.caption(snippet)

        st.session_state.messages.append({"role": "assistant", "content": response})
        storage.save_session(
            st.session_state.session_id,
            st.session_state.messages,
            metadata={"model": config["model"]},
        )


if __name__ == "__main__":
    main()
