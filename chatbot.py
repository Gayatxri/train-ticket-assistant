import streamlit as st
import google.generativeai as genai

# ── Config ──────────────────────────────────────────────────────────────────
API_KEY = "AIzaSyAGn9lT5kMa0wuSnJOuWzK4R3BaONyGHfE"   # <-- paste your key here
KB_FILE = "trains_cleartrip.csv"
MODEL   = "gemini-2.5-flash"

SYSTEM_PROMPT = """You are a helpful train ticket assistant.
Use the knowledge base below to answer user questions about train bookings,
cancellations, refunds, and schedules.

Knowledge Base:
{kb}
"""

# ── Load KB once ─────────────────────────────────────────────────────────────
@st.cache_resource
def load_resources():
    with open(KB_FILE, "r") as f:
        kb = f.read()

    genai.configure(api_key=API_KEY)
    prompt = SYSTEM_PROMPT.format(kb=kb)
    gemini_model = genai.GenerativeModel(
        model_name=MODEL,
        system_instruction=prompt,
    )
    return gemini_model

# ── Page setup ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="Train Assistant", page_icon="🚆")
st.title("🚆 Train Ticket Assistant")
st.caption("Ask me anything about your train bookings, cancellations, or refunds.")

gemini_model = load_resources()

# ── Session state ─────────────────────────────────────────────────────────────
if "chat" not in st.session_state:
    st.session_state.chat = gemini_model.start_chat(history=[])

if "messages" not in st.session_state:
    st.session_state.messages = []   # list of {"role": ..., "content": ...}

# ── Render history ────────────────────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ── Input ─────────────────────────────────────────────────────────────────────
if user_input := st.chat_input("Type your question…"):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get Gemini response (same logic as notebook)
    with st.chat_message("assistant"):
        with st.spinner("Thinking…"):
            response = st.session_state.chat.send_message(user_input)
            reply = response.text
        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})