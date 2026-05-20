"""
Scribe agent: converts a clinical transcript into a structured SOAP note.
"""

from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableConfig

from src.config import get_chat_model, scribe_prompt_str
from src.utils.parsers import parse_soap

_scribe_prompt = ChatPromptTemplate.from_messages([
    ("system", scribe_prompt_str),
    MessagesPlaceholder("messages"),
])


def _chain():
    return _scribe_prompt | get_chat_model()


def scribe_node(state: dict, config: RunnableConfig) -> dict:
    """LangGraph node: generate a SOAP note from the clinical transcript."""
    response = _chain().invoke({"messages": state["messages"]}, config)
    content = response.content.strip()
    soap_note = parse_soap(content)
    if soap_note is None:
        raise ValueError("Scribe output did not include required SOAP sections: S, O, A, P.")

    return {
        "messages": [AIMessage(content=content, name="scribe")],
        "soap_note": soap_note,
    }
