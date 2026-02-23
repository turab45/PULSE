from graph import build_graph
from langchain_core.messages import HumanMessage

if __name__ == "__main__":


    thread_id = '1'

    while True:

        user_input = input("Type your message (or 'quit' to exit): ")
        if user_input.strip().lower() in ["quit", "exit", "bye", "q"]:
            break

        graph = build_graph()

        user_message = HumanMessage(content=user_input)

        # Print the user message
        user_message.pretty_print()

        config = {
            "configurable": {
                "thread_id": thread_id
            }
        }

        response = graph.invoke({"messages": [user_message]}, config=config)

        # Print the model response
        response["messages"][-1].pretty_print()
    
        