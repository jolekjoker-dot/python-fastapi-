import type { ExecutionResult } from '../../types/code'

interface OutputConsoleProps {
  result: ExecutionResult | null
}

export function OutputConsole({ result }: OutputConsoleProps) {
  if (!result) {
    return (
      <div className="flex flex-col h-full">
        <div className="px-4 py-2 bg-surface-panel border-b border-text-muted/20 shrink-0">
          <span className="text-sm text-text-muted">Console</span>
        </div>
        <div className="flex-1 flex items-center justify-center text-text-muted text-sm p-4">
          点击 Run 或按 Ctrl+Enter 运行代码
        </div>
      </div>
    )
  }

  const { stdout, stderr, passed, execution_time } = result

  return (
    <div className="flex flex-col h-full">
      <div className="flex items-center justify-between px-4 py-2 bg-surface-panel border-b border-text-muted/20 shrink-0">
        <span className="text-sm text-text-muted">Console</span>
        <div className="flex items-center gap-3 text-xs">
          <span className="text-text-muted">{execution_time.toFixed(3)}s</span>
          <span className={passed ? 'text-success' : 'text-error'}>
            {passed ? 'PASS' : 'FAIL'}
          </span>
        </div>
      </div>
      <div className="flex-1 overflow-auto p-4 font-mono text-sm">
        {stdout && (
          <pre className="text-success whitespace-pre-wrap m-0">{stdout}</pre>
        )}
        {stderr && (
          <pre className="text-error whitespace-pre-wrap m-0">{stderr}</pre>
        )}
        {!stdout && !stderr && (
          <span className="text-text-muted">(no output)</span>
        )}
      </div>
    </div>
  )
}
