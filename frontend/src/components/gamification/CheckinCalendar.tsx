interface CheckinCalendarProps {
  checkins: string[]
}

export function CheckinCalendar({ checkins }: CheckinCalendarProps) {
  const checkinSet = new Set(checkins)
  const today = new Date()
  const days: { date: Date; checked: boolean; future: boolean }[] = []

  // Show last 84 days (12 weeks)
  for (let i = 83; i >= 0; i--) {
    const d = new Date(today)
    d.setDate(d.getDate() - i)
    const ds = d.toISOString().slice(0, 10)
    days.push({
      date: d,
      checked: checkinSet.has(ds),
      future: d > today,
    })
  }

  // Group by week
  const weeks: typeof days[] = []
  for (let i = 0; i < days.length; i += 7) {
    weeks.push(days.slice(i, i + 7))
  }

  const getColor = (checked: boolean, future: boolean) => {
    if (future) return 'bg-surface-panel/30'
    if (checked) return 'bg-success'
    return 'bg-text-muted/15'
  }

  return (
    <div className="flex gap-1">
      {weeks.map((week, wi) => (
        <div key={wi} className="flex flex-col gap-1">
          {week.map((day, di) => (
            <div
              key={di}
              className={`w-3.5 h-3.5 rounded-sm ${getColor(day.checked, day.future)}`}
              title={day.date.toISOString().slice(0, 10)}
            />
          ))}
        </div>
      ))}
    </div>
  )
}
