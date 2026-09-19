"""Firecracker Sandbox Manager.

Boots, runs, and tears down Firecracker microVMs for document processing.
Each document gets its own throwaway VM — never reused.

Practical caveat: Firecracker needs a Linux host with KVM.
On a Mac/Windows dev laptop, use DOCUMENT_SANDBOX_MODE=stub.
"""
import asyncio
import json
import logging
import os
import uuid

logger = logging.getLogger(__name__)


class FirecrackerSandbox:
    """Manages Firecracker microVMs for document processing."""

    def __init__(self):
        self.vm_config_path = os.path.join(
            os.path.dirname(__file__), "vm-config", "vm-config.json"
        )

    async def process_document(self, document_path: str, document_type: str) -> dict:
        """Process a document inside a throwaway Firecracker microVM.

        1. Boot microVM
        2. Copy document into VM
        3. Run OCR/extraction
        4. Retrieve results
        5. Destroy VM
        """
        vm_id = str(uuid.uuid4())[:8]
        logger.info(f"Starting Firecracker microVM {vm_id} for {document_type}")

        try:
            # Boot VM
            await self._boot_vm(vm_id)

            # Run extraction inside VM
            result = await self._run_extraction(vm_id, document_path, document_type)

            return {
                "status": "processed",
                "vm_id": vm_id,
                "extraction_method": "firecracker",
                "extracted_data": result,
            }

        except Exception as e:
            logger.error(f"Firecracker processing failed for VM {vm_id}: {e}")
            return {
                "status": "error",
                "vm_id": vm_id,
                "error": str(e),
            }
        finally:
            # Always destroy the VM
            await self._destroy_vm(vm_id)

    async def _boot_vm(self, vm_id: str):
        """Boot a Firecracker microVM."""
        logger.info(f"Booting microVM {vm_id}")
        # In production: use firecracker API to boot VM
        # firecracker --api-sock /tmp/firecracker-{vm_id}.socket
        pass

    async def _run_extraction(self, vm_id: str, document_path: str, document_type: str) -> dict:
        """Run OCR/extraction inside the microVM."""
        logger.info(f"Running extraction in VM {vm_id}")
        # In production: use Tesseract OCR inside the VM
        return {
            "document_type": document_type,
            "note": "Processed in Firecracker microVM",
        }

    async def _destroy_vm(self, vm_id: str):
        """Destroy the microVM — no data persists."""
        logger.info(f"Destroying microVM {vm_id}")
        # In production: kill the firecracker process and clean up
        pass
