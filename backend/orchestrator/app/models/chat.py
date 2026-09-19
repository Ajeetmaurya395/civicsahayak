"""Pydantic models for chat messages."""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ChatMessage(BaseModel):
    """A single chat message."""
    role: str = Field(..., description="user or assistant")
    content: str
    timestamp: Optional[datetime] = None
    metadata: Optional[dict] = None


class ChatRequest(BaseModel):
    """Request for a chat turn."""
    message: str
    conversation_id: Optional[str] = None
    profile: Optional[dict] = None


class ChatResponse(BaseModel):
    """Response from a chat turn."""
    message: str
    conversation_id: str
    profile: Optional[dict] = None
    schemes: Optional[list[dict]] = None
    eligibility_results: Optional[list[dict]] = None
    action: Optional[str] = Field(None, description="ask_profile|searching|results|general")
    follow_up_questions: Optional[list[str]] = None
