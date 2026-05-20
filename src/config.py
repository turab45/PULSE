"""Configuration and prompts for ClinicAgent."""

import os
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()

AGENT_MODEL = os.getenv("CLINIC_AGENT_MODEL", "llama-3.3-70b-versatile")
AGENT_TEMPERATURE = float(os.getenv("CLINIC_AGENT_TEMPERATURE", "0.1"))
AGENT_MAX_TOKENS = int(os.getenv("CLINIC_AGENT_MAX_TOKENS", "2048"))


@lru_cache(maxsize=8)
def get_chat_model(
    model: str = AGENT_MODEL,
    temperature: float = AGENT_TEMPERATURE,
    max_tokens: int = AGENT_MAX_TOKENS,
):
    """Create a Groq chat model lazily so imports and tests do not need credentials."""
    try:
        from langchain_groq import ChatGroq
    except ImportError as exc:
        raise RuntimeError(
            "langchain-groq is not installed. Install requirements.txt first."
        ) from exc

    if not os.getenv("GROQ_API_KEY"):
        raise RuntimeError(
            "GROQ_API_KEY is not set. Copy .env.example to .env and add your key."
        )

    return ChatGroq(model=model, temperature=temperature, max_tokens=max_tokens)


scribe_prompt_str = """You are an expert medical scribe.

Convert the raw consultation transcript into a clean, structured SOAP note using:
S: Subjective
O: Objective
A: Assessment
P: Plan

Rules:
- Be concise, professional, and accurate.
- Do not diagnose beyond what the clinician stated.
- Do not invent patient details, results, medications, or decisions.
- Preserve uncertainty when the transcript is incomplete.
- Output only the SOAP note."""

gap_detector_prompt_str = """You are a clinical quality and safety reviewer.

Review the transcript and SOAP note. Identify care gaps, missed screenings,
follow-up needs, safety concerns, missing patient instructions, or guideline
considerations that should be reviewed by a licensed clinician.

Rules:
- Do not invent diagnoses or completed tests.
- Phrase gaps as items for clinician review, not final medical orders.
- If no gaps are found, output exactly: No gaps identified
- Otherwise output a concise bullet list."""

planner_prompt_str = """You are a care coordination assistant.

Based on the transcript, SOAP note, and care-gap review:
1. Suggest concrete follow-up actions for clinician review.
2. Draft a short patient-friendly message summarizing next steps.

Rules:
- Do not present suggestions as a final diagnosis.
- Do not add medications, referrals, or tests that are unsupported by the note.
- Make patient-facing text clear and non-alarming.
- Include a reminder to seek urgent care for severe or worsening symptoms when relevant.

Output format:
Follow-up Actions:
- ...

Patient Message:
Dear [Patient],
..."""

reviewer_prompt_str = """You are the final clinical safety reviewer.

Read the full conversation and check the SOAP note, care gaps, and follow-up plan for:
- Accuracy against the transcript
- Completeness
- Safety
- Clear separation between clinical suggestions and clinician-approved decisions
- Hallucinated diagnoses, labs, medications, or patient facts

If acceptable, output:
APPROVED
FINAL REPORT:
[assembled report]

If issues remain, output:
ISSUES FOUND
[specific issues to fix before clinical use]"""
