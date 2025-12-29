'use client'

import { useState, useEffect } from 'react'
import { AlertTriangle, Users, Building, DollarSign, Activity, Shield } from 'lucide-react'

interface DashboardMetrics {
  incidents: {
    total: number
    by_severity: Record<string, number>
  }
  threats: {
    total: number
  }
  transactions: {
    flagged: number
  }
}

export default function Dashboard() {
  const [metrics, setMetrics] = useState<DashboardMetrics | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchMetrics()
    const interval = setInterval(fetchMetrics, 30000) // Refresh every 30 seconds
    return () => clearInterval(interval)
  }, [])

  const fetchMetrics = async () => {
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
      const response = await fetch(`${apiUrl}/api/analytics/dashboard`)
      const data = await response.json()
      setMetrics(data)
    } catch (error) {
      console.error('Error fetching metrics:', error)
    } finally {
      setLoading(false)
    }
  }

  const severityColors: Record<string, string> = {
    critical: 'bg-threat-critical',
    high: 'bg-threat-high',
    medium: 'bg-threat-medium',
    low: 'bg-threat-low',
    info: 'bg-threat-info'
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-2xl font-bold text-white">Security Dashboard</h2>
        <p className="text-gray-400 mt-1">Real-time cybersecurity intelligence overview</p>
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {/* Incidents Card */}
        <MetricCard
          title="Active Incidents"
          value={metrics?.incidents?.total || 0}
          icon={<AlertTriangle className="w-6 h-6" />}
          color="threat-high"
          loading={loading}
        />

        {/* Threats Card */}
        <MetricCard
          title="Threat Intelligence"
          value={metrics?.threats?.total || 0}
          icon={<Shield className="w-6 h-6" />}
          color="threat-medium"
          loading={loading}
        />

        {/* Flagged Transactions */}
        <MetricCard
          title="Flagged Transactions"
          value={metrics?.transactions?.flagged || 0}
          icon={<DollarSign className="w-6 h-6" />}
          color="threat-critical"
          loading={loading}
        />

        {/* Agents Status */}
        <MetricCard
          title="Agents Operational"
          value="7/7"
          icon={<Activity className="w-6 h-6" />}
          color="threat-low"
          loading={false}
        />
      </div>

      {/* Incidents by Severity */}
      {metrics?.incidents?.by_severity && (
        <div className="bg-dark-card rounded-lg border border-dark-border p-6">
          <h3 className="text-lg font-semibold text-white mb-4">Incidents by Severity</h3>
          <div className="space-y-3">
            {Object.entries(metrics.incidents.by_severity).map(([severity, count]) => (
              <div key={severity} className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className={`w-3 h-3 rounded-full ${severityColors[severity] || 'bg-gray-500'}`}></div>
                  <span className="text-gray-300 capitalize">{severity}</span>
                </div>
                <span className="text-white font-semibold">{count}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Quick Actions */}
      <div className="bg-dark-card rounded-lg border border-dark-border p-6">
        <h3 className="text-lg font-semibold text-white mb-4">Quick Actions</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <ActionButton
            icon={<Users className="w-5 h-5" />}
            title="Analyze User"
            description="Check user behavior and risk"
            onClick={() => window.location.hash = 'chat'}
          />
          <ActionButton
            icon={<Building className="w-5 h-5" />}
            title="Check Organization"
            description="View security posture"
            onClick={() => window.location.hash = 'chat'}
          />
          <ActionButton
            icon={<Shield className="w-5 h-5" />}
            title="Threat Intelligence"
            description="Search threats and IOCs"
            onClick={() => window.location.hash = 'chat'}
          />
        </div>
      </div>

      {/* Threat Map Placeholder */}
      {/* Threat Map Placeholder */}
      <div className="bg-dark-card rounded-lg border border-dark-border p-6">
        <h3 className="text-lg font-semibold text-white mb-4">Global Threat Map</h3>
        <div className="h-64 bg-dark-bg rounded-lg flex items-center justify-center border border-dark-border">
          <p className="text-gray-400">Threat map visualization would appear here</p>
          <p className="text-gray-500 text-sm mt-2">(Integration with Leaflet/maps library pending)</p>
        </div>
      </div>
    </div>
  )
}

interface MetricCardProps {
  title: string
  value: string | number
  icon: React.ReactNode
  color: string
  loading: boolean
}

function MetricCard({ title, value, icon, color, loading }: MetricCardProps) {
  return (
    <div className="bg-dark-card rounded-lg border border-dark-border p-6">
      <div className="flex items-center justify-between mb-2">
        <p className="text-gray-400 text-sm">{title}</p>
        <div className={`text-${color}`}>{icon}</div>
      </div>
      {loading ? (
        <div className="h-8 w-20 bg-dark-bg rounded animate-pulse"></div>
      ) : (
        <p className={`text-3xl font-bold text-${color}`}>{value}</p>
      )}
    </div>
  )
}

interface ActionButtonProps {
  icon: React.ReactNode
  title: string
  description: string
  onClick: () => void
}

function ActionButton({ icon, title, description, onClick }: ActionButtonProps) {
  return (
    <button
      onClick={onClick}
      className="bg-dark-bg hover:bg-dark-hover border border-dark-border rounded-lg p-4 text-left transition-colors group"
    >
      <div className="flex items-center gap-3 mb-2">
        <div className="text-gray-400 group-hover:text-threat-info transition-colors">
          {icon}
        </div>
        <h4 className="font-semibold text-white">{title}</h4>
      </div>
      <p className="text-sm text-gray-400">{description}</p>
    </button>
  )
}
