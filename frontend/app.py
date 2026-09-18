import streamlit as st
from uuid import uuid4
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.telecom_billing_agent_litellm_app import investigate_billing


st.title("Telecom Billing Agent")


# ---------------------------------------------------------
# Chat session management
# ---------------------------------------------------------

if "chats" not in st.session_state:
    st.session_state.chats = {
        "chat_1": {
            "title": "New Chat",
            "messages": []
        }
    }


if "active_chat_id" not in st.session_state:
    st.session_state.active_chat_id = "chat_1"


def create_new_chat():

    chat_id = str(uuid4())

    st.session_state.chats[chat_id] = {
        "title": "New Chat",
        "messages": []
    }

    st.session_state.active_chat_id = chat_id


# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------

with st.sidebar:

    st.header("Chats")

    if st.button(
        "New Chat",
        use_container_width=True
    ):
        create_new_chat()
        st.rerun()

    st.divider()

    for chat_id, chat in st.session_state.chats.items():

        if st.button(
            chat["title"],
            key=f"btn_{chat_id}",
            use_container_width=True
        ):
            st.session_state.active_chat_id = chat_id
            st.rerun()


# ---------------------------------------------------------
# Active chat
# ---------------------------------------------------------

active_chat = st.session_state.chats[
    st.session_state.active_chat_id
]


# ---------------------------------------------------------
# Welcome message
# ---------------------------------------------------------

if not active_chat["messages"]:

    active_chat["messages"] = [
        {
            "role": "assistant",
            "content": (
                "Welcome! I am your automated billing assistant. "
                "Please specify your query."
            )
        }
    ]


# ---------------------------------------------------------
# Display conversation
# ---------------------------------------------------------

for message in active_chat["messages"]:

    with st.chat_message(message["role"]):
        st.write(message["content"])


# ---------------------------------------------------------
# User input
# ---------------------------------------------------------

user_input = st.chat_input(
    "Please specify your query"
)


if user_input:

    # Create chat title
    if active_chat["title"] == "New Chat":

        active_chat["title"] = (
            user_input[:20] + "..."
            if len(user_input) > 20
            else user_input
        )

    # Store user message
    active_chat["messages"].append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.chat_message("user"):
        st.write(user_input)


    # -----------------------------------------------------
    # Call backend agent
    # -----------------------------------------------------

    assistant_response = investigate_billing(
        user_input
    )


    # Store assistant response
    active_chat["messages"].append(
        {
            "role": "assistant",
            "content": assistant_response
        }
    )


    # Display assistant response
    with st.chat_message("assistant"):
        st.write(assistant_response)