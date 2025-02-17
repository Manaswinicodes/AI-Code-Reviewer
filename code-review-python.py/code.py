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

try:
    API_KEY = st.secrets["general"]["API_KEY"]
except:
    API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    st.error("⚠️ API Key not found. Please set it in `.streamlit/secrets.toml` or as an environment variable.")
    st.stop()

genai.configure(api_key=API_KEY)

PROMPTS = {
    "Standard Review": """You are an advanced Python code reviewer. Your task is to analyze the given Python code, 
identify potential bugs, logical errors, and areas of improvement, and suggest fixes.
                
Response Format:
1. **Issues Detected**: List any errors, inefficiencies, or improvements needed.
2. **Fixed Code**: Provide the corrected version of the code.
3. **Explanation**: Explain why the changes were made concisely.
If the code is already optimal, acknowledge it and suggest best practices.""",

    "Performance Optimization": """You are a Python performance optimization expert. Analyze the given code and suggest improvements
for better execution speed, memory usage, and algorithm efficiency.

Response Format:
1. **Performance Issues**: Identify code parts that could be optimized.
2. **Optimized Code**: Provide the optimized version of the code.
3. **Explanation**: Explain the performance benefits of each change.
4. **Benchmarks**: When possible, provide estimated performance improvements.""",

    "Security Analysis": """You are a Python security expert. Review the code for security vulnerabilities, injection risks,
improper error handling, insecure dependencies, and other security concerns.

Response Format:
1. **Security Vulnerabilities**: List all potential security issues found.
2. **Secure Code**: Provide the secure version of the code.
3. **Risk Assessment**: Rate each vulnerability's severity (Low/Medium/High).
4. **Explanation**: Explain why these changes improve security.""",

    "Beginner Friendly": """You are a patient Python instructor helping a beginner improve their code. Provide gentle and educational
feedback that helps them learn best practices while fixing their code.

Response Format:
1. **Learning Opportunities**: Identify areas where the code could be improved.
2. **Improved Code**: Provide a better version of the code with comments.
3. **Explanation**: Explain improvements in simple terms for a beginner.
4. **Additional Resources**: Suggest tutorials or documentation for concepts used."""
}

def code_review(code, review_type, model_version):
    try:
        model = genai.GenerativeModel(model_name=model_version)
        sys_prompt = PROMPTS[review_type]
        user_prompt = f"{sys_prompt}\n\nReview the following Python code:\n\n```python\n{code}\n```"
        
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        ]
        
        response = model.generate_content(
            user_prompt,
            safety_settings=safety_settings
        )
        
        if response.text:
            return response.text.strip()
        else:
            return "⚠️ No response received from AI. Try again."
    
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

col1, col2 = st.columns([3, 1])

with col2:
    st.subheader("Review Options")
    
    model_version = st.selectbox(
        "Select AI Model:",
        ["gemini-1.5-pro", "gemini-1.5-flash"],
        help="Pro offers more detailed analysis but may be slower. Flash is faster but may provide less detail."
    )
    
    review_type = st.selectbox(
        "Select Review Type:",
        list(PROMPTS.keys()),
        help="Choose the type of review you need"
    )
    
    with st.expander("📚 Example Code Snippets"):
        example_codes = {
            "Basic Function": """def calculate_average(numbers):
    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)""",
            
            "List Comprehension": """# Get even numbers
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
even_numbers = [x for x in numbers if x % 2 == 0]
print(even_numbers)""",

            "Error Handling": """def divide(a, b):
    try:
        result = a / b
    except:
        print("Error occurred")
        result = None
    return result"""
        }
        
        selected_example = st.selectbox("Choose an example:", list(example_codes.keys()))
        if st.button("Insert Example"):
            st.session_state.code_input = example_codes[selected_example]
            st.experimental_rerun()

with col1:
    if 'code_input' not in st.session_state:
        st.session_state.code_input = ""
    
    code_input = st.text_area(
        "Enter your Python code:",
        value=st.session_state.code_input,
        height=300,
        placeholder="Paste your Python code here...",
        key="code_area"
    )
    
    st.session_state.code_input = code_input
    
    review_button = st.button("🔍 Review Code", use_container_width=True)

if review_button:
    if code_input.strip():
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.text("Initializing review...")
        progress_bar.progress(10)
        time.sleep(0.5)
        
        status_text.text("Analyzing your code with Google AI...")
        progress_bar.progress(30)
        
        feedback = code_review(code_input, review_type, model_version)
        
        progress_bar.progress(90)
        status_text.text("Formatting results...")
        time.sleep(0.5)
        
        progress_bar.progress(100)
        status_text.text("Review complete!")
        time.sleep(0.5)
        
        progress_bar.empty()
        status_text.empty()
        
        if feedback:
            st.subheader("📋 Code Review Report")
            st.markdown(feedback)
            
            st.download_button(
                label="📥 Download Review Report",
                data=feedback,
                file_name="code_review_report.md",
                mime="text/markdown"
            )
    else:
        st.warning("⚠️ Please enter some Python code before submitting.")

st.markdown("---")
st.markdown("""
<div style='display: flex; justify-content: space-between; align-items: center;'>
    <p style='text-align: left; font-size: 14px;'>Powered by Google Gemini API</p>
    <p style='text-align: center; font-size: 16px;'>👨‍💻 Made by <b>Yashwanth</b></p>
    <p style='text-align: right; font-size: 14px;'>v1.2.0</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("About")
    st.info(
        """
        **AI Python Code Reviewer** uses Google's Gemini AI to analyze your Python code for:
        - Bugs and syntax errors
        - Performance issues
        - Security vulnerabilities
        - Style and best practices
        
        Simply paste your code, select the type of review you need, and get instant AI-powered feedback!
        """
    )
    
    st.subheader("How It Works")
    st.markdown(
        """
        1. Paste your Python code
        2. Select your review options
        3. Click "Review Code"
        4. Get detailed AI analysis
        """
    )
    
    st.subheader("Future Enhancements")
    st.markdown(
        """
        - Support for more programming languages
        - Code formatting and linting options
        - Direct GitHub integration
        - Customizable review criteria
        - Bulk code review for multiple files
        """
    )
    
    st.subheader("Feedback")
    st.markdown("Did you find this tool helpful? Let us know!")
    
    feedback_score = st.slider("Rate your experience (1-5):", 1, 5, 5)
    feedback_text = st.text_area("Suggestions for improvement:", height=100)
    
    if st.button("Submit Feedback"):
        st.success("Thanks for your feedback! We appreciate your input.")
