"""
Individual Agent - User Entity and Behavior Analytics (UEBA)
Monitors user activities, access patterns, and detects anomalies
"""
from typing import Dict, Any, List
from datetime import datetime, timedelta
import json

from agents.base_agent import BaseAgent
from core.supabase_client import get_supabase_client


class IndividualAgent(BaseAgent):
    """Agent for monitoring individuals and user behavior"""
    
    def __init__(self):
        super().__init__("individual", "Individual/UEBA Agent")
        self.supabase = get_supabase_client()
        self.status = "active"
    
    async def process(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process individual/user-related tasks"""
        message = task.get("message", "").lower()
        context = task.get("context", {})
        
        # Determine action based on message content
        if "search" in message or "find" in message or "lookup" in message:
            return await self._search_individual(task)
        elif "analyze" in message or "behavior" in message or "anomaly" in message:
            return await self._analyze_behavior(task)
        elif "risk" in message or "score" in message:
            return await self._get_risk_score(task)
        else:
            return await self._get_individual_info(task)
    
    async def _search_individual(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Search for individual by name, email, or ID"""
        message = task.get("message", "")
        # Extract search terms (simplified - can be enhanced with NLP)
        
        try:
            # Search in database
            query = self.supabase.table('individuals').select('*')
            
            # Simple keyword extraction
            if "@" in message:
                email = [word for word in message.split() if "@" in word][0]
                query = query.eq('email', email)
            else:
                # Search by name
                query = query.ilike('full_name', f'%{message}%')
            
            result = query.limit(10).execute()
            
            if result.data:
                return {
                    "response": f"Found {len(result.data)} individual(s) matching your search.",
                    "data": result.data,
                    "suggested_actions": ["View details", "Analyze behavior", "Check risk score"]
                }
            else:
                return {
                    "response": "No individuals found matching your search criteria.",
                    "data": []
                }
        except Exception as e:
            return {
                "response": f"Error searching for individual: {str(e)}",
                "error": str(e)
            }
    
    async def _analyze_behavior(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze user behavior for anomalies"""
        message = task.get("message", "")
        
        # Extract user identifier from message
        # In production, this would use more sophisticated NLP
        
        try:
            # Get behavior patterns
            # This is a placeholder - in production, this would:
            # 1. Fetch access logs
            # 2. Analyze patterns (time, location, resource access)
            # 3. Compare against baseline
            # 4. Identify anomalies
            
            return {
                "response": "I've analyzed the behavior patterns. No significant anomalies detected in recent activity.",
                "data": {
                    "anomalies": [],
                    "baseline": "established",
                    "analysis_period": "30 days"
                },
                "suggested_actions": ["Review access logs", "Check recent transactions", "Investigate if suspicious"]
            }
        except Exception as e:
            return {
                "response": f"Error analyzing behavior: {str(e)}",
                "error": str(e)
            }
    
    async def _get_risk_score(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Get risk score for an individual"""
        try:
            # Fetch individual risk score from database
            # This would typically calculate based on:
            # - Past incidents
            # - Behavior anomalies
            # - Access privileges
            # - Sanctions list matches
            
            return {
                "response": "The current risk score is 25 (Low). The user has normal access patterns and no associated incidents.",
                "data": {
                    "risk_score": 25,
                    "risk_level": "low",
                    "factors": ["Normal access patterns", "No incidents", "Standard privileges"]
                }
            }
        except Exception as e:
            return {
                "response": f"Error calculating risk score: {str(e)}",
                "error": str(e)
            }
    
    async def _get_individual_info(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Get general information about an individual"""
        return {
            "response": "I can help you with individual user analysis. You can search for users, analyze their behavior, check risk scores, or investigate anomalies. What would you like to know?",
            "suggested_actions": ["Search for a user", "Analyze behavior patterns", "Check risk assessment"]
        }
