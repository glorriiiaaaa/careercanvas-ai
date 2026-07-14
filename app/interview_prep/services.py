# app/interview_prep/services.py
from app.ai.gemini_client import generate_json_response


def build_questions_prompt(category, resume_text=None):
    if category == "Resume-Based" and resume_text:
        context = f"Base the questions on this candidate resume text:\n{resume_text[:2000]}"
    else:
        context = f"Generate general {category} interview questions for a job-seeking student/fresh graduate."

    return f"""You are an expert technical interviewer and career coach.
{context}
Respond with ONLY valid JSON (no markdown, no explanation outside the JSON) matching exactly this schema:

{{
  "questions": [<4 short interview question strings appropriate for category "{category}">]
}}
"""


def generate_questions(category, resume_text=None):
    prompt = build_questions_prompt(category, resume_text)
    data = generate_json_response(prompt)
    return data["questions"]


def build_feedback_prompt(question, answer):
    return f"""You are an expert interview coach evaluating a candidate's answer.

QUESTION: {question}
CANDIDATE ANSWER: {answer}

Respond with ONLY valid JSON (no markdown, no explanation outside the JSON) matching exactly this schema:

{{
  "feedback": "<2-3 sentences of constructive feedback on this specific answer>",
  "answer_rating": "<one word: Excellent, Good, Average, or Needs Improvement>",
  "confidence_score": <integer 0-100, how confident and well-structured the answer sounds>,
  "grammar_score": <integer 0-100, grammatical correctness of the answer>
}}
"""


def evaluate_answer(question, answer):
    prompt = build_feedback_prompt(question, answer)
    return generate_json_response(prompt)
