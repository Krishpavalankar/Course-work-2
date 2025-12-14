import streamlit as st
from openai import OpenAI
import httpx

def get_ai_reply(prompt: str) -> str:
    client = OpenAI(
        api_key=st.secrets["OPENAI_API_KEY"],
        http_client=httpx.Client(verify=False)
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a cyber security assistant."},
            {"role": "user", "content": prompt},
        ],
    )

    return response.choices[0].message.content.strip()
