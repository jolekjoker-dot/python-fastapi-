export function TutorialPanel() {
  return (
    <div className="flex flex-col h-full">
      <div className="px-4 py-2 bg-surface-panel border-b border-text-muted/20 shrink-0">
        <span className="text-sm text-text-muted">Tutorial</span>
      </div>
      <div className="flex-1 overflow-auto p-4 text-sm leading-relaxed">
        <h2 className="text-gold text-lg font-bold mb-3">Welcome to Code Quest!</h2>

        <p className="text-text-primary mb-4">
          This is the interactive Python learning playground. Soon, quests and
          challenges will appear here. For now, try writing some Python code!
        </p>

        <h3 className="text-success font-semibold mb-2">Try this:</h3>
        <pre className="bg-editor-bg rounded-lg p-3 text-sm text-text-primary font-mono mb-4">
{`name = input("What's your name? ")
print(f"Hello, {name}!")
print("Welcome to Code Quest!")`}
        </pre>

        <div className="border-t border-text-muted/20 pt-4 mt-4">
          <h3 className="text-gold font-semibold mb-2">Shortcuts</h3>
          <ul className="text-text-muted space-y-1">
            <li><code className="text-gold">Ctrl+Enter</code> — Run code</li>
            <li>The editor supports syntax highlighting and auto-complete</li>
          </ul>
        </div>

        <div className="border-t border-text-muted/20 pt-4 mt-4">
          <h3 className="text-text-muted mb-2">Coming Soon</h3>
          <ul className="text-text-muted space-y-1 text-xs">
            <li>25 quest levels (Python → FastAPI → Full-Stack)</li>
            <li>XP, achievements, and boss battles</li>
            <li>Quest map with progress tracking</li>
          </ul>
        </div>
      </div>
    </div>
  )
}
