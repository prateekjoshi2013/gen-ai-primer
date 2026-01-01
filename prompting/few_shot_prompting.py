# Using openai client to use Gemini via OpenAI-compatible API
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY", ""),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

SYSTEM_PROMPT = """
You are a code assistant and only answer coding-related questions, do not answer non coding questions.
Your name is CodeBuddy and if user asks non coding related questions jus say sorry.

Examples:
Q: Can You tell me a joke?
A: Sorry, I can only assist with coding-related questions.
Q: Can You tell me a python code to reverse a string?
A: Sure! Here is a Python code snippet to reverse a string:
```python
def reverse_string(s):
    return s[::-1]
print(reverse_string("Hello, World!"))
```      
"""

response1 = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "Can You tell me a joke?"},
    ],
)

print(response1.choices[0].message)

response2 = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "Can You tell me a python code to reverse a string?"},
    ],
)

print(response2.choices[0].message)
