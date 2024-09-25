import os
import streamlit as st
import openai
from streamlit_chat import message
from openai import AzureOpenAI
import datetime
import json
st.set_page_config(layout="centered", page_title="Project: Toastmasters Table Topics Generator")
st.title("Toastmasters 'Table Topic' Questions Generator")
st.write("Table Topics® is a long-standing Toastmasters tradition intended to \
            help members develop their ability to organize their thoughts quickly and \
            respond to an impromptu question or topic.")

st.write("I created this app as occassionally I do not have time to prepare 10+ creative\
          questions surrounding a particular theme to ask fellow Toastmasters during the meeting.")

st.write("This app is an Azure OpenAI instance of gpt-35-turbo, that is then set as a page in the larger\
         Streamlit portfolio. The portfolio is containerized with Docker and runs on an Azure cloud compute\
          instance.")

key = os.getenv('API_KEY')
endpoint = os.getenv('endpoint')
deployment_name = os.getenv('deployment_name')

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