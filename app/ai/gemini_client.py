# app/ai/gemini_client.py
#
# WHY THIS FILE EXISTS:
# Single, reusable wrapper around our AI provider. Every AI-powered module
# (Resume Analyzer, Roadmap, Interview Prep, AI Coach) imports from here
# instead of configuring the API separately - one place to change models,
# handle errors, or swap providers later.
#
# NOTE: This file is named gemini_client.py for historical reasons (we
# started with Gemini), but currently calls Groq's API instead, since
# Gemini's free tier requires billing in some regions. The function name
# generate_json_response() is kept the same so no other file in the app
# needs to change - this is exactly why we isolated AI logic into one file.

import os
import json
from groq import Groq

_client = Groq(api_key=os.environ.get('GROQ_API_KEY'))
_MODEL_NAME = 'llama-3.3-70b-versatile'


def generate_json_response(prompt):
    """
    Sends a prompt to the AI model and parses the response as JSON.
    We instruct the model (in the prompt itself, built by callers)
    to return ONLY JSON - this function strips common wrapping
    (like markdown code fences) before parsing, since models
    sometimes add ```json ... ``` around output despite instructions.
    """
    response = _client.chat.completions.create(
        model=_MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
    )
    text = response.choices[0].message.content.strip()

    if text.startswith('```'):
        text = text.split('```')[1]
        if text.startswith('json'):
            text = text[4:]
    text = text.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        raise ValueError(f'AI did not return valid JSON. Raw response: {text[:500]}')
