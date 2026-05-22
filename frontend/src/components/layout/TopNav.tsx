import { useNavigate } from 'react-router-dom'
import { useUserStore } from '../../stores/userStore'

function xpForLevel(level: number) {
  return level * 1000
}

export function TopNav() {
  const { user, logout } = useUserStore()
  const navigate = useNavigate()

  const currentXp = user?.xp ?? 0
  const level = user?.level ?? 1
  const xpForCurrent = xpForLevel(level)
  const xpForPrev = xpForLevel(level - 1)
  const xpInLevel = xpForCurrent - xpForPrev
  const progress = xpInLevel > 0 ? ((currentXp - xpForPrev) / xpInLevel) * 100 : 0

  return (
    <nav className="bg-surface-panel border-b border-text-muted/20 shrink-0">
      <div className="h-10 flex items-center justify-between px-4">
        <div className="flex items-center gap-3">
          <span
            className="text-gold font-bold text-lg cursor-pointer"
            onClick={() => navigate('/map')}
          >
            Code Quest
          </span>
          <span className="text-text-muted text-sm hidden sm:inline">|</span>
          <button
            onClick={() => navigate('/map')}
            className="text-text-muted text-sm hover:text-gold transition-colors cursor-pointer hidden sm:inline"
          >
            Map
          </button>
          <button
            onClick={() => navigate('/achievements')}
            className="text-text-muted text-sm hover:text-gold transition-colors cursor-pointer"
          >
            Achievements
          </button>
          <button
            onClick={() => navigate('/shop')}
            className="text-text-muted text-sm hover:text-gold transition-colors cursor-pointer"
          >
            Shop
          </button>
          <button
            onClick={() => navigate('/leaderboard')}
            className="text-text-muted text-sm hover:text-gold transition-colors cursor-pointer"
          >
            Leaderboard
          </button>
        </div>

        <div className="flex items-center gap-4 text-sm">
          <span className="text-gold font-semibold">Lv.{level}</span>
          <span className="text-success text-xs w-16 text-right">
            {currentXp} / {xpForCurrent} XP
          </span>
          <span className="text-gold/80">{user?.coins ?? 0} coins</span>
          <span className="text-text-primary">{user?.username}</span>
          <button
            onClick={logout}
            className="text-text-muted hover:text-error transition-colors cursor-pointer"
          >
            Exit
          </button>
        </div>
      </div>

      {/* XP progress bar */}
      <div className="h-1 bg-surface-dark">
        <div
          className="h-full bg-gradient-to-r from-gold to-success transition-all duration-700 ease-out"
          style={{ width: `${Math.min(100, progress)}%` }}
        />
      </div>
    </nav>
  )
}
