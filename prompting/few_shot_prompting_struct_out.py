# Using openai client to use Gemini via OpenAI-compatible API
from openai import OpenAI

# needs the OPENAI_API_KEY environment variable set
client = OpenAI()


SYSTEM_PROMPT = """
You are a code assistant and only answer coding-related questions, do not answer non coding questions.
Your name is CodeBuddy and return answer in the below format.

Output format : {{"code": str or null,"isCodingQuestion": boolean}}

Examples:
Q: Can You tell me a joke?
A: {{"code": null,"isCodingQuestion": false}}
Q: Can You tell me a python code to reverse a string?
A: {{"code": "python\ndef reverse_string(s):\n\treturn s[::-1]","isCodingQuestion": true}}
"""      

response1 = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "Can You tell me a joke?"},
    ],
)

print(response1.choices[0].message)

response2 = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "Can You tell me a python code to reverse a string?"},
    ],
)

print(response2.choices[0].message)

response3 = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "Can You tell me a python code to add two numbers?"},
    ],
)

print(response3.choices[0].message)
