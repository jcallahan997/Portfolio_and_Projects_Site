import os
import streamlit as st
from openai import AzureOpenAI

LLM_API_KEY = os.getenv('API_KEY')
LLM_ENDPOINT = os.getenv('endpoint')
DEPLOYMENT_NAME = os.getenv('deployment_name')

endpoint = os.getenv("ENDPOINT_URL", LLM_ENDPOINT)
deployment = os.getenv("DEPLOYMENT_NAME", DEPLOYMENT_NAME)
subscription_key = os.getenv("AZURE_OPENAI_API_KEY", LLM_API_KEY)


def create_chat_completion(endpoint, subscription_key, deployment, messages):
    # Initialize Azure OpenAI client with key-based authentication
    client = AzureOpenAI( 
        azure_endpoint = endpoint,
        api_key = subscription_key,
        api_version = "2024-05-01-preview",
    )

    completion = client.chat.completions.create(
        model=deployment,
        messages= [
        {
            "role": "system",
            "content": "You are an AI assistant that helps people find information."
        }
    ],
        past_messages=10,
        max_tokens=800,
        temperature=0.7,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
        stream=False
    )

    print(completion.to_json())

