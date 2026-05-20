"""Command-line entry point for ClinicAgent."""

from __future__ import annotations

import argparse
import uuid
from pathlib import Path

from langchain_core.messages import AIMessage, HumanMessage

from src.graph import build_graph
from src.state import ClinicalState

DEFAULT_TRANSCRIPT = """
Patient: I've been feeling tired, thirsty a lot, peeing more. Weight down 8 lb last 3 months.
Doctor: Any family history diabetes? Blurry vision? Numbness feet?
Patient: Mom had type 2. No numbness yet.
Doctor: BP 138/84, weight 210 lb, height 5'10". I'll order A1c, lipid panel, urine microalb.
""".strip()


def build_initial_state(transcript: str) -> ClinicalState:
    """Create the initial LangGraph state for a consultation transcript."""
    return {
        "messages": [HumanMessage(content=f"New consultation transcript:\n{transcript}")],
        "transcript": transcript,
        "care_gaps": [],
    }


def run_workflow(transcript: str, thread_id: str | None = None) -> ClinicalState:
    """Run the graph and return its final state."""
    graph = build_graph()
    config = {
        "configurable": {"thread_id": thread_id or str(uuid.uuid4())},
        "recursion_limit": 12,
    }
    return graph.invoke(build_initial_state(transcript), config=config)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a SOAP note, care-gap review, follow-up plan, and final report."
    )
    parser.add_argument(
        "--transcript-file",
        type=Path,
        help="Path to a plain-text consultation transcript. Uses a demo transcript if omitted.",
    )
    parser.add_argument(
        "--thread-id",
        help="Optional LangGraph thread ID for checkpointed runs.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    transcript = (
        args.transcript_file.read_text(encoding="utf-8")
        if args.transcript_file
        else DEFAULT_TRANSCRIPT
    )

    final_state = run_workflow(transcript, thread_id=args.thread_id)
    final_message = final_state["messages"][-1]

    if isinstance(final_message, AIMessage):
        print(final_message.content)
    else:
        print(final_state.get("final_report", "No final report generated."))


if __name__ == "__main__":
    main()
