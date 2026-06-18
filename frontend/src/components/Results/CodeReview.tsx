import { AlertCircle, Lightbulb, CheckCircle2, XCircle } from 'lucide-react'
import type { CodeReviewResult } from '../../types'
import { Badge } from '../ui/Badge'

interface CodeReviewProps {
  review: CodeReviewResult
}

export function CodeReview({ review }: CodeReviewProps) {
  return (
    <div className="space-y-5 animate-slide-up">
      {review.summary && (
        <div className="rounded-xl border border-border bg-surface p-5">
          <h3 className="text-sm font-semibold text-text mb-2">Summary</h3>
          <p className="text-sm text-text-secondary leading-relaxed">{review.summary}</p>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {review.filename_check && (
          <div className={`rounded-xl border p-4 ${
            review.filename_check.passed ? 'border-emerald-200 bg-emerald-50/50 dark:border-emerald-800 dark:bg-emerald-900/10' : 'border-red-200 bg-red-50/50 dark:border-red-800 dark:bg-red-900/10'
          }`}>
            <div className="flex items-center gap-2 mb-1">
              {review.filename_check.passed ? <CheckCircle2 size={16} className="text-emerald-600" /> : <XCircle size={16} className="text-red-600" />}
              <span className="text-xs font-semibold uppercase tracking-wider text-text-secondary">Filename Check</span>
            </div>
            <p className="text-sm text-text-secondary">{review.filename_check.message}</p>
          </div>
        )}
        {review.structure_check && (
          <div className={`rounded-xl border p-4 ${
            review.structure_check.passed ? 'border-emerald-200 bg-emerald-50/50 dark:border-emerald-800 dark:bg-emerald-900/10' : 'border-red-200 bg-red-50/50 dark:border-red-800 dark:bg-red-900/10'
          }`}>
            <div className="flex items-center gap-2 mb-1">
              {review.structure_check.passed ? <CheckCircle2 size={16} className="text-emerald-600" /> : <XCircle size={16} className="text-red-600" />}
              <span className="text-xs font-semibold uppercase tracking-wider text-text-secondary">Structure Check</span>
            </div>
            <p className="text-sm text-text-secondary">{review.structure_check.message}</p>
          </div>
        )}
      </div>

      {review.mistakes.length > 0 && (
        <div className="rounded-xl border border-border bg-surface p-5">
          <div className="flex items-center gap-2 mb-4">
            <AlertCircle size={18} className="text-red-500" />
            <h3 className="text-sm font-semibold text-text">Mistakes</h3>
            <Badge variant="error">{review.mistakes.length}</Badge>
          </div>
          <ul className="space-y-2">
            {review.mistakes.map((m, i) => (
              <li key={i} className="flex items-start gap-3 text-sm text-text-secondary">
                <span className="w-5 h-5 rounded-full bg-red-50 dark:bg-red-900/20 text-red-600 text-xs flex items-center justify-center shrink-0 mt-0.5">{i + 1}</span>
                {m}
              </li>
            ))}
          </ul>
        </div>
      )}

      {review.suggestions.length > 0 && (
        <div className="rounded-xl border border-border bg-surface p-5">
          <div className="flex items-center gap-2 mb-4">
            <Lightbulb size={18} className="text-amber-500" />
            <h3 className="text-sm font-semibold text-text">Suggestions</h3>
            <Badge variant="warning">{review.suggestions.length}</Badge>
          </div>
          <ul className="space-y-2">
            {review.suggestions.map((s, i) => (
              <li key={i} className="flex items-start gap-3 text-sm text-text-secondary">
                <span className="w-5 h-5 rounded-full bg-amber-50 dark:bg-amber-900/20 text-amber-600 text-xs flex items-center justify-center shrink-0 mt-0.5">{i + 1}</span>
                {s}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}
