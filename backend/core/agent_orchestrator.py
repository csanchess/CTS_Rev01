"""
Master Agent Orchestrator
Coordinates all specialized agents in the platform
"""
from typing import Dict, List, Optional, Any
import asyncio
from datetime import datetime
import uuid

from agents.master_agent import MasterAgent
from agents.individual_agent import IndividualAgent
from agents.organization_agent import OrganizationAgent
from agents.transaction_agent import TransactionAgent
from agents.supervisor_agent import SupervisorAgent
from agents.threat_intel_agent import ThreatIntelAgent
from agents.soar_agent import SOARAgent
from core.supabase_client import get_supabase_client


class AgentOrchestrator:
    """Master orchestrator that coordinates all agents"""
    
    def __init__(self):
        self.supabase = get_supabase_client()
        self.master_agent: Optional[MasterAgent] = None
        self.agents: Dict[str, Any] = {}
        self.status = "initializing"
        self.initialized = False
    
    async def initialize(self):
        """Initialize all agents"""
        try:
            print("Initializing specialized agents...")
            
            # Initialize specialized agents
            self.agents['individual'] = IndividualAgent()
            self.agents['organization'] = OrganizationAgent()
            self.agents['transaction'] = TransactionAgent()
            self.agents['supervisor'] = SupervisorAgent(self.agents)
            self.agents['threat_intel'] = ThreatIntelAgent()
            self.agents['soar'] = SOARAgent()
            
            # Initialize master agent
            self.master_agent = MasterAgent(self.agents)
            
            # Register agents in database
            await self._register_agents()
            
            # Start supervisor monitoring
            if 'supervisor' in self.agents:
                asyncio.create_task(self.agents['supervisor'].start_monitoring())
            
            self.status = "operational"
            self.initialized = True
            print("All agents initialized successfully")
            
        except Exception as e:
            print(f"Error initializing agents: {e}")
            self.status = "error"
            raise
    
    async def _register_agents(self):
        """Register all agents in the database"""
        try:
            agent_types = {
                'master': 'Master Orchestrator',
                'individual': 'Individual/UEBA Agent',
                'organization': 'Organization Agent',
                'transaction': 'Transaction Agent',
                'supervisor': 'Supervisor Agent',
                'threat_intel': 'Threat Intelligence Agent',
                'soar': 'SOAR Agent'
            }
            
            for agent_type, name in agent_types.items():
                # Check if agent exists
                result = self.supabase.table('agents').select('id').eq('agent_type', agent_type).execute()
                
                if not result.data:
                    # Create agent record
                    self.supabase.table('agents').insert({
                        'agent_type': agent_type,
                        'name': name,
                        'status': 'active',
                        'health_status': {'status': 'healthy'},
                        'last_heartbeat': datetime.utcnow().isoformat(),
                        'configuration': {},
                        'performance_metrics': {}
                    }).execute()
                else:
                    # Update heartbeat
                    self.supabase.table('agents').update({
                        'status': 'active',
                        'last_heartbeat': datetime.utcnow().isoformat()
                    }).eq('agent_type', agent_type).execute()
                    
        except Exception as e:
            print(f"Error registering agents: {e}")
    
    async def process_chat_message(self, message: str, user_id: str, session_id: str) -> Dict[str, Any]:
        """Process a chat message through the master agent"""
        if not self.master_agent:
            raise RuntimeError("Master agent not initialized")
        
        return await self.master_agent.process_message(message, user_id, session_id)
    
    async def get_agent_status(self) -> Dict[str, Any]:
        """Get status of all agents"""
        status = {
            'orchestrator': self.status,
            'agents': {}
        }
        
        for agent_type, agent in self.agents.items():
            try:
                agent_status = await agent.get_status() if hasattr(agent, 'get_status') else {'status': 'unknown'}
                status['agents'][agent_type] = agent_status
            except Exception as e:
                status['agents'][agent_type] = {'status': 'error', 'error': str(e)}
        
        return status
    
    async def shutdown(self):
        """Gracefully shutdown all agents"""
        print("Shutting down agents...")
        self.status = "shutting_down"
        
        for agent_type, agent in self.agents.items():
            try:
                if hasattr(agent, 'shutdown'):
                    await agent.shutdown()
            except Exception as e:
                print(f"Error shutting down {agent_type} agent: {e}")
        
        # Update agent statuses in database
        try:
            self.supabase.table('agents').update({
                'status': 'inactive',
                'last_heartbeat': datetime.utcnow().isoformat()
            }).execute()
        except Exception as e:
            print(f"Error updating agent statuses: {e}")
        
        self.status = "shutdown"
        print("All agents shut down")
