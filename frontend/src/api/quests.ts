import type { QuestData, QuestSummary, TaskSubmitResult } from '../types/quest'
import { apiFetch } from './client'

export function listQuests(): Promise<QuestSummary[]> {
  return apiFetch<QuestSummary[]>('/quests')
}

export function getQuest(id: string): Promise<QuestData> {
  return apiFetch<QuestData>(`/quests/${id}`)
}

export function submitTask(
  questId: string,
  taskId: string,
  code: string,
): Promise<TaskSubmitResult> {
  return apiFetch<TaskSubmitResult>(`/quests/${questId}/submit`, {
    method: 'POST',
    body: JSON.stringify({ task_id: taskId, code }),
  })
}
