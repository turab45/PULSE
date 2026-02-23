from state import ChatState
from nodes import chat_node
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver,  MemorySaver

# Persistence for the graph state
checkpoint_saver = MemorySaver()

def build_graph():
    graph = StateGraph(ChatState)

    # Add nodes to the graph
    graph.add_node("chat_node", chat_node)

    # Add edges to define the flow of the graph
    graph.add_edge(START, "chat_node")
    graph.add_edge("chat_node", END)

    return graph.compile(checkpointer=checkpoint_saver)



