# def generate_fix(parsed_issue):
#     return "def function(x): return x + 1  # sample fix"

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Added the function here.
# def clean_code(text):
#     return text.replace("```python", "").replace("```", "").strip()

def clean_code(text):
    text = text.replace("```python", "").replace("```", "")
    text = text.replace(")", ")")  # basic safety
    return text.strip()

def generate_fix(parsed_issue):
    prompt = f"""
    You are a senior Python Developer.

    A bug is reported:
    {parsed_issue['description']}
    
    The function must return the absolute value of x.
    Rules: 
    - For negative x, return -x
    - For positive x, return x
    - For zero, return 0
    - Do NOT use recursion
    - Return ONLY valid Python code
    - NO comments
    - NO explanation
    - NO markdown
    - Code must be clean and complete.


    Output format:
    def function(x):
        ...
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    return clean_code(response.choices[0].message.content)



