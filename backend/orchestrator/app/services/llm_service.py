"""LLM service — model-agnostic wiring for Strands Agents.

Build It track: Ollama (local, free).
Ship It track: flip MODEL_PROVIDER to bedrock — nothing else changes.
"""
import os


def get_model():
    """Return the configured LLM model for Strands agents."""
    provider = os.getenv("MODEL_PROVIDER", "ollama")

    if provider == "ollama":
        from strands.models.ollama import OllamaModel
        return OllamaModel(
            host=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
            model_id=os.getenv("OLLAMA_MODEL", "llama3.1"),
        )
    elif provider == "bedrock":
        from strands.models import BedrockModel
        return BedrockModel(
            model_id=os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-sonnet-20240229-v1:0"),
        )
    else:
        raise ValueError(f"Unknown MODEL_PROVIDER: {provider}")
