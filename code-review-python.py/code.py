import streamlit as st
import sys
import subprocess
import openai
import os

# Function to ensure openai package is installed
def install_openai():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "openai"])
    except subprocess.CalledProcessError as e:
        st.error(f"Failed to install 'openai' package. Error: {e}")
        st.stop()

# Ensure openai package is installed
try:
    import openai
except ImportError:
    st.warning("The 'openai' package is not installed. Attempting to install it now...")
    install_openai()
    # Reattempt to import after installation
    import openai
    st.success("'openai' package installed successfully!")

# Get OpenAI API key from environment variables
openai.api_key = os.getenv('OPENAI_API_KEY', 'your-api-key')

if openai.api_key == 'your-api-key':
    st.warning("API key is not set. Please set your OpenAI API key in environment variables.")

# Function to generate detailed review prompts based on review type
def get_review_prompt(code, review_type):
    prompts = {
        'syntax': f"Review the following Python code for syntax errors and suggest corrections:\n\n{code}",
        'optimization': f"Review the following Python code and suggest performance optimizations:\n\n{code}",
        'best_practices': f"Review the following Python code and suggest improvements following Python best practices:\n\n{code}",
        'security': f"Review the following Python code for security vulnerabilities and provide suggestions to fix them:\n\n{code}"
    }
    return prompts.get(review_type, f"Please analyze the following Python code:\n\n{code}")

# Function to analyze code using OpenAI API
def analyze_code(code, review_type):
    try:
        prompt = get_review_prompt(code, review_type)
        response = openai.Completion.create(
            engine="text-davinci-003",  # Update to your preferred engine
            prompt=prompt,
            max_tokens=500,
            temperature=0.5
        )
        analysis = response.choices[0].text.strip()
        return analysis
    except openai.error.OpenAIError as e:
        st.error(f"OpenAI API error: {e}")
        return None
    except Exception as e:
        st.error(f"An error occurred while analyzing the code: {e}")
        return None

# Streamlit app interface
st.title("AI-Powered Code Reviewer")

# Code input by the user
user_code = st.text_area("Paste your Python code here:")

# Review type selection
review_type = st.selectbox(
    "Select the type of review you want:",
    ("syntax", "optimization", "best_practices", "security")
)

# Button to submit the code for review
if st.button("Review Code"):
    if user_code:
        if openai.api_key == 'your-api-key':
            st.error("API key is not configured properly. Please set the OpenAI API key.")
        else:
            st.info("Analyzing code, please wait...")
            feedback = analyze_code(user_code, review_type)
            if feedback:
                st.subheader("Feedback from AI:")
                st.write(feedback)
            else:
                st.error("Failed to generate feedback.")
    else:
        st.error("Please paste some code to analyze.")
