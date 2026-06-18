import { BookOpen, Lightbulb, HelpCircle } from 'lucide-react'
import type { TutorResult } from '../../types'

interface TutorExplanationProps {
  tutor: TutorResult
}

export function TutorExplanation({ tutor }: TutorExplanationProps) {
  return (
    <div className="space-y-4 animate-slide-up">
      {tutor.concepts_explained.length > 0 && (
        <div className="rounded-xl border border-border bg-surface p-5">
          <div className="flex items-center gap-2 mb-4">
            <BookOpen size={18} className="text-ai-500" />
            <h3 className="text-sm font-semibold text-text">Concepts Explained</h3>
          </div>
          <ul className="space-y-3">
            {tutor.concepts_explained.map((c, i) => (
              <li key={i} className="flex items-start gap-3 text-sm text-text-secondary leading-relaxed">
                <span className="w-6 h-6 rounded-full bg-ai-50 dark:bg-ai-900/30 text-ai-600 text-xs flex items-center justify-center shrink-0 mt-0.5">{i + 1}</span>
                {c}
              </li>
            ))}
          </ul>
        </div>
      )}

      {tutor.learning_resources.length > 0 && (
        <div className="rounded-xl border border-border bg-surface p-5">
          <div className="flex items-center gap-2 mb-4">
            <Lightbulb size={18} className="text-ai-500" />
            <h3 className="text-sm font-semibold text-text">Learning Resources</h3>
          </div>
          <ul className="space-y-2">
            {tutor.learning_resources.map((r, i) => (
              <li key={i} className="flex items-start gap-3 text-sm text-text-secondary">
                <span className="w-1.5 h-1.5 rounded-full bg-ai-400 mt-2 shrink-0" />
                {r}
              </li>
            ))}
          </ul>
        </div>
      )}

      {tutor.misconceptions.length > 0 && (
        <div className="rounded-xl border border-amber-200 dark:border-amber-800 bg-amber-50/50 dark:bg-amber-900/10 p-5">
          <div className="flex items-center gap-2 mb-4">
            <HelpCircle size={18} className="text-amber-600" />
            <h3 className="text-sm font-semibold text-text">Common Misconceptions</h3>
          </div>
          <ul className="space-y-2">
            {tutor.misconceptions.map((m, i) => (
              <li key={i} className="flex items-start gap-3 text-sm text-text-secondary">
                <span className="w-1.5 h-1.5 rounded-full bg-amber-400 mt-2 shrink-0" />
                {m}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}
