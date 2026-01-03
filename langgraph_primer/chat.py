import json
from typing import Annotated
from marshmallow import pprint
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model

llm = init_chat_model(
    model="gpt-4.1-mini",
    model_provider="openai",
)


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

graph = graph_builder.compile()

updated_state = graph.invoke(State({"messages": ["Hi my name is Prateek"]}))
print("Updated State:", updated_state)
