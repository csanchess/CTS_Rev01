"""
Base Agent Class
All specialized agents inherit from this base class
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime
import uuid


class BaseAgent(ABC):
    """Base class for all agents"""
    
    def __init__(self, agent_type: str, agent_name: str):
        self.agent_type = agent_type
        self.agent_name = agent_name
        self.agent_id = str(uuid.uuid4())
        self.status = "initializing"
        self.created_at = datetime.utcnow()
    
    @abstractmethod
    async def process(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process a task - must be implemented by subclasses"""
        pass
    
    async def get_status(self) -> Dict[str, Any]:
        """Get agent status"""
        return {
            "agent_type": self.agent_type,
            "agent_name": self.agent_name,
            "agent_id": self.agent_id,
            "status": self.status,
            "created_at": self.created_at.isoformat()
        }
    
    async def initialize(self):
        """Initialize the agent"""
        self.status = "active"
    
    async def shutdown(self):
        """Shutdown the agent"""
        self.status = "inactive"
    
    def _create_task_id(self) -> str:
        """Generate a unique task ID"""
        return f"{self.agent_type}_{uuid.uuid4().hex[:12]}"
