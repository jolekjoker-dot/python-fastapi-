import { create } from 'zustand'
import type { UserResponse } from '../types/user'
import { login as apiLogin, getMe } from '../api/auth'

interface UserState {
  user: UserResponse | null
  token: string | null
  loading: boolean
  login: (username: string) => Promise<void>
  restore: () => Promise<void>
  logout: () => void
}

const hasToken = !!localStorage.getItem('token')

export const useUserStore = create<UserState>((set) => ({
  user: null,
  token: localStorage.getItem('token'),
  loading: hasToken,

  login: async (username: string) => {
    set({ loading: true })
    const res = await apiLogin(username)
    localStorage.setItem('token', res.access_token)
    set({ user: res.user, token: res.access_token, loading: false })
  },

  restore: async () => {
    const token = localStorage.getItem('token')
    if (!token) {
      set({ loading: false })
      return
    }
    try {
      const user = await getMe()
      set({ user, token, loading: false })
    } catch {
      localStorage.removeItem('token')
      set({ user: null, token: null, loading: false })
    }
  },

  logout: () => {
    localStorage.removeItem('token')
    set({ user: null, token: null })
  },
}))
