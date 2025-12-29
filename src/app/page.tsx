'use client'

import { useState, useEffect } from 'react'
import Dashboard from '@/components/Dashboard'
import ChatInterface from '@/components/ChatInterface'

export default function Home() {
  const [activeView, setActiveView] = useState<'dashboard' | 'chat'>('dashboard')
  const [userId] = useState('user-' + Math.random().toString(36).substr(2, 9))

  return (
    <main className="min-h-screen bg-dark-bg">
      {/* Navigation */}
      <nav className="bg-dark-card border-b border-dark-border">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-bold text-white">Cybersecurity Intelligence Platform</h1>
            </div>
            <div className="flex items-center space-x-4">
              <button
                onClick={() => setActiveView('dashboard')}
                className={`px-4 py-2 rounded-lg transition-colors ${
                  activeView === 'dashboard'
                    ? 'bg-threat-info text-white'
                    : 'text-gray-400 hover:text-white'
                }`}
              >
                Dashboard
              </button>
              <button
                onClick={() => setActiveView('chat')}
                className={`px-4 py-2 rounded-lg transition-colors ${
                  activeView === 'chat'
                    ? 'bg-threat-info text-white'
                    : 'text-gray-400 hover:text-white'
                }`}
              >
                Chat
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeView === 'dashboard' ? (
          <Dashboard />
        ) : (
          <ChatInterface userId={userId} />
        )}
      </div>
    </main>
  )
}
