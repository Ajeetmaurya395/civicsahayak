"""Pydantic models for eligibility evaluation results."""
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class EligibilityStatus(str, Enum):
    ELIGIBLE = "ELIGIBLE"
    POTENTIALLY_ELIGIBLE = "POTENTIALLY_ELIGIBLE"
    NOT_ELIGIBLE = "NOT_ELIGIBLE"
    INSUFFICIENT_INFORMATION = "INSUFFICIENT_INFORMATION"


class CriterionResult(BaseModel):
    """Result for a single eligibility criterion."""
    criterion: str
    passed: Optional[bool] = None
    detail: str
    user_value: Optional[str] = None
    required_value: Optional[str] = None


class EligibilityResult(BaseModel):
    """Full eligibility evaluation for one scheme."""
    scheme_id: str
    scheme_name: str
    status: EligibilityStatus
    matched: list[str] = []
    unmatched: list[str] = []
    missing: list[str] = []
    criteria_results: list[CriterionResult] = []
    explanation: list[str] = []
    gap_description: Optional[str] = None
    confidence: float = 0.0


class EligibilityRequest(BaseModel):
    """Request to evaluate eligibility."""
    user_profile: dict
    scheme_criteria: list[dict]


class EligibilityResponse(BaseModel):
    """Response with eligibility results."""
    results: list[EligibilityResult] = []
