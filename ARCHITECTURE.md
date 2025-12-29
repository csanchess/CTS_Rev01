# Architecture Overview

## System Architecture

The Cybersecurity Intelligence Platform follows a **multi-agent architecture** with a master orchestrator pattern.

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (Next.js)                   │
│  ┌──────────────┐  ┌──────────────┐                    │
│  │  Dashboard   │  │ Chat Interface│                    │
│  └──────────────┘  └──────────────┘                    │
└───────────────────┬─────────────────────────────────────┘
                    │ HTTP/REST API
┌───────────────────┴─────────────────────────────────────┐
│              Backend (FastAPI)                          │
│  ┌──────────────────────────────────────────┐          │
│  │      Master Agent Orchestrator           │          │
│  │  (Routes requests to specialized agents) │          │
│  └──────┬───────────────────────────────────┘          │
│         │                                               │
│    ┌────┴────────────────────────────────┐            │
│    │                                      │            │
│  ┌─▼──────────┐  ┌──────────────────┐   │            │
│  │ Individual │  │  Organization    │   │            │
│  │   Agent    │  │     Agent        │   │            │
│  └────────────┘  └──────────────────┘   │            │
│                                            │            │
│  ┌──────────────┐  ┌──────────────────┐  │            │
│  │ Transaction  │  │ Threat Intel     │  │            │
│  │    Agent     │  │     Agent        │  │            │
│  └──────────────┘  └──────────────────┘  │            │
│                                            │            │
│  ┌──────────────┐  ┌──────────────────┐  │            │
│  │  Supervisor  │  │    SOAR Agent    │  │            │
│  │    Agent     │  │                  │  │            │
│  └──────────────┘  └──────────────────┘  │            │
└──────────────────────┬─────────────────────────────────┘
                       │
┌──────────────────────┴─────────────────────────────────┐
│              Supabase (PostgreSQL)                     │
│  - Users, Organizations, Individuals                   │
│  - Transactions, Threats, Incidents                    │
│  - Agents, Tasks, Analytics                            │
│  - Sanctions Lists, Threat Feeds                       │
└────────────────────────────────────────────────────────┘
```

## Agent Types

### 1. Master Agent
- **Purpose**: Single point of contact for users
- **Responsibilities**:
  - Routes incoming messages to appropriate specialized agents
  - Coordinates multi-agent workflows
  - Aggregates responses from multiple agents
  - Manages conversation context

### 2. Individual Agent (UEBA)
- **Purpose**: User Entity and Behavior Analytics
- **Responsibilities**:
  - Monitor user activities and access patterns
  - Detect anomalous behavior
  - Calculate risk scores for individuals
  - Identify potential insider threats

### 3. Organization Agent
- **Purpose**: Network and system monitoring
- **Responsibilities**:
  - Monitor organizational security posture
  - Track vulnerabilities and patch status
  - Analyze network traffic patterns
  - Assess overall security health

### 4. Transaction Agent
- **Purpose**: Fraud detection and transaction monitoring
- **Responsibilities**:
  - Monitor financial transactions
  - Detect fraudulent patterns
  - Analyze transaction anomalies
  - Flag suspicious activities

### 5. Supervisor Agent
- **Purpose**: Health and integrity monitoring
- **Responsibilities**:
  - Monitor health of all other agents
  - Perform security audits
  - Verify data integrity
  - Track performance metrics

### 6. Threat Intelligence Agent
- **Purpose**: Threat data aggregation and analysis
- **Responsibilities**:
  - Integrate threat feeds (OSINT, commercial, government)
  - Check sanctions lists (UN, US, UK, EU)
  - Analyze IOCs (Indicators of Compromise)
  - Correlate threat data

### 7. SOAR Agent
- **Purpose**: Security Orchestration, Automation, and Response
- **Responsibilities**:
  - Execute automated response playbooks
  - Coordinate incident response workflows
  - Trigger automated containment actions
  - Manage security automation

## Data Flow

1. **User Input**: User sends message via chat interface
2. **Master Agent**: Receives message and determines routing
3. **Specialized Agent**: Processes request based on domain expertise
4. **Data Processing**: Agent queries database, performs analysis
5. **Response Generation**: Agent generates response with data/actions
6. **Master Agent**: Aggregates and formats response
7. **User Output**: Response displayed in chat interface

## Database Schema

### Core Entities
- **users**: User accounts and authentication
- **organizations**: Organization records
- **individuals**: Individual/user entity records with behavior data
- **transactions**: Transaction records for fraud detection
- **threats**: Threat intelligence data
- **incidents**: Security incident records
- **agents**: Agent registry and status
- **sanctions_entries**: Sanctions list entries

### Supporting Tables
- **agent_tasks**: Task tracking for agents
- **soar_playbooks**: Automation playbooks
- **soar_executions**: Playbook execution logs
- **data_ingestions**: Data import tracking
- **threat_feeds**: Threat feed configurations
- **analytics**: Metrics and analytics data
- **chat_conversations**: Chat history

## Technology Stack

### Frontend
- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first styling
- **Supabase Client**: Database and auth client

### Backend
- **FastAPI**: Modern Python web framework
- **Python 3.11+**: Backend language
- **LangChain**: AI agent framework (optional)
- **Celery**: Background task processing
- **Redis**: Task queue backend

### Database
- **Supabase/PostgreSQL**: Primary database
- **Row Level Security (RLS)**: Data access control

## Security Features

1. **Row Level Security**: Database-level access control
2. **Role-Based Access Control**: User roles (admin, analyst, viewer, ciso)
3. **Encrypted Communications**: HTTPS/TLS for all communications
4. **Audit Logging**: Comprehensive logging of all operations
5. **Agent Integrity Monitoring**: Supervisor agent ensures agent security

## Scalability Considerations

- **Modular Agents**: Each agent can be scaled independently
- **Horizontal Scaling**: Agents can run on multiple instances
- **Async Processing**: Background tasks for heavy operations
- **Database Indexing**: Optimized queries with proper indexes
- **Caching**: Redis for frequently accessed data

## Future Enhancements

- Machine learning models for threat detection
- Real-time threat map with WebSocket updates
- Advanced visualization components
- Integration with external SIEM/SOAR platforms
- Enhanced NLP for better message routing
- Multi-tenant support
- API rate limiting and throttling
