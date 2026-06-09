import React from 'react'
import { useParams } from 'react-router-dom'
import { useFarm, useFarmStats } from '@/hooks/useFarms'

export default function FarmDetail() {
  const { id } = useParams()
  const { data: farm, isLoading } = useFarm(id as string)
  const { data: stats } = useFarmStats(id as string)

  if (isLoading) return <div className="p-6">Loading...</div>

  return (
    <div className="p-6">
      <h1 className="text-2xl font-semibold">{farm.name}</h1>
      <div className="mt-4 grid grid-cols-2 gap-4">
        <div className="p-4 bg-white rounded shadow">
          <div className="text-sm text-slate-500">Location</div>
          <div className="mt-1">{farm.location || '—'}</div>
        </div>
        <div className="p-4 bg-white rounded shadow">
          <div className="text-sm text-slate-500">Acreage</div>
          <div className="mt-1">{farm.acreage || '—'}</div>
        </div>
      </div>

      <div className="mt-6">
        <h2 className="text-lg font-medium">Stats</h2>
        <pre className="p-4 bg-white rounded mt-2">{JSON.stringify(stats, null, 2)}</pre>
      </div>
    </div>
  )
}
