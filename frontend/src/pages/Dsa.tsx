import { useEffect, useState } from 'react'
import { api } from '../api'
import { ProgressBar } from '../components/ProgressBar'
import { masteryColor, masteryLabel, topicStatusBadge } from '../lib/ui'
import type { Level, ProblemOutcome, Topic } from '../types'

const outcomes: { value: ProblemOutcome; label: string; cls: string }[] = [
  { value: 'solved_fast', label: '⚡ Fast', cls: 'bg-green-100 text-green-700 hover:bg-green-200' },
  { value: 'solved_slow', label: '✅ Slow', cls: 'bg-lime-100 text-lime-700 hover:bg-lime-200' },
  { value: 'partial', label: '◑ Partial', cls: 'bg-yellow-100 text-yellow-700 hover:bg-yellow-200' },
  { value: 'unsolved', label: '✗ Unsolved', cls: 'bg-red-100 text-red-700 hover:bg-red-200' },
]

export function Dsa() {
  const [levels, setLevels] = useState<Level[]>([])
  const [loading, setLoading] = useState(true)
  const [message, setMessage] = useState<string | null>(null)

  useEffect(() => {
    api
      .listLevels()
      .then(setLevels)
      .finally(() => setLoading(false))
  }, [])

  const replaceTopic = (updated: Topic) => {
    setLevels((prev) =>
      prev.map((lvl) =>
        lvl.id === updated.level_id
          ? {
              ...lvl,
              topics: lvl.topics.map((t) => (t.id === updated.id ? updated : t)),
              mastery_pct:
                Math.round(
                  (lvl.topics.reduce(
                    (s, t) => s + (t.id === updated.id ? updated.mastery_pct : t.mastery_pct),
                    0,
                  ) /
                    lvl.topics.length) *
                    10,
                ) / 10,
            }
          : lvl,
      ),
    )
  }

  const submit = async (topic: Topic, outcome: ProblemOutcome) => {
    const updated = await api.submitResult(topic.id, outcome)
    replaceTopic(updated)
    setMessage(`${topic.name}: mastery now ${updated.mastery_pct}% (${masteryLabel(updated.mastery_pct)})`)
  }

  const watch = async (topic: Topic) => {
    const updated = await api.watchVideo(topic.id)
    replaceTopic(updated)
  }

  if (loading) return <p className="text-slate-500">Loading…</p>

  return (
    <div className="space-y-6">
      <header>
        <h2 className="text-2xl font-bold">TLE Eliminator Course</h2>
        <p className="text-slate-500">
          Track lectures and master each topic. Log problem results to drive the adaptive engine.
        </p>
      </header>

      {message && (
        <div className="rounded-lg bg-blue-50 px-4 py-2 text-sm text-blue-800">{message}</div>
      )}

      {levels.map((level) => (
        <section key={level.id} className="rounded-xl border border-slate-200 bg-white shadow-sm">
          <div className="border-b border-slate-100 px-5 py-4">
            <div className="mb-2 flex items-center justify-between">
              <h3 className="font-semibold">{level.name}</h3>
              <span className="text-sm text-slate-500">{level.mastery_pct}% avg mastery</span>
            </div>
            <ProgressBar value={level.mastery_pct} color={masteryColor(level.mastery_pct)} />
          </div>
          <ul className="divide-y divide-slate-100">
            {level.topics.map((topic) => {
              const badge = topicStatusBadge(topic.status)
              return (
                <li key={topic.id} className="px-5 py-4">
                  <div className="flex flex-wrap items-center justify-between gap-2">
                    <div className="flex items-center gap-2">
                      <span className="font-medium">{topic.name}</span>
                      <span className="rounded bg-slate-100 px-1.5 py-0.5 text-xs capitalize text-slate-500">
                        {topic.difficulty}
                      </span>
                      <span className={`rounded-full px-2 py-0.5 text-xs ${badge.bg} ${badge.text}`}>
                        {badge.label}
                      </span>
                    </div>
                    <span
                      className="text-sm font-semibold"
                      style={{ color: masteryColor(topic.mastery_pct) }}
                    >
                      {topic.mastery_pct}% · {masteryLabel(topic.mastery_pct)}
                    </span>
                  </div>

                  <div className="mt-2">
                    <ProgressBar value={topic.mastery_pct} color={masteryColor(topic.mastery_pct)} />
                  </div>

                  <div className="mt-2 flex flex-wrap items-center gap-x-4 gap-y-1 text-xs text-slate-500">
                    <span>
                      🎬 {topic.videos_watched}/{topic.video_count} videos
                    </span>
                    <span>
                      🧩 {topic.problems_solved} solved · {topic.problems_assigned} assigned
                    </span>
                  </div>

                  <div className="mt-3 flex flex-wrap gap-2">
                    <button
                      onClick={() => watch(topic)}
                      disabled={topic.videos_watched >= topic.video_count}
                      className="rounded-md bg-slate-100 px-2.5 py-1 text-xs font-medium text-slate-700 hover:bg-slate-200 disabled:opacity-40"
                    >
                      ▶ Watched a video
                    </button>
                    {outcomes.map((o) => (
                      <button
                        key={o.value}
                        onClick={() => submit(topic, o.value)}
                        className={`rounded-md px-2.5 py-1 text-xs font-medium ${o.cls}`}
                      >
                        {o.label}
                      </button>
                    ))}
                  </div>
                </li>
              )
            })}
          </ul>
        </section>
      ))}
    </div>
  )
}
