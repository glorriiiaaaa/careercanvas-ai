# app/project_recommender/services.py
from app.ai.gemini_client import generate_json_response


def build_projects_prompt(interests):
    return f"""You are a senior software mentor helping a student build a strong portfolio.
The student's interests/skills are: {interests}

Suggest 3 portfolio project ideas tailored to these interests. Respond with ONLY valid JSON (no markdown, no explanation outside the JSON) matching exactly this schema:

{{
  "projects": [
    {{
      "title": "<short project title>",
      "difficulty": "<Beginner, Intermediate, or Advanced>",
      "timeline": "<e.g. '2-3 weeks'>",
      "required_skills": [<3-5 short skill strings>],
      "tech_stack": [<3-6 short technology name strings>],
      "db_design": "<1-2 sentence description of the core data model/tables needed>",
      "github_structure": "<1-2 sentence description of suggested repo/folder structure>",
      "resume_description": "<one polished resume bullet point describing this project, with a measurable/impressive angle>"
    }}
  ]
}}
"""


def generate_project_ideas(interests):
    prompt = build_projects_prompt(interests)
    data = generate_json_response(prompt)
    return data["projects"]
