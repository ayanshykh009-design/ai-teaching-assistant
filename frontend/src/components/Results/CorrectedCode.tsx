import { Code } from 'lucide-react'

interface CorrectedCodeProps {
  code: string | null
}

export function CorrectedCode({ code }: CorrectedCodeProps) {
  if (!code) return null

  const clean = code.replace(/^```(?:js|javascript)?\s*/, '').replace(/\s*```$/, '')

  return (
    <div className="rounded-xl border border-border bg-surface overflow-hidden animate-slide-up">
      <div className="flex items-center gap-2 px-5 py-3 border-b border-border bg-surface-tertiary/50">
        <Code size={16} className="text-emerald-500" />
        <span className="text-xs font-semibold text-text-secondary uppercase tracking-wider">Corrected Code</span>
      </div>
      <pre className="p-5 overflow-x-auto text-sm leading-relaxed font-mono text-text">
        <code>{clean}</code>
      </pre>
    </div>
  )
}
