import os
import streamlit as st
import openai
from openai import AzureOpenAI
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

LLM_API_KEY = os.getenv('API_KEY')
LLM_ENDPOINT = os.getenv('endpoint')
DEPLOYMENT_NAME = os.getenv('deployment_name')


openai.api_type = "azure"
openai.api_base = LLM_ENDPOINT
openai.api_key = LLM_API_KEY
openai.api_version = "2024-05-01-preview"


st.title("ChatGPT-like clone")
