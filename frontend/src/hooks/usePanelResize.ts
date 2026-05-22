import { useState, useCallback, useEffect, useRef } from 'react'

export function usePanelResize(
  initialRatio: number,
  minRatio: number,
  maxRatio: number,
  windowWidth: number,
  reverse = false,
) {
  const [ratio, setRatio] = useState(initialRatio)
  const [dragging, setDragging] = useState(false)
  const prevWindowWidth = useRef(windowWidth)
  const sign = reverse ? -1 : 1

  // Recalculate width when window resizes (keep the same ratio)
  useEffect(() => {
    if (!dragging && prevWindowWidth.current !== windowWidth && prevWindowWidth.current > 0) {
      const scale = windowWidth / prevWindowWidth.current
      setRatio((prev) => Math.max(minRatio, Math.min(maxRatio, prev * scale)))
    }
    prevWindowWidth.current = windowWidth
  }, [windowWidth, dragging, minRatio, maxRatio])

  const onMouseDown = useCallback((e: React.MouseEvent) => {
    e.preventDefault()
    setDragging(true)
  }, [])

  useEffect(() => {
    if (!dragging) return

    const onMouseMove = (e: MouseEvent) => {
      setRatio((prev) => {
        const delta = (e.movementX * sign) / windowWidth
        return Math.max(minRatio, Math.min(maxRatio, prev + delta))
      })
    }

    const onMouseUp = () => setDragging(false)

    window.addEventListener('mousemove', onMouseMove)
    window.addEventListener('mouseup', onMouseUp)
    return () => {
      window.removeEventListener('mousemove', onMouseMove)
      window.removeEventListener('mouseup', onMouseUp)
    }
  }, [dragging, windowWidth, minRatio, maxRatio, sign])

  const width = Math.floor(ratio * windowWidth)

  return { width, dragging, onMouseDown }
}
