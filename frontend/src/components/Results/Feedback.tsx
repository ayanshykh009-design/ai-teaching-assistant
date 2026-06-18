import { Sparkles, TrendingUp, Heart } from 'lucide-react'
import type { FeedbackResult } from '../../types'

interface FeedbackViewProps {
  feedback: FeedbackResult
}

export function FeedbackView({ feedback }: FeedbackViewProps) {
  return (
    <div className="space-y-4 animate-slide-up">
      {feedback.strengths.length > 0 && (
        <div className="rounded-xl border border-emerald-200 dark:border-emerald-800 bg-emerald-50/50 dark:bg-emerald-900/10 p-5">
          <div className="flex items-center gap-2 mb-4">
            <Sparkles size={18} className="text-emerald-600" />
            <h3 className="text-sm font-semibold text-text">Strengths</h3>
          </div>
          <ul className="space-y-2">
            {feedback.strengths.map((s, i) => (
              <li key={i} className="flex items-start gap-3 text-sm text-text-secondary">
                <span className="w-5 h-5 rounded-full bg-emerald-100 dark:bg-emerald-900/30 text-emerald-600 text-xs flex items-center justify-center shrink-0 mt-0.5">✓</span>
                {s}
              </li>
            ))}
          </ul>
        </div>
      )}

      {feedback.improvements.length > 0 && (
        <div className="rounded-xl border border-amber-200 dark:border-amber-800 bg-amber-50/50 dark:bg-amber-900/10 p-5">
          <div className="flex items-center gap-2 mb-4">
            <TrendingUp size={18} className="text-amber-600" />
            <h3 className="text-sm font-semibold text-text">Areas for Improvement</h3>
          </div>
          <ul className="space-y-2">
            {feedback.improvements.map((imp, i) => (
              <li key={i} className="flex items-start gap-3 text-sm text-text-secondary">
                <span className="w-5 h-5 rounded-full bg-amber-100 dark:bg-amber-900/30 text-amber-600 text-xs flex items-center justify-center shrink-0 mt-0.5">→</span>
                {imp}
              </li>
            ))}
          </ul>
        </div>
      )}

      {feedback.overall_comment && (
        <div className="rounded-xl border border-border bg-surface p-5">
          <div className="flex items-center gap-2 mb-3">
            <Heart size={18} className="text-rose-500" />
            <h3 className="text-sm font-semibold text-text">Overall Comment</h3>
          </div>
          <p className="text-sm text-text-secondary leading-relaxed">{feedback.overall_comment}</p>
        </div>
      )}
    </div>
  )
}
