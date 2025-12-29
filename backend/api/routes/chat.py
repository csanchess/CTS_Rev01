"""
Chat API Routes - Master agent interface
"""
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import Optional
import uuid

from core.agent_orchestrator import AgentOrchestrator
from core.supabase_client import get_supabase_client

router = APIRouter()


class ChatMessage(BaseModel):
    message: str
    user_id: str
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    agent_used: str
    session_id: str
    data: Optional[dict] = None
    suggested_actions: Optional[list] = None


def get_orchestrator(request: Request) -> AgentOrchestrator:
    """Get orchestrator from app state"""
    orchestrator = getattr(request.app.state, 'orchestrator', None)
    if orchestrator is None:
        raise HTTPException(status_code=503, detail="Orchestrator not initialized")
    return orchestrator


@router.post("/", response_model=ChatResponse)
async def chat(chat_message: ChatMessage, request: Request):
    """Send a message to the master agent"""
    try:
        orchestrator = get_orchestrator(request)
        
        # Generate session ID if not provided
        session_id = chat_message.session_id or str(uuid.uuid4())
        
        # Process message through orchestrator
        result = await orchestrator.process_chat_message(
            chat_message.message,
            chat_message.user_id,
            session_id
        )
        
        return ChatResponse(
            response=result.get("response", ""),
            agent_used=result.get("agent_used", "master"),
            session_id=session_id,
            data=result.get("data"),
            suggested_actions=result.get("suggested_actions", [])
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history/{session_id}")
async def get_chat_history(session_id: str):
    """Get chat history for a session"""
    try:
        supabase = get_supabase_client()
        result = supabase.table('chat_conversations')\
            .select('*')\
            .eq('session_id', session_id)\
            .order('created_at', desc=False)\
            .execute()
        
        return {"conversations": result.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
