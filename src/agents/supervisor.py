"""Deterministic workflow supervisor for ClinicAgent."""

from __future__ import annotations

from typing import Any

from src.utils.parsers import has_gap_analysis

VALID_NEXT_STEPS = {"scribe", "gap_detector", "planner", "reviewer", "__end__"}


def determine_next_step(state: dict[str, Any]) -> str:
    """Choose the next graph node from state flags.

    Routing is deterministic on purpose. The content-generation agents use an
    LLM, but workflow control should be testable, repeatable, and easy to audit.
    """
    if state.get("final_report"):
        return "__end__"

    if not state.get("soap_note"):
        return "scribe"

    if not has_gap_analysis(state.get("care_gaps")):
        return "gap_detector"

    if not state.get("follow_up_plan"):
        return "planner"

    return "reviewer"


def supervisor_node(state: dict[str, Any]) -> dict:
    """LangGraph node: store the next workflow step in state."""
    return {"next": determine_next_step(state)}
