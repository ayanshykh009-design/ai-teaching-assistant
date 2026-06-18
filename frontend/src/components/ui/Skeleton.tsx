export function Skeleton({ className = '' }: { className?: string }) {
  return <div className={`rounded-lg animate-shimmer ${className}`} />
}

export function CardSkeleton() {
  return (
    <div className="rounded-xl border border-border bg-surface p-6 space-y-4 animate-slide-up">
      <Skeleton className="h-5 w-1/3" />
      <Skeleton className="h-4 w-full" />
      <Skeleton className="h-4 w-2/3" />
    </div>
  )
}

export function ResultSkeleton() {
  return (
    <div className="space-y-6 animate-fade-in">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {[...Array(4)].map((_, i) => (
          <div key={i} className="rounded-xl border border-border bg-surface p-5 space-y-3">
            <Skeleton className="h-8 w-8 rounded-full" />
            <Skeleton className="h-4 w-1/2" />
            <Skeleton className="h-8 w-16" />
          </div>
        ))}
      </div>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {[...Array(4)].map((_, i) => (
          <div key={i} className="rounded-xl border border-border bg-surface p-6 space-y-4">
            <Skeleton className="h-5 w-1/3" />
            <Skeleton className="h-4 w-full" />
            <Skeleton className="h-4 w-5/6" />
            <Skeleton className="h-4 w-4/6" />
          </div>
        ))}
      </div>
    </div>
  )
}
