import { apiFetch } from './client'

export interface Achievement {
  id: string
  name: string
  icon: string
  desc: string
  unlocked: boolean
  xp: number
}

export interface ShopItem {
  id: string
  name: string
  icon: string
  price: number
  desc: string
  owned?: boolean
}

export interface CheckinData {
  checkins: string[]
  streak: number
}

export function getAchievements(): Promise<Achievement[]> {
  return apiFetch('/game/achievements')
}

export function checkAchievements(): Promise<{ new_achievements: Achievement[] }> {
  return apiFetch('/game/check-achievements', { method: 'POST' })
}

export function doCheckin(): Promise<{ streak: number; already_checked: boolean }> {
  return apiFetch('/game/checkin', { method: 'POST' })
}

export function getCheckin(): Promise<CheckinData> {
  return apiFetch('/game/checkin')
}

export function getShopItems(): Promise<{ items: ShopItem[] }> {
  return apiFetch('/game/shop')
}

export function buyItem(itemId: string): Promise<{ ok: boolean; error?: string; coins?: number }> {
  return apiFetch(`/game/shop/buy/${itemId}`, { method: 'POST' })
}

export function getLeaderboard(): Promise<import('../types/user').UserResponse[]> {
  return apiFetch('/game/leaderboard')
}
