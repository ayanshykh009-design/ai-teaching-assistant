import { useCallback, useRef, useState } from 'react'
import { Upload, FileCode, X } from 'lucide-react'

interface UploadZoneProps {
  onFile: (file: File) => void
  disabled?: boolean
}

export function UploadZone({ onFile, disabled }: UploadZoneProps) {
  const inputRef = useRef<HTMLInputElement>(null)
  const [dragOver, setDragOver] = useState(false)
  const [file, setFile] = useState<File | null>(null)

  const handle = useCallback((f: File) => {
    if (f.name.endsWith('.js')) {
      setFile(f)
      onFile(f)
    }
  }, [onFile])

  const onDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setDragOver(false)
    const f = e.dataTransfer.files[0]
    if (f) handle(f)
  }, [handle])

  return (
    <div
      onDrop={onDrop}
      onDragOver={(e) => { e.preventDefault(); setDragOver(true) }}
      onDragLeave={() => setDragOver(false)}
      onClick={() => !file && inputRef.current?.click()}
      className={`
        relative border-2 border-dashed rounded-xl p-8 text-center cursor-pointer
        transition-all duration-200
        ${dragOver ? 'border-ai-500 bg-ai-50/50 dark:bg-ai-900/20 scale-[1.01]' : 'border-border hover:border-ai-400 hover:bg-surface-tertiary/50'}
        ${file ? 'bg-surface-tertiary/30' : ''}
        ${disabled ? 'opacity-50 pointer-events-none' : ''}
      `}
    >
      <input ref={inputRef} type="file" accept=".js" hidden onChange={(e) => {
        const f = e.target.files?.[0]
        if (f) handle(f)
      }} />

      {file ? (
        <div className="flex items-center justify-between p-4 rounded-lg bg-surface border border-border max-w-md mx-auto">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-ai-50 dark:bg-ai-900/30 flex items-center justify-center">
              <FileCode size={20} className="text-ai-500" />
            </div>
            <div className="text-left">
              <p className="text-sm font-medium text-text">{file.name}</p>
              <p className="text-xs text-text-tertiary">{(file.size / 1024).toFixed(1)} KB</p>
            </div>
          </div>
          <button
            onClick={(e) => { e.stopPropagation(); setFile(null) }}
            className="p-1.5 rounded-lg hover:bg-surface-tertiary text-text-tertiary"
          >
            <X size={16} />
          </button>
        </div>
      ) : (
        <div className="space-y-3">
          <div className="w-14 h-14 rounded-xl bg-ai-50 dark:bg-ai-900/30 flex items-center justify-center mx-auto">
            <Upload size={24} className="text-ai-500" />
          </div>
          <div>
            <p className="text-sm font-medium text-text">
              Drop your <code className="px-1.5 py-0.5 rounded bg-surface-tertiary text-ai-500 text-xs font-mono">.js</code> file here
            </p>
            <p className="text-xs text-text-tertiary mt-1">or click to browse</p>
          </div>
          <p className="text-[11px] text-text-tertiary">Only .js files up to 1 MB</p>
        </div>
      )}
    </div>
  )
}
