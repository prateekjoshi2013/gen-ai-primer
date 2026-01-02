# Using openai client to use Gemini via OpenAI-compatible API
import json
from openai import OpenAI

# needs the OPENAI_API_KEY environment variable set
client = OpenAI()


SYSTEM_PROMPT = """
You are an expert AI assistant in resolving user queries using chan of thhoughts.
You work on START, PLAN and OUTOUT structure to break down complex problems.
You need to first PLAN what needs to be done.The PLAN can be multiple steps.
Once you think enough PLAN has been done, you will OUTPUT the final answer.

Rules:
- Strictly follow the given JSON output format.
- Only run one step at a time.
- The sequence of steps is START (where user gives query), PLAN (where you plan the steps), OUTPUT (where you give final answer).

Example:

START: Hey, Can you solve 2 + 3 * 5 / 10
PLAN: {"step": "PLAN" , "content": "Seems like user us interested in math problem" }
PLAN: {"step": "PLAN" , "content": "According to BODMAS, we need to first do multiplication and division before addition" }
PLAN: {"step": "PLAN" , "content": "So first we do 3 * 5 = 15" }
PLAN: {"step": "PLAN" , "content": "Next we do 15 / 10 = 1.5" }
PLAN: {"step": "PLAN" , "content": "Finally we do 2 + 1.5 = 3.5" }
OUTPUT: {"step": "OUTPUT" , "content": "The final answer is 3.5" }
"""

message_history = []
user_input = input("User: 👉 ")
message_history.extend(
    [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"{user_input}"},
    ]
)

while message_history:

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=message_history,
    )

    result = response.choices[0].message.content
    message_history.append({"role": "assistant", "content": result})
    parsed_result = json.loads(result)
    if parsed_result["step"] == "START":
        print(f"🔥 : {parsed_result['content']}")
    elif parsed_result["step"] == "PLAN":
        print(f"🧠 : {parsed_result['content']}")
    elif parsed_result["step"] == "OUTPUT":
        print(f"✅ : {parsed_result['content']}")
        break
