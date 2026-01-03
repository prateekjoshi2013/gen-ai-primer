from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph


class State(TypedDict):
    # The list of messages in the chat history Annotated with the add_messagesfunction
    # that will manage adding messages to the state when the graph is executed.
    messages: Annotated[list, add_messages]


def chatbot(state: State) -> State:
    # Here you can implement the logic for the chatbot using the messages in the state.
    # For example, you could call an LLM to generate a response based on the chat history.
    # and on returning because of the Annotated type, new messages will be added to state['messages']
    return {"messages": ["Hi, this is a message from Chatbot Node."]}


def samplenode(state: State) -> State:
    # A sample node function that processes the state.
    return {"messages": ["Sample mesage from Sample Node."]}


graph_builder = StateGraph(State)
graph_builder.add_node("chatbot_node",chatbot)
graph_builder.add_node("sample_node", samplenode)