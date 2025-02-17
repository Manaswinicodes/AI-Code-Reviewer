import streamlit as st
import sys
import subprocess

# Attempt to import openai, and if not available, try to install it automatically.
try:
    import openai
except ImportError:
    st.warning("The 'openai' package is not installed. Attempting to install it now...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "openai"])
        import openai
        st.success("'openai' package installed successfully!")
    except Exception as install_error:
        st.error(
            "Automatic installation failed. "
            "Please install it manually using 'pip install openai' and restart the app."
        )
        st.error(f"Error details: {install_error}")
        st.stop()  # Stop further execution if openai cannot be imported

# Set your OpenAI API key (consider using environment variables for security)
openai.api_key = 'your-api-key'

# Function to generate a detailed prompt based on the review type
def get_review_prompt(code, review_type):
    prompts = {
        'syntax': f"Review the following Python code for syntax errors and suggest corrections:\n\n{code}",
        'optimization': f"Review the following Python code and suggest performance optimizations:\n\n{code}",
        'best_practices': f"Review the following Python code and suggest improvements following Python best practices:\n\n{code}",
        'security': f"Review the following Python code for security vulnerabilities and provide suggestions to fix them:\n\n{code}"
    }
    return prompts.get(review_type, f"Please analyze the following Python code:\n\n{code}")

# Function to call the OpenAI API for code analysis
def analyze_code(code, review_type):
    try:
        prompt = get_review_prompt(code, review_type)
        response = openai.Completion.create(
            engine="text-davinci-003",  # Update to your desired engine
            prompt=prompt,
            max_tokens=500,
            temperature=0.5
        )
        analysis = response.choices[0].text.strip()
        return analysis
    except Exception as e:
        return f"An error occurred while analyzing the code: {e}"

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
        st.info("Analyzing code, please wait...")
        feedback = analyze_code(user_code, review_type)
        st.subheader("Feedback from AI:")
        st.write(feedback)
    else:
        st.error("Please paste some code to analyze.")
