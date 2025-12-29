"""
Incidents API Routes
"""
from fastapi import APIRouter, HTTPException
from typing import Optional
from pydantic import BaseModel

from core.supabase_client import get_supabase_client

router = APIRouter()


@router.get("/")
async def get_incidents(limit: int = 20, status: Optional[str] = None):
    """Get incidents"""
    try:
        supabase = get_supabase_client()
        query = supabase.table('incidents').select('*')
        
        if status:
            query = query.eq('status', status)
        
        query = query.order('created_at', desc=True).limit(limit)
        result = query.execute()
        
        return {"incidents": result.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{incident_id}")
async def get_incident(incident_id: str):
    """Get specific incident"""
    try:
        supabase = get_supabase_client()
        result = supabase.table('incidents').select('*').eq('id', incident_id).execute()
        
        if not result.data:
            raise HTTPException(status_code=404, detail="Incident not found")
        
        return {"incident": result.data[0]}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
