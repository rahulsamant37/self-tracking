interface ProgressBarProps {
  value: number
  color?: string
  height?: number
}

export function ProgressBar({ value, color = '#2563eb', height = 8 }: ProgressBarProps) {
  const clamped = Math.max(0, Math.min(100, value))
  return (
    <div
      className="w-full overflow-hidden rounded-full bg-slate-200"
      style={{ height }}
      role="progressbar"
      aria-valuenow={clamped}
      aria-valuemin={0}
      aria-valuemax={100}
    >
      <div
        className="h-full rounded-full transition-all duration-500"
        style={{ width: `${clamped}%`, backgroundColor: color }}
      />
    </div>
  )
}
