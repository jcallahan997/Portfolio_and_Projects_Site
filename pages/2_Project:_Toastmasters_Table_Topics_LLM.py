import os
import streamlit as st
import openai
from streamlit_chat import message
from openai import AzureOpenAI
import datetime
import json
from dotenv import load_dotenv
load_dotenv()
st.set_page_config(layout="centered", page_title="Project: Toastmasters Table Topics Generator")
st.title("Toastmasters 'Table Topic' Questions Generator")
st.write("Table Topics® is a long-standing Toastmasters tradition intended to \
            help members develop their ability to organize their thoughts quickly and \
            respond to an impromptu question or topic.")

st.write("I created this app as occassionally I do not have time to prepare 10+ creative\
          questions surrounding a preselected theme to ask fellow Toastmasters during the meeting.")

st.write("This app is an Azure OpenAI instance of gpt-35-turbo, that is then set as a page in the larger\
         Streamlit portfolio. The portfolio is containerized with Docker and runs on an Azure cloud compute\
          instance.")


key = os.getenv('API_KEY')
endpoint = os.getenv('endpoint')
deployment_name = os.getenv('deployment_name')


# Set OpenAI configuration settings
openai.api_type = "azure"
openai.api_base = endpoint
openai.api_version = "2024-05-01-preview"
openai.api_key = key

def create_chat_completion(deployment_name, messages, endpoint, key):
    client = openai.AzureOpenAI(
        api_key=key,
        api_version="2024-05-01-preview",
        azure_endpoint = endpoint
    )
    # Create and return a new chat completion request
    return client.chat.completions.create(
        model=deployment_name,
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in messages
        ],
        stream=True
    )

def create_chat_with_data_completion(deployment_name, messages, endpoint, key):
    client = openai.AzureOpenAI(
        api_key=key,
        api_version="2024-05-01-preview",
        azure_endpoint=endpoint
    )
    # Create and return a new chat completion request
    return client.chat.completions.create(
        model=deployment_name,
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in messages
        ],
        stream=True,
        extra_body={
            "data_sources": [
                {
                    "type": "azure_search",
                    "parameters": {
                        "authentication": {
                            "type": "api_key",
                        }
                    }
                }
            ]
        }
    )


def handle_chat_prompt(prompt, deployment_name, endpoint, key, model_type):
    # Echo the user's prompt to the chat window
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Send the user's prompt to Azure OpenAI and display the response
    # The call to Azure OpenAI is handled in create_chat_completion()
    # This function loops through the responses and displays them as they come in.
    # It also appends the full response to the chat history.
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        if model_type == "Use base GPT-4 model":
            for response in create_chat_completion(deployment_name, st.session_state.messages, endpoint, key):
                if response.choices:
                    full_response += (response.choices[0].delta.content or "")
                    message_placeholder.markdown(full_response + "▌")
        else:
            for response in create_chat_with_data_completion(deployment_name, st.session_state.messages, endpoint, key):
                if response.choices:
                    full_response += (response.choices[0].delta.content or "")
                    message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})

def main():
    
    # model_type = st.sidebar.radio(label = "Select an Option", options = ["Use base GPT-4 model", "Use schema-aware GPT-4 model"])
    model_type = 'Use base GPT-4 model'
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    endpoint = os.getenv('endpoint')
    key = os.getenv('API_KEY')
    deployment_name = os.getenv('deployment_name')

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


    else:
        if ('transcription_results' in st.session_state):
            speech_contents = ' '.join(st.session_state.transcription_results)
            del st.session_state.transcription_results
            handle_chat_prompt(speech_contents, deployment_name, endpoint, key, model_type)

    # Await a user message and handle the chat prompt when it comes in.
    if prompt := st.chat_input("Enter a message:"):
        handle_chat_prompt(prompt, deployment_name, endpoint, key, model_type)

if __name__ == "__main__":
    main()

