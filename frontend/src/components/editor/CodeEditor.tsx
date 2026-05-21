import Editor, { type OnMount } from '@monaco-editor/react'
import type { editor } from 'monaco-editor'

interface CodeEditorProps {
  code: string
  onChange: (value: string) => void
  onRun: () => void
  running: boolean
}

export function CodeEditor({ code, onChange, onRun, running }: CodeEditorProps) {
  const handleMount: OnMount = (_editor, monaco) => {
    monaco.editor.defineTheme('code-quest', {
      base: 'vs-dark',
      inherit: true,
      rules: [
        { token: 'comment', foreground: '6A9955', fontStyle: 'italic' },
        { token: 'keyword', foreground: '569CD6' },
        { token: 'string', foreground: 'CE9178' },
        { token: 'number', foreground: 'B5CEA8' },
        { token: 'function', foreground: 'DCDCAA' },
      ],
      colors: {
        'editor.background': '#0d1117',
        'editor.foreground': '#e0e0e0',
        'editor.lineHighlightBackground': '#16213e',
        'editor.selectionBackground': '#264f78',
        'editorCursor.foreground': '#e2a03f',
        'editorLineNumber.foreground': '#484f58',
        'editorLineNumber.activeForeground': '#e2a03f',
      },
    })
    monaco.editor.setTheme('code-quest')
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
      e.preventDefault()
      onRun()
    }
  }

  return (
    <div className="flex flex-col h-full" onKeyDown={handleKeyDown}>
      <div className="flex items-center justify-between px-4 py-2 bg-surface-panel border-b border-text-muted/20 shrink-0">
        <span className="text-sm text-text-muted">main.py</span>
        <div className="flex items-center gap-2">
          <span className="text-xs text-text-muted">Ctrl+Enter Run</span>
          <button
            onClick={onRun}
            disabled={running}
            className="px-4 py-1 rounded bg-success text-surface-dark font-semibold text-sm hover:bg-success/80 disabled:opacity-50 transition-all cursor-pointer"
          >
            {running ? 'Running...' : 'Run'}
          </button>
        </div>
      </div>
      <div className="flex-1">
        <Editor
          height="100%"
          defaultLanguage="python"
          value={code}
          onChange={(v) => onChange(v ?? '')}
          theme="code-quest"
          onMount={handleMount}
          options={{
            fontSize: 14,
            fontFamily: "'Cascadia Code', 'Fira Code', 'Consolas', monospace",
            minimap: { enabled: false },
            scrollBeyondLastLine: false,
            lineNumbers: 'on',
            renderLineHighlight: 'line',
            bracketPairColorization: { enabled: true },
            automaticLayout: true,
            tabSize: 4,
            insertSpaces: true,
            padding: { top: 8 },
          }}
        />
      </div>
    </div>
  )
}
