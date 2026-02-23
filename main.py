from graph import build_graph

if __name__ == "__main__":
    initial_state = {
        "messages": [
            {"role": "user", "content": "What are the symptoms of COVID-19?"}
        ]
        }

    graph = build_graph()

    final_state = graph.invoke(initial_state)
    
    for message in final_state["messages"]:
        # use pretty print to display the messages
        message.pretty_print()