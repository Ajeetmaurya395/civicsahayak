"""CivicOS Orchestrator — FastAPI application entry point."""
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from app.api import chat, profile, schemes, documents  # noqa: E402
from app.db.mongo import connect_db, close_db  # noqa: E402


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown lifecycle."""
    await connect_db()
    yield
    await close_db()


app = FastAPI(
    title="CivicOS Orchestrator",
    description="AI-powered Government Scheme Discovery Platform for India",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API routers
app.include_router(chat.router, prefix="/chat", tags=["Chat"])
app.include_router(profile.router, prefix="/profile", tags=["Profile"])
app.include_router(schemes.router, prefix="/schemes", tags=["Schemes"])
app.include_router(documents.router, prefix="/documents", tags=["Documents"])


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "civicos-orchestrator"}
