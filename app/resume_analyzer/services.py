# app/resume_analyzer/services.py
#
# WHY THIS FILE EXISTS:
# Business logic for resume analysis lives here, not in routes.py.
# This keeps the route thin (parse request, call service, render response)
# and makes this logic independently testable/reusable later
# (e.g. if we build an API endpoint for mobile that needs the same logic).

from pypdf import PdfReader
from app.ai.gemini_client import generate_json_response


def extract_text_from_pdf(file_stream):
    """Reads a PDF file stream and returns all extracted text as one string."""
    reader = PdfReader(file_stream)
    text_parts = [page.extract_text() or "" for page in reader.pages]
    return "\n".join(text_parts).strip()


def build_analysis_prompt(resume_text):
    """
    Builds the prompt sent to Gemini. We explicitly demand JSON-only output
    with a fixed schema, so our code can reliably parse the response instead
    of trying to regex-parse free-form text.
    """
    return f"""You are an expert ATS (Applicant Tracking System) resume reviewer and career coach.
Analyze the resume text below and respond with ONLY valid JSON (no markdown, no explanation outside the JSON) matching exactly this schema:

{{
  "ats_score": <integer 0-100>,
  "strengths": [<3-5 short strings>],
  "weaknesses": [<3-5 short strings>],
  "missing_skills": [<3-6 short strings of skills/keywords missing for a strong tech resume>],
  "keyword_suggestions": [<3-6 short strings of ATS keywords to add>],
  "improved_bullets": [
    {{"original": "<a weak bullet point found in the resume>", "improved": "<a stronger rewritten version with measurable impact>"}}
  ]
}}

Provide 2-3 items in improved_bullets, picking the weakest bullet points you find.

RESUME TEXT:
{resume_text}
"""


def analyze_resume_text(resume_text):
    """
    Sends resume text to Gemini and returns the parsed analysis dict.
    Raises ValueError (bubbled up from gemini_client) if the AI response
    cannot be parsed - the route is responsible for catching and
    showing a friendly error in that case.
    """
    prompt = build_analysis_prompt(resume_text)
    return generate_json_response(prompt)
