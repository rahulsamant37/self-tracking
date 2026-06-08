import { useEffect, useMemo, useState } from 'react'
import { api } from '../api'
import { formatMinutes, taskTypeIcon } from '../lib/ui'
import type { Task } from '../types'

const today = new Date().toISOString().slice(0, 10)

export function Today() {
  const [tasks, setTasks] = useState<Task[]>([])
  const [loading, setLoading] = useState(true)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let active = true
    api
      .listTasks(today)
      .then((d) => active && setTasks(d))
      .catch((e) => active && setError(String(e)))
      .finally(() => active && setLoading(false))
    return () => {
      active = false
    }
  }, [])

  const generate = async () => {
    setBusy(true)
    try {
      const created = await api.generateTasks(today)
      setTasks(created)
    } catch (e) {
      setError(String(e))
    } finally {
      setBusy(false)
    }
  }

  const toggle = async (task: Task) => {
    const next = task.status === 'completed' ? 'pending' : 'completed'
    const updated = await api.updateTask(task.id, { status: next })
    setTasks((prev) => prev.map((t) => (t.id === task.id ? updated : t)))
  }

  const grouped = useMemo(() => {
    const map = new Map<string, Task[]>()
    for (const t of tasks) {
      const key = t.goal_name ?? 'Other'
      if (!map.has(key)) map.set(key, [])
      map.get(key)!.push(t)
    }
    return Array.from(map.entries())
  }, [tasks])

  const totalMin = tasks.reduce((s, t) => s + t.estimated_minutes, 0)
  const completed = tasks.filter((t) => t.status === 'completed').length

  if (loading) return <p className="text-slate-500">Loading…</p>

  return (
    <div className="space-y-6">
      <header className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h2 className="text-2xl font-bold">Today's Tasks</h2>
          <p className="text-slate-500">
            {new Date().toLocaleDateString(undefined, {
              weekday: 'long',
              month: 'long',
              day: 'numeric',
            })}
          </p>
        </div>
        {tasks.length > 0 && (
          <div className="rounded-lg bg-white px-4 py-2 text-sm shadow-sm">
            <span className="font-semibold">{completed}</span>/{tasks.length} done ·{' '}
            <span className="font-semibold">{formatMinutes(totalMin)}</span> planned
          </div>
        )}
      </header>

      {error && <p className="text-red-600">{error}</p>}

      {tasks.length === 0 ? (
        <div className="rounded-xl border border-dashed border-slate-300 bg-white p-10 text-center">
          <p className="mb-4 text-slate-500">No plan generated for today yet.</p>
          <button
            onClick={generate}
            disabled={busy}
            className="rounded-lg bg-blue-600 px-5 py-2.5 text-sm font-semibold text-white hover:bg-blue-700 disabled:opacity-50"
          >
            {busy ? 'Generating…' : "✨ Generate today's plan"}
          </button>
        </div>
      ) : (
        <div className="space-y-6">
          {grouped.map(([goalName, goalTasks]) => (
            <section key={goalName}>
              <h3
                className="mb-2 flex items-center gap-2 text-sm font-semibold uppercase tracking-wide text-slate-500"
                style={{ color: goalTasks[0]?.goal_color ?? undefined }}
              >
                {goalName}
              </h3>
              <ul className="space-y-2">
                {goalTasks.map((task) => (
                  <li
                    key={task.id}
                    className={`flex items-start gap-3 rounded-xl border bg-white p-4 shadow-sm transition-colors ${
                      task.status === 'completed' ? 'border-green-200 bg-green-50' : 'border-slate-200'
                    }`}
                  >
                    <input
                      type="checkbox"
                      checked={task.status === 'completed'}
                      onChange={() => toggle(task)}
                      className="mt-1 h-5 w-5 cursor-pointer rounded border-slate-300 text-blue-600"
                      aria-label={`Complete ${task.title}`}
                    />
                    <div className="flex-1">
                      <p
                        className={`font-medium ${
                          task.status === 'completed' ? 'text-slate-400 line-through' : ''
                        }`}
                      >
                        {taskTypeIcon[task.type]} {task.title}
                      </p>
                      {task.description && (
                        <p className="text-sm text-slate-500">{task.description}</p>
                      )}
                      <div className="mt-1 flex flex-wrap items-center gap-3 text-xs text-slate-500">
                        <span>⏱️ {formatMinutes(task.estimated_minutes)}</span>
                        {task.cf_rating && <span>★ {task.cf_rating} rating</span>}
                        {task.cf_url && (
                          <a
                            href={task.cf_url}
                            target="_blank"
                            rel="noreferrer"
                            className="text-blue-600 hover:underline"
                          >
                            Open problem ↗
                          </a>
                        )}
                      </div>
                    </div>
                  </li>
                ))}
              </ul>
            </section>
          ))}
        </div>
      )}
    </div>
  )
}
