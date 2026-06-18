import type { RubricResult } from '../../types'
import { CircularScore } from '../ui/CircularScore'
import { ProgressBar } from '../ui/ProgressBar'
import { MessageSquare } from 'lucide-react'

interface RubricScoringProps {
  rubric: RubricResult
}

const colors: Record<string, string> = {
  correctness: 'bg-emerald-500',
  efficiency: 'bg-ai-500',
  style: 'bg-violet-500',
  documentation: 'bg-amber-500',
}

export function RubricScoring({ rubric }: RubricScoringProps) {
  return (
    <div className="space-y-5 animate-slide-up">
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {Object.entries(rubric.scores).map(([key, val]) => (
          <div key={key} className="rounded-xl border border-border bg-surface p-4 text-center">
            <span className="text-xs font-medium text-text-tertiary uppercase tracking-wider block mb-3">{key}</span>
            <span className={`inline-flex items-center justify-center w-12 h-12 rounded-xl text-white text-lg font-bold ${colors[key] || 'bg-ai-500'}`}>
              {val}
            </span>
          </div>
        ))}
      </div>

      <div className="rounded-xl border border-border bg-surface p-5">
        <h3 className="text-sm font-semibold text-text mb-4">Detailed Breakdown</h3>
        <div className="space-y-4">
          {Object.entries(rubric.scores).map(([key, val]) => (
            <ProgressBar key={key} value={val} max={10} label={key.charAt(0).toUpperCase() + key.slice(1)} color={colors[key] || 'bg-ai-500'} />
          ))}
        </div>
      </div>

      <div className="flex items-center justify-center p-5 rounded-xl border border-border bg-surface">
        <CircularScore value={rubric.total_score} max={rubric.max_score} label="Total Score" />
      </div>

      {rubric.comments.length > 0 && (
        <div className="rounded-xl border border-border bg-surface p-5">
          <div className="flex items-center gap-2 mb-4">
            <MessageSquare size={18} className="text-ai-500" />
            <h3 className="text-sm font-semibold text-text">Grading Comments</h3>
          </div>
          <ul className="space-y-2">
            {rubric.comments.map((c, i) => (
              <li key={i} className="flex items-start gap-3 text-sm text-text-secondary leading-relaxed">
                <span className="w-1.5 h-1.5 rounded-full bg-ai-400 mt-2 shrink-0" />
                {c}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}
