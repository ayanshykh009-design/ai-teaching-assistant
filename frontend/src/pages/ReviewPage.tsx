import { useState, useCallback } from 'react'
import { UploadZone } from '../components/Upload/UploadZone'
import { CodeReview } from '../components/Results/CodeReview'
import { TutorExplanation } from '../components/Results/TutorExplanation'
import { RubricScoring } from '../components/Results/RubricScoring'
import { FeedbackView } from '../components/Results/Feedback'
import { CorrectedCode } from '../components/Results/CorrectedCode'
import { ResultSkeleton } from '../components/ui/Skeleton'
import { Badge } from '../components/ui/Badge'
import { reviewFile } from '../api/client'
import type { ReviewResponse, ReviewStatus } from '../types'
import { Loader2, CheckCircle2, AlertCircle } from 'lucide-react'
import toast from 'react-hot-toast'

export function ReviewPage() {
  const [status, setStatus] = useState<ReviewStatus>('idle')
  const [result, setResult] = useState<ReviewResponse | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [filename, setFilename] = useState<string | null>(null)

  const handleFile = useCallback(async (file: File) => {
    setFilename(file.name)
    setStatus('uploading')
    setError(null)

    // Slight delay to show animation
    await new Promise((r) => setTimeout(r, 600))

    setStatus('reviewing')
    try {
      const res = await reviewFile(file)
      if (!res.ok) {
        const err = await res.json()
        throw new Error(err.detail || `Server returned ${res.status}`)
      }
      const data: ReviewResponse = await res.json()
      setResult(data)
      setStatus('done')
      toast.success('Review completed')
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Unknown error')
      setStatus('error')
      toast.error('Review failed')
    }
  }, [])

  const score = result?.rubric?.total_score ?? 0
  const maxScore = result?.rubric?.max_score ?? 40

  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h1 className="text-2xl font-bold text-text">Review Code</h1>
        <p className="text-sm text-text-secondary mt-1">Upload a JavaScript file for multi-agent AI analysis</p>
      </div>

      <UploadZone onFile={handleFile} disabled={status === 'uploading' || status === 'reviewing'} />

      {/* Status indicators */}
      {status === 'uploading' && (
        <div className="flex items-center gap-3 p-4 rounded-xl border border-ai-200 dark:border-ai-800 bg-ai-50/50 dark:bg-ai-900/10 animate-fade-in">
          <Loader2 size={20} className="text-ai-500 animate-spin" />
          <div>
            <p className="text-sm font-medium text-text">Uploading file...</p>
            <p className="text-xs text-text-tertiary">{filename}</p>
          </div>
        </div>
      )}

      {status === 'reviewing' && (
        <div className="space-y-4 animate-fade-in">
          <div className="flex items-center gap-3 p-4 rounded-xl border border-violet-200 dark:border-violet-800 bg-violet-50/50 dark:bg-violet-900/10">
            <div className="relative">
              <Loader2 size={20} className="text-violet-500 animate-spin" />
              <span className="absolute inset-0 rounded-full animate-ping bg-violet-400/20" />
            </div>
            <div>
              <p className="text-sm font-medium text-text">AI agents are reviewing your code...</p>
              <p className="text-xs text-text-tertiary">Running code review, tutor, rubric & feedback agents</p>
            </div>
          </div>
          <ResultSkeleton />
        </div>
      )}

      {status === 'error' && (
        <div className="flex items-center gap-3 p-4 rounded-xl border border-red-200 dark:border-red-800 bg-red-50/50 dark:bg-red-900/10 animate-fade-in">
          <AlertCircle size={20} className="text-red-500" />
          <div>
            <p className="text-sm font-medium text-text">Review failed</p>
            <p className="text-xs text-text-tertiary">{error || 'An unexpected error occurred'}</p>
          </div>
        </div>
      )}

      {/* Results */}
      {status === 'done' && result && (
        <div className="space-y-6">
          <div className="flex items-center gap-3 p-4 rounded-xl border border-emerald-200 dark:border-emerald-800 bg-emerald-50/50 dark:bg-emerald-900/10 animate-fade-in">
            <CheckCircle2 size={20} className="text-emerald-500" />
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-text">Analysis complete</p>
              <p className="text-xs text-text-tertiary truncate">{result.filename}</p>
            </div>
            <div className="flex items-center gap-2">
              <Badge variant="info">Score: {score}/{maxScore}</Badge>
              <Badge variant={result.code_review.mistakes.length === 0 ? 'success' : 'error'}>
                {result.code_review.mistakes.length} mistakes
              </Badge>
            </div>
          </div>

          {/* Score Dashboard */}
          <div className="grid grid-cols-1 lg:grid-cols-4 gap-4 animate-slide-up">
            <div className="lg:col-span-1">
              <div className="rounded-xl border border-border bg-surface p-5 flex flex-col items-center justify-center h-full">
                <div className="relative w-28 h-28 flex items-center justify-center mb-2">
                  <svg className="absolute inset-0 w-full h-full -rotate-90" viewBox="0 0 120 120">
                    <circle cx="60" cy="60" r="52" fill="none" stroke="var(--color-surface-tertiary)" strokeWidth="8" />
                    <circle
                      cx="60" cy="60" r="52"
                      fill="none" stroke={score >= 32 ? '#22c55e' : score >= 24 ? '#eab308' : '#ef4444'}
                      strokeWidth="8" strokeLinecap="round"
                      strokeDasharray={2 * Math.PI * 52}
                      strokeDashoffset={2 * Math.PI * 52 * (1 - Math.min(1, score / maxScore))}
                      className="transition-all duration-1000 ease-out"
                    />
                  </svg>
                  <div className="text-center">
                    <span className="text-3xl font-bold text-text">{score}</span>
                    <span className="text-sm text-text-tertiary block">/ {maxScore}</span>
                  </div>
                </div>
                {score >= 32 && <Badge variant="success">Excellent</Badge>}
                {score >= 24 && score < 32 && <Badge variant="warning">Good</Badge>}
                {score < 24 && <Badge variant="error">Needs work</Badge>}
              </div>
            </div>

            <div className="lg:col-span-3 grid grid-cols-1 sm:grid-cols-3 gap-4">
              {Object.entries(result.rubric.scores).map(([key, val]) => (
                <div key={key} className="rounded-xl border border-border bg-surface p-4 text-center">
                  <span className="text-xs font-medium text-text-tertiary uppercase tracking-wider block mb-2">{key}</span>
                  <div className="w-full bg-surface-tertiary rounded-full h-2 mb-2">
                    <div
                      className={`h-2 rounded-full transition-all duration-700 ${
                        key === 'correctness' ? 'bg-emerald-500' :
                        key === 'efficiency' ? 'bg-ai-500' :
                        key === 'style' ? 'bg-violet-500' : 'bg-amber-500'
                      }`}
                      style={{ width: `${(val / 10) * 100}%` }}
                    />
                  </div>
                  <span className="text-lg font-bold text-text">{val}<span className="text-xs text-text-tertiary">/10</span></span>
                </div>
              ))}
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <CodeReview review={result.code_review} />
            <TutorExplanation tutor={result.tutor_explanation} />
            <RubricScoring rubric={result.rubric} />
            <FeedbackView feedback={result.feedback} />
          </div>

          <CorrectedCode code={result.code_review.corrected_code} />
        </div>
      )}
    </div>
  )
}
