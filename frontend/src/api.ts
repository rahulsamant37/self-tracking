import type {
  DashboardStats,
  Goal,
  GoalCreate,
  Level,
  ProblemOutcome,
  Task,
  TaskStatus,
  Topic,
} from './types'

const BASE = import.meta.env.VITE_API_BASE ?? ''

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })
  if (!res.ok) {
    const text = await res.text()
    throw new Error(`${res.status}: ${text}`)
  }
  if (res.status === 204) return undefined as T
  return res.json() as Promise<T>
}

export const api = {
  getDashboard: () => request<DashboardStats>('/api/dashboard'),

  listGoals: () => request<Goal[]>('/api/goals'),
  createGoal: (payload: GoalCreate) =>
    request<Goal>('/api/goals', { method: 'POST', body: JSON.stringify(payload) }),
  deleteGoal: (id: number) => request<void>(`/api/goals/${id}`, { method: 'DELETE' }),

  listTasks: (date?: string) =>
    request<Task[]>(`/api/tasks${date ? `?task_date=${date}` : ''}`),
  generateTasks: (date?: string) =>
    request<Task[]>('/api/tasks/generate', {
      method: 'POST',
      body: JSON.stringify({ date: date ?? null }),
    }),
  updateTask: (id: number, payload: { status?: TaskStatus; actual_minutes?: number; notes?: string }) =>
    request<Task>(`/api/tasks/${id}`, { method: 'PATCH', body: JSON.stringify(payload) }),

  listLevels: () => request<Level[]>('/api/tle/levels'),
  submitResult: (topicId: number, outcome: ProblemOutcome) =>
    request<Topic>(`/api/tle/topics/${topicId}/result`, {
      method: 'POST',
      body: JSON.stringify({ outcome }),
    }),
  watchVideo: (topicId: number) =>
    request<Topic>(`/api/tle/topics/${topicId}/watch`, { method: 'POST' }),
}
