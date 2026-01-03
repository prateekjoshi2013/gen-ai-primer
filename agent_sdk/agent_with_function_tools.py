from agents import Agent, Runner, WebSearchTool, function_tool
import requests


@function_tool()
def get_weather(city: str):
    """
    Get the current weather for a given city.

    :param city: Name of the city to get the weather for.
    :return: A string describing the current weather.
    """
    response = requests.get(f"https://wttr.in/{city}?format=%C+%t+%w+%h+%p&lang=en")
    return response.text if response.status_code == 200 else "Could not retrieve weather data."


hello_agent = Agent(
    name="HelloAgent",
    instructions="You are a friendly assistant that greets users with emojis in funny way.",
    tools=[
        WebSearchTool(),  # Adding a web search tool to the agent which is tool created by openai
        get_weather,
    ],
)
response = Runner.run_sync(
    hello_agent,
    "can you find the documentation on vscode devcontainers tutorial which is user friendly and not too official",
)  # run_sync is a blocking call
print(response)
response = Runner.run_sync(
    hello_agent,
    "get me weather for lahore chanfdigarh delhi",
)  # run_sync is a blocking call
print(response)
