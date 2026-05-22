export interface QuestSummary {
  id: string
  title: string
  phase: number
  order: number
  xp_reward: number
  completed: boolean
  unlocked: boolean
}

export interface TestCase {
  type: string
  expected: string
  input_data: string | null
  description: string
}

export interface QuestTask {
  id: string
  description: string
  starter_code: string
  test_cases: TestCase[]
  hints: string[]
  order: number
}

export interface QuestData {
  id: string
  title: string
  phase: number
  order: number
  story: string
  content: string
  tasks: QuestTask[]
  challenge: QuestTask | null
  xp_reward: number
  coin_reward: number
}

export interface TestResult {
  passed: boolean
  description: string
  expected: string
  actual: string
  error: string | null
}

export interface TaskSubmitResult {
  task_id: string
  passed: boolean
  test_results: TestResult[]
  execution_time: number
  stdout: string
  stderr: string
}
