"""
Analytics API Routes
"""
from fastapi import APIRouter, HTTPException
from typing import Optional
from datetime import datetime, timedelta

from core.supabase_client import get_supabase_client

router = APIRouter()


@router.get("/dashboard")
async def get_dashboard_analytics(days: int = 7):
    """Get dashboard analytics"""
    try:
        supabase = get_supabase_client()
        
        # Get various metrics
        # Incidents by severity
        incidents_result = supabase.table('incidents').select('severity').execute()
        
        # Threats count
        threats_result = supabase.table('threats').select('id', count='exact').execute()
        
        # Transactions flagged
        transactions_result = supabase.table('transactions')\
            .select('id', count='exact')\
            .eq('fraud_indicator', True)\
            .execute()
        
        return {
            "incidents": {
                "total": len(incidents_result.data),
                "by_severity": _count_by_field(incidents_result.data, 'severity')
            },
            "threats": {
                "total": threats_result.count if hasattr(threats_result, 'count') else len(threats_result.data)
            },
            "transactions": {
                "flagged": transactions_result.count if hasattr(transactions_result, 'count') else len(transactions_result.data)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def _count_by_field(data: list, field: str) -> dict:
    """Helper to count items by field"""
    counts = {}
    for item in data:
        value = item.get(field, 'unknown')
        counts[value] = counts.get(value, 0) + 1
    return counts
