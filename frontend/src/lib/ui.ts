import type { TaskType, TopicStatus } from '../types'

export function masteryColor(pct: number): string {
  if (pct >= 91) return '#15803d' // dark green - mastered
  if (pct >= 71) return '#65a30d' // light green - comfortable
  if (pct >= 41) return '#ca8a04' // yellow - learning
  return '#dc2626' // red - beginner
}

export function masteryLabel(pct: number): string {
  if (pct >= 91) return 'Mastered'
  if (pct >= 71) return 'Comfortable'
  if (pct >= 41) return 'Learning'
  return 'Beginner'
}

export function statusBadge(label: string): { bg: string; text: string } {
  switch (label) {
    case 'on-track':
      return { bg: 'bg-green-100', text: 'text-green-700' }
    case 'at-risk':
      return { bg: 'bg-yellow-100', text: 'text-yellow-700' }
    case 'behind':
      return { bg: 'bg-red-100', text: 'text-red-700' }
    default:
      return { bg: 'bg-slate-100', text: 'text-slate-700' }
  }
}

export function topicStatusBadge(status: TopicStatus): { bg: string; text: string; label: string } {
  switch (status) {
    case 'mastered':
      return { bg: 'bg-green-100', text: 'text-green-700', label: 'Mastered' }
    case 'in_progress':
      return { bg: 'bg-blue-100', text: 'text-blue-700', label: 'In Progress' }
    default:
      return { bg: 'bg-slate-100', text: 'text-slate-600', label: 'Not Started' }
  }
}

export const taskTypeIcon: Record<TaskType, string> = {
  video: '🎬',
  problem: '🧩',
  codeforces: '⚔️',
  revision: '🔁',
  mock: '📝',
  study: '📚',
}

export function formatMinutes(min: number): string {
  if (min < 60) return `${min} min`
  const h = Math.floor(min / 60)
  const m = min % 60
  return m ? `${h}h ${m}m` : `${h}h`
}
