# Cybersecurity Intelligence Platform (CTS)

A comprehensive cybersecurity intelligence infrastructure with a multi-agent architecture, designed to provide comprehensive threat detection, analysis, and response capabilities.

## Quick Links

- **[Setup Guide](./SETUP.md)** - Detailed setup instructions
- **[Architecture Documentation](./ARCHITECTURE.md)** - System architecture overview  
- **[Project Summary](./PROJECT_SUMMARY.md)** - Feature summary and status

## Architecture Overview

This platform implements a **master-agent orchestration pattern** where:
- **Single Chat Interface**: Users interact through one unified chat interface
- **Master Agent**: Coordinates and routes tasks to specialized agents
- **Specialized Agents**: Handle specific domains (Individuals, Organizations, Transactions, etc.)

## Key Features

### Core Components
- **Master Agent Orchestrator**: Central coordination hub for all agents
- **Individual Agent (UEBA)**: User Entity and Behavior Analytics
- **Organization Agent**: Network and system monitoring
- **Transaction Agent**: Fraud detection and transaction monitoring
- **Supervisor Agent**: Health checks and integrity monitoring of other agents
- **Threat Intelligence Agent**: Aggregates and analyzes threat data
- **SOAR Agent**: Security Orchestration, Automation, and Response

### Data Capabilities
- **Multi-format Ingestion**: Supports spreadsheets, PDFs, documents, APIs, logs
- **Threat Intelligence Integration**: OSINT feeds, commercial feeds, community sharing (STIX/TAXII)
- **Sanctions List Integration**: UN, US (OFAC), UK, EU sanctions screening
- **Real-time Monitoring**: Live threat detection and alerting

### Dashboard & Interface
- Modern dark-mode UI optimized for SOC operations
- Real-time threat maps and geospatial visualizations
- Interactive link analysis graphs
- Predictive risk scoring and prioritization
- Integrated incident response workflows

## Technology Stack

### Frontend
- **Next.js 14** (React framework)
- **TypeScript** (type safety)
- **Tailwind CSS** (styling)
- **Recharts** (data visualization)
- **Leaflet** (geospatial maps)

### Backend
- **Python 3.11+**
- **FastAPI** (API framework)
- **LangChain** (agent orchestration)
- **Celery** (background tasks)
- **Supabase** (PostgreSQL database)

### Database
- **Supabase** (PostgreSQL with real-time capabilities)

## Getting Started

### Prerequisites
- Node.js 18+ and npm
- Python 3.11+
- Supabase account and project
- Redis (for background tasks)

### Installation

1. **Clone and install frontend dependencies:**
```bash
npm install
```

2. **Install backend dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables:**
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. **Set up Supabase:**
   - Create a new Supabase project
   - Run the SQL schema from `supabase/schema.sql` in the Supabase SQL editor
   - Add your Supabase URL and keys to `.env`

5. **Start the development servers:**

Frontend (Terminal 1):
```bash
npm run dev
```

Backend (Terminal 2):
```bash
cd backend
uvicorn main:app --reload --port 8000
```

Celery Worker (Terminal 3):
```bash
cd backend
celery -A tasks.celery_app worker --loglevel=info
```

6. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## Project Structure

```
CTS_Rev01/
├── src/                    # Next.js frontend source
│   ├── app/               # Next.js app router
│   ├── components/        # React components
│   ├── lib/              # Utilities and Supabase client
│   └── types/            # TypeScript types
├── backend/              # Python backend
│   ├── agents/          # Agent implementations
│   ├── api/             # FastAPI routes
│   ├── core/            # Core utilities
│   ├── data_ingestion/  # Data ingestion handlers
│   ├── intelligence/    # Threat intelligence modules
│   └── main.py          # FastAPI application
├── supabase/            # Database schema
└── README.md
```

## Key Concepts

### Agent Architecture
Agents are specialized modules that process specific types of data:
- Each agent is independent and can be scaled horizontally
- Agents communicate through the master orchestrator
- All agent activities are logged for audit and analysis

### Data Flow
1. Data enters through various ingestion channels
2. Master agent receives requests via chat interface
3. Master agent routes to appropriate specialized agent
4. Agents process and enrich data
5. Results are stored in Supabase and displayed in dashboard
6. Automated responses triggered via SOAR when configured

### Security Features
- Row Level Security (RLS) on all database tables
- Encrypted data transmission
- Audit logging for all operations
- Role-based access control (RBAC)

## License

This project is proprietary and confidential.

## Support

For questions or issues, please contact the development team.