import { useEffect, useState, useCallback } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { getQuest, submitTask } from '../api/quests'
import type { QuestData, QuestTask, TaskSubmitResult } from '../types/quest'
import { TopNav } from '../components/layout/TopNav'
import { CodeEditor } from '../components/editor/CodeEditor'
import { ResizeHandle } from '../components/ui/ResizeHandle'
import { usePanelResize } from '../hooks/usePanelResize'
import ReactMarkdown from 'react-markdown'
import toast from 'react-hot-toast'
import { useUserStore } from '../stores/userStore'

export function QuestDetailPage() {
  const { questId } = useParams<{ questId: string }>()
  const navigate = useNavigate()
  const [quest, setQuest] = useState<QuestData | null>(null)
  const [loading, setLoading] = useState(true)
  const [activeIndex, setActiveIndex] = useState(0)
  const [code, setCode] = useState('')
  const [running, setRunning] = useState(false)
  const [result, setResult] = useState<TaskSubmitResult | null>(null)
  const [completedTasks, setCompletedTasks] = useState<Set<string>>(new Set())
  const { user } = useUserStore()

  const leftPanel = usePanelResize(320, 220, 560)
  const rightPanel = usePanelResize(320, 240, 500, true)

  // Load quest
  useEffect(() => {
    if (!questId) return
    getQuest(questId)
      .then((q) => {
        setQuest(q)
        const first = getActiveTask(q, 0)
        if (first) setCode(first.starter_code)
      })
      .finally(() => setLoading(false))
  }, [questId])

  // Get active task
  const getActiveTask = (q: QuestData, idx: number): QuestTask | null => {
    const allTasks = [...q.tasks, ...(q.challenge ? [q.challenge] : [])]
    return allTasks[idx] ?? null
  }

  const allTasks = quest
    ? [...quest.tasks, ...(quest.challenge ? [quest.challenge] : [])]
    : []

  const activeTask = quest ? getActiveTask(quest, activeIndex) : null

  // Switch task
  const switchTask = (idx: number) => {
    setActiveIndex(idx)
    setResult(null)
    if (!quest) return
    const task = getActiveTask(quest, idx)
    if (task) setCode(task.starter_code)
  }

  // Submit code
  const handleRun = useCallback(async () => {
    if (!quest || !activeTask) return
    setRunning(true)
    setResult(null)
    try {
      const res = await submitTask(quest.id, activeTask.id, code)
      setResult(res)

      if (res.passed) {
        const newCompleted = new Set(completedTasks)
        newCompleted.add(activeTask.id)
        setCompletedTasks(newCompleted)
        toast.success('通过！', { duration: 2000 })

        // Check if all tasks are done
        if (newCompleted.size >= allTasks.length) {
          toast.success(`通关！获得 ${quest.xp_reward} XP！`, { duration: 4000 })
          // Refresh user data after a moment
          setTimeout(() => {
            useUserStore.getState().restore()
          }, 1500)
        }
      }
    } catch (err) {
      toast.error(err instanceof Error ? err.message : '提交失败')
    } finally {
      setRunning(false)
    }
  }, [quest, activeTask, code, completedTasks, allTasks.length])

  // Get a hint
  const showHint = () => {
    if (!activeTask || activeTask.hints.length === 0) return
    const hint = activeTask.hints[Math.floor(Math.random() * activeTask.hints.length)]
    toast(hint, { icon: '💡', duration: 6000, style: { background: '#16213e', color: '#e2a03f' } })
  }

  if (loading) {
    return (
      <div className="h-screen flex flex-col">
        <TopNav />
        <div className="flex-1 flex items-center justify-center text-text-muted">
          Loading quest...
        </div>
      </div>
    )
  }

  if (!quest) {
    return (
      <div className="h-screen flex flex-col">
        <TopNav />
        <div className="flex-1 flex items-center justify-center text-text-muted">
          Quest not found
        </div>
      </div>
    )
  }

  const allCompleted = completedTasks.size >= allTasks.length

  return (
    <div className="h-screen flex flex-col">
      <TopNav />
      <div className="flex-1 flex overflow-hidden">
        {/* Left: Tutorial Panel */}
        <div
          className="shrink-0 border-r border-text-muted/20 bg-surface-panel/50 overflow-hidden flex flex-col"
          style={{ width: leftPanel.width }}
        >
          <div className="px-4 py-2 bg-surface-panel border-b border-text-muted/20 shrink-0 flex items-center justify-between">
            <button
              onClick={() => navigate('/map')}
              className="text-text-muted hover:text-gold transition-colors text-sm cursor-pointer"
            >
              ← Map
            </button>
            <span className="text-sm text-gold font-semibold">{quest.title}</span>
          </div>
          <div className="flex-1 overflow-auto p-4 text-sm leading-relaxed">
            {/* Story */}
            <div className="prose prose-invert prose-sm max-w-none mb-4 text-text-primary">
              <ReactMarkdown>{quest.story}</ReactMarkdown>
            </div>

            {/* Task navigation */}
            <div className="flex gap-1 mb-4 flex-wrap">
              {allTasks.map((task, i) => (
                <button
                  key={task.id}
                  onClick={() => switchTask(i)}
                  className={`px-2 py-1 rounded text-xs transition-all cursor-pointer ${
                    i === activeIndex
                      ? 'bg-gold text-surface-dark font-bold'
                      : completedTasks.has(task.id)
                        ? 'bg-success/20 text-success border border-success/40'
                        : 'bg-surface-dark text-text-muted border border-text-muted/30'
                  }`}
                >
                  {completedTasks.has(task.id) ? '✓' : ''}
                  {task.order === 99 ? '挑战' : `任务${task.order}`}
                </button>
              ))}
            </div>

            {/* Knowledge content (only show on first task) */}
            {activeIndex === 0 && (
              <div className="prose prose-invert prose-sm max-w-none mb-4 text-text-primary">
                <ReactMarkdown>{quest.content}</ReactMarkdown>
              </div>
            )}

            {/* Task description */}
            <div className="prose prose-invert prose-sm max-w-none text-text-primary">
              <ReactMarkdown>{activeTask?.description ?? ''}</ReactMarkdown>
            </div>

            {/* Hints */}
            {activeTask && activeTask.hints.length > 0 && (
              <button
                onClick={showHint}
                className="mt-4 px-4 py-2 rounded-lg bg-surface-dark border border-gold/40 text-gold hover:bg-gold/10 transition-all text-sm cursor-pointer w-full"
              >
                💡 获取提示
              </button>
            )}

            {/* Completion status */}
            {allCompleted && (
              <div className="mt-4 p-3 rounded-lg bg-success/10 border border-success/40 text-success text-center">
                全部任务完成！获得 {quest.xp_reward} XP + {quest.coin_reward} 金币
              </div>
            )}
          </div>
        </div>

        {/* Left ↔ Center resize handle */}
        <ResizeHandle onMouseDown={leftPanel.onMouseDown} dragging={leftPanel.dragging} />

        {/* Center: Code Editor */}
        <div className="flex-1 min-w-0 overflow-hidden">
          <CodeEditor
            code={code}
            onChange={setCode}
            onRun={handleRun}
            running={running}
          />
        </div>

        {/* Center ↔ Right resize handle */}
        <ResizeHandle onMouseDown={rightPanel.onMouseDown} dragging={rightPanel.dragging} />

        {/* Right: Test Results */}
        <div
          className="shrink-0 border-l border-text-muted/20 bg-surface-dark overflow-hidden flex flex-col"
          style={{ width: rightPanel.width }}
        >
          <div className="px-4 py-2 bg-surface-panel border-b border-text-muted/20 shrink-0">
            <span className="text-sm text-text-muted">Test Results</span>
          </div>
          <div className="flex-1 overflow-auto p-4">
            {!result ? (
              <p className="text-text-muted text-sm">点击 Run 提交代码</p>
            ) : (
              <div className="space-y-3">
                {/* Overall status */}
                <div
                  className={`p-3 rounded-lg text-sm font-semibold ${
                    result.passed
                      ? 'bg-success/10 text-success border border-success/30'
                      : 'bg-error/10 text-error border border-error/30'
                  }`}
                >
                  {result.passed ? 'PASS' : 'FAIL'} ({result.execution_time.toFixed(3)}s)
                </div>

                {/* Test cases */}
                {result.test_results.map((tc, i) => (
                  <div
                    key={i}
                    className={`p-3 rounded-lg text-xs ${
                      tc.passed
                        ? 'bg-success/5 border border-success/20'
                        : 'bg-error/5 border border-error/20'
                    }`}
                  >
                    <div className="flex items-center gap-1 mb-1">
                      <span className={tc.passed ? 'text-success' : 'text-error'}>
                        {tc.passed ? '✓' : '✗'}
                      </span>
                      <span className="text-text-muted">{tc.description}</span>
                    </div>
                    {!tc.passed && (
                      <>
                        <div className="text-text-muted mt-1">
                          Expected: <span className="text-success">{tc.expected}</span>
                        </div>
                        <div className="text-text-muted">
                          Got: <span className="text-error">{tc.actual || '(empty)'}</span>
                        </div>
                      </>
                    )}
                    {tc.error && (
                      <pre className="text-error whitespace-pre-wrap mt-1 text-xs">{tc.error}</pre>
                    )}
                  </div>
                ))}

                {/* Output */}
                {result.stdout && (
                  <div className="p-3 rounded-lg bg-editor-bg text-xs">
                    <div className="text-text-muted mb-1">Output:</div>
                    <pre className="text-success whitespace-pre-wrap">{result.stdout}</pre>
                  </div>
                )}
                {result.stderr && (
                  <div className="p-3 rounded-lg bg-editor-bg text-xs">
                    <div className="text-text-muted mb-1">Errors:</div>
                    <pre className="text-error whitespace-pre-wrap">{result.stderr}</pre>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
