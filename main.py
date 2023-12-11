import streamlit as st
from langchain.prompts import MessagesPlaceholder
from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationSummaryBufferMemory
from langchain.callbacks import get_openai_callback
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory
import time
from tools import *
import os


api_key = st.secrets["OPENAI_API_KEY"]
# setting entrypoint page
st.set_page_config(
    page_title="Namaskar",
    page_icon="🙏",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Optionally, specify your own session_state key for storing messages
msgs = StreamlitChatMessageHistory()
agent_kwargs = {
    "extra_prompt_messages": [MessagesPlaceholder(variable_name="chat_history")],
}

llm = ChatOpenAI(temperature=0.3, model="gpt-3.5-turbo-1106", api_key=api_key)
memory = ConversationSummaryBufferMemory(
    llm=llm,
    memory_key="chat_history",
    chat_memory=msgs,
    return_messages=True,
    max_token_limit=350,
)


# Agent
agent_executor = initialize_agent(
    tools,
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    agent_kwargs=agent_kwargs,
    verbose=True,
    memory=memory,
)


st.title("Neuro Nexus")
## Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

## Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # a=agent_executor.invoke({"input": prompt})

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        with get_openai_callback() as cb:
            a = agent_executor.run(prompt)
            print(cb)

        assistant_response = a
        print(a)
        # Simulate stream of response with milliseconds delay
        for chunk in assistant_response.split(" "):
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": a})
