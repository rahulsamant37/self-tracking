import { useEffect, useState, type FormEvent, type ReactNode } from 'react'
import { api } from '../api'
import { ProgressBar } from '../components/ProgressBar'
import { statusBadge } from '../lib/ui'
import type { Goal, GoalCreate, GoalKind } from '../types'

const emptyForm: GoalCreate = {
  name: '',
  description: '',
  kind: 'skill',
  target_date: '',
  daily_minutes: 120,
  priority: 1,
  color: '#2563eb',
}

export function Goals() {
  const [goals, setGoals] = useState<Goal[]>([])
  const [form, setForm] = useState<GoalCreate>(emptyForm)
  const [error, setError] = useState<string | null>(null)
  const [showForm, setShowForm] = useState(false)

  const load = () => api.listGoals().then(setGoals)
  useEffect(() => {
    load()
  }, [])

  const submit = async (e: FormEvent) => {
    e.preventDefault()
    setError(null)
    try {
      await api.createGoal({
        ...form,
        target_date: form.target_date ? form.target_date : null,
      })
      setForm(emptyForm)
      setShowForm(false)
      await load()
    } catch (err) {
      setError(
        String(err).includes('422')
          ? 'Target date must be in the future.'
          : String(err),
      )
    }
  }

  const remove = async (id: number) => {
    await api.deleteGoal(id)
    await load()
  }

  return (
    <div className="space-y-6">
      <header className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold">Goals</h2>
          <p className="text-slate-500">Manage your concurrent goals and deadlines.</p>
        </div>
        <button
          onClick={() => setShowForm((s) => !s)}
          className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-semibold text-white hover:bg-blue-700"
        >
          {showForm ? 'Cancel' : '+ New goal'}
        </button>
      </header>

      {showForm && (
        <form
          onSubmit={submit}
          className="space-y-4 rounded-xl border border-slate-200 bg-white p-5 shadow-sm"
        >
          {error && <p className="text-sm text-red-600">{error}</p>}
          <div className="grid gap-4 md:grid-cols-2">
            <Field label="Name">
              <input
                required
                value={form.name}
                onChange={(e) => setForm({ ...form, name: e.target.value })}
                className="input"
                placeholder="e.g. CAT 2026"
              />
            </Field>
            <Field label="Type">
              <select
                value={form.kind}
                onChange={(e) => setForm({ ...form, kind: e.target.value as GoalKind })}
                className="input"
              >
                <option value="exam">Exam-based</option>
                <option value="skill">Skill-based</option>
                <option value="dsa">DSA</option>
              </select>
            </Field>
            <Field label="Target date">
              <input
                type="date"
                value={form.target_date ?? ''}
                onChange={(e) => setForm({ ...form, target_date: e.target.value })}
                className="input"
              />
            </Field>
            <Field label="Daily minutes">
              <input
                type="number"
                min={15}
                value={form.daily_minutes}
                onChange={(e) => setForm({ ...form, daily_minutes: Number(e.target.value) })}
                className="input"
              />
            </Field>
            <Field label="Priority (1 = highest)">
              <input
                type="number"
                min={1}
                value={form.priority}
                onChange={(e) => setForm({ ...form, priority: Number(e.target.value) })}
                className="input"
              />
            </Field>
            <Field label="Color">
              <input
                type="color"
                value={form.color}
                onChange={(e) => setForm({ ...form, color: e.target.value })}
                className="h-10 w-full cursor-pointer rounded-lg border border-slate-300"
              />
            </Field>
          </div>
          <Field label="Description">
            <textarea
              value={form.description}
              onChange={(e) => setForm({ ...form, description: e.target.value })}
              className="input"
              rows={2}
            />
          </Field>
          <button
            type="submit"
            className="rounded-lg bg-green-600 px-4 py-2 text-sm font-semibold text-white hover:bg-green-700"
          >
            Create goal
          </button>
        </form>
      )}

      <div className="grid gap-4 md:grid-cols-2">
        {goals.map((goal) => {
          const badge = statusBadge(goal.status_label)
          return (
            <div key={goal.id} className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
              <div className="mb-1 flex items-start justify-between">
                <div className="flex items-center gap-2">
                  <span
                    className="inline-block h-3 w-3 rounded-full"
                    style={{ backgroundColor: goal.color }}
                  />
                  <h4 className="font-semibold">{goal.name}</h4>
                  <span className="rounded bg-slate-100 px-1.5 py-0.5 text-xs uppercase text-slate-500">
                    {goal.kind}
                  </span>
                </div>
                <span
                  className={`rounded-full px-2 py-0.5 text-xs font-medium ${badge.bg} ${badge.text}`}
                >
                  {goal.status_label}
                </span>
              </div>
              {goal.description && <p className="mb-2 text-sm text-slate-500">{goal.description}</p>}
              <div className="mb-1 flex justify-between text-sm text-slate-500">
                <span>{goal.progress_pct}%</span>
                <span>
                  {goal.days_remaining != null
                    ? `${goal.days_remaining} days left`
                    : 'No deadline'}
                </span>
              </div>
              <ProgressBar value={goal.progress_pct} color={goal.color} />
              <div className="mt-3 flex justify-between text-xs text-slate-400">
                <span>{goal.daily_minutes} min/day</span>
                <button onClick={() => remove(goal.id)} className="text-red-500 hover:underline">
                  Delete
                </button>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}

function Field({ label, children }: { label: string; children: ReactNode }) {
  return (
    <label className="block">
      <span className="mb-1 block text-sm font-medium text-slate-600">{label}</span>
      {children}
    </label>
  )
}
