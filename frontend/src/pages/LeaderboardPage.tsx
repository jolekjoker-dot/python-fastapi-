import { useEffect, useState } from 'react'
import { getLeaderboard } from '../api/game'
import type { UserResponse } from '../types/user'
import { TopNav } from '../components/layout/TopNav'
import { useUserStore } from '../stores/userStore'

export function LeaderboardPage() {
  const [users, setUsers] = useState<UserResponse[]>([])
  const { user } = useUserStore()

  useEffect(() => {
    getLeaderboard().then(setUsers)
  }, [])

  return (
    <div className="h-screen flex flex-col">
      <TopNav />
      <div className="flex-1 overflow-auto p-8">
        <div className="max-w-xl mx-auto">
          <h1 className="text-2xl font-bold text-gold mb-6 text-center">学院排行榜</h1>

          <div className="space-y-2">
            {users.map((u, i) => {
              const isMe = u.id === user?.id
              const medals = ['🥇', '🥈', '🥉']
              return (
                <div
                  key={u.id}
                  className={`flex items-center gap-4 p-4 rounded-xl border transition-colors ${
                    isMe
                      ? 'border-gold/40 bg-gold/5'
                      : 'border-text-muted/20 bg-surface-panel/30'
                  }`}
                >
                  <div className="w-8 text-center text-lg font-bold">
                    {i < 3 ? medals[i] : <span className="text-text-muted">{i + 1}</span>}
                  </div>
                  <div className="flex-1">
                    <div className="font-semibold text-text-primary">
                      {u.username}
                      {isMe && <span className="text-gold text-xs ml-2">(你)</span>}
                    </div>
                    <div className="text-xs text-text-muted">Lv.{u.level}</div>
                  </div>
                  <div className="text-right">
                    <div className="text-gold font-bold">{u.xp} XP</div>
                    <div className="text-xs text-text-muted">{u.coins} coins</div>
                  </div>
                </div>
              )
            })}
            {users.length === 0 && (
              <p className="text-text-muted text-center">暂无排名数据</p>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
