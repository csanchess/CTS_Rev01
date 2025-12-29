"""
Data Ingestion API Routes
"""
from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import Optional

from core.supabase_client import get_supabase_client
from data_ingestion.processors import DataIngestionProcessor

router = APIRouter()


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    source_type: Optional[str] = None
):
    """Upload and process a file"""
    try:
        # Determine source type from file extension if not provided
        if not source_type:
            ext = file.filename.split('.')[-1].lower() if file.filename else 'unknown'
            source_type_map = {
                'xlsx': 'spreadsheet',
                'xls': 'spreadsheet',
                'csv': 'spreadsheet',
                'pdf': 'pdf',
                'doc': 'doc',
                'docx': 'doc',
                'txt': 'log'
            }
            source_type = source_type_map.get(ext, 'file')
        
        # Process file
        processor = DataIngestionProcessor()
        result = await processor.process_file(file, source_type)
        
        return {
            "message": "File processed successfully",
            "ingestion_id": result.get("ingestion_id"),
            "records_processed": result.get("records_processed", 0)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status/{ingestion_id}")
async def get_ingestion_status(ingestion_id: str):
    """Get ingestion status"""
    try:
        supabase = get_supabase_client()
        result = supabase.table('data_ingestions')\
            .select('*')\
            .eq('id', ingestion_id)\
            .execute()
        
        if not result.data:
            raise HTTPException(status_code=404, detail="Ingestion not found")
        
        return {"ingestion": result.data[0]}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
