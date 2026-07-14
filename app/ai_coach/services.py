# app/ai_coach/services.py
#
# WHY THIS FILE EXISTS:
# Unlike our other AI modules (which ask for structured JSON), the
# Coach needs free-form conversational text - so we bypass
# generate_json_response() and talk to Groq directly here, building
# a proper multi-turn message list instead of a single prompt string.

import os
from groq import Groq

_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
_MODEL_NAME = "llama-3.3-70b-versatile"

SYSTEM_PROMPT = """You are an encouraging, knowledgeable AI career coach inside CareerCanvas AI,
a platform helping students and fresh graduates become job-ready. You help with resume advice,
interview preparation tips, learning/skill advice, job search strategy, and motivation.
Keep responses concise (2-4 short paragraphs max), practical, and encouraging. Avoid generic
platitudes - give specific, actionable advice whenever possible."""


def get_coach_reply(conversation_history):
    """
    conversation_history: list of {"role": "user"|"assistant", "content": str},
    ordered oldest to newest. Returns the AI's reply as a plain string.
    """
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + conversation_history

    response = _client.chat.completions.create(
        model=_MODEL_NAME,
        messages=messages,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()
