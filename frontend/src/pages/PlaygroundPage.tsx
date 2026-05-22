import { useState, useCallback } from 'react'
import { TopNav } from '../components/layout/TopNav'
import { TutorialPanel } from '../components/layout/TutorialPanel'
import { CodeEditor } from '../components/editor/CodeEditor'
import { OutputConsole } from '../components/output/OutputConsole'
import { ResizeHandle } from '../components/ui/ResizeHandle'
import { usePanelResize } from '../hooks/usePanelResize'
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

  const leftPanel = usePanelResize(288, 200, 500)
  const rightPanel = usePanelResize(320, 240, 500)

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
        <div
          className="shrink-0 border-r border-text-muted/20 bg-surface-panel/50 overflow-hidden"
          style={{ width: leftPanel.width }}
        >
          <TutorialPanel />
        </div>

        <ResizeHandle onMouseDown={leftPanel.onMouseDown} dragging={leftPanel.dragging} />

        {/* Code Editor (Center) */}
        <div className="flex-1 min-w-0 overflow-hidden">
          <CodeEditor
            code={code}
            onChange={setCode}
            onRun={handleRun}
            running={running}
          />
        </div>

        <ResizeHandle onMouseDown={rightPanel.onMouseDown} dragging={rightPanel.dragging} />

        {/* Output Console (Right) */}
        <div
          className="shrink-0 border-l border-text-muted/20 bg-surface-dark overflow-hidden"
          style={{ width: rightPanel.width }}
        >
          <OutputConsole result={result} />
        </div>
      </div>
    </div>
  )
}
