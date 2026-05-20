from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableConfig

from src.config import get_chat_model, planner_prompt_str
from src.utils.parsers import parse_plan

prompt_template = ChatPromptTemplate.from_messages([
    ("system", planner_prompt_str),
    MessagesPlaceholder("messages"),
])


def _chain():
    return prompt_template | get_chat_model()


def planner_node(state: dict, config: RunnableConfig | None = None) -> dict:
    """LangGraph node: plan care interventions based on identified gaps."""
    response = _chain().invoke({"messages": state["messages"]}, config)
    content = response.content.strip()
    follow_up_plan = parse_plan(content)
    if follow_up_plan is None:
        raise ValueError(
            "Planner output did not include required sections: Follow-up Actions and Patient Message."
        )

    return {
        "messages": [AIMessage(content=content, name="planner")],
        "follow_up_plan": follow_up_plan,
    }
