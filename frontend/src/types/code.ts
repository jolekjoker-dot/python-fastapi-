export interface ExecutionResult {
  stdout: string
  stderr: string
  passed: boolean
  execution_time: number
  error: string | null
}
