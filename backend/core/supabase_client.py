"""
Supabase client configuration and utilities
"""
from supabase import create_client, Client
import os
from typing import Optional

_supabase_client: Optional[Client] = None


def get_supabase_client() -> Client:
    """Get or create Supabase client instance"""
    global _supabase_client
    
    if _supabase_client is None:
        supabase_url = os.getenv("NEXT_PUBLIC_SUPABASE_URL") or os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY")
        
        if not supabase_url or not supabase_key:
            raise ValueError("Supabase URL and key must be set in environment variables")
        
        _supabase_client = create_client(supabase_url, supabase_key)
    
    return _supabase_client


def get_supabase_client_anon() -> Client:
    """Get Supabase client with anon key (for client-side use)"""
    supabase_url = os.getenv("NEXT_PUBLIC_SUPABASE_URL") or os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY")
    
    if not supabase_url or not supabase_key:
        raise ValueError("Supabase URL and anon key must be set")
    
    return create_client(supabase_url, supabase_key)
