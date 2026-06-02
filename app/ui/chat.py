import streamlit as st


def render_chat_history() -> None:
    messages = st.session_state.get("messages", [])

    if not messages:
        _render_welcome()
        return

    for message in messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def _render_welcome() -> None:
    st.markdown(
        """
## Welcome to AI Mentor 🎓

I'm your personal AI companion for learning **Artificial Intelligence, Machine Learning, and Data Science**.

---

### What I can do for you

| Feature | How to use |
|---|---|
| 💬 **Chat** | Type any question below |
| 📍 **Learning Roadmap** | Use the sidebar → Generate Roadmap |
| 💡 **Concept Explanations** | Use the sidebar → Explain Concept |
| 🛠️ **Project Ideas** | Use the sidebar → Recommend Projects |

---

### Try asking me

- *"I'm a complete beginner — where do I start with AI?"*
- *"Explain transformers like I'm 12 years old."*
- *"What's the difference between supervised and unsupervised learning?"*
- *"How do I go from Python beginner to ML engineer?"*

**Select your model in the sidebar, then start chatting!**
"""
    )
