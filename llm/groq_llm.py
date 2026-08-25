import os
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()


def get_llm():
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        try:
            api_key = st.secrets["GROQ_API_KEY"]
        except Exception:
            api_key = None

    if not api_key:
        raise ValueError("GROQ_API_KEY is not configured in .env or Streamlit secrets.")

    # Primary unblocked model on your Groq project
    llm = ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0.2,
        api_key=api_key,
        max_tokens=1500
    )

    return llm