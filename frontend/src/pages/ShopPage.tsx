import { useEffect, useState } from 'react'
import { getShopItems, buyItem } from '../api/game'
import type { ShopItem } from '../api/game'
import { TopNav } from '../components/layout/TopNav'
import { useUserStore } from '../stores/userStore'
import toast from 'react-hot-toast'

export function ShopPage() {
  const [items, setItems] = useState<ShopItem[]>([])
  const { user, restore } = useUserStore()

  useEffect(() => {
    getShopItems().then((d) => setItems(d.items))
  }, [])

  const handleBuy = async (item: ShopItem) => {
    try {
      const res = await buyItem(item.id)
      if (res.ok) {
        toast.success(`购买成功！`)
        restore()
      } else {
        toast.error(res.error || '购买失败')
      }
    } catch {
      toast.error('购买失败')
    }
  }

  return (
    <div className="h-screen flex flex-col">
      <TopNav />
      <div className="flex-1 overflow-auto p-8">
        <div className="max-w-3xl mx-auto">
          <div className="flex items-center justify-between mb-6">
            <h1 className="text-2xl font-bold text-gold">魔法商店</h1>
            <span className="text-gold font-semibold">{user?.coins ?? 0} coins</span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {items.map((item) => {
              const canBuy = (user?.coins ?? 0) >= item.price
              return (
                <div
                  key={item.id}
                  className="p-5 rounded-xl bg-surface-panel/50 border border-text-muted/20 flex items-start gap-4"
                >
                  <span className="text-3xl">{item.icon}</span>
                  <div className="flex-1">
                    <div className="font-semibold text-text-primary">{item.name}</div>
                    <div className="text-xs text-text-muted mt-1">{item.desc}</div>
                    <div className="flex items-center justify-between mt-3">
                      <span className="text-gold font-bold text-sm">{item.price} coins</span>
                      <button
                        onClick={() => handleBuy(item)}
                        disabled={!canBuy}
                        className="px-3 py-1 rounded-lg bg-gold text-surface-dark font-semibold text-xs hover:bg-gold/80 disabled:opacity-40 disabled:cursor-not-allowed transition-all cursor-pointer"
                      >
                        {canBuy ? '购买' : '金币不足'}
                      </button>
                    </div>
                  </div>
                </div>
              )
            })}
          </div>
        </div>
      </div>
    </div>
  )
}
