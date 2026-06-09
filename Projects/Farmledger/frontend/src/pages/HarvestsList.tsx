import React from 'react'
import { Link } from 'react-router-dom'
import { useHarvests } from '@/hooks/useHarvests'
import Button from '@/components/ui/Button'
import Card from '@/components/ui/Card'

export default function HarvestsList() {
  const { data, isLoading } = useHarvests()
  const items = data?.results || data || []

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-semibold">Harvests</h1>
        <Link to="/app/harvests/new"><Button>New Harvest</Button></Link>
      </div>
      <div className="grid gap-3">
        {isLoading && <div>Loading...</div>}
        {items.map((h: any) => (
          <Card key={h.id}>
            <div className="flex justify-between">
              <div>
                <div className="font-medium">{h.crop || 'Harvest'}</div>
                <div className="text-sm text-slate-600">{h.quantity} {h.unit}</div>
              </div>
              <div className="text-sm">{new Date(h.harvested_at).toLocaleString()}</div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  )
}
