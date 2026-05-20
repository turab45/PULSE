from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableConfig

from src.config import gap_detector_prompt_str, get_chat_model
from src.utils.parsers import parse_gaps

prompt_template = ChatPromptTemplate.from_messages([
    ("system", gap_detector_prompt_str),
    MessagesPlaceholder("messages"),
])


def _chain():
    return prompt_template | get_chat_model()


def gap_detector_node(state: dict, config: RunnableConfig | None = None) -> dict:
    """LangGraph node: identify care gaps from SOAP note and transcript."""
    response = _chain().invoke({"messages": state["messages"]}, config)
    content = response.content.strip()
    return {
        "messages": [AIMessage(content=content, name="gap_detector")],
        "care_gaps": parse_gaps(content),
    }
