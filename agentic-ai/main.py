# Using openai client to use Gemini via OpenAI-compatible API
import json
from openai import OpenAI
import requests

# needs the OPENAI_API_KEY environment variable set
client = OpenAI()


def get_weather(city):
    response = requests.get(f"https://wttr.in/{city}?format=%C+%t+%w+%h+%p&lang=en")
    return response.text if response.status_code == 200 else "Could not retrieve weather data."


SYSTEM_PROMPT = """
You are an expert AI assistant in resolving user queries using chain of thoughts.
You work on START, PLAN and OUTPUT structure to break down complex problems.
You need to first PLAN what needs to be done.The PLAN can be multiple steps.
Once you think enough PLAN has been done, you will OUTPUT the final answer.
You can also call a tool if required from the list of available tools.
For every tool call , wait for the RESULT which is the output of the tool before proceeding further.

Rules:
- Strictly follow the given JSON output format.
- Only run one step at a time.
- The sequence of steps is:
    - START (where user gives query)
    - PLAN (where you plan the steps)
    - TOOL (where you call a tool)
    - RESULT (where you get the output of the tool)
    - OUTPUT (where you give final answer).

AVAILABLE TOOLS:
1. get_weather(city: str): returns the current weather information for a specified city as string.

Output JSON format:
{"step": "START" | "PLAN" | "OUTPUT" | "TOOL" | "RESULT", "content": "<CONTENT>"}

Example 1:

START: Hey, Can you solve 2 + 3 * 5 / 10
PLAN: {"step": "PLAN" , "content": "Seems like user us interested in math problem" }
PLAN: {"step": "PLAN" , "content": "According to BODMAS, we need to first do multiplication and division before addition" }
PLAN: {"step": "PLAN" , "content": "So first we do 3 * 5 = 15" }
PLAN: {"step": "PLAN" , "content": "Next we do 15 / 10 = 1.5" }
PLAN: {"step": "PLAN" , "content": "Finally we do 2 + 1.5 = 3.5" }
OUTPUT: {"step": "OUTPUT" , "content": "The final answer is 3.5" }

Example 2:

START: Hey, what's the weather like in Delhi today?
PLAN: {"step": "PLAN" , "content": "Seems like user is interested in getting weather details of a city" }
PLAN: {"step": "PLAN" , "content": "Check if there is a tool available for getting weather details" }
PLAN: {"step": "PLAN" , "content": "Found one tool : get_weather to get current weather information" }
PLAN: {"step": "PLAN" , "content": "Call get_weather with the specified city" }
PLAN: {"step": "TOOL" , "tool": "get_weather", "content": "Delhi" }
PLAN: {"step": "RESULT" , "tool": "get_weather", "content": "Its raining heavily today with temperature around 25°C" }
PLAN: {"step": "PLAN" ,  "content": "Got the weather details of Delhi" }
OUTPUT: {"step": "OUTPUT" , "content": "The weather in Delhi today is: Its raining heavily today with temperature around 25°C" }
"""
tools = {"get_weather": get_weather}


def main():
    while True:
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
            parsed_result = json.loads(result)
            if parsed_result["step"] == "START":
                print(f"🔥 : {parsed_result['content']}")
                message_history.append({"role": "assistant", "content": result})
            elif parsed_result["step"] == "PLAN":
                print(f"🤖 : {parsed_result['content']}")
                message_history.append({"role": "assistant", "content": result})
            elif parsed_result["step"] == "TOOL":
                print(
                    f"🔧 : Calling tool {parsed_result['tool']} with content: {parsed_result['content']}"
                )
                if parsed_result["tool"] == "get_weather":
                    city = parsed_result["content"]
                    tool_result = get_weather(city)
                    message_history.append(
                        {
                            "role": "assistant",
                            "content": json.dumps(
                                {
                                    "step": "RESULT",
                                    "tool": "get_weather",
                                    "content": tool_result,
                                }
                            ),
                        }
                    )
            elif parsed_result["step"] == "OUTPUT":
                print(f"✅ : {parsed_result['content']}")
                message_history.append({"role": "assistant", "content": result})
                message_history.clear()  # Exit the inner loop to ask new user input

main()