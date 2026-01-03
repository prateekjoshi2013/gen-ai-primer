from agents import Agent,Runner

hello_agent = Agent( 
    name="HelloAgent",
    instructions="You are a friendly assistant that greets users with emojis in funny way.",
)
response = Runner.run_sync(hello_agent, "Say hello to me !") # run_sync is a blocking call
print(response)