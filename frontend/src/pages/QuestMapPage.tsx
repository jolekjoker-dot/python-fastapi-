import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { listQuests } from '../api/quests'
import type { QuestSummary } from '../types/quest'
import { TopNav } from '../components/layout/TopNav'

export function QuestMapPage() {
  const [quests, setQuests] = useState<QuestSummary[]>([])
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()

  useEffect(() => {
    listQuests()
      .then(setQuests)
      .finally(() => setLoading(false))
  }, [])

  const phase1 = quests.filter((q) => q.phase === 1)

  if (loading) {
    return (
      <div className="h-screen flex flex-col">
        <TopNav />
        <div className="flex-1 flex items-center justify-center text-text-muted">
          Loading quest map...
        </div>
      </div>
    )
  }

  return (
    <div className="h-screen flex flex-col">
      <TopNav />
      <div className="flex-1 overflow-auto p-8">
        <h1 className="text-3xl font-bold text-gold text-center mb-2">
          魔法学院 关卡地图
        </h1>
        <p className="text-text-muted text-center mb-10">
          第一篇章：学徒试炼 — Python 基础
        </p>

        {/* Quest nodes */}
        <div className="max-w-3xl mx-auto">
          <div className="flex flex-wrap justify-center gap-4">
            {phase1.map((quest, i) => {
              const isLast = quest.order === 10
              return (
                <div key={quest.id} className="flex items-center">
                  <button
                    onClick={() => {
                      if (quest.unlocked || quest.completed) {
                        navigate(`/quest/${quest.id}`)
                      }
                    }}
                    disabled={!quest.unlocked && !quest.completed}
                    className={`w-36 h-36 rounded-xl flex flex-col items-center justify-center gap-1 border-2 transition-all cursor-pointer ${
                      quest.completed
                        ? 'border-success bg-success/10 hover:bg-success/20'
                        : quest.unlocked
                          ? 'border-gold bg-gold/10 hover:bg-gold/20 animate-pulse'
                          : 'border-text-muted/30 bg-surface-panel/50 opacity-50 cursor-not-allowed'
                    }`}
                  >
                    {isLast ? (
                      <span className="text-3xl">👑</span>
                    ) : (
                      <span className="text-2xl font-bold text-gold">
                        {quest.order}
                      </span>
                    )}
                    <span className="text-xs text-center px-1 text-text-primary leading-tight">
                      {quest.title.split('—')[0].trim()}
                    </span>
                    <span className="text-xs text-text-muted">
                      {quest.xp_reward} XP
                    </span>
                    {quest.completed && (
                      <span className="text-success text-lg">✓</span>
                    )}
                    {quest.unlocked && !quest.completed && (
                      <span className="text-gold text-xs">Ready</span>
                    )}
                  </button>

                  {/* Connector line */}
                  {i < phase1.length - 1 && (
                    <div
                      className={`w-8 h-0.5 -ml-1 -mr-1 ${
                        quest.completed ? 'bg-success' : 'bg-text-muted/30'
                      }`}
                    />
                  )}
                </div>
              )
            })}
          </div>
        </div>

        {/* Coming soon */}
        <div className="max-w-3xl mx-auto mt-12 opacity-40">
          <h2 className="text-xl text-center text-text-muted mb-4">
            第二篇章：魔法阵构筑 — FastAPI（即将开放）
          </h2>
          <div className="flex justify-center gap-3">
            {[11, 12, 13, 14, 15, 16, 17, 18].map((n) => (
              <div
                key={n}
                className="w-20 h-20 rounded-lg bg-surface-panel/50 border border-text-muted/30 flex items-center justify-center text-text-muted text-sm"
              >
                {n === 18 ? '👑' : n}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
