import { BookOpen, ScrollText, AlertTriangle, ClipboardList, MessageSquare } from 'lucide-react'

const icons: Record<string, React.ReactNode> = {
  notes: <BookOpen size={20} />,
  rubrics: <ScrollText size={20} />,
  mistakes: <AlertTriangle size={20} />,
  assignments: <ClipboardList size={20} />,
  feedback_examples: <MessageSquare size={20} />,
}

const colors: Record<string, string> = {
  notes: 'text-blue-600 bg-blue-50 dark:text-blue-400 dark:bg-blue-900/30',
  rubrics: 'text-violet-600 bg-violet-50 dark:text-violet-400 dark:bg-violet-900/30',
  mistakes: 'text-amber-600 bg-amber-50 dark:text-amber-400 dark:bg-amber-900/30',
  assignments: 'text-emerald-600 bg-emerald-50 dark:text-emerald-400 dark:bg-emerald-900/30',
  feedback_examples: 'text-rose-600 bg-rose-50 dark:text-rose-400 dark:bg-rose-900/30',
}

interface CollectionCardProps {
  name: string
  data: {
    points_count: number
    description: string
  }
}

export function CollectionCard({ name, data }: CollectionCardProps) {
  const color = colors[name] || 'text-ai-600 bg-ai-50 dark:text-ai-400 dark:bg-ai-900/30'
  const icon = icons[name] || <BookOpen size={20} />
  const label = name.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase())

  return (
    <div className="rounded-xl border border-border bg-surface p-5 hover:shadow-md transition-shadow animate-slide-up">
      <div className="flex items-start justify-between mb-4">
        <div className={`w-10 h-10 rounded-xl flex items-center justify-center ${color}`}>
          {icon}
        </div>
        <span className={`text-xs font-semibold tabular-nums px-2.5 py-1 rounded-full ${
          data.points_count > 0
            ? 'bg-emerald-50 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-400'
            : 'bg-surface-tertiary text-text-tertiary'
        }`}>
          {data.points_count} pts
        </span>
      </div>
      <h4 className="text-sm font-semibold text-text mb-1">{label}</h4>
      <p className="text-xs text-text-tertiary leading-relaxed">{data.description}</p>
    </div>
  )
}
