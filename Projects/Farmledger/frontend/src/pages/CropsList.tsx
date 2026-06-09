import React from 'react'
import { Link } from 'react-router-dom'
import { useCrops } from '@/hooks/useCrops'

export default function CropsList() {
  const { data, isLoading, isError } = useCrops()

  if (isLoading) return <div className="p-6">Loading crops...</div>
  if (isError) return <div className="p-6">Failed to load crops</div>

  const crops = data?.results || data || []

  return (
    <div className="p-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold">Crops</h1>
        <Link to="/app/crops/new" className="bg-slate-800 text-white px-3 py-1 rounded">New Crop</Link>
      </div>

      <div className="mt-4 grid grid-cols-1 gap-4">
        {crops.length === 0 && <div className="text-slate-500">No crops yet.</div>}
        {crops.map((c: any) => (
          <Link key={c.id} to={`/app/crops/${c.id}`} className="p-4 bg-white rounded shadow hover:shadow-md">
            <div className="text-lg font-medium">{c.name}</div>
            <div className="text-sm text-slate-500">{c.variety || '—'}</div>
          </Link>
        ))}
      </div>
    </div>
  )
}
