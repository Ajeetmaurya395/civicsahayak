"""Documents API — upload and process documents."""
import json
import uuid
import logging
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.agents.document_agent import process_document

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    document_type: str = Form("unknown"),
):
    """Upload a document for processing.

    Routes to Firecracker sandbox (or stub) for OCR/extraction.
    """
    try:
        doc_id = str(uuid.uuid4())

        # Read file content (limit size)
        content = await file.read()
        if len(content) > 10 * 1024 * 1024:  # 10MB limit
            raise HTTPException(status_code=413, detail="File too large (max 10MB)")

        # Process via document agent
        result_json = process_document(json.dumps({
            "document_id": doc_id,
            "document_type": document_type,
            "filename": file.filename,
            "content_type": file.content_type,
            "size_bytes": len(content),
        }))

        result = json.loads(result_json)
        result["document_id"] = doc_id

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Document upload failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{document_id}/status")
async def get_document_status(document_id: str):
    """Get document processing status."""
    return {
        "document_id": document_id,
        "status": "processed",
        "message": "Document processing complete",
    }
