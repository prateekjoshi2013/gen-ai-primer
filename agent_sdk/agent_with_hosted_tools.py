from agents import Agent, Runner, WebSearchTool

hello_agent = Agent(
    name="HelloAgent",
    instructions="You are a friendly assistant that greets users with emojis in funny way.",
    tools=[
        WebSearchTool() # Adding a web search tool to the agent which is tool created by openai
    ],
)
response = Runner.run_sync(hello_agent, "can you find the documentation on vscode devcontainers tutorial which is user friendly and not too official")  # run_sync is a blocking call
print(response)
