import { useUserStore } from '../../stores/userStore'

export function TopNav() {
  const { user, logout } = useUserStore()

  return (
    <nav className="h-12 bg-surface-panel border-b border-text-muted/20 flex items-center justify-between px-4 shrink-0">
      <div className="flex items-center gap-3">
        <span className="text-gold font-bold text-lg">Code Quest</span>
        <span className="text-text-muted text-sm hidden sm:inline">|</span>
        <span className="text-text-muted text-sm hidden sm:inline">Python 学习冒险</span>
      </div>

      <div className="flex items-center gap-4 text-sm">
        <span className="text-gold">Lv.{user?.level ?? 1}</span>
        <span className="text-success">{user?.xp ?? 0} XP</span>
        <span className="text-gold/80">{user?.coins ?? 0} coins</span>
        <span className="text-text-primary">{user?.username}</span>
        <button
          onClick={logout}
          className="text-text-muted hover:text-error transition-colors cursor-pointer"
        >
          Exit
        </button>
      </div>
    </nav>
  )
}
