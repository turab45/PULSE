from state import ChatState
from llm import get_chat_model

def chat_node(state: ChatState):
    # get all user messages from the state
    user_quries = state["messages"]
    # get the model
    model = get_chat_model()
    # invoke the model with the user messages
    model_response = model.invoke(user_quries)

    return {
        "messages": [model_response]
        }