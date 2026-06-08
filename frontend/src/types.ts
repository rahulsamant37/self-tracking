export type GoalKind = 'exam' | 'skill' | 'dsa'
export type Difficulty = 'easy' | 'medium' | 'hard'
export type TopicStatus = 'not_started' | 'in_progress' | 'mastered'
export type TaskType = 'video' | 'problem' | 'codeforces' | 'revision' | 'mock' | 'study'
export type TaskStatus = 'pending' | 'completed' | 'partial' | 'deferred'
export type ProblemOutcome = 'solved_fast' | 'solved_slow' | 'partial' | 'unsolved'

export interface Goal {
  id: number
  name: string
  description: string
  kind: GoalKind
  target_date: string | null
  daily_minutes: number
  priority: number
  color: string
  active: boolean
  days_remaining: number | null
  progress_pct: number
  status_label: 'on-track' | 'at-risk' | 'behind'
}

export interface Task {
  id: number
  date: string
  goal_id: number | null
  topic_id: number | null
  title: string
  description: string
  type: TaskType
  estimated_minutes: number
  actual_minutes: number | null
  status: TaskStatus
  resource_ref: string
  cf_rating: number | null
  cf_url: string
  notes: string
  goal_name: string | null
  goal_color: string | null
}

export interface Topic {
  id: number
  level_id: number
  name: string
  order: number
  difficulty: Difficulty
  video_count: number
  videos_watched: number
  problems_assigned: number
  problems_solved: number
  mastery_pct: number
  status: TopicStatus
}

export interface Level {
  id: number
  number: number
  name: string
  topics: Topic[]
  mastery_pct: number
}

export interface DashboardStats {
  streak: number
  today_total: number
  today_completed: number
  total_tasks_completed: number
  goals: Goal[]
}

export interface GoalCreate {
  name: string
  description?: string
  kind: GoalKind
  target_date?: string | null
  daily_minutes?: number
  priority?: number
  color?: string
}
