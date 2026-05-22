import { useEffect, useState } from 'react'
import { getAchievements, doCheckin, getCheckin, checkAchievements } from '../api/game'
import type { Achievement, CheckinData } from '../api/game'
import { TopNav } from '../components/layout/TopNav'
import { CheckinCalendar } from '../components/gamification/CheckinCalendar'

export function AchievementsPage() {
  const [achievements, setAchievements] = useState<Achievement[]>([])
  const [checkin, setCheckin] = useState<CheckinData | null>(null)
  const [streakMsg, setStreakMsg] = useState('')

  useEffect(() => {
    // Catch-up: check achievements based on existing progress
    checkAchievements().then(() => getAchievements().then(setAchievements))
    getCheckin().then(setCheckin)
  }, [])

  const handleCheckin = async () => {
    try {
      const res = await doCheckin()
      if (res.already_checked) {
        setStreakMsg(`今日已打卡！连续 ${res.streak} 天`)
      } else {
        setStreakMsg(`打卡成功！连续 ${res.streak} 天`)
        getCheckin().then(setCheckin)
      }
    } catch {
      setStreakMsg('打卡失败')
    }
  }

  const unlocked = achievements.filter((a) => a.unlocked).length

  return (
    <div className="h-screen flex flex-col">
      <TopNav />
      <div className="flex-1 overflow-auto p-8">
        <div className="max-w-3xl mx-auto">
          <div className="flex items-center justify-between mb-6">
            <h1 className="text-2xl font-bold text-gold">成就殿堂</h1>
            <span className="text-text-muted text-sm">
              {unlocked} / {achievements.length} 已解锁
            </span>
          </div>

          {/* Achievement grid */}
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-4 mb-8">
            {achievements.map((a) => (
              <div
                key={a.id}
                className={`p-4 rounded-xl text-center border transition-all ${
                  a.unlocked
                    ? 'border-gold/40 bg-gold/5 hover:bg-gold/10'
                    : 'border-text-muted/20 bg-surface-panel/30 opacity-50'
                }`}
              >
                <div className="text-3xl mb-1">{a.unlocked ? a.icon : '🔒'}</div>
                <div className="text-sm font-semibold text-text-primary">{a.name}</div>
                <div className="text-xs text-text-muted mt-1">{a.desc}</div>
                {a.unlocked && (
                  <div className="text-xs text-gold mt-1">+{a.xp} XP</div>
                )}
              </div>
            ))}
          </div>

          {/* Checkin section */}
          <div className="bg-surface-panel/50 rounded-xl p-6 border border-text-muted/20">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-bold text-gold">每日打卡</h2>
              <div className="flex items-center gap-3">
                {checkin && (
                  <span className="text-text-muted text-sm">
                    连续 {checkin.streak} 天
                  </span>
                )}
                <button
                  onClick={handleCheckin}
                  className="px-4 py-1.5 rounded-lg bg-gold text-surface-dark font-semibold text-sm hover:bg-gold/80 transition-all cursor-pointer"
                >
                  打卡
                </button>
              </div>
            </div>
            {streakMsg && (
              <div className="text-sm text-success mb-3">{streakMsg}</div>
            )}
            {checkin && <CheckinCalendar checkins={checkin.checkins} />}
          </div>
        </div>
      </div>
    </div>
  )
}
