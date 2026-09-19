"""Profile API — extract and manage user profiles."""
import json
import logging
from fastapi import APIRouter, HTTPException
from app.models.profile import ProfileExtractionRequest, ProfileExtractionResponse
from app.agents.profile_agent import extract_profile

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/extract", response_model=ProfileExtractionResponse)
async def extract_profile_endpoint(request: ProfileExtractionRequest):
    """Extract structured profile from text."""
    try:
        result_json = extract_profile(request.text)
        result = json.loads(result_json)

        return ProfileExtractionResponse(
            profile=result.get("profile", {}),
            missing_fields=result.get("missing_fields", []),
            follow_up_questions=result.get("follow_up_questions", []),
            confidence=result.get("confidence", 0.0),
        )
    except Exception as e:
        logger.error(f"Profile extraction failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
