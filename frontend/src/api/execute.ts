import type { ExecutionResult } from '../types/code'
import { apiFetch } from './client'

export function executeCode(code: string): Promise<ExecutionResult> {
  return apiFetch<ExecutionResult>('/execute', {
    method: 'POST',
    body: JSON.stringify({ code }),
  })
}
