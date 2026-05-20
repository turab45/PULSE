from typing import Annotated, Literal, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class ClinicalState(TypedDict, total=False):
    patient_info: str
    messages: Annotated[list[BaseMessage], add_messages]
    transcript: str
    soap_note: str | None
    care_gaps: list[str]
    follow_up_plan: str | None
    final_report: str | None
    review_status: Literal["approved", "issues"] | None
    next: Literal["scribe", "gap_detector", "planner", "reviewer", "__end__"]
