import streamlit as st
from graph import build_graph
from langchain_core.messages import HumanMessage

CONFIG = {
        "configurable": {
            "thread_id": '1'
        }
    }

if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

for message in st.session_state["message_history"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Type your message here...")

if user_input:
    
    st.session_state["message_history"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    llm_response = build_graph().invoke({"messages": [HumanMessage(content=user_input)]}, config=CONFIG)
    st.session_state["message_history"].append({"role": "assistant", "content": llm_response["messages"][-1].content})
    with st.chat_message("assistant"):
        st.markdown(llm_response["messages"][-1].content)