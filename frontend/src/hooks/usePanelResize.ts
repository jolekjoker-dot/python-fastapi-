import { useState, useCallback, useEffect } from 'react'

export function usePanelResize(initial: number, min: number, max: number) {
  const [width, setWidth] = useState(initial)
  const [dragging, setDragging] = useState(false)

  const onMouseDown = useCallback((e: React.MouseEvent) => {
    e.preventDefault()
    setDragging(true)
  }, [])

  useEffect(() => {
    if (!dragging) return

    const onMouseMove = (e: MouseEvent) => {
      setWidth((prev) => {
        const next = prev + e.movementX
        return Math.max(min, Math.min(max, next))
      })
    }

    const onMouseUp = () => setDragging(false)

    window.addEventListener('mousemove', onMouseMove)
    window.addEventListener('mouseup', onMouseUp)
    return () => {
      window.removeEventListener('mousemove', onMouseMove)
      window.removeEventListener('mouseup', onMouseUp)
    }
  }, [dragging, min, max])

  return { width, dragging, onMouseDown }
}
