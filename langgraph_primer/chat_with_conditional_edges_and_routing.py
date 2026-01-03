from typing import Annotated, Literal, Optional
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from openai import OpenAI
from ollama import Client

open_client = OpenAI()
ollama_client = Client(
    host="http://ollama:11434",
)


class State(TypedDict):
    user_query: str
    llm_output: Optional[str]
    is_good: Optional[bool]

# Ollama Chatbot node
def ollama_chatbot(state: State) -> State:
    response = ollama_client.chat(
        model="mistral:7b", messages=[{"role": "user", "content": state["user_query"]}]
    )
    state["llm_output"] = response.message.content
    print("Ollama Response:", state["llm_output"])
    return state

# Mini OpenAI Chatbot node
def openai_mini_chatbot(state: State) -> State:
    response = open_client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": state["user_query"]},
        ],
    )
    state["llm_output"] = response.choices[0].message.content
    print("OpenAI Mini Response:", state["llm_output"])
    return state

# Full OpenAI Chatbot node
def openai_chatbot(state: State) -> State:
    response = open_client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": state["user_query"]},
        ],
    )
    state["llm_output"] = response.choices[0].message.content
    print("OpenAI Chatbot Response:", state["llm_output"])
    return state

# Conditional edge function to evaluate response quality
def response_evaluator(state: State) -> Literal["openai_mini_chatbot", "endnode"]:
    response = open_client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {
                "role": "system",
                "content": f"""
                You are a response evaluator which evaluates whether RESPONSE to user QUERY is correct or not.
                Respond with True if RESPONSE is correct else respond with False.

                OUTPUT: 
                True | False
                
                EXAMPLE:
                
                QUERY: "what is capital of france"
                RESPONSE: "Paris is the capital of France."
                
                OUTPUT: True
                """,
            },
            {
                "role": "user",
                "content": f"""
                QUERY:{state["user_query"]}
                RESPONSE:{state["llm_output"]}
                """,
            },
        ],
    )
    evaluator_response = response.choices[0].message.content
    print("Evaluator Response:", evaluator_response)
    state["is_good"] = evaluator_response.strip().lower() == "true"
    return "endnode" if state["is_good"] else "openai_mini_chatbot"


def endnode(state: State) -> State:
    return state


graph_builder = StateGraph(State) # create the graph builder
graph_builder.add_node("ollama_chatbot", ollama_chatbot) # add Ollama chatbot node
graph_builder.add_node("openai_mini_chatbot", openai_mini_chatbot) # add OpenAI mini chatbot node
graph_builder.add_node("openai_chatbot", openai_chatbot) # add full OpenAI chatbot node
graph_builder.add_node("endnode", endnode) # add end node

graph_builder.add_edge(START, "ollama_chatbot") # edge from START to Ollama chatbot
graph_builder.add_conditional_edges("ollama_chatbot", response_evaluator) # conditional routing based on evaluator
graph_builder.add_edge("openai_mini_chatbot", "endnode")  # edge from mini chatbot to END
graph_builder.add_edge("endnode", END) # edge from END node to END
graph = graph_builder.compile() # compile the graph

while True:
    user_input = input("Enter your question (or 'exit' to quit): 👉 ")
    if user_input.lower() == "exit":
        break
    updated_state = graph.invoke(State({"user_query": user_input})) # invoke the graph with user input
    print("Updated State:", updated_state) # print the updated state
