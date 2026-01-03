from mem0 import Memory
from openai import OpenAI
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

config = {
    "version": "v1.1",
    "embedder": {
        "provider": "openai",
        "config": {"api_key": OPENAI_API_KEY, "model": "text-embedding-3-small"},
    },
    "llm": {"provider": "openai", "config": {"api_key": OPENAI_API_KEY, "model": "gpt-4.1-mini"}},
    "vector_store": {
        "provider": "qdrant",
        "config": {"host": "qdrant", "port": 6333},
    },
}

mem_client = Memory.from_config(config)


# needs the OPENAI_API_KEY environment variable set
client = OpenAI()

while True:
    user_query = input("Enter your message: ")
    if user_query.lower() == "exit" or user_query.lower() == "e":
        break
    search_memory = mem_client.search(user_id="prateek", query=user_query)
    print("Retrieved Memories:\n", search_memory['results'])
    memories = "\n".join(
        [f"- Memory {i+1}: {mem['memory']}" for i, mem in enumerate(search_memory["results"])]
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": f"""
            You are an AI assistant that helps users by utilizing their past memories.
            Use the following memories to provide contextually relevant responses to the user's queries.
            Memories:
            {memories}""",
            },
            {"role": "user", "content": user_query},
        ],
    )
    ai_response = response.choices[0].message.content

    print("AI:", ai_response)

    mem_client.add(
        user_id="prateek",
        messages=[
            {"role": "user", "content": user_query},
            {"role": "assistant", "content": ai_response},
        ],
    )

    print("Memory has been updated with the conversation.")
