from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableConfig

from src.config import get_chat_model, reviewer_prompt_str
from src.utils.parsers import parse_review_status

prompt_template = ChatPromptTemplate.from_messages([
    ("system", reviewer_prompt_str),
    MessagesPlaceholder("messages"),
])


def _chain():
    return prompt_template | get_chat_model()


def reviewer_node(state: dict, config: RunnableConfig | None = None) -> dict:
    """LangGraph node: review care interventions based on identified gaps."""
    response = _chain().invoke({"messages": state["messages"]}, config)
    content = response.content.strip()
    return {
        "messages": [AIMessage(content=content, name="reviewer")],
        "final_report": content,
        "review_status": parse_review_status(content),
    }
