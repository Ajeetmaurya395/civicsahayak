"""OpenSearch client — read-through/write-through cache for scheme data.

OpenSearch only ever holds the output of a real search-and-extract cycle.
Nothing is ever inserted by hand. A read-through/write-through cache,
not a database of schemes.
"""
import os
import json
import logging
from datetime import datetime, timedelta
from strands import tool

logger = logging.getLogger(__name__)

CACHE_TTL_HOURS = 24  # Schemes expire after 24 hours


def _get_client():
    """Get OpenSearch client, or None if not available."""
    try:
        from opensearchpy import OpenSearch
        url = os.getenv("OPENSEARCH_URL", "http://localhost:9200")
        client = OpenSearch(
            hosts=[url],
            use_ssl=False,
            verify_certs=False,
        )
        # Quick health check
        client.cluster.health()
        return client
    except Exception as e:
        logger.warning(f"OpenSearch not available: {e}")
        return None


def cache_scheme(scheme_data: dict) -> bool:
    """Write a scheme to the OpenSearch cache."""
    client = _get_client()
    if not client:
        return False

    try:
        doc = {
            **scheme_data,
            "retrieved_at": datetime.utcnow().isoformat(),
            "expires_at": (datetime.utcnow() + timedelta(hours=CACHE_TTL_HOURS)).isoformat(),
        }

        # Use source_url as doc ID for dedup
        doc_id = scheme_data.get("source_url", "")
        if not doc_id:
            import hashlib
            doc_id = hashlib.md5(
                json.dumps(scheme_data, sort_keys=True).encode()
            ).hexdigest()

        client.index(
            index="government_schemes",
            id=doc_id,
            body=doc,
        )
        return True
    except Exception as e:
        logger.error(f"Failed to cache scheme: {e}")
        return False


def search_cached_schemes(profile: dict, limit: int = 10) -> list[dict]:
    """Search cached schemes in OpenSearch using hybrid keyword + profile matching."""
    client = _get_client()
    if not client:
        return []

    try:
        # Build query from profile
        must_clauses = []
        should_clauses = []

        state = profile.get("state")
        if state:
            should_clauses.append({"match": {"eligibility.states": state}})
            should_clauses.append({"match": {"state": state}})

        occupation = profile.get("occupation")
        if occupation:
            should_clauses.append({"match": {"description": occupation}})
            should_clauses.append({"match": {"sector": occupation}})

        category = profile.get("category")
        if category:
            should_clauses.append({"match": {"eligibility.categories": category}})

        # Filter out expired entries
        must_clauses.append({
            "range": {
                "expires_at": {"gte": datetime.utcnow().isoformat()}
            }
        })

        query = {
            "bool": {
                "must": must_clauses,
                "should": should_clauses,
                "minimum_should_match": 1 if should_clauses else 0,
            }
        }

        response = client.search(
            index="government_schemes",
            body={"query": query, "size": limit},
        )

        hits = response.get("hits", {}).get("hits", [])
        return [hit["_source"] for hit in hits]

    except Exception as e:
        logger.error(f"OpenSearch search failed: {e}")
        return []


@tool
def search_opensearch_cache(profile_json: str) -> str:
    """Search the OpenSearch cache for previously discovered schemes.

    Returns cached schemes that match the given profile.
    If the cache is empty or unavailable, returns an empty list.
    """
    try:
        profile = json.loads(profile_json) if isinstance(profile_json, str) else profile_json
    except json.JSONDecodeError:
        return json.dumps({"error": "Invalid profile JSON", "cached_schemes": []})

    cached = search_cached_schemes(profile)
    return json.dumps({
        "cached_schemes": cached,
        "total_cached": len(cached),
        "cache_available": _get_client() is not None,
    })
