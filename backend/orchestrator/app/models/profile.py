"""Pydantic models for user profiles."""
from pydantic import BaseModel, Field
from typing import Optional


class UserProfile(BaseModel):
    """Structured user profile extracted from conversation."""
    age: Optional[int] = Field(None, description="User's age in years")
    gender: Optional[str] = Field(None, description="male/female/other")
    state: Optional[str] = Field(None, description="Indian state of residence")
    district: Optional[str] = Field(None, description="District within state")
    annual_family_income: Optional[float] = Field(None, description="Annual family income in INR")
    occupation: Optional[str] = Field(None, description="Current occupation")
    education_level: Optional[str] = Field(None, description="Highest education level")
    category: Optional[str] = Field(None, description="Social category: General/OBC/SC/ST/EWS")
    is_bpl: Optional[bool] = Field(None, description="Below Poverty Line status")
    disability: Optional[str] = Field(None, description="Type of disability if any")
    marital_status: Optional[str] = Field(None, description="Married/Single/Widowed/Divorced")
    land_ownership: Optional[str] = Field(None, description="Land ownership details")
    is_farmer: Optional[bool] = Field(None, description="Whether the person is a farmer")
    num_children: Optional[int] = Field(None, description="Number of children")
    religion: Optional[str] = Field(None, description="Religion if relevant to scheme")
    is_minority: Optional[bool] = Field(None, description="Whether belongs to minority community")


class ProfileExtractionRequest(BaseModel):
    """Request to extract profile from text."""
    text: str
    existing_profile: Optional[UserProfile] = None


class ProfileExtractionResponse(BaseModel):
    """Response with extracted profile and missing fields."""
    profile: UserProfile
    missing_fields: list[str] = []
    follow_up_questions: list[str] = []
    confidence: float = 0.0
