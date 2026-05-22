import { apiFetch } from './client'

export interface ExecutionRecord {
  id: number
  quest_id: string
  task_id: string
  code: string
  stdout: string
  stderr: string
  passed: boolean
  execution_time: number
  created_at: string
}

export interface CodeDraftResponse {
  quest_id: string
  task_id: string
  code: string
}

export function getHistory(questId?: string): Promise<ExecutionRecord[]> {
  const q = questId ? `?quest_id=${questId}` : ''
  return apiFetch(`/history${q}`)
}

export function getDraft(questId: string, taskId: string): Promise<CodeDraftResponse> {
  return apiFetch(`/drafts/${questId}/${taskId}`)
}

export function saveDraft(questId: string, taskId: string, code: string): Promise<{ ok: boolean }> {
  return apiFetch('/drafts', {
    method: 'POST',
    body: JSON.stringify({ quest_id: questId, task_id: taskId, code }),
  })
}

export function getPreferences(): Promise<Record<string, string>> {
  return apiFetch('/preferences')
}

export function savePreference(key: string, value: string): Promise<{ ok: boolean }> {
  return apiFetch('/preferences', {
    method: 'POST',
    body: JSON.stringify({ key, value }),
  })
}
