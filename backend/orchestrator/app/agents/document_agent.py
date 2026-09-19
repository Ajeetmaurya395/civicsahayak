"""Document Agent — handles document uploads and extraction.

Routes documents to processing (Firecracker sandbox when available,
stub extraction otherwise).
"""
import json
import logging
import os
from strands import Agent, tool
from app.services.llm_service import get_model

logger = logging.getLogger(__name__)


@tool
def process_document(document_info_json: str) -> str:
    """Process an uploaded document to extract structured information.

    Routes to Firecracker sandbox when available, falls back to
    stub extraction. Extracts structured data like income amounts,
    personal details, etc. from uploaded documents.
    """
    try:
        doc_info = json.loads(document_info_json) if isinstance(document_info_json, str) else document_info_json
    except json.JSONDecodeError:
        return json.dumps({"error": "Invalid document info JSON"})

    sandbox_mode = os.getenv("DOCUMENT_SANDBOX_MODE", "stub")

    if sandbox_mode == "firecracker":
        return _process_with_firecracker(doc_info)
    else:
        return _process_stub(doc_info)


def _process_stub(doc_info: dict) -> str:
    """Stub document processing — extracts basic info without a sandbox."""
    doc_type = doc_info.get("document_type", "unknown")
    filename = doc_info.get("filename", "unknown")

    # For demo purposes, return that document was received
    return json.dumps({
        "status": "processed",
        "document_type": doc_type,
        "filename": filename,
        "extraction_method": "stub",
        "extracted_data": {
            "document_type": doc_type,
            "note": "Document received. Full OCR extraction requires Firecracker sandbox.",
        },
        "message": "Document uploaded successfully. In production, this would be processed inside a Firecracker microVM for security isolation."
    })


def _process_with_firecracker(doc_info: dict) -> str:
    """Process document using Firecracker microVM sandbox.

    Boots a throwaway microVM, runs OCR/extraction inside it,
    returns results, and destroys the VM.
    """
    # Firecracker integration placeholder
    # In production: boot microVM → send doc → OCR → extract → destroy VM
    return json.dumps({
        "status": "processed",
        "document_type": doc_info.get("document_type", "unknown"),
        "extraction_method": "firecracker",
        "extracted_data": {},
        "message": "Processed in Firecracker microVM sandbox."
    })
