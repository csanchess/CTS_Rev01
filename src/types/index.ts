// Type definitions for the platform

export interface User {
  id: string
  email: string
  full_name?: string
  role: 'admin' | 'analyst' | 'viewer' | 'ciso'
  organization_id?: string
  created_at: string
  updated_at: string
}

export interface Organization {
  id: string
  name: string
  domain?: string
  industry?: string
  country_code?: string
  risk_score: number
  status: 'active' | 'suspended' | 'blocked'
  metadata?: Record<string, any>
  created_at: string
  updated_at: string
}

export interface Individual {
  id: string
  user_id?: string
  email?: string
  full_name?: string
  organization_id?: string
  risk_score: number
  behavior_profile?: Record<string, any>
  access_patterns?: Record<string, any>
  anomaly_flags?: Record<string, any>
  status: 'active' | 'suspended' | 'investigating'
  created_at: string
  updated_at: string
}

export interface Transaction {
  id: string
  transaction_id: string
  individual_id?: string
  organization_id?: string
  amount: number
  currency: string
  transaction_type?: string
  status: 'pending' | 'completed' | 'flagged' | 'blocked'
  risk_score: number
  fraud_indicator: boolean
  metadata?: Record<string, any>
  source_ip?: string
  geolocation?: Record<string, any>
  created_at: string
}

export interface Threat {
  id: string
  threat_id: string
  title: string
  description?: string
  severity: 'critical' | 'high' | 'medium' | 'low' | 'info'
  threat_type?: string
  source?: string
  ioc_type?: 'ip' | 'domain' | 'url' | 'hash' | 'email' | 'filename'
  ioc_value?: string
  mitre_attack_tactics?: string[]
  mitre_attack_techniques?: string[]
  related_threat_actors?: string[]
  metadata?: Record<string, any>
  first_seen: string
  last_seen: string
  created_at: string
}

export interface Incident {
  id: string
  incident_id: string
  title: string
  description?: string
  severity: 'critical' | 'high' | 'medium' | 'low'
  status: 'open' | 'investigating' | 'contained' | 'resolved' | 'closed'
  assigned_to?: string
  individual_id?: string
  organization_id?: string
  threat_id?: string
  timeline?: Record<string, any>
  forensic_data?: Record<string, any>
  response_actions?: Record<string, any>
  created_at: string
  updated_at: string
  resolved_at?: string
}

export interface Agent {
  id: string
  agent_type: 'master' | 'individual' | 'organization' | 'transaction' | 'supervisor' | 'threat_intel' | 'soar'
  name: string
  status: 'active' | 'inactive' | 'error'
  health_status?: Record<string, any>
  last_heartbeat?: string
  configuration?: Record<string, any>
  performance_metrics?: Record<string, any>
  created_at: string
  updated_at: string
}
