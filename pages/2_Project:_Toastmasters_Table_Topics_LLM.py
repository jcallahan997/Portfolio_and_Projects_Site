import os
import streamlit as st
from openai import AzureOpenAI
st.set_page_config(layout="centered")
st.header("Containerized Azure OpenAI instance of gpt-35-turbo")
st.title("Toastmasters 'Table Topic' Questions Generator")
st.write("Table Topics® is a long-standing Toastmasters tradition intended to \
            help members develop their ability to organize their thoughts quickly and \
            respond to an impromptu question or topic")

LLM_API_KEY = os.getenv('API_KEY')
LLM_ENDPOINT = os.getenv('endpoint')
DEPLOYMENT_NAME = os.getenv('deployment_name')

endpoint = os.getenv("ENDPOINT_URL", LLM_ENDPOINT)
deployment = os.getenv("DEPLOYMENT_NAME", DEPLOYMENT_NAME)
subscription_key = os.getenv("AZURE_OPENAI_API_KEY", LLM_API_KEY)

st.title("ChatGPT-like clone")

client = AzureOpenAI( 
        azure_endpoint = endpoint,
        api_key = subscription_key,
        api_version = "2024-05-01-preview",
    )

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "..."

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
        
    st.session_state.messages.append({"role": "assistant", "content": response})