import streamlit as st
from openai import OpenAI
from uuid import uuid4
import os

client = OpenAI()

VECTOR_STORE_ID = os.getenv("VECTOR_STORE_ID")

st.title("Telecom Billing Agent")

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
               "title" : "New Chat",
               "messages":[]
          }
     st.session_state.active_chat_id = chat_id

with st.sidebar:
     st.header("Chats")
     if st.button("New Chat", use_container_width=True):
          create_new_chat()
          st.rerun()
     st.divider()
     for chat_id, chat in st.session_state.chats.items():
          if st.button(chat["title"], key=f"btn_{chat_id}", use_container_width=True):
               st.session_state.active_chat_id = chat_id
               st.rerun()

active_chat = st.session_state.chats[st.session_state.active_chat_id]       

if not active_chat["messages"]:
    active_chat["messages"] = [
        {
            "role": "assistant",
            "content":"Select specific domains:<br/>1.Customer<br/>2.Accounts<br/>3.Bills"
        }
    ]

for message in active_chat["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"], unsafe_allow_html=True)
    
user_input = st.chat_input("Please specify your query")

if user_input:
    
    if active_chat["title"] == "New Chat":
        active_chat["title"] = user_input[:20] + "..." if len(user_input) > 20 else user_input
    active_chat["messages"].append({"role":"user", "content": user_input})
    with st.chat_message("user"):
            st.markdown(user_input)

    response = client.responses.create(
         model='gpt-5.6-luna', 
         input=user_input, 
         tools=[
        {
            "type": "file_search",
            "vector_store_ids": [VECTOR_STORE_ID]
        }])
    active_chat["messages"].append({"role":"assistant", "content": response.output_text})
    with st.chat_message("assistant"):
        st.markdown(response.output_text)
    
    