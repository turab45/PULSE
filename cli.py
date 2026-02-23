from graph import build_graph

if __name__ == "__main__":
    initial_state = {"runs": 120, "balls": 100, "fours": 10, "sixes": 5}

    graph = build_graph()

    final_state = graph.invoke(initial_state)
    print(final_state["summary"])
