interface ProgressBarProps {
  value: number
  max: number
  label?: string
  color?: string
  size?: 'sm' | 'md'
}

export function ProgressBar({ value, max, label, color = 'bg-ai-500', size = 'md' }: ProgressBarProps) {
  const pct = Math.min(100, Math.round((value / max) * 100))
  const h = size === 'sm' ? 'h-1.5' : 'h-2.5'
  return (
    <div className="w-full">
      {label && (
        <div className="flex justify-between mb-1.5">
          <span className="text-sm text-text-secondary">{label}</span>
          <span className="text-sm font-medium text-text">{value}/{max}</span>
        </div>
      )}
      <div className={`w-full bg-surface-tertiary rounded-full ${h} overflow-hidden`}>
        <div
          className={`${color} ${h} rounded-full transition-all duration-700 ease-out`}
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  )
}
