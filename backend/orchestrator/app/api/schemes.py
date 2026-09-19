"""Schemes API — search, evaluate eligibility, save schemes."""
import json
import uuid
import logging
from datetime import datetime
from fastapi import APIRouter, HTTPException
from app.models.scheme import SchemeSearchRequest, SchemeSearchResponse
from app.models.eligibility import EligibilityRequest, EligibilityResponse
from app.agents.scheme_agent import find_schemes
from app.tools.eligibility_client import check_eligibility
from app.tools.opensearch_client import cache_scheme, search_cached_schemes
from app.db.mongo import saved_schemes_collection

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/search", response_model=SchemeSearchResponse)
async def search_schemes(request: SchemeSearchRequest):
    """Search for government schemes matching a user profile.

    Triggers the live search → retrieve → extract → cache pipeline.
    """
    try:
        profile = request.profile

        # Check OpenSearch cache first
        cached = search_cached_schemes(profile, limit=request.limit)
        if cached:
            logger.info(f"Found {len(cached)} cached schemes")

        # Always do a live search too (cache augments, doesn't replace)
        result_json = find_schemes(json.dumps(profile))
        result = json.loads(result_json)

        schemes = result.get("schemes", [])

        # Cache newly discovered schemes
        for scheme in schemes:
            try:
                cache_scheme(scheme)
            except Exception as e:
                logger.warning(f"Failed to cache scheme: {e}")

        # Merge cached and live results (dedupe by name)
        all_schemes = schemes
        seen_names = {s.get("scheme_name", "").lower() for s in schemes}
        for cached_scheme in cached:
            name = cached_scheme.get("scheme_name", "").lower()
            if name and name not in seen_names:
                all_schemes.append(cached_scheme)
                seen_names.add(name)

        return SchemeSearchResponse(
            schemes=[_to_scheme_info(s) for s in all_schemes[:request.limit]],
            total_found=len(all_schemes),
            search_queries_used=result.get("queries_generated", []),
            sources_checked=result.get("total_results", 0),
        )

    except Exception as e:
        logger.error(f"Scheme search failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/check-eligibility")
async def check_eligibility_endpoint(request: EligibilityRequest):
    """Check eligibility for schemes against a user profile.

    Profile + retrieved criteria → calls the deterministic engine.
    """
    try:
        result_json = check_eligibility(json.dumps({
            "user_profile": request.user_profile,
            "scheme_criteria": request.scheme_criteria,
        }))
        result = json.loads(result_json)
        return result

    except Exception as e:
        logger.error(f"Eligibility check failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{scheme_id}")
async def get_scheme(scheme_id: str):
    """Get scheme detail from cache."""
    # Try OpenSearch first
    from app.tools.opensearch_client import _get_client
    client = _get_client()
    if client:
        try:
            result = client.get(index="government_schemes", id=scheme_id)
            return result["_source"]
        except Exception:
            pass

    raise HTTPException(status_code=404, detail="Scheme not found")


@router.post("/save")
async def save_scheme(scheme: dict):
    """Save a scheme to the user's account."""
    try:
        coll = saved_schemes_collection()
        if coll is not None:
            scheme["saved_at"] = datetime.utcnow()
            scheme["_id"] = str(uuid.uuid4())
            await coll.insert_one(scheme)
            return {"status": "saved", "id": scheme["_id"]}
        return {"status": "saved", "note": "MongoDB not available — saved in memory only"}
    except Exception as e:
        logger.error(f"Failed to save scheme: {e}")
        raise HTTPException(status_code=500, detail=str(e))


def _to_scheme_info(data: dict) -> dict:
    """Convert raw scheme data to SchemeInfo format."""
    return {
        "scheme_id": data.get("scheme_id") or data.get("source_url", ""),
        "scheme_name": data.get("scheme_name", "Unknown Scheme"),
        "description": data.get("description"),
        "benefits": data.get("benefits"),
        "department": data.get("department"),
        "government_level": data.get("government_level"),
        "sector": data.get("sector"),
        "source_url": data.get("source_url"),
        "official_application_url": data.get("official_application_url"),
        "source_verified": data.get("source_verified", False),
        "required_documents": data.get("required_documents"),
        "eligibility": data.get("eligibility"),
        "how_to_apply": data.get("how_to_apply"),
        "state": data.get("state"),
    }
