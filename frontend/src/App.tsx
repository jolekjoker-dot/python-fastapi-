import { useEffect } from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import { useUserStore } from './stores/userStore'
import { LoginPage } from './pages/LoginPage'
import { PlaygroundPage } from './pages/PlaygroundPage'
import { QuestMapPage } from './pages/QuestMapPage'
import { QuestDetailPage } from './pages/QuestDetailPage'
import { AchievementsPage } from './pages/AchievementsPage'
import { ShopPage } from './pages/ShopPage'
import { LeaderboardPage } from './pages/LeaderboardPage'

export default function App() {
  const { user, restore, loading } = useUserStore()

  useEffect(() => {
    restore()
  }, [restore])

  if (loading) {
    return (
      <div className="h-screen flex items-center justify-center bg-surface-dark">
        <p className="text-text-muted text-lg">Loading...</p>
      </div>
    )
  }

  return (
    <BrowserRouter>
      <Toaster position="top-right" toastOptions={{ style: { background: '#16213e', color: '#e0e0e0' } }} />
      <Routes>
        <Route path="/" element={user ? <Navigate to="/map" /> : <LoginPage />} />
        <Route path="/map" element={user ? <QuestMapPage /> : <Navigate to="/" />} />
        <Route path="/quest/:questId" element={user ? <QuestDetailPage /> : <Navigate to="/" />} />
        <Route path="/playground" element={user ? <PlaygroundPage /> : <Navigate to="/" />} />
        <Route path="/achievements" element={user ? <AchievementsPage /> : <Navigate to="/" />} />
        <Route path="/shop" element={user ? <ShopPage /> : <Navigate to="/" />} />
        <Route path="/leaderboard" element={user ? <LeaderboardPage /> : <Navigate to="/" />} />
      </Routes>
    </BrowserRouter>
  )
}
