"""Chat API — conversational endpoint for CivicOS."""
import json
import uuid
import logging
from datetime import datetime
from fastapi import APIRouter, HTTPException
from app.models.chat import ChatRequest, ChatResponse
from app.agents.orchestrator_agent import create_orchestrator
from app.db.mongo import conversations_collection

logger = logging.getLogger(__name__)
router = APIRouter()

# In-memory conversation history (per-session; production would use DB)
_conversations: dict[str, list[dict]] = {}


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Conversational turn — orchestrator decides whether to ask a follow-up or start searching."""
    conversation_id = request.conversation_id or str(uuid.uuid4())

    # Get or create conversation history
    if conversation_id not in _conversations:
        _conversations[conversation_id] = []

    history = _conversations[conversation_id]
    history.append({
        "role": "user",
        "content": request.message,
        "timestamp": datetime.utcnow().isoformat(),
    })

    try:
        # Build context from conversation history
        context = "\n".join([
            f"{'User' if msg['role'] == 'user' else 'Assistant'}: {msg['content']}"
            for msg in history[-10:]  # Last 10 messages for context
        ])

        # Create orchestrator and get response
        orchestrator = create_orchestrator()
        result = orchestrator(
            f"Conversation so far:\n{context}\n\nUser's latest message: {request.message}"
        )

        response_text = str(result.message) if hasattr(result, 'message') else str(result)

        # Store assistant response
        history.append({
            "role": "assistant",
            "content": response_text,
            "timestamp": datetime.utcnow().isoformat(),
        })

        # Try to save to MongoDB
        try:
            coll = conversations_collection()
            if coll is not None:
                await coll.update_one(
                    {"conversation_id": conversation_id},
                    {"$set": {
                        "conversation_id": conversation_id,
                        "messages": history,
                        "updated_at": datetime.utcnow(),
                    }},
                    upsert=True,
                )
        except Exception as e:
            logger.warning(f"Failed to save conversation to MongoDB: {e}")

        # Determine action type from response content
        action = "general"
        response_lower = response_text.lower()
        if any(kw in response_lower for kw in ["searching", "let me search", "finding schemes", "looking for"]):
            action = "searching"
        elif any(kw in response_lower for kw in ["appear to meet", "eligible", "qualify", "scheme"]):
            action = "results"
        elif any(kw in response_lower for kw in ["what is your", "how old", "which state", "tell me about"]):
            action = "ask_profile"

        return ChatResponse(
            message=response_text,
            conversation_id=conversation_id,
            action=action,
            profile=request.profile,
        )

    except Exception as e:
        logger.error(f"Chat failed: {e}")
        raise HTTPException(status_code=500, detail=f"Chat processing failed: {str(e)}")


@router.get("/history/{conversation_id}")
async def get_history(conversation_id: str):
    """Get conversation history."""
    history = _conversations.get(conversation_id, [])
    return {"conversation_id": conversation_id, "messages": history}
