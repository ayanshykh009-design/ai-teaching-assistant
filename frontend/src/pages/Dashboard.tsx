import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Upload, Brain, BookOpen, Activity, ArrowRight, Database, GitBranch, Sparkles } from 'lucide-react'
import { fetchHealth, fetchKnowledgeStats } from '../api/client'
import type { HealthResponse, KnowledgeStatsResponse } from '../types'

export function Dashboard() {
  const navigate = useNavigate()
  const [health, setHealth] = useState<HealthResponse | null>(null)
  const [stats, setStats] = useState<KnowledgeStatsResponse | null>(null)

  useEffect(() => {
    fetchHealth().then(async (r) => {
      if (r.ok) setHealth(await r.json())
    })
    fetchKnowledgeStats().then(async (r) => {
      if (r.ok) setStats(await r.json())
    })
  }, [])

  const features = [
    { icon: Upload, label: 'Upload Code', desc: 'Submit your JavaScript assignment for instant AI review', color: 'text-ai-600 bg-ai-50 dark:text-ai-400 dark:bg-ai-900/30', onClick: () => navigate('/review') },
    { icon: Brain, label: 'Multi-Agent Review', desc: 'Code review, tutoring, rubric scoring, and feedback agents', color: 'text-violet-600 bg-violet-50 dark:text-violet-400 dark:bg-violet-900/30', onClick: () => navigate('/review') },
    { icon: BookOpen, label: 'Knowledge Base', desc: 'Search class notes, rubrics, and past feedback', color: 'text-emerald-600 bg-emerald-50 dark:text-emerald-400 dark:bg-emerald-900/30', onClick: () => navigate('/knowledge') },
    { icon: Activity, label: 'API Dashboard', desc: 'Explore API endpoints via Swagger documentation', color: 'text-amber-600 bg-amber-50 dark:text-amber-400 dark:bg-amber-900/30', onClick: () => window.open('/api/docs', '_blank') },
  ]

  const totalPoints = stats ? Object.values(stats.collections).reduce((a, c) => a + c.points_count, 0) : null
  const totalCols = stats ? Object.keys(stats.collections).length : null

  return (
    <div className="space-y-8 animate-fade-in">
      <div>
        <h1 className="text-2xl font-bold text-text">AI Teaching Assistant</h1>
        <p className="text-sm text-text-secondary mt-1">Intelligent code review platform powered by Gemini & RAG</p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="rounded-xl border border-border bg-surface p-5 flex items-center gap-4">
          <div className="w-12 h-12 rounded-xl bg-ai-50 dark:bg-ai-900/30 flex items-center justify-center">
            <Database size={22} className="text-ai-500" />
          </div>
          <div>
            <p className="text-xs text-text-tertiary uppercase tracking-wider">Knowledge Points</p>
            <p className="text-2xl font-bold text-text">{totalPoints ?? <span className="text-text-tertiary">—</span>}</p>
          </div>
        </div>
        <div className="rounded-xl border border-border bg-surface p-5 flex items-center gap-4">
          <div className="w-12 h-12 rounded-xl bg-emerald-50 dark:bg-emerald-900/30 flex items-center justify-center">
            <GitBranch size={22} className="text-emerald-500" />
          </div>
          <div>
            <p className="text-xs text-text-tertiary uppercase tracking-wider">Collections</p>
            <p className="text-2xl font-bold text-text">{totalCols ?? <span className="text-text-tertiary">—</span>}</p>
          </div>
        </div>
        <div className="rounded-xl border border-border bg-surface p-5 flex items-center gap-4">
          <div className="w-12 h-12 rounded-xl bg-amber-50 dark:bg-amber-900/30 flex items-center justify-center">
            <Brain size={22} className="text-amber-500" />
          </div>
          <div>
            <p className="text-xs text-text-tertiary uppercase tracking-wider">AI Agents</p>
            <p className="text-2xl font-bold text-text">4</p>
          </div>
        </div>
        <div className="rounded-xl border border-border bg-surface p-5 flex items-center gap-4">
          <div className={`w-12 h-12 rounded-xl flex items-center justify-center ${health?.qdrant_connected ? 'bg-emerald-50 dark:bg-emerald-900/30' : 'bg-red-50 dark:bg-red-900/30'}`}>
            <Sparkles size={22} className={health?.qdrant_connected ? 'text-emerald-500' : 'text-red-500'} />
          </div>
          <div>
            <p className="text-xs text-text-tertiary uppercase tracking-wider">Qdrant Status</p>
            <p className={`text-lg font-bold ${health?.qdrant_connected ? 'text-emerald-600' : 'text-red-600'}`}>
              {health?.qdrant_connected ? 'Connected' : 'Offline'}
            </p>
          </div>
        </div>
      </div>

      <div>
        <h2 className="text-base font-semibold text-text mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {features.map((f) => (
            <button
              key={f.label}
              onClick={f.onClick}
              className="group rounded-xl border border-border bg-surface p-5 text-left hover:border-ai-300 hover:shadow-md transition-all"
            >
              <div className={`w-10 h-10 rounded-xl flex items-center justify-center mb-3 ${f.color}`}>
                <f.icon size={20} />
              </div>
              <div className="flex items-center gap-1.5 mb-1">
                <h3 className="text-sm font-semibold text-text group-hover:text-ai-600 transition-colors">{f.label}</h3>
                <ArrowRight size={14} className="text-text-tertiary group-hover:text-ai-500 group-hover:translate-x-0.5 transition-all" />
              </div>
              <p className="text-xs text-text-tertiary leading-relaxed">{f.desc}</p>
            </button>
          ))}
        </div>
      </div>

      {health && (
        <div className="rounded-xl border border-border bg-surface p-5">
          <h3 className="text-sm font-semibold text-text mb-3">System Status</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
            <div>
              <span className="text-text-tertiary">Service</span>
              <p className="text-text font-medium">{health.service}</p>
            </div>
            <div>
              <span className="text-text-tertiary">Version</span>
              <p className="text-text font-medium">{health.version}</p>
            </div>
            <div>
              <span className="text-text-tertiary">Auth</span>
              <p className="text-text font-medium">{health.auth_enabled ? 'Enabled' : 'Disabled'}</p>
            </div>
            <div>
              <span className="text-text-tertiary">Client</span>
              <p className="text-text font-medium">{health.client_host || '—'}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
