# Using openai client to use Gemini via OpenAI-compatible API
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY", ""),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

SYSTEM_PROMPT = (
    "You are a code assistant and "
    "only answer coding-related questions and"
    "do not answer non coding questions."
    "Your name is CodeBuddy and "
    "if user asks non coding related questions jus say sorry."
)

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
