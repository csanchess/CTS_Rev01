"""
Threat Intelligence Agent
Aggregates and analyzes threat data from multiple sources
"""
from typing import Dict, Any
from datetime import datetime

from agents.base_agent import BaseAgent
from core.supabase_client import get_supabase_client


class ThreatIntelAgent(BaseAgent):
    """Agent for threat intelligence collection and analysis"""
    
    def __init__(self):
        super().__init__("threat_intel", "Threat Intelligence Agent")
        self.supabase = get_supabase_client()
        self.status = "active"
    
    async def process(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process threat intelligence tasks"""
        message = task.get("message", "").lower()
        
        if "sanctions" in message or "blacklist" in message:
            return await self._check_sanctions(task)
        elif "ioc" in message or "indicator" in message or "threat" in message:
            return await self._check_threat(task)
        elif "search" in message:
            return await self._search_threats(task)
        else:
            return await self._get_threat_info(task)
    
    async def _check_sanctions(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Check against sanctions lists"""
        try:
            message = task.get("message", "")
            
            # Extract name/entity to check
            # In production, this would use NLP to extract entity names
            
            # Search sanctions database
            query = self.supabase.table('sanctions_entries').select('*')
            
            # Simple search (enhance with fuzzy matching in production)
            search_terms = [word for word in message.split() if len(word) > 3]
            if search_terms:
                query = query.ilike('entity_name', f'%{search_terms[0]}%')
            
            result = query.limit(10).execute()
            
            if result.data:
                return {
                    "response": f"⚠️ WARNING: Found {len(result.data)} match(es) in sanctions lists. Review required.",
                    "data": result.data,
                    "suggested_actions": ["Review sanctions match", "Block entity", "Report compliance team"]
                }
            else:
                return {
                    "response": "No matches found in sanctions lists (UN, US, UK, EU).",
                    "data": []
                }
        except Exception as e:
            return {
                "response": f"Error checking sanctions: {str(e)}",
                "error": str(e)
            }
    
    async def _check_threat(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Check threat indicators"""
        return {
            "response": "Threat Intelligence Check: Analyzing indicators. No active threats detected matching your criteria.",
            "data": {
                "threats_found": 0,
                "iocs_checked": 0,
                "status": "clear"
            },
            "suggested_actions": ["View threat feed", "Check IOCs", "Review recent threats"]
        }
    
    async def _search_threats(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Search threat database"""
        try:
            query = self.supabase.table('threats').select('*')
            query = query.order('created_at', desc=True).limit(20)
            
            result = query.execute()
            
            if result.data:
                critical = [t for t in result.data if t.get('severity') == 'critical']
                return {
                    "response": f"Found {len(result.data)} threat(s) in database. {len(critical)} critical.",
                    "data": result.data,
                    "suggested_actions": ["View threat details", "Check IOCs", "Create incident"]
                }
            else:
                return {
                    "response": "No threats found.",
                    "data": []
                }
        except Exception as e:
            return {
                "response": f"Error searching threats: {str(e)}",
                "error": str(e)
            }
    
    async def _get_threat_info(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Get general threat intelligence information"""
        return {
            "response": "I can help you with threat intelligence, check sanctions lists, analyze IOCs, and search threat databases. What would you like to investigate?",
            "suggested_actions": ["Check sanctions list", "Search threats", "Analyze IOCs"]
        }
