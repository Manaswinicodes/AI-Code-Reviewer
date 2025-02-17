import openai
import streamlit as st

# Set API key for OpenAI
openai.api_key = 'your-api-key'

# Function to generate prompt based on review type
def get_review_prompt(code, review_type):
    prompts = {
        'syntax': f"Please analyze the following Python code for any syntax errors and suggest improvements:\n\n{code}",
        'optimization': f"Please analyze the following Python code and suggest optimizations for performance improvements:\n\n{code}",
        'best_practices': f"Please analyze the following Python code and suggest improvements according to Python best practices:\n\n{code}",
        'security': f"Please analyze the following Python code for any security vulnerabilities and provide suggestions:\n\n{code}"
    }
    return prompts.get(review_type, f"Please analyze the following Python code:\n\n{code}")

# Function to call AI model for code analysis
def analyze_code(code, review_type):
    try:
        prompt = get_review_prompt(code, review_type)
        response = openai.Completion.create(
            engine="text-davinci-003",  # Or use the preferred engine like GPT-4
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

# Code input by user
user_code = st.text_area("Paste your Python code here:")

# Review type selection
review_type = st.selectbox(
    "Select the type of review you want:",
    ("syntax", "optimization", "best_practices", "security")
)

# Button to submit code for review
if st.button("Review Code"):
    if user_code:
        st.write("Analyzing code...")
        feedback = analyze_code(user_code, review_type)
        st.subheader("Feedback from AI:")
        st.write(feedback)
    else:
        st.error("Please paste some code to analyze.")

