export interface UserResponse {
  id: number
  username: string
  xp: number
  level: number
  coins: number
  created_at: string
}

export interface TokenResponse {
  access_token: string
  token_type: string
  user: UserResponse
}
