"""CivicOS Eligibility Engine — Deterministic rules evaluation.

This is a standalone FastAPI service that evaluates eligibility
using pure deterministic logic. NO LLM calls. The LLM only
extracts criteria; this engine decides eligibility.

Replaces the Java/Corretto engine from the original spec.
"""
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from engine.rule_evaluator import evaluate_eligibility
from pydantic import BaseModel
from typing import Optional

app = FastAPI(
    title="CivicOS Eligibility Engine",
    description="Deterministic eligibility rules evaluation — no LLM",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class EvaluateRequest(BaseModel):
    user_profile: dict
    scheme_criteria: list[dict]


@app.post("/evaluate")
async def evaluate(request: EvaluateRequest):
    """Evaluate user eligibility against scheme criteria.

    POST /evaluate — the single endpoint. Deterministic only.
    """
    results = evaluate_eligibility(
        user_profile=request.user_profile,
        scheme_criteria=request.scheme_criteria,
    )
    return {"results": results}


@app.get("/health")
async def health():
    return {"status": "healthy", "service": "eligibility-engine"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8081)
