from time import time
from httpcore import request
from mem0 import Memory
from ollama import Client
import os


config = {
    "version": "v1.1",
    "llm": {
        "provider": "ollama",
        "config": {
            "model": "mistral:7b",
            "ollama_base_url": "http://ollama:11434",
            "temperature": 0.1,  # Lower temperature for more consistent JSON output
        },
    },
    "embedder": {
        "provider": "ollama",
        "config": {"model": "nomic-embed-text", "ollama_base_url": "http://ollama:11434"},
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": "qdrant",
            "port": 6333,
            "collection_name": "mem0_ollama",
            "embedding_model_dims": 768,
        },
    },
}

client = Client(
    host="http://ollama:11434",
)

mem_client = Memory.from_config(config)
user_id = "prateek" + str(time())  # Fixed user ID to persist memories across runs
while True:
    user_query = input("Enter your message: ")
    if user_query.lower() == "exit" or user_query.lower() == "e":
        break
    search_memory = mem_client.search(user_id=user_id, query=user_query)
    print("Retrieved Memories:\n", search_memory["results"])
    memories = "\n".join(
        [f"- Memory {i+1}: {mem['memory']}" for i, mem in enumerate(search_memory["results"])]
    )
    response = client.chat(
        model="mistral:7b",
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

    ai_response = response.message.content

    print("AI:", ai_response)

    # Add memory with error handling for JSON parsing issues
    try:
        mem_client.add(
            user_id=user_id,
            messages=[
                {"role": "user", "content": user_query},
                {"role": "assistant", "content": ai_response},
            ],
        )
        print("Memory has been updated with the conversation.")
    except Exception as e:
        print(f"Warning: Could not update memory: {e}")
        # Optionally, manually add as a simple fact
        try:
            mem_client.add(
                user_id=user_id,
                data=user_query + " " + ai_response,
            )
            print("Memory updated using fallback method.")
        except:
            print("Memory update failed completely.")

    print("Memory has been updated with the conversation.")
