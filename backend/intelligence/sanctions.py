"""
Sanctions List Integration
Handles UN, US, UK, EU sanctions lists
"""
from typing import List, Dict, Any, Optional
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import csv
import io

from core.supabase_client import get_supabase_client
from core.config import settings


class SanctionsListManager:
    """Manage sanctions lists from various sources"""
    
    def __init__(self):
        self.supabase = get_supabase_client()
    
    async def sync_un_sanctions(self):
        """Sync UN sanctions list"""
        try:
            response = requests.get(settings.un_sanctions_url, timeout=30)
            response.raise_for_status()
            
            # Parse XML
            root = ET.fromstring(response.content)
            
            # Process sanctions entries
            # This is simplified - actual UN list structure is complex
            entries = []
            for individual in root.findall('.//INDIVIDUAL'):
                name = individual.findtext('FIRST_NAME', '') + ' ' + individual.findtext('SECOND_NAME', '')
                entries.append({
                    'entity_name': name.strip(),
                    'entity_type': 'individual',
                    'list_source': 'UN',
                    'identifiers': {},
                    'raw_data': ET.tostring(individual, encoding='unicode')
                })
            
            # Store in database
            if entries:
                self.supabase.table('sanctions_entries').upsert(
                    entries,
                    on_conflict='entity_name,list_source'
                ).execute()
            
            return len(entries)
        except Exception as e:
            print(f"Error syncing UN sanctions: {e}")
            return 0
    
    async def sync_ofac_sanctions(self):
        """Sync OFAC (US) sanctions list"""
        try:
            # OFAC provides CSV format
            response = requests.get(settings.ofac_sanctions_url, timeout=30)
            response.raise_for_status()
            
            # Parse CSV
            csv_content = io.StringIO(response.text)
            reader = csv.DictReader(csv_content)
            
            entries = []
            for row in reader:
                entries.append({
                    'entity_name': row.get('Name', ''),
                    'entity_type': 'individual' if row.get('Type') == 'Individual' else 'organization',
                    'list_source': 'US_OFAC',
                    'identifiers': {
                        'program': row.get('Program', ''),
                        'sdn_type': row.get('Type', '')
                    },
                    'raw_data': row
                })
            
            if entries:
                self.supabase.table('sanctions_entries').upsert(
                    entries,
                    on_conflict='entity_name,list_source'
                ).execute()
            
            return len(entries)
        except Exception as e:
            print(f"Error syncing OFAC sanctions: {e}")
            return 0
    
    async def check_sanctions(self, entity_name: str) -> List[Dict[str, Any]]:
        """Check if an entity is on any sanctions list"""
        try:
            result = self.supabase.table('sanctions_entries')\
                .select('*')\
                .ilike('entity_name', f'%{entity_name}%')\
                .execute()
            
            return result.data or []
        except Exception as e:
            print(f"Error checking sanctions: {e}")
            return []
    
    async def sync_all_sanctions(self):
        """Sync all sanctions lists"""
        results = {
            'UN': await self.sync_un_sanctions(),
            'US_OFAC': await self.sync_ofac_sanctions(),
            # UK and EU would be added similarly
        }
        return results
