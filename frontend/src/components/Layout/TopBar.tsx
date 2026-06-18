import { Menu, Moon, Sun } from 'lucide-react'

interface TopBarProps {
  theme: 'light' | 'dark'
  onToggleTheme: () => void
  onMenuClick: () => void
}

export function TopBar({ theme, onToggleTheme, onMenuClick }: TopBarProps) {
  return (
    <header className="h-16 border-b border-border bg-surface flex items-center justify-between px-4 lg:px-6 sticky top-0 z-30">
      <button onClick={onMenuClick} className="lg:hidden p-2 rounded-lg hover:bg-surface-tertiary text-text-secondary">
        <Menu size={20} />
      </button>

      <div className="hidden lg:flex items-center gap-2 text-sm text-text-secondary">
        <span className="w-2 h-2 rounded-full bg-emerald-500" />
        All systems operational
      </div>

      <div className="flex items-center gap-3 ml-auto">
        <button
          onClick={onToggleTheme}
          className="p-2 rounded-lg hover:bg-surface-tertiary text-text-secondary transition-colors"
          aria-label="Toggle theme"
        >
          {theme === 'dark' ? <Sun size={18} /> : <Moon size={18} />}
        </button>
        <div className="w-8 h-8 rounded-full bg-ai-500 flex items-center justify-center text-white text-xs font-semibold">
          TA
        </div>
      </div>
    </header>
  )
}
