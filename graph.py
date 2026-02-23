from state import BatsmanState
from nodes import strike_rate_node, boundary_per_ball_node, boundary_percentage_node, summary_node
from langgraph.graph import StateGraph, START, END


def build_graph():
    graph = StateGraph(BatsmanState)

    graph.add_node("strike_rate", strike_rate_node)
    graph.add_node("boundary_per_ball", boundary_per_ball_node)
    graph.add_node("boundary_percentage", boundary_percentage_node)
    graph.add_node("summary", summary_node)

    graph.add_edge(START, "strike_rate")
    graph.add_edge(START, "boundary_per_ball")
    graph.add_edge(START, "boundary_percentage")

    graph.add_edge("strike_rate", "summary")
    graph.add_edge("boundary_per_ball", "summary")
    graph.add_edge("boundary_percentage", "summary")
    graph.add_edge("summary", END)

    return graph.compile()



