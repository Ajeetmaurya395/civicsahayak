"""Scheme Agent — searches live government sources for schemes.

Uses the agents-as-tools pattern: this agent is wrapped in a @tool
function that the orchestrator calls like any other tool.

Generates several targeted queries, searches, retrieves only trusted
government domains, and extracts structured criteria.
Never invents a scheme, benefit, or URL. Unknown fields are null.
"""
import json
import logging
from strands import Agent, tool
from app.services.llm_service import get_model
from app.tools.search_government_web import search_government_web
from app.tools.government_retriever import government_retriever
from app.tools.scheme_extractor import scheme_extractor
from app.services.deduplication import deduplicate_schemes

logger = logging.getLogger(__name__)

SCHEME_SYSTEM_PROMPT = """You are the Scheme Discovery Agent for CivicOS. Your job is to find relevant government schemes for Indian citizens.

WORKFLOW:
1. Take the user profile and generate targeted search queries
2. Use search_government_web to search for schemes matching the profile
3. Use government_retriever to fetch the actual government pages
4. Use scheme_extractor to extract structured scheme data from pages
5. Return all discovered schemes

CRITICAL RULES:
- Generate MULTIPLE targeted queries, never one giant query
- ONLY use results from trusted government domains (.gov.in, .nic.in)
- NEVER invent a scheme name, benefit, URL, or any detail
- Unknown fields are null, never guessed
- If search returns no results, say so honestly — don't make things up
- Always include the source URL for every scheme

You have access to these tools:
- search_government_web: Search the web for government schemes
- government_retriever: Fetch and parse government web pages
- scheme_extractor: Extract structured scheme data from page content"""


def _create_scheme_agent():
    """Create a fresh scheme agent instance."""
    return Agent(
        model=get_model(),
        tools=[search_government_web, government_retriever, scheme_extractor],
        system_prompt=SCHEME_SYSTEM_PROMPT,
    )


@tool
def find_schemes(profile_json: str) -> str:
    """Search live government sources for schemes matching a user profile.

    Takes the user profile as JSON, generates targeted search queries,
    retrieves and verifies scheme information from official sources,
    and returns structured scheme data.
    """
    try:
        profile = json.loads(profile_json) if isinstance(profile_json, str) else profile_json
    except json.JSONDecodeError:
        return json.dumps({"error": "Invalid profile JSON", "schemes": []})

    agent = _create_scheme_agent()

    prompt = f"""Find government schemes for this user profile:
{json.dumps(profile, indent=2)}

Steps:
1. Call search_government_web with the profile JSON to search for relevant schemes
2. From the search results, pick URLs from trusted government domains
3. Call government_retriever with those URLs to fetch the pages
4. Call scheme_extractor with the page content to extract structured scheme data
5. Return ALL discovered schemes

Start by calling search_government_web with this profile: {json.dumps(profile)}"""

    try:
        result = agent(prompt)
        response_text = str(result.message) if hasattr(result, 'message') else str(result)

        # Try to extract JSON from response
        try:
            # Look for JSON array or object in the response
            cleaned = response_text.strip()
            if "```json" in cleaned:
                start = cleaned.index("```json") + 7
                end = cleaned.index("```", start)
                cleaned = cleaned[start:end].strip()
            elif "```" in cleaned:
                start = cleaned.index("```") + 3
                end = cleaned.index("```", start)
                cleaned = cleaned[start:end].strip()

            data = json.loads(cleaned)
            if isinstance(data, list):
                schemes = data
            elif isinstance(data, dict) and "schemes" in data:
                schemes = data["schemes"]
            else:
                schemes = [data]
        except (json.JSONDecodeError, ValueError):
            # Return raw response as a scheme discovery report
            schemes = []
            logger.info("Scheme agent returned non-JSON response — treating as text report")

        # Deduplicate
        schemes = deduplicate_schemes(schemes)

        return json.dumps({
            "schemes": schemes,
            "total_found": len(schemes),
            "raw_response": response_text[:2000],
        })

    except Exception as e:
        logger.error(f"Scheme discovery failed: {e}")
        return json.dumps({"error": str(e), "schemes": []})
