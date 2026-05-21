import { useState } from 'react'
import { useUserStore } from '../stores/userStore'

export function LoginPage() {
  const [username, setUsername] = useState('')
  const { login, loading } = useUserStore()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (username.trim()) {
      await login(username.trim())
    }
  }

  return (
    <div className="h-screen flex items-center justify-center bg-surface-dark">
      <div className="bg-surface-panel p-10 rounded-2xl shadow-2xl w-96 text-center border border-gold/20">
        <h1 className="text-4xl font-bold text-gold mb-2">Code Quest</h1>
        <p className="text-text-muted mb-8">Python 学习冒险之旅</p>

        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="输入你的法师名..."
            className="px-4 py-3 rounded-lg bg-surface-dark border border-text-muted/30 text-text-primary placeholder-text-muted focus:outline-none focus:border-gold transition-colors text-center"
            autoFocus
            maxLength={20}
          />
          <button
            type="submit"
            disabled={loading || !username.trim()}
            className="px-6 py-3 rounded-lg bg-gold text-surface-dark font-bold hover:bg-gold/90 disabled:opacity-40 disabled:cursor-not-allowed transition-all cursor-pointer"
          >
            {loading ? 'Loading...' : '进入学院'}
          </button>
        </form>
      </div>
    </div>
  )
}
