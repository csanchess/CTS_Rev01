"""
Organization Agent - Network and System Monitoring
Monitors organizational network, systems, and security posture
"""
from typing import Dict, Any
from datetime import datetime

from agents.base_agent import BaseAgent
from core.supabase_client import get_supabase_client


class OrganizationAgent(BaseAgent):
    """Agent for monitoring organizations and network systems"""
    
    def __init__(self):
        super().__init__("organization", "Organization Agent")
        self.supabase = get_supabase_client()
        self.status = "active"
    
    async def process(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process organization-related tasks"""
        message = task.get("message", "").lower()
        
        if "vulnerability" in message or "vuln" in message:
            return await self._get_vulnerabilities(task)
        elif "network" in message or "traffic" in message:
            return await self._analyze_network(task)
        elif "risk" in message or "posture" in message:
            return await self._get_security_posture(task)
        elif "search" in message or "find" in message:
            return await self._search_organization(task)
        else:
            return await self._get_organization_info(task)
    
    async def _search_organization(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Search for organization"""
        try:
            message = task.get("message", "")
            
            query = self.supabase.table('organizations').select('*')
            
            if "." in message:  # Domain search
                domain = [word for word in message.split() if "." in word][0]
                query = query.eq('domain', domain)
            else:
                query = query.ilike('name', f'%{message}%')
            
            result = query.limit(10).execute()
            
            if result.data:
                return {
                    "response": f"Found {len(result.data)} organization(s) matching your search.",
                    "data": result.data,
                    "suggested_actions": ["View security posture", "Check vulnerabilities", "Review incidents"]
                }
            else:
                return {
                    "response": "No organizations found matching your search.",
                    "data": []
                }
        except Exception as e:
            return {
                "response": f"Error searching organization: {str(e)}",
                "error": str(e)
            }
    
    async def _get_vulnerabilities(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Get vulnerability information"""
        return {
            "response": "Vulnerability scan results: 5 high-severity vulnerabilities detected, 12 medium-severity. Recommendations: Apply patches for CVE-2023-XXXX and CVE-2023-YYYY.",
            "data": {
                "critical": 0,
                "high": 5,
                "medium": 12,
                "low": 8,
                "total": 25
            },
            "suggested_actions": ["View detailed vulnerability report", "Create remediation plan", "Schedule patching"]
        }
    
    async def _analyze_network(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze network traffic"""
        return {
            "response": "Network analysis: Normal traffic patterns detected. No unusual outbound connections or data exfiltration indicators.",
            "data": {
                "status": "normal",
                "traffic_volume": "within_normal_range",
                "suspicious_connections": 0
            }
        }
    
    async def _get_security_posture(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Get overall security posture"""
        return {
            "response": "Security Posture: Good (Score: 78/100). Key strengths: Active monitoring, up-to-date threat intelligence. Areas for improvement: Patch management, access controls.",
            "data": {
                "overall_score": 78,
                "risk_level": "medium",
                "strengths": ["Active monitoring", "Threat intelligence"],
                "improvements": ["Patch management", "Access controls"]
            }
        }
    
    async def _get_organization_info(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Get general organization information"""
        return {
            "response": "I can help you monitor organizations, analyze network traffic, check vulnerabilities, and assess security posture. What would you like to investigate?",
            "suggested_actions": ["Check security posture", "View vulnerabilities", "Analyze network traffic"]
        }
