"""Parsing helpers shared by ClinicAgent nodes."""

from __future__ import annotations


NO_GAPS = "No gaps identified"


def parse_soap(content: str) -> str | None:
    """Return a SOAP note only when all required sections are present."""
    normalized = content.strip()
    required_sections = ("S:", "O:", "A:", "P:")
    if all(section in normalized for section in required_sections):
        return normalized
    return None


def parse_gaps(content: str) -> list[str]:
    """Extract bullet-list care gaps or the no-gaps sentinel."""
    normalized = content.strip()
    if not normalized:
        return [NO_GAPS]

    if normalized.lower() == NO_GAPS.lower():
        return [NO_GAPS]

    gaps = [
        line.strip()
        for line in normalized.splitlines()
        if line.strip().startswith(("-", "*"))
    ]
    return gaps or [NO_GAPS]


def has_gap_analysis(care_gaps: list[str] | None) -> bool:
    """Return True once the gap detector has produced any structured result."""
    return bool(care_gaps)


def has_meaningful_gaps(care_gaps: list[str] | None) -> bool:
    """Return True when the result contains gaps beyond the no-gaps sentinel."""
    if not care_gaps:
        return False

    return any(gap.strip().lower() != NO_GAPS.lower() for gap in care_gaps)


def parse_plan(content: str) -> str | None:
    """Return the plan when the expected sections are present."""
    normalized = content.strip()
    if "Follow-up Actions:" in normalized and "Patient Message:" in normalized:
        return normalized
    return None


def parse_review_status(content: str) -> str:
    """Map reviewer output to a compact status."""
    normalized = content.strip().upper()
    if normalized.startswith("APPROVED"):
        return "approved"
    return "issues"
