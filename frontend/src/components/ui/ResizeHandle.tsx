interface ResizeHandleProps {
  onMouseDown: (e: React.MouseEvent) => void
  dragging: boolean
}

export function ResizeHandle({ onMouseDown, dragging }: ResizeHandleProps) {
  return (
    <div
      onMouseDown={onMouseDown}
      className={`w-1.5 shrink-0 cursor-col-resize transition-colors rounded-full my-4 ${
        dragging
          ? 'bg-gold'
          : 'bg-text-muted/20 hover:bg-gold/60'
      }`}
    />
  )
}
