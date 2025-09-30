import streamlit as st
from langgraph_backend import graph
from langchain_core.messages import HumanMessage, AIMessage

st.set_page_config(page_title="Friesland Campina pre-sales ChatBot", layout="wide")

# -----------------------------
# Top bar layout
# -----------------------------
col1, col2, col3 = st.columns([0.2, 0.6, 0.2])

with col1:
    pass  # left empty

with col2:
    st.markdown("<h1 style='text-align: center;'>💬 Friesland Campina ChatBot</h1>", unsafe_allow_html=True)

with col3:
    btn_col1, btn_col2 = st.columns([0.5, 0.5])
    with btn_col1:
        if st.button("🆕 New Chat"):
            st.session_state["message_history"] = []
    with btn_col2:
        if st.button("⚙️ Settings"):
            st.sidebar.header("Settings")
            st.sidebar.text("Configure your chatbot here")
            model_choice = st.sidebar.selectbox("Select Model", ["gpt-4o", "gpt-3.5-turbo"])
            st.sidebar.write(f"Selected model: {model_choice}")

# -----------------------------
# Initialize session state
# -----------------------------
if "message_history" not in st.session_state:
    st.session_state["message_history"] = []


# -----------------------------
# Display previous messages
# -----------------------------
for msg in st.session_state["message_history"]:
    if msg["role"] == "user":
        with st.chat_message("user", avatar="👤"):
            st.markdown(msg["content"])
    else:
        with st.chat_message("assistant", avatar="✨"):
            st.markdown(msg["content"])

# -----------------------------
# User input
# -----------------------------
# user_input = st.chat_input("Type here...")
user_input = st.chat_input("👤 Type here...") 

if user_input:
    # Add user message
    st.session_state["message_history"].append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)

    # Prepare conversation for backend
    history_messages = []
    for msg in st.session_state["message_history"]:
        if msg["role"] == "user":
            history_messages.append(HumanMessage(content=msg["content"]))
        else:
            history_messages.append(AIMessage(content=msg["content"]))

    # Call backend graph
    CONFIG = {"configurable": {"thread_id": "session-1"}}
    response = graph.invoke({"messages": history_messages}, config=CONFIG)
    ai_message = response["messages"][-1].content

    # Add AI response
    st.session_state["message_history"].append({"role": "assistant", "content": ai_message})
    with st.chat_message("assistant", avatar="✨"):
        st.markdown(ai_message)

