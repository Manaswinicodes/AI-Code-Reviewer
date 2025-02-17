import streamlit as st
import os
from openai import OpenAI
from typing import Dict, Optional, Tuple
import time

class CodeReviewError(Exception):
    """Custom exception for code review errors"""
    pass

class AICodeReviewer:
    def __init__(self):
        self.client = self._initialize_openai()
        self.review_prompts = self._get_detailed_prompts()
        
    def _initialize_openai(self) -> OpenAI:
        """Initialize OpenAI client with error handling"""
        api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise CodeReviewError("OpenAI API key not found. Please set it in Streamlit secrets or environment variables.")
        return OpenAI(api_key=api_key)
    
    def _get_detailed_prompts(self) -> Dict[str, str]:
        """Define detailed prompts for each review type"""
        return {
            'syntax': """
                You are an expert Python code reviewer focusing on syntax and correctness.
                
                Analyze the following code and provide feedback in this structure:
                1. Syntax Issues:
                   - List each syntax error found
                   - Provide the corrected version
                   - Explain why the correction is needed
                
                2. Code Structure:
                   - Identify any structural issues
                   - Suggest improvements
                
                3. Corrected Code:
                   - Provide the complete corrected version
                
                Code to analyze:
                {code}
                """,
                
            'optimization': """
                You are a Python performance optimization expert.
                
                Analyze the following code and provide feedback in this structure:
                1. Performance Issues:
                   - Identify performance bottlenecks
                   - Explain why they impact performance
                   - Suggest specific optimizations
                
                2. Complexity Analysis:
                   - Provide time complexity analysis
                   - Suggest ways to improve complexity
                
                3. Memory Usage:
                   - Identify memory inefficiencies
                   - Suggest memory optimizations
                
                4. Optimized Code:
                   - Provide the optimized version with comments
                
                Code to analyze:
                {code}
                """,
                
            'best_practices': """
                You are a Python best practices and clean code expert.
                
                Analyze the following code and provide feedback in this structure:
                1. Code Style:
                   - PEP 8 compliance issues
                   - Naming conventions
                   - Code formatting
                
                2. Code Organization:
                   - Function/class structure
                   - Module organization
                   - Import statements
                
                3. Documentation:
                   - Docstring coverage
                   - Comment quality
                   - Type hints
                
                4. Improved Code:
                   - Provide the refactored version with comments
                
                Code to analyze:
                {code}
                """,
                
            'security': """
                You are a Python security expert.
                
                Analyze the following code and provide feedback in this structure:
                1. Security Vulnerabilities:
                   - List each vulnerability found
                   - Explain the potential risks
                   - Provide mitigation strategies
                
                2. Input Validation:
                   - Identify unsafe input handling
                   - Suggest secure alternatives
                
                3. Data Protection:
                   - Identify sensitive data exposure
                   - Suggest security best practices
                
                4. Secure Code:
                   - Provide the secured version with comments
                
                Code to analyze:
                {code}
                """
        }

    def analyze_code(self, code: str, review_type: str) -> Tuple[bool, str]:
        """
        Analyze code using OpenAI API with retry mechanism
        Returns: (success: bool, result: str)
        """
        max_retries = 3
        retry_delay = 1
        
        for attempt in range(max_retries):
            try:
                prompt = self.review_prompts[review_type].format(code=code)
                
                response = self.client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are an expert Python code reviewer. Provide detailed, actionable feedback."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=2000
                )
                
                return True, response.choices[0].message.content
                
            except Exception as e:
                if attempt == max_retries - 1:
                    return False, f"Failed to analyze code after {max_retries} attempts: {str(e)}"
                time.sleep(retry_delay)
                retry_delay *= 2

def main():
    st.set_page_config(
        page_title="Advanced AI Code Reviewer",
        page_icon="💻",
        layout="wide"
    )
    
    st.title("🤖 Advanced AI Code Reviewer")
    
    try:
        reviewer = AICodeReviewer()
        
        with st.expander("ℹ️ About this tool", expanded=False):
            st.markdown("""
                This advanced code reviewer analyzes your Python code using AI to provide detailed feedback on:
                - Syntax and correctness
                - Performance optimizations
                - Best practices and clean code
                - Security vulnerabilities
                
                Each analysis includes specific suggestions and corrected code examples.
            """)
        
        # Code input with syntax highlighting
        user_code = st.text_area(
            "📝 Paste your Python code here:",
            height=300,
            help="Paste the Python code you want to analyze"
        )
        
        # Review type selection with detailed descriptions
        review_options = {
            "syntax": "Identify syntax errors and suggest corrections",
            "optimization": "Analyze performance and suggest optimizations",
            "best_practices": "Check adherence to Python best practices and clean code principles",
            "security": "Identify security vulnerabilities and suggest fixes"
        }
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            review_type = st.selectbox(
                "Select Review Type:",
                options=list(review_options.keys()),
                format_func=lambda x: f"{x.title()} Review"
            )
            
            st.info(review_options[review_type])
            
            analyze_button = st.button("🔍 Analyze Code", use_container_width=True)
        
        with col2:
            if analyze_button:
                if not user_code.strip():
                    st.error("⚠️ Please paste some code to analyze.")
                    return
                
                with st.spinner("🤔 Analyzing your code... This may take a moment."):
                    success, feedback = reviewer.analyze_code(user_code, review_type)
                    
                    if success:
                        st.success("✅ Analysis complete!")
                        
                        # Display feedback in a structured way
                        feedback_container = st.container()
                        with feedback_container:
                            st.markdown("### 📊 Analysis Results")
                            st.markdown(feedback)
                            
                            # Add copy button for feedback
                            if st.button("📋 Copy Analysis to Clipboard"):
                                st.write("Analysis copied to clipboard!")
                                st.session_state['clipboard'] = feedback
                    else:
                        st.error(f"❌ {feedback}")
                        st.button("🔄 Retry Analysis")

    except CodeReviewError as e:
        st.error(f"⚠️ Configuration Error: {str(e)}")
    except Exception as e:
        st.error(f"❌ An unexpected error occurred: {str(e)}")
        st.button("🔄 Restart Application")

if __name__ == "__main__":
    main()
