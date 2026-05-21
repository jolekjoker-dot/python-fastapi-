import { useState, useCallback } from 'react'
import { TopNav } from '../components/layout/TopNav'
import { TutorialPanel } from '../components/layout/TutorialPanel'
import { CodeEditor } from '../components/editor/CodeEditor'
import { OutputConsole } from '../components/output/OutputConsole'
import { executeCode } from '../api/execute'
import type { ExecutionResult } from '../types/code'

const DEFAULT_CODE = `# Welcome to Code Quest!
# Write your Python code here and press Run

print("Hello, Code Quest!")

name = "Mage"
print(f"Welcome, {name}!")

# Try some math:
result = sum(range(1, 11))
print(f"1+2+...+10 = {result}")
`

export function PlaygroundPage() {
  const [code, setCode] = useState(DEFAULT_CODE)
  const [result, setResult] = useState<ExecutionResult | null>(null)
  const [running, setRunning] = useState(false)

  const handleRun = useCallback(async () => {
    setRunning(true)
    setResult(null)
    try {
      const res = await executeCode(code)
      setResult(res)
    } catch (err) {
      setResult({
        stdout: '',
        stderr: err instanceof Error ? err.message : 'Execution failed',
        passed: false,
        execution_time: 0,
        error: err instanceof Error ? err.message : 'Unknown error',
      })
    } finally {
      setRunning(false)
    }
  }, [code])

  return (
    <div className="h-screen flex flex-col">
      <TopNav />
      <div className="flex-1 flex overflow-hidden">
        {/* Tutorial Panel (Left) */}
        <div className="w-72 shrink-0 border-r border-text-muted/20 bg-surface-panel/50 overflow-hidden">
          <TutorialPanel />
        </div>

        {/* Code Editor (Center) */}
        <div className="flex-1 min-w-0 overflow-hidden">
          <CodeEditor
            code={code}
            onChange={setCode}
            onRun={handleRun}
            running={running}
          />
        </div>

        {/* Output Console (Right) */}
        <div className="w-80 shrink-0 border-l border-text-muted/20 bg-surface-dark overflow-hidden">
          <OutputConsole result={result} />
        </div>
      </div>
    </div>
  )
}
