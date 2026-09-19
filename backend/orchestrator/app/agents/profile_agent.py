"""Profile Agent — extracts structured user profile from natural language.

Uses the agents-as-tools pattern: this agent is wrapped in a @tool
function that the orchestrator calls like any other tool.
"""
import json
import logging
from strands import Agent, tool
from app.services.llm_service import get_model

logger = logging.getLogger(__name__)

PROFILE_SYSTEM_PROMPT = """You are a Profile Extraction Agent for CivicOS, a government scheme discovery platform for India.

Your job is to extract structured user profile information from natural language text.
Extract ONLY what the user explicitly states. Never assume or invent information.

Return a JSON object with these fields (set to null if not mentioned):
{
  "age": number or null,
  "gender": "male"/"female"/"other" or null,
  "state": "Indian state name" or null,
  "district": "district name" or null,
  "annual_family_income": number in INR or null,
  "occupation": "string" or null,
  "education_level": "string" or null,
  "category": "General"/"OBC"/"SC"/"ST"/"EWS" or null,
  "is_bpl": boolean or null,
  "disability": "type of disability" or null,
  "marital_status": "married"/"single"/"widowed"/"divorced" or null,
  "land_ownership": "string" or null,
  "is_farmer": boolean or null,
  "num_children": number or null,
  "is_minority": boolean or null
}

Also identify missing critical fields and suggest follow-up questions.
Income should be converted to annual INR. For example:
- "2 lakh" = 200000
- "20,000 per month" = 240000
- "₹1.5 lakh per annum" = 150000

Return valid JSON only. No extra text."""


def _create_profile_agent():
    """Create a fresh profile agent instance."""
    return Agent(
        model=get_model(),
        system_prompt=PROFILE_SYSTEM_PROMPT,
    )


@tool
def extract_profile(user_text: str) -> str:
    """Extract a structured user profile from natural language text.

    Analyzes the user's description and returns structured profile data
    with identified missing fields and follow-up questions.
    """
    agent = _create_profile_agent()

    prompt = f"""Extract the user profile from this text:

"{user_text}"

Return a JSON object with:
1. "profile": the extracted profile fields
2. "missing_fields": list of important fields not mentioned (e.g., ["age", "state", "income"])
3. "follow_up_questions": list of natural language questions to ask the user for missing info
4. "confidence": a number 0-1 indicating how complete the profile is

Return ONLY valid JSON."""

    try:
        result = agent(prompt)
        response_text = str(result.message) if hasattr(result, 'message') else str(result)

        # Clean markdown code blocks
        cleaned = response_text.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        if cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        cleaned = cleaned.strip()

        parsed = json.loads(cleaned)
        return json.dumps(parsed)

    except json.JSONDecodeError:
        logger.error(f"Failed to parse profile extraction response")
        return json.dumps({
            "profile": {},
            "missing_fields": ["age", "state", "income", "occupation"],
            "follow_up_questions": [
                "How old are you?",
                "Which state do you live in?",
                "What is your family's yearly income?",
                "What do you do for a living?"
            ],
            "confidence": 0.0
        })
    except Exception as e:
        logger.error(f"Profile extraction failed: {e}")
        return json.dumps({"error": str(e), "profile": {}})
