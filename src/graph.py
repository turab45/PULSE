"""LangGraph workflow assembly for ClinicAgent."""

from __future__ import annotations

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph

from src.agents.gap_detector import gap_detector_node
from src.agents.planner import planner_node
from src.agents.reviewer import reviewer_node
from src.agents.scribe import scribe_node
from src.agents.supervisor import supervisor_node
from src.state import ClinicalState


def route_supervisor(state: ClinicalState) -> str:
    """Return the node selected by the supervisor."""
    return state.get("next", "__end__")


def build_graph(checkpointer: MemorySaver | None = None):
    """Build and compile the clinical documentation workflow."""
    workflow = StateGraph(ClinicalState)

    workflow.add_node("supervisor", supervisor_node)
    workflow.add_node("scribe", scribe_node)
    workflow.add_node("gap_detector", gap_detector_node)
    workflow.add_node("planner", planner_node)
    workflow.add_node("reviewer", reviewer_node)

    workflow.add_edge(START, "supervisor")

    for node_name in ("scribe", "gap_detector", "planner", "reviewer"):
        workflow.add_edge(node_name, "supervisor")

    workflow.add_conditional_edges(
        "supervisor",
        route_supervisor,
        {
            "scribe": "scribe",
            "gap_detector": "gap_detector",
            "planner": "planner",
            "reviewer": "reviewer",
            "__end__": END,
        },
    )

    return workflow.compile(checkpointer=checkpointer or MemorySaver())
