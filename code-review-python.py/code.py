import streamlit as st
import google.generativeai as genai
import time
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="AI Python Code Reviewer",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 AI Python Code Reviewer")
st.write("Submit your Python code for an automated review and receive a bug report with suggested fixes.")

API_KEY = os.getenv("AIzaSyDpglMCYn9pQO7A1oP_bXcesgaE7f2nh-g")
if not API_KEY:
    st.error("\u26a0\ufe0f API Key not found. Please set it as an environment variable.")
    st.stop()

genai.configure(api_key=API_KEY)

PROMPTS = {
    "Standard Review": "...",
    "Performance Optimization": "...",
    "Security Analysis": "...",
    "Beginner Friendly": "..."
}

def code_review(code, review_type, model_version):
    try:
        model = genai.GenerativeModel(model_name=model_version)
        user_prompt = f"{PROMPTS[review_type]}\n\nReview the following Python code:\n\n```python\n{code}\n```"
        response = model.generate_content(user_prompt)
        return response.text.strip() if response.text else "\u26a0\ufe0f No response received from AI. Try again."
    except Exception as e:
        return f"\u26a0\ufe0f Error: {str(e)}"

col1, col2 = st.columns([3, 1])

with col2:
    model_version = st.selectbox("Select AI Model:", ["gemini-1.5-pro", "gemini-1.5-flash"])
    review_type = st.selectbox("Select Review Type:", list(PROMPTS.keys()))

with col1:
    code_input = st.text_area("Enter your Python code:", height=300, placeholder="Paste your Python code here...")
    if st.button("\ud83d\udd0d Review Code") and code_input.strip():
        st.markdown(code_review(code_input, review_type, model_version))

st.sidebar.info("AI Python Code Reviewer uses Google's Gemini AI to analyze Python code.")
