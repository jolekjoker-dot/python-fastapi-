import { useEffect } from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import { useUserStore } from './stores/userStore'
import { LoginPage } from './pages/LoginPage'
import { PlaygroundPage } from './pages/PlaygroundPage'

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
        <Route path="/" element={user ? <Navigate to="/playground" /> : <LoginPage />} />
        <Route path="/playground" element={user ? <PlaygroundPage /> : <Navigate to="/" />} />
      </Routes>
    </BrowserRouter>
  )
}
