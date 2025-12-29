"""
Agents API Routes
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import Optional

from core.agent_orchestrator import AgentOrchestrator

router = APIRouter()


def get_orchestrator() -> AgentOrchestrator:
    """Get orchestrator instance - simplified for now"""
    raise HTTPException(status_code=501, detail="Orchestrator dependency injection not yet implemented")


@router.get("/status")
async def get_agents_status():
    """Get status of all agents"""
    # This will be properly implemented with dependency injection
    return {
        "message": "Agent status endpoint - requires orchestrator integration",
        "agents": {}
    }
