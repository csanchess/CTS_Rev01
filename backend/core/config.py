"""
Configuration settings
"""
import os
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings"""
    
    # Supabase
    supabase_url: str = os.getenv("NEXT_PUBLIC_SUPABASE_URL", "")
    supabase_service_key: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
    supabase_anon_key: str = os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY", "")
    
    # API
    api_url: str = os.getenv("API_URL", "http://localhost:8000")
    allowed_origins: List[str] = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
    
    # OpenAI
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    
    # Redis
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # Threat Intelligence
    virustotal_api_key: str = os.getenv("VIRUSTOTAL_API_KEY", "")
    alienvault_otx_api_key: str = os.getenv("ALIENVAULT_OTX_API_KEY", "")
    
    # Sanctions Lists
    un_sanctions_url: str = os.getenv("UN_SANCTIONS_LIST_URL", "https://scsanctions.un.org/resources/xml/en/consolidated.xml")
    ofac_sanctions_url: str = os.getenv("OFAC_SANCTIONS_LIST_URL", "https://ofac.treasury.gov/consolidated-sanctions-list-data-files")
    
    # Security
    jwt_secret: str = os.getenv("JWT_SECRET", "")
    encryption_key: str = os.getenv("ENCRYPTION_KEY", "")
    
    # Debug
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
