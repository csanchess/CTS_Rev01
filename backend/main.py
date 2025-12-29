"""
Cybersecurity Intelligence Platform - FastAPI Backend
Main application entry point
"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

from api.routes import chat, agents, threats, incidents, data_ingestion, analytics
from core.supabase_client import get_supabase_client
from core.agent_orchestrator import AgentOrchestrator

load_dotenv()

# Global agent orchestrator instance
orchestrator: AgentOrchestrator = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown"""
    global orchestrator
    # Startup
    print("Initializing Agent Orchestrator...")
    orchestrator = AgentOrchestrator()
    await orchestrator.initialize()
    # Store orchestrator in app state for dependency injection
    app.state.orchestrator = orchestrator
    yield
    # Shutdown
    print("Shutting down Agent Orchestrator...")
    if orchestrator:
        await orchestrator.shutdown()


app = FastAPI(
    title="Cybersecurity Intelligence Platform API",
    description="Multi-agent cybersecurity intelligence and threat detection platform",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Cybersecurity Intelligence Platform API",
        "version": "1.0.0",
        "status": "operational"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    global orchestrator
    health_status = {
        "status": "healthy",
        "orchestrator": orchestrator.status if orchestrator else "not_initialized"
    }
    return health_status


# Include routers
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(agents.router, prefix="/api/agents", tags=["agents"])
app.include_router(threats.router, prefix="/api/threats", tags=["threats"])
app.include_router(incidents.router, prefix="/api/incidents", tags=["incidents"])
app.include_router(data_ingestion.router, prefix="/api/ingestion", tags=["ingestion"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc) if os.getenv("DEBUG") == "true" else "An error occurred"
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
