# app.py
import time
import streamlit as st

APP_TITLE = "RAG / Fine-tune Chatbot Demo"
APP_SUBTITLE = "Frontend prototype (backend currently stubbed)."

st.set_page_config(page_title=APP_TITLE, page_icon="💬", layout="centered")

def init_state() -> None:
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi. This is a stubbed chatbot UI. Ask me anything to test the interface."}
        ]
    if "last_debug" not in st.session_state:
        st.session_state.last_debug = {}

def answer(user_message: str, chat_history: list[dict], settings: dict) -> tuple[str, dict]:
    """
    Stub backend. Later, replace this with your RAG/fine-tune call.
    Returns: (assistant_text, debug_payload)
    """
    t0 = time.time()

    mode = settings.get("mode", "Stub")
    top_k = settings.get("top_k", 5)

    if mode == "RAG (coming soon)":
        assistant_text = (
            "RAG mode is not wired yet. This is still a stub response.\n\n"
            f"You said: {user_message}\n\n"
            f"(Planned settings: top_k={top_k})"
        )
        retrieved = []
    else:
        assistant_text = f"Stub response:\n\nYou said: {user_message}"
        retrieved = []

    debug = {
        "mode": mode,
        "top_k": top_k,
        "history_len": len(chat_history),
        "retrieved_chunks": retrieved,
        "latency_ms": round((time.time() - t0) * 1000, 1),
    }
    return assistant_text, debug


def main() -> None:
    init_state()

    st.title(APP_TITLE)
    st.caption(APP_SUBTITLE)

    with st.sidebar:
        st.header("Test Controls")

        mode = st.selectbox("Mode", ["Stub", "RAG (coming soon)"], index=0)
        top_k = st.slider("Top-k (for RAG)", min_value=1, max_value=20, value=5, step=1)
        show_debug = st.toggle("Show debug", value=False)

        if st.button("Reset chat", use_container_width=True):
            st.session_state.messages = [
                {"role": "assistant", "content": "Chat reset. Ask me anything to test the interface."}
            ]
            st.session_state.last_debug = {}
            st.rerun()

    settings = {"mode": mode, "top_k": top_k}

    # Render chat history
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    # Input
    user_message = st.chat_input("Type your message...")
    if user_message:
        st.session_state.messages.append({"role": "user", "content": user_message})
        with st.chat_message("user"):
            st.markdown(user_message)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                assistant_text, debug = answer(
                    user_message=user_message,
                    chat_history=st.session_state.messages,
                    settings=settings,
                )
                st.markdown(assistant_text)
                st.session_state.last_debug = debug

        st.session_state.messages.append({"role": "assistant", "content": assistant_text})

    if show_debug and st.session_state.last_debug:
        st.divider()
        st.subheader("Debug")
        st.json(st.session_state.last_debug)


if __name__ == "__main__":
    main()

