import json
import streamlit as st
from openai import OpenAI
from uuid import uuid4
from tools import TOOLS, execute_tool
from prompts import BILLING_AGENT_INSTRUCTIONS


client = OpenAI()

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
            "content":"Welcome! I am your automated billing assistant. Please specify your query."
        }
    ]

for message in active_chat["messages"]:
    with st.chat_message(message["role"]):
        st.text(message["content"])
    
user_input = st.chat_input("Please specify your query")

if user_input:
    
    if active_chat["title"] == "New Chat":
        active_chat["title"] = user_input[:20] + "..." if len(user_input) > 20 else user_input
    active_chat["messages"].append({"role":"user", "content": user_input})
    with st.chat_message("user"):
            st.write(user_input)

    response = client.responses.create(
         model='gpt-5.6-luna',
         instructions = BILLING_AGENT_INSTRUCTIONS,
         input=user_input, 
         tools = TOOLS)

    while True:
        tool_outputs = []

        for item in response.output:
            if item.type == "function_call":
                arguments = json.loads(item.arguments)

                result = execute_tool(
                    item.name,
                    arguments
                )

                tool_outputs.append({
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": json.dumps(result)
                })

        # No function call means the AI has produced its final answer
        if not tool_outputs:
            break

        response = client.responses.create(
            model="gpt-5.6-luna",
            instructions = BILLING_AGENT_INSTRUCTIONS,
            previous_response_id=response.id,
            input=tool_outputs,
            tools=TOOLS
        ) 
    
    active_chat["messages"].append({"role":"assistant", "content": response.output_text})
    with st.chat_message("assistant"):
        st.write(response.output_text)