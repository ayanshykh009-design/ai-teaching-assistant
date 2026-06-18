import { NavLink } from 'react-router-dom'
import { Upload, LayoutDashboard, BookOpen, GraduationCap, Settings, X } from 'lucide-react'

const links = [
  { to: '/', icon: LayoutDashboard, label: 'Dashboard' },
  { to: '/review', icon: Upload, label: 'Review Code' },
  { to: '/knowledge', icon: BookOpen, label: 'Knowledge Base' },
  { to: '/docs', icon: GraduationCap, label: 'API Docs' },
]

interface SidebarProps {
  open: boolean
  onClose: () => void
}

export function Sidebar({ open, onClose }: SidebarProps) {
  return (
    <>
      {open && <div className="fixed inset-0 bg-black/30 z-40 lg:hidden" onClick={onClose} />}
      <aside className={`
        fixed top-0 left-0 z-50 h-full w-64 bg-surface border-r border-border
        transform transition-transform duration-300 ease-in-out
        lg:translate-x-0 lg:static lg:z-auto
        ${open ? 'translate-x-0' : '-translate-x-full'}
      `}>
        <div className="flex items-center justify-between h-16 px-6 border-b border-border">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-ai-500 flex items-center justify-center">
              <GraduationCap size={18} className="text-white" />
            </div>
            <div>
              <span className="font-semibold text-text">AI Tutor</span>
              <span className="block text-[10px] text-text-tertiary leading-tight">Teaching Assistant</span>
            </div>
          </div>
          <button onClick={onClose} className="lg:hidden p-1 rounded-md hover:bg-surface-tertiary text-text-secondary">
            <X size={20} />
          </button>
        </div>

        <nav className="p-3 space-y-1">
          {links.map((link) => (
            <NavLink
              key={link.to}
              to={link.to}
              end={link.to === '/'}
              onClick={onClose}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                  isActive
                    ? 'bg-ai-50 text-ai-600 dark:bg-ai-900/30 dark:text-ai-400'
                    : 'text-text-secondary hover:bg-surface-tertiary hover:text-text'
                }`
              }
            >
              <link.icon size={18} />
              {link.label}
            </NavLink>
          ))}
        </nav>

        <div className="absolute bottom-0 left-0 right-0 p-3 border-t border-border">
          <div className="flex items-center gap-3 px-3 py-2.5 rounded-lg text-text-secondary">
            <Settings size={18} />
            <span className="text-sm font-medium">Settings</span>
          </div>
        </div>
      </aside>
    </>
  )
}
