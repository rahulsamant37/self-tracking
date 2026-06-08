import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { api } from '../api'
import { ProgressBar } from '../components/ProgressBar'
import { statusBadge } from '../lib/ui'
import type { DashboardStats } from '../types'

export function Dashboard() {
  const [stats, setStats] = useState<DashboardStats | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    api
      .getDashboard()
      .then(setStats)
      .catch((e) => setError(String(e)))
  }, [])

  if (error) return <p className="text-red-600">Failed to load: {error}</p>
  if (!stats) return <p className="text-slate-500">Loading…</p>

  return (
    <div className="space-y-8">
      <header>
        <h2 className="text-2xl font-bold">Dashboard</h2>
        <p className="text-slate-500">Your goals at a glance.</p>
      </header>

      <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
        <StatCard label="🔥 Streak" value={`${stats.streak} day${stats.streak === 1 ? '' : 's'}`} />
        <StatCard label="Today completed" value={`${stats.today_completed}/${stats.today_total}`} />
        <StatCard label="Tasks done (all-time)" value={String(stats.total_tasks_completed)} />
        <StatCard label="Active goals" value={String(stats.goals.filter((g) => g.active).length)} />
      </div>

      <section className="space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold">Goals</h3>
          <Link to="/goals" className="text-sm font-medium text-blue-600 hover:underline">
            Manage goals →
          </Link>
        </div>
        <div className="grid gap-4 md:grid-cols-2">
          {stats.goals.map((goal) => {
            const badge = statusBadge(goal.status_label)
            return (
              <div
                key={goal.id}
                className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm"
              >
                <div className="mb-2 flex items-start justify-between">
                  <div className="flex items-center gap-2">
                    <span
                      className="inline-block h-3 w-3 rounded-full"
                      style={{ backgroundColor: goal.color }}
                    />
                    <h4 className="font-semibold">{goal.name}</h4>
                  </div>
                  <span
                    className={`rounded-full px-2 py-0.5 text-xs font-medium ${badge.bg} ${badge.text}`}
                  >
                    {goal.status_label}
                  </span>
                </div>
                <div className="mb-1 flex justify-between text-sm text-slate-500">
                  <span>{goal.progress_pct}% complete</span>
                  <span>
                    {goal.days_remaining != null ? `${goal.days_remaining} days left` : 'No deadline'}
                  </span>
                </div>
                <ProgressBar value={goal.progress_pct} color={goal.color} />
              </div>
            )
          })}
        </div>
      </section>

      <Link
        to="/today"
        className="inline-flex items-center gap-2 rounded-lg bg-blue-600 px-4 py-2 text-sm font-semibold text-white hover:bg-blue-700"
      >
        Go to today's tasks →
      </Link>
    </div>
  )
}

function StatCard({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
      <p className="text-xs font-medium uppercase tracking-wide text-slate-500">{label}</p>
      <p className="mt-1 text-2xl font-bold">{value}</p>
    </div>
  )
}
