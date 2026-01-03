from time import time
from typing import Annotated
from marshmallow import pprint
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.mongodb import MongoDBSaver

llm = init_chat_model(
    model="mistral:7b",
    model_provider="ollama",
    base_url="http://ollama:11434",
)
# llm = init_chat_model(
#     model="gpt-4.1-mini",
#     model_provider="openai",
# )

# Connection string with authentication and correct hostname
DB_URI = "mongodb://admin:admin@mongodb:27017/devdb?authSource=admin"


class State(TypedDict):
    # The list of messages in the chat history Annotated with the add_messagesfunction
    # that will manage adding messages to the state when the graph is executed.
    messages: Annotated[list, add_messages]


def chatbot(state: State) -> State:
    # Here you can implement the logic for the chatbot using the messages in the state.
    # For example, you could call an LLM to generate a response based on the chat history.
    # and on returning because of the Annotated type, new messages will be added to state['messages']
    response = llm.invoke(state["messages"])
    return {"messages": [response]}


def samplenode(state: State) -> State:
    # A sample node function that processes the state.
    return {"messages": ["Sample mesage from Sample Node."]}


graph_builder = StateGraph(State)
graph_builder.add_node("chatbot_node", chatbot)
graph_builder.add_node("sample_node", samplenode)

graph_builder.add_edge(START, "chatbot_node")
graph_builder.add_edge("chatbot_node", "sample_node")
graph_builder.add_edge("sample_node", END)

# Example configuration for checkpointing this saves all messages under a specific thread_id
config = {
    "configurable": {
        # thread_id for the entire conversation to maintain context
        "thread_id": f"prateek-{time()}"
    }
}
# Create MongoDB checkpoint saver once, outside the loop
with MongoDBSaver.from_conn_string(DB_URI) as checkpointer:
    # Compile graph with checkpointer to enable state persistence
    graph_with_checkpointer = graph_builder.compile(checkpointer=checkpointer)
    # Infinite loop to continuously accept user input
    while True:
        # Prompt user for input message
        query = input("Enter your message (or 'exit' to quit): 👉 ")
        # Check if user wants to exit the conversation
        if query.lower() == "exit":
            break  # Exit the while loop

        # Stream execution results chunk by chunk as they're generated
        for chunk in graph_with_checkpointer.stream(
            # Pass only the new user message, checkpointer loads previous history
            # stream_mode="values" returns state updates
            {"messages": [("user", query)]},
            config,
            stream_mode="values",
        ):
            # Access the last message in the chunk and print it in a formatted way
            chunk["messages"][-1].pretty_print()
