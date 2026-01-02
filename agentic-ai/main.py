# Using openai client to use Gemini via OpenAI-compatible API
import json
from typing import Optional
from openai import OpenAI
import requests
from pydantic import BaseModel, Field
from os import system

# needs the OPENAI_API_KEY environment variable set
client = OpenAI()


class MyOutputFormat(BaseModel):
    step: str = Field(..., description="One of START, PLAN, OUTPUT, TOOL, RESULT")
    content: Optional[str] = Field(None, description="Optional string content of the step")
    tool: Optional[str] = Field(None, description="Optional string only for TOOL and RESULT steps")
    input: Optional[str] = Field(None, description="Optional string only for TOOL steps")


def run_command(command: str) -> str:
    try:
        output = system(command)
        return str(output)
    except Exception as e:
        return f"Error executing command: {e}"


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
2. run_command(command: str): executes a command on the host os and returns the result back in string.

Output JSON format:
{"step": "START" | "PLAN" | "OUTPUT" | "TOOL" | "RESULT", "content": "<CONTENT>"}

IMPORTANT FOR TOOL STEPS:
- When step is TOOL, you MUST include the tool name in the "tool" field
- You MUST include the input parameter (city name or command) in the "content" field
- Example: {"step": "TOOL", "tool": "get_weather", "content": "Moscow"}

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
TOOL: {"step": "TOOL" , "tool": "get_weather", "content": "Delhi" }
RESULT: {"step": "RESULT" , "tool": "get_weather", "content": "Its raining heavily today with temperature around 25°C" }
PLAN: {"step": "PLAN" ,  "content": "Got the weather details of Delhi" }
OUTPUT: {"step": "OUTPUT" , "content": "The weather in Delhi today is: Its raining heavily today with temperature around 25°C" }
"""
tools = {"get_weather": get_weather, "run_command": run_command}


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

            response = client.chat.completions.parse(
                model="gpt-4o",
                response_format=MyOutputFormat,
                messages=message_history,
            )

            result = response.choices[0].message.parsed
            print(f"🏹 {result}")
            if result.step == "START":
                print(f"🔥 : {result.content}")
                message_history.append(
                    {"role": "assistant", "content": json.dumps(result.model_dump())}
                )
            elif result.step == "PLAN":
                print(f"🤖 : {result.content}")
                message_history.append(
                    {"role": "assistant", "content": json.dumps(result.model_dump())}
                )
            elif result.step == "TOOL":
                print(f"🔧 : Calling tool {result.tool} with content: {result.content}")
                if result.tool == "get_weather":
                    city = result.content
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
                elif result.tool == "run_command":
                    command = result.content
                    tool_result = run_command(command)
                    message_history.append(
                        {
                            "role": "assistant",
                            "content": json.dumps(
                                {
                                    "step": "RESULT",
                                    "tool": "run_command",
                                    "content": tool_result,
                                }
                            ),
                        }
                    )
                    # Add a user message to prompt the model to continue
                    message_history.append(
                        {
                            "role": "user",
                            "content": "Continue with the next step.",
                        }
                    )
            elif result.step == "OUTPUT":
                print(f"✅ : {result.content}")
                message_history.clear()  # Exit the inner loop to ask new user input


main()
