"""
Threats API Routes
"""
from fastapi import APIRouter, HTTPException
from typing import Optional
from pydantic import BaseModel

from core.supabase_client import get_supabase_client

router = APIRouter()


class ThreatQuery(BaseModel):
    ioc_value: Optional[str] = None
    severity: Optional[str] = None
    limit: int = 20


@router.get("/")
async def get_threats(limit: int = 20, severity: Optional[str] = None):
    """Get threats"""
    try:
        supabase = get_supabase_client()
        query = supabase.table('threats').select('*')
        
        if severity:
            query = query.eq('severity', severity)
        
        query = query.order('created_at', desc=True).limit(limit)
        result = query.execute()
        
        return {"threats": result.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{threat_id}")
async def get_threat(threat_id: str):
    """Get specific threat"""
    try:
        supabase = get_supabase_client()
        result = supabase.table('threats').select('*').eq('id', threat_id).execute()
        
        if not result.data:
            raise HTTPException(status_code=404, detail="Threat not found")
        
        return {"threat": result.data[0]}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
