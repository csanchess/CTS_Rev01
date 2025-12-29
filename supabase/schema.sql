-- Cybersecurity Intelligence Platform Database Schema
-- Supabase/PostgreSQL Schema

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users and Authentication (Supabase handles auth, this is for additional user data)
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    email TEXT UNIQUE,
    full_name TEXT,
    role TEXT CHECK (role IN ('admin', 'analyst', 'viewer', 'ciso')),
    organization_id UUID,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Organizations
CREATE TABLE IF NOT EXISTS organizations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    domain TEXT,
    industry TEXT,
    country_code TEXT,
    risk_score NUMERIC(5,2) DEFAULT 0,
    status TEXT CHECK (status IN ('active', 'suspended', 'blocked')) DEFAULT 'active',
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Individuals (User Entity and Behavior Analytics)
CREATE TABLE IF NOT EXISTS individuals (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    email TEXT,
    full_name TEXT,
    organization_id UUID REFERENCES organizations(id),
    risk_score NUMERIC(5,2) DEFAULT 0,
    behavior_profile JSONB,
    access_patterns JSONB,
    anomaly_flags JSONB,
    status TEXT CHECK (status IN ('active', 'suspended', 'investigating')) DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Transactions
CREATE TABLE IF NOT EXISTS transactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    transaction_id TEXT UNIQUE,
    individual_id UUID REFERENCES individuals(id),
    organization_id UUID REFERENCES organizations(id),
    amount NUMERIC(15,2),
    currency TEXT DEFAULT 'USD',
    transaction_type TEXT,
    status TEXT CHECK (status IN ('pending', 'completed', 'flagged', 'blocked')) DEFAULT 'pending',
    risk_score NUMERIC(5,2) DEFAULT 0,
    fraud_indicator BOOLEAN DEFAULT FALSE,
    metadata JSONB,
    source_ip TEXT,
    geolocation JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Agents Registry
CREATE TABLE IF NOT EXISTS agents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    agent_type TEXT NOT NULL CHECK (agent_type IN ('master', 'individual', 'organization', 'transaction', 'supervisor', 'threat_intel', 'soar')),
    name TEXT NOT NULL,
    status TEXT CHECK (status IN ('active', 'inactive', 'error')) DEFAULT 'active',
    health_status JSONB,
    last_heartbeat TIMESTAMP WITH TIME ZONE,
    configuration JSONB,
    performance_metrics JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Threats and Intelligence
CREATE TABLE IF NOT EXISTS threats (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    threat_id TEXT UNIQUE,
    title TEXT NOT NULL,
    description TEXT,
    severity TEXT CHECK (severity IN ('critical', 'high', 'medium', 'low', 'info')) DEFAULT 'medium',
    threat_type TEXT,
    source TEXT,
    ioc_type TEXT CHECK (ioc_type IN ('ip', 'domain', 'url', 'hash', 'email', 'filename')),
    ioc_value TEXT,
    mitre_attack_tactics TEXT[],
    mitre_attack_techniques TEXT[],
    related_threat_actors TEXT[],
    metadata JSONB,
    first_seen TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_seen TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Sanctions Lists
CREATE TABLE IF NOT EXISTS sanctions_entries (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    entity_name TEXT NOT NULL,
    entity_type TEXT CHECK (entity_type IN ('individual', 'organization', 'vessel', 'aircraft')),
    list_source TEXT CHECK (list_source IN ('UN', 'US_OFAC', 'UK', 'EU')),
    country TEXT,
    date_of_birth DATE,
    aliases TEXT[],
    identifiers JSONB,
    sanctions_program TEXT,
    listing_date DATE,
    raw_data JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(entity_name, list_source, identifiers)
);

-- Incidents
CREATE TABLE IF NOT EXISTS incidents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    incident_id TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    severity TEXT CHECK (severity IN ('critical', 'high', 'medium', 'low')) DEFAULT 'medium',
    status TEXT CHECK (status IN ('open', 'investigating', 'contained', 'resolved', 'closed')) DEFAULT 'open',
    assigned_to UUID REFERENCES users(id),
    individual_id UUID REFERENCES individuals(id),
    organization_id UUID REFERENCES organizations(id),
    threat_id UUID REFERENCES threats(id),
    timeline JSONB,
    forensic_data JSONB,
    response_actions JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    resolved_at TIMESTAMP WITH TIME ZONE
);

-- Agent Tasks and Workflows
CREATE TABLE IF NOT EXISTS agent_tasks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    task_id TEXT UNIQUE NOT NULL,
    agent_id UUID REFERENCES agents(id),
    task_type TEXT NOT NULL,
    status TEXT CHECK (status IN ('pending', 'running', 'completed', 'failed')) DEFAULT 'pending',
    input_data JSONB,
    output_data JSONB,
    error_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE
);

-- SOAR Playbooks
CREATE TABLE IF NOT EXISTS soar_playbooks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    description TEXT,
    trigger_conditions JSONB,
    actions JSONB,
    status TEXT CHECK (status IN ('active', 'inactive', 'draft')) DEFAULT 'draft',
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- SOAR Executions
CREATE TABLE IF NOT EXISTS soar_executions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    playbook_id UUID REFERENCES soar_playbooks(id),
    incident_id UUID REFERENCES incidents(id),
    status TEXT CHECK (status IN ('running', 'completed', 'failed')) DEFAULT 'running',
    execution_log JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE
);

-- Data Ingestion Logs
CREATE TABLE IF NOT EXISTS data_ingestions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_type TEXT CHECK (source_type IN ('api', 'file', 'spreadsheet', 'pdf', 'doc', 'email', 'log')),
    source_name TEXT,
    file_name TEXT,
    status TEXT CHECK (status IN ('pending', 'processing', 'completed', 'failed')) DEFAULT 'pending',
    records_processed INTEGER DEFAULT 0,
    records_failed INTEGER DEFAULT 0,
    error_log JSONB,
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE
);

-- Threat Intelligence Feeds
CREATE TABLE IF NOT EXISTS threat_feeds (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    feed_name TEXT NOT NULL,
    feed_type TEXT CHECK (feed_type IN ('osint', 'commercial', 'community', 'government')),
    source_url TEXT,
    update_frequency TEXT,
    last_update TIMESTAMP WITH TIME ZONE,
    status TEXT CHECK (status IN ('active', 'inactive', 'error')) DEFAULT 'active',
    configuration JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Analytics and Metrics
CREATE TABLE IF NOT EXISTS analytics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    metric_type TEXT NOT NULL,
    metric_name TEXT NOT NULL,
    value NUMERIC(15,2),
    metadata JSONB,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(metric_type, metric_name, timestamp)
);

-- Chat Conversations (for master agent interface)
CREATE TABLE IF NOT EXISTS chat_conversations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    session_id TEXT NOT NULL,
    message TEXT NOT NULL,
    response TEXT,
    agent_used TEXT,
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_individuals_user_id ON individuals(user_id);
CREATE INDEX IF NOT EXISTS idx_individuals_organization_id ON individuals(organization_id);
CREATE INDEX IF NOT EXISTS idx_transactions_individual_id ON transactions(individual_id);
CREATE INDEX IF NOT EXISTS idx_transactions_organization_id ON transactions(organization_id);
CREATE INDEX IF NOT EXISTS idx_threats_severity ON threats(severity);
CREATE INDEX IF NOT EXISTS idx_threats_ioc_value ON threats(ioc_value);
CREATE INDEX IF NOT EXISTS idx_incidents_status ON incidents(status);
CREATE INDEX IF NOT EXISTS idx_incidents_severity ON incidents(severity);
CREATE INDEX IF NOT EXISTS idx_sanctions_entity_name ON sanctions_entries(entity_name);
CREATE INDEX IF NOT EXISTS idx_sanctions_list_source ON sanctions_entries(list_source);
CREATE INDEX IF NOT EXISTS idx_agents_type ON agents(agent_type);
CREATE INDEX IF NOT EXISTS idx_agents_status ON agents(status);
CREATE INDEX IF NOT EXISTS idx_chat_user_id ON chat_conversations(user_id);
CREATE INDEX IF NOT EXISTS idx_chat_session_id ON chat_conversations(session_id);

-- Row Level Security (RLS) - Enable on all tables
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE organizations ENABLE ROW LEVEL SECURITY;
ALTER TABLE individuals ENABLE ROW LEVEL SECURITY;
ALTER TABLE transactions ENABLE ROW LEVEL SECURITY;
ALTER TABLE threats ENABLE ROW LEVEL SECURITY;
ALTER TABLE incidents ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_conversations ENABLE ROW LEVEL SECURITY;

-- Basic RLS Policies (can be customized based on requirements)
CREATE POLICY "Users can view their own data" ON users FOR SELECT USING (auth.uid() = id);
CREATE POLICY "Users can view organizations" ON organizations FOR SELECT USING (true);
CREATE POLICY "Users can view incidents" ON incidents FOR SELECT USING (true);
CREATE POLICY "Users can view threats" ON threats FOR SELECT USING (true);
CREATE POLICY "Users can view their own conversations" ON chat_conversations FOR SELECT USING (auth.uid() = user_id);
