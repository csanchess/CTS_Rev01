"""
Master Agent - Routes requests to specialized agents
Acts as the single point of contact for users via chat interface
"""
from typing import Dict, Any, Optional
import json
from datetime import datetime

from agents.base_agent import BaseAgent
from core.supabase_client import get_supabase_client


class MasterAgent(BaseAgent):
    """Master agent that orchestrates other agents"""
    
    def __init__(self, agents: Dict[str, Any]):
        super().__init__("master", "Master Orchestrator")
        self.agents = agents
        self.supabase = get_supabase_client()
        self.status = "active"
    
    async def process_message(self, message: str, user_id: str, session_id: str) -> Dict[str, Any]:
        """Process a chat message and route to appropriate agent"""
        try:
            # Determine which agent should handle this message
            routing_decision = await self._route_message(message)
            target_agent_type = routing_decision.get("agent_type")
            
            # Get the appropriate agent
            agent = self.agents.get(target_agent_type)
            
            if not agent:
                return {
                    "response": "I apologize, but I couldn't determine which specialist to route your request to. Could you please rephrase your question?",
                    "agent_used": "master",
                    "confidence": 0.0
                }
            
            # Create task for the agent
            task = {
                "task_id": self._create_task_id(),
                "message": message,
                "user_id": user_id,
                "session_id": session_id,
                "context": routing_decision.get("context", {})
            }
            
            # Process with the specialized agent
            result = await agent.process(task)
            
            # Log the conversation
            await self._log_conversation(user_id, session_id, message, result.get("response", ""), target_agent_type)
            
            return {
                "response": result.get("response", "I've processed your request."),
                "agent_used": target_agent_type,
                "data": result.get("data"),
                "confidence": routing_decision.get("confidence", 0.8),
                "suggested_actions": result.get("suggested_actions", [])
            }
            
        except Exception as e:
            return {
                "response": f"I encountered an error processing your request: {str(e)}",
                "agent_used": "master",
                "error": str(e),
                "confidence": 0.0
            }
    
    async def _route_message(self, message: str) -> Dict[str, Any]:
        """
        Route message to appropriate agent based on content
        In a production system, this would use NLP/ML models
        """
        message_lower = message.lower()
        
        # Simple keyword-based routing (can be enhanced with ML)
        routing_keywords = {
            "individual": ["user", "person", "employee", "individual", "account", "login", "access", "behavior", "anomaly"],
            "organization": ["company", "organization", "network", "system", "infrastructure", "vulnerability", "scan"],
            "transaction": ["transaction", "payment", "fraud", "money", "transfer", "financial", "purchase"],
            "threat": ["threat", "malware", "attack", "indicator", "ioc", "threat intelligence", "sanctions"],
            "incident": ["incident", "breach", "alert", "investigation", "forensic"],
            "soar": ["automate", "playbook", "workflow", "response", "contain", "block"]
        }
        
        scores = {}
        for agent_type, keywords in routing_keywords.items():
            score = sum(1 for keyword in keywords if keyword in message_lower)
            if score > 0:
                scores[agent_type] = score
        
        if scores:
            # Get agent with highest score
            target_agent = max(scores.items(), key=lambda x: x[1])
            confidence = min(target_agent[1] / len(message_lower.split()) * 2, 1.0)
            
            return {
                "agent_type": target_agent[0],
                "confidence": confidence,
                "context": {"keywords_matched": target_agent[1]}
            }
        
        # Default to threat intelligence if unclear
        return {
            "agent_type": "threat_intel",
            "confidence": 0.5,
            "context": {}
        }
    
    async def _log_conversation(self, user_id: str, session_id: str, message: str, response: str, agent_used: str):
        """Log conversation to database"""
        try:
            self.supabase.table('chat_conversations').insert({
                'user_id': user_id,
                'session_id': session_id,
                'message': message,
                'response': response,
                'agent_used': agent_used,
                'metadata': {},
                'created_at': datetime.utcnow().isoformat()
            }).execute()
        except Exception as e:
            print(f"Error logging conversation: {e}")
    
    async def process(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process task (implements base class method)"""
        return await self.process_message(
            task.get("message", ""),
            task.get("user_id", ""),
            task.get("session_id", "")
        )
