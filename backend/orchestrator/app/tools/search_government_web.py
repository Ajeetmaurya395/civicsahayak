"""Web search tool — Tavily-powered multi-query government scheme search.

Never one giant query. Given a profile, generate several targeted ones.
Isolated behind this single function so the provider can be swapped
without touching agents.
"""
import os
import json
import logging
from strands import tool

logger = logging.getLogger(__name__)


def _build_search_queries(profile: dict) -> list[str]:
    """Generate multiple targeted search queries from a user profile.

    Never one giant query. For each profile, generate several targeted ones
    so that a student, farmer, entrepreneur, etc. all get relevant results
    from the same generic pipeline.
    """
    queries = []

    age = profile.get("age")
    state = profile.get("state", "")
    occupation = profile.get("occupation", "")
    category = profile.get("category", "")
    gender = profile.get("gender", "")
    income = profile.get("annual_family_income")
    education = profile.get("education_level", "")
    is_farmer = profile.get("is_farmer", False)
    disability = profile.get("disability")

    # Core identity-based query
    parts = []
    if occupation:
        parts.append(occupation)
    if state:
        parts.append(state)
    if category:
        parts.append(category)

    if parts:
        queries.append(f"site:myscheme.gov.in {' '.join(parts)} government scheme")

    # Sector-specific queries
    if occupation and occupation.lower() in ["student", "college student", "school student"]:
        q = "scholarship scheme"
        if state:
            q += f" {state}"
        if category:
            q += f" {category}"
        queries.append(f"site:myscheme.gov.in {q}")
        queries.append(f"site:scholarships.gov.in {q}")
        if education:
            queries.append(f"site:gov.in {education} scholarship financial assistance")

    if is_farmer or (occupation and "farmer" in occupation.lower()):
        queries.append(f"site:myscheme.gov.in farmer agriculture scheme {state}")
        queries.append(f"site:gov.in farmer financial assistance scheme {state}")

    if gender and gender.lower() == "female":
        queries.append(f"site:myscheme.gov.in women scheme {state}")
        queries.append(f"site:gov.in women empowerment scheme financial assistance")

    if age and age >= 60:
        queries.append(f"site:myscheme.gov.in senior citizen pension scheme {state}")

    if disability:
        queries.append(f"site:myscheme.gov.in disability scheme {state}")

    if income and income <= 250000:
        queries.append(f"site:myscheme.gov.in BPL low income scheme {state}")

    # General fallback
    if state:
        queries.append(f"site:gov.in government scheme {state} {occupation or 'benefits'}")

    # Ensure at least one query
    if not queries:
        base = "government scheme India"
        if state:
            base += f" {state}"
        if occupation:
            base += f" {occupation}"
        queries.append(f"site:myscheme.gov.in {base}")

    # Deduplicate
    seen = set()
    unique_queries = []
    for q in queries:
        normalized = q.strip().lower()
        if normalized not in seen:
            seen.add(normalized)
            unique_queries.append(q.strip())

    return unique_queries[:6]  # Cap at 6 queries to stay within free tier


@tool
def search_government_web(profile_json: str) -> str:
    """Search the web for government schemes matching a user profile.

    Takes a JSON string of the user profile and returns search results
    from trusted government domains. Uses Tavily API for search.
    """
    try:
        profile = json.loads(profile_json) if isinstance(profile_json, str) else profile_json
    except json.JSONDecodeError:
        return json.dumps({"error": "Invalid profile JSON", "results": []})

    queries = _build_search_queries(profile)
    all_results = []
    api_key = os.getenv("TAVILY_API_KEY", "")

    if not api_key:
        logger.warning("TAVILY_API_KEY not set — using fallback search")
        return json.dumps({
            "error": "Search API key not configured",
            "queries_generated": queries,
            "results": [],
            "suggestion": "Set TAVILY_API_KEY in .env to enable live search"
        })

    try:
        from tavily import TavilyClient
        client = TavilyClient(api_key=api_key)

        for query in queries:
            try:
                response = client.search(
                    query=query,
                    search_depth="basic",
                    max_results=5,
                    include_domains=["gov.in", "nic.in", "myscheme.gov.in", "india.gov.in"],
                )
                for result in response.get("results", []):
                    all_results.append({
                        "title": result.get("title", ""),
                        "url": result.get("url", ""),
                        "content": result.get("content", ""),
                        "score": result.get("score", 0),
                        "query_used": query,
                    })
            except Exception as e:
                logger.error(f"Search failed for query '{query}': {e}")
                continue

    except ImportError:
        logger.error("tavily-python not installed")
        return json.dumps({"error": "tavily-python not installed", "results": []})
    except Exception as e:
        logger.error(f"Search failed: {e}")
        return json.dumps({"error": str(e), "results": []})

    # Deduplicate by URL
    seen_urls = set()
    unique_results = []
    for r in all_results:
        url = r.get("url", "").lower().rstrip("/")
        if url and url not in seen_urls:
            seen_urls.add(url)
            unique_results.append(r)

    return json.dumps({
        "queries_generated": queries,
        "total_results": len(unique_results),
        "results": unique_results[:15],  # Cap total results
    })
