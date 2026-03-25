# def generate_tests(parsed_issue):
#     return """
# def test_function():
#     assert function(1) == 2
# """

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# ADDED THIS FUNCTION HERE (after imports)
# def clean_code(text):
#     return text.replace("```python", "").replace("```", "").strip()

def clean_code(text):
    text = text.replace("```python", "").replace("```", "")
    text = text.replace(")", ")")  # basic safety
    return text.strip()

def generate_tests(parsed_issue):
    prompt = f"""
    You are a Python Testing Expert.

    Based on this bug:
    {parsed_issue['description']}
    
    Write proper unit tests for an already implemented function function(x).

STRICT RULES:
- DO NOT redefine the function
- DO NOT create any new function
- Use unittest
- Use correct expected values:
    function(-5) = 5
    function(5) = 5
    function(0) = 0
- NO strings unless necessary
- NO comments
- NO markdown

Output format:
import unittest

class TestFunction(unittest.TestCase):
    def test_positive(self):
        ...
    
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    return clean_code(response.choices[0].message.content)