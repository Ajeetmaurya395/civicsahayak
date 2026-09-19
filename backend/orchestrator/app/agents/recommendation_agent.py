"""Recommendation Agent — groups schemes, explains gaps, suggests combinations.

Never crowns one scheme "the best" or ranks by anything subjective.
Shows all relevant schemes with facts; lets the user decide.
"""
import json
import logging
from strands import Agent, tool
from app.services.llm_service import get_model

logger = logging.getLogger(__name__)

RECOMMENDATION_SYSTEM_PROMPT = """You are the Recommendation Agent for CivicOS, a government scheme discovery platform for India.

Your job is to take eligibility results and generate clear, honest recommendations.

RULES:
1. NEVER say "you are eligible" — say "you appear to meet the published criteria"
2. NEVER rank schemes by subjective "best" — present facts and let the user decide
3. Group complementary schemes (e.g., scholarship + hostel + travel assistance)
4. Explain WHY someone does or doesn't match, citing specific criteria
5. For NOT_ELIGIBLE schemes, compute and state the actual gap (e.g., "income exceeds threshold by ₹42,000")
6. For POTENTIALLY_ELIGIBLE schemes, list exactly what information is still needed
7. Suggest which missing documents or information would unlock more schemes
8. Be honest — if no schemes match, say so clearly
9. Always point to the official portal for final verification

Return a JSON object with:
{
  "summary": "Brief overall summary",
  "scheme_groups": [
    {
      "group_name": "e.g., Education Support Package",
      "description": "Why these go together",
      "schemes": ["scheme_id1", "scheme_id2"]
    }
  ],
  "recommendations": [
    {
      "scheme_id": "id",
      "scheme_name": "name",
      "status": "ELIGIBLE/POTENTIALLY_ELIGIBLE/NOT_ELIGIBLE",
      "why": "Plain language explanation",
      "action": "What the user should do next",
      "official_url": "URL or null"
    }
  ],
  "missing_info_impact": "What additional info could unlock more schemes",
  "next_steps": ["Step 1", "Step 2"]
}"""


def _create_recommendation_agent():
    """Create a fresh recommendation agent instance."""
    return Agent(
        model=get_model(),
        system_prompt=RECOMMENDATION_SYSTEM_PROMPT,
    )


@tool
def explain_and_group(eligibility_results_json: str) -> str:
    """Generate recommendations, groupings, and explanations for eligibility results.

    Takes eligibility results and scheme data, groups complementary schemes,
    explains gaps, and provides actionable next steps.
    Never says 'you are eligible' — says 'you appear to meet the published criteria'.
    """
    try:
        data = json.loads(eligibility_results_json) if isinstance(eligibility_results_json, str) else eligibility_results_json
    except json.JSONDecodeError:
        return json.dumps({"error": "Invalid results JSON"})

    agent = _create_recommendation_agent()

    prompt = f"""Analyze these eligibility results and generate recommendations:

{json.dumps(data, indent=2)}

Group complementary schemes, explain gaps for non-eligible ones,
identify what missing information would unlock more schemes,
and provide clear next steps. Return valid JSON."""

    try:
        result = agent(prompt)
        response_text = str(result.message) if hasattr(result, 'message') else str(result)

        # Parse JSON
        cleaned = response_text.strip()
        if "```json" in cleaned:
            start = cleaned.index("```json") + 7
            end = cleaned.index("```", start)
            cleaned = cleaned[start:end].strip()
        elif "```" in cleaned:
            start = cleaned.index("```") + 3
            end = cleaned.index("```", start)
            cleaned = cleaned[start:end].strip()

        return cleaned

    except Exception as e:
        logger.error(f"Recommendation generation failed: {e}")
        return json.dumps({
            "summary": "Unable to generate detailed recommendations at this time.",
            "recommendations": [],
            "next_steps": ["Please try again or check the schemes individually."],
            "error": str(e),
        })
