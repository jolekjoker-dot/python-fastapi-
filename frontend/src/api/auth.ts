import type { TokenResponse, UserResponse } from '../types/user'
import { apiFetch } from './client'

export function login(username: string): Promise<TokenResponse> {
  return apiFetch<TokenResponse>('/auth/login', {
    method: 'POST',
    body: JSON.stringify({ username }),
  })
}

export function getMe(): Promise<UserResponse> {
  return apiFetch<UserResponse>('/auth/me')
}
