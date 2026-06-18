import { useEffect, useState } from 'react'
import { Search, RefreshCw, Loader2 } from 'lucide-react'
import { fetchKnowledgeStats, searchKnowledge, ingestKnowledge } from '../api/client'
import type { KnowledgeStatsResponse, KnowledgeSearchResponse } from '../types'
import { CollectionCard } from '../components/Knowledge/CollectionCard'
import { Badge } from '../components/ui/Badge'
import toast from 'react-hot-toast'

const collections = ['notes', 'rubrics', 'mistakes', 'assignments', 'feedback_examples']

export function KnowledgePage() {
  const [stats, setStats] = useState<KnowledgeStatsResponse | null>(null)
  const [searchQuery, setSearchQuery] = useState('')
  const [searchCol, setSearchCol] = useState('notes')
  const [searchResult, setSearchResult] = useState<KnowledgeSearchResponse | null>(null)
  const [searching, setSearching] = useState(false)
  const [ingesting, setIngesting] = useState(false)


  const loadStats = async () => {
    const r = await fetchKnowledgeStats()
    if (r.ok) setStats(await r.json())
  }

  useEffect(() => { loadStats() }, [])

  const handleSearch = async () => {
    if (!searchQuery.trim()) return
    setSearching(true)
    try {
      const r = await searchKnowledge(searchQuery.trim(), searchCol, 5)
      if (r.ok) setSearchResult(await r.json())
      else toast.error('Search failed')
    } finally {
      setSearching(false)
    }
  }

  const handleIngest = async () => {
    setIngesting(true)
    try {
      const r = await ingestKnowledge()
      if (r.ok) {
        toast.success('Knowledge ingested')
        await loadStats()
      } else {
        toast.error('Ingestion failed')
      }
    } finally {
      setIngesting(false)
    }
  }

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-start justify-between">
        <div>
          <h1 className="text-2xl font-bold text-text">Knowledge Base</h1>
          <p className="text-sm text-text-secondary mt-1">Qdrant vector database — class notes, rubrics, and feedback</p>
        </div>
        <div className="flex items-center gap-2">
          <Badge variant={stats ? 'success' : 'error'}>{stats ? 'Connected' : 'Offline'}</Badge>
          <button
            onClick={handleIngest}
            disabled={ingesting}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium bg-ai-500 text-white hover:bg-ai-600 disabled:opacity-50 transition-colors"
          >
            {ingesting ? <Loader2 size={14} className="animate-spin" /> : <RefreshCw size={14} />}
            {ingesting ? 'Ingesting...' : 'Re-ingest'}
          </button>
        </div>
      </div>

      {/* Collection Cards */}
      {stats && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-4">
          {collections.map((name) => {
            const data = stats.collections[name]
            return data ? <CollectionCard key={name} name={name} data={data} /> : null
          })}
        </div>
      )}

      {!stats && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-4">
          {[...Array(5)].map((_, i) => (
            <div key={i} className="rounded-xl border border-border bg-surface p-5 space-y-3 animate-shimmer">
              <div className="w-10 h-10 rounded-xl bg-surface-tertiary" />
              <div className="h-4 w-2/3 bg-surface-tertiary rounded" />
              <div className="h-3 w-full bg-surface-tertiary rounded" />
            </div>
          ))}
        </div>
      )}

      {/* Search */}
      <div className="rounded-xl border border-border bg-surface p-5">
        <h3 className="text-sm font-semibold text-text mb-4">Search Knowledge Base</h3>
        <div className="flex flex-col sm:flex-row gap-3">
          <select
            value={searchCol}
            onChange={(e) => setSearchCol(e.target.value)}
            className="px-3 py-2 rounded-lg border border-border bg-surface text-sm text-text focus:outline-none focus:ring-2 focus:ring-ai-500/30"
          >
            {collections.map((c) => (
              <option key={c} value={c}>{c.replace(/_/g, ' ').replace(/\b\w/g, (x) => x.toUpperCase())}</option>
            ))}
          </select>
          <div className="flex-1 flex gap-2">
            <div className="relative flex-1">
              <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-text-tertiary" />
              <input
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
                placeholder="Search by topic, function, or concept..."
                className="w-full pl-9 pr-3 py-2 rounded-lg border border-border bg-surface text-sm text-text placeholder:text-text-tertiary focus:outline-none focus:ring-2 focus:ring-ai-500/30"
              />
            </div>
            <button
              onClick={handleSearch}
              disabled={searching}
              className="px-4 py-2 rounded-lg text-sm font-medium bg-ai-500 text-white hover:bg-ai-600 disabled:opacity-50 transition-colors whitespace-nowrap"
            >
              {searching ? <Loader2 size={16} className="animate-spin" /> : 'Search'}
            </button>
          </div>
        </div>

        {/* Search Results */}
        {searchResult && (
          <div className="mt-4 space-y-3">
            <p className="text-xs text-text-tertiary">
              Found {searchResult.results.length} result{searchResult.results.length !== 1 ? 's' : ''} in {searchResult.collection}
            </p>
            {searchResult.results.map((r) => (
              <div key={r.id} className="rounded-lg border border-border-light bg-surface-tertiary/50 p-4">
                <div className="flex items-start justify-between mb-1">
                  <span className="text-xs text-text-tertiary font-mono">{r.source}</span>
                  <span className="text-xs text-text-tertiary">{(r.score * 100).toFixed(0)}%</span>
                </div>
                <p className="text-sm text-text-secondary">{r.text}</p>
              </div>
            ))}
            {searchResult.results.length === 0 && (
              <p className="text-sm text-text-tertiary text-center py-4">No results found</p>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
