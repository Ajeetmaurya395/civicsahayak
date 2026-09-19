"""Pydantic models for government schemes."""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class SchemeEligibility(BaseModel):
    """Structured eligibility criteria extracted from a scheme."""
    age_min: Optional[int] = None
    age_max: Optional[int] = None
    income_max: Optional[float] = None
    income_min: Optional[float] = None
    states: Optional[list[str]] = None
    categories: Optional[list[str]] = None
    genders: Optional[list[str]] = None
    occupations: Optional[list[str]] = None
    education_levels: Optional[list[str]] = None
    is_bpl_required: Optional[bool] = None
    disability_required: Optional[bool] = None
    is_farmer_required: Optional[bool] = None
    marital_status: Optional[list[str]] = None
    land_ownership_required: Optional[bool] = None
    custom_criteria: Optional[dict] = None


class SchemeInfo(BaseModel):
    """A government scheme discovered from official sources."""
    scheme_id: Optional[str] = None
    scheme_name: str
    description: Optional[str] = None
    benefits: Optional[str] = None
    department: Optional[str] = None
    government_level: Optional[str] = Field(None, description="central/state/district")
    sector: Optional[str] = Field(None, description="education/healthcare/agriculture/housing/etc")
    source_url: Optional[str] = None
    official_application_url: Optional[str] = None
    source_verified: bool = False
    required_documents: Optional[list[str]] = None
    eligibility: Optional[SchemeEligibility] = None
    retrieved_at: Optional[datetime] = None
    how_to_apply: Optional[str] = None
    state: Optional[str] = None


class SchemeSearchRequest(BaseModel):
    """Request to search for schemes."""
    profile: dict
    query: Optional[str] = None
    limit: int = 10


class SchemeSearchResponse(BaseModel):
    """Response with discovered schemes."""
    schemes: list[SchemeInfo] = []
    total_found: int = 0
    search_queries_used: list[str] = []
    sources_checked: int = 0
