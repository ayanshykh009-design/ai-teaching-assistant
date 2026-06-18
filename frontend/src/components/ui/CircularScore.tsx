interface CircularScoreProps {
  value: number
  max: number
  size?: number
  strokeWidth?: number
  label?: string
}

export function CircularScore({ value, max, size = 120, strokeWidth = 8, label }: CircularScoreProps) {
  const pct = Math.min(100, Math.round((value / max) * 100))
  const r = (size - strokeWidth) / 2
  const c = 2 * Math.PI * r
  const offset = c - (pct / 100) * c
  const getColor = () => {
    if (pct >= 80) return '#22c55e'
    if (pct >= 60) return '#eab308'
    return '#ef4444'
  }
  return (
    <div className="flex flex-col items-center gap-1">
      <div className="relative" style={{ width: size, height: size }}>
        <svg width={size} height={size} className="transform -rotate-90">
          <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke="var(--color-surface-tertiary)" strokeWidth={strokeWidth} />
          <circle
            cx={size / 2} cy={size / 2} r={r}
            fill="none" stroke={getColor()}
            strokeWidth={strokeWidth} strokeLinecap="round"
            strokeDasharray={c} strokeDashoffset={offset}
            className="transition-all duration-1000 ease-out"
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className="text-2xl font-bold text-text">{value}</span>
          <span className="text-xs text-text-tertiary">/ {max}</span>
        </div>
      </div>
      {label && <span className="text-xs text-text-secondary font-medium">{label}</span>}
    </div>
  )
}
