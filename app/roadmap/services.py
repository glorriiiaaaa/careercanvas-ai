# app/roadmap/services.py
from app.ai.gemini_client import generate_json_response


def build_roadmap_prompt(career_goal):
    return f"""You are an expert career mentor and curriculum designer.
Create a learning roadmap for someone who wants to become a {career_goal}, starting from beginner/intermediate level.
Respond with ONLY valid JSON (no markdown, no explanation outside the JSON) matching exactly this schema:

{{
  "estimated_timeline": "<a short string like '4-6 months'>",
  "weekly_plan": [
    {{"week": "<e.g. Week 1-2>", "focus": "<short focus area title>", "topics": [<3-5 short topic strings>]}}
  ],
  "recommended_courses": [<4-6 short strings naming real, well-known online courses or resources relevant to {career_goal}>],
  "suggested_projects": [<3-5 short strings, each a specific project idea to build portfolio experience for {career_goal}>]
}}

Provide 5-8 entries in weekly_plan, covering a logical progression from fundamentals to job-ready skills.

CAREER GOAL: {career_goal}
"""


def generate_roadmap(career_goal):
    prompt = build_roadmap_prompt(career_goal)
    return generate_json_response(prompt)
