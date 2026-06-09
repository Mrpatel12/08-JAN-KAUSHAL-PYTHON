import React from 'react'
import { Link } from 'react-router-dom'
import { useFarms } from '@/hooks/useFarms'
import Card from '@/components/ui/Card'

export default function Farms() {
  const { data, isLoading, isError } = useFarms()

  if (isLoading) return <div className="p-6">Loading...</div>
  if (isError) return <div className="p-6">Failed to load farms</div>

  const farms = data?.results || data || []

  return (
    <div className="p-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold">Farms</h1>
        <Link to="/app/farms/new" className="bg-slate-800 text-white px-3 py-1 rounded">New Farm</Link>
      </div>
      <div className="mt-4 grid grid-cols-1 gap-4">
        {farms.length === 0 && <div className="text-slate-500">No farms yet.</div>}
        {farms.map((f: any) => (
          <Link key={f.id} to={`/app/farms/${f.id}`}>
            <Card className="hover:shadow-md">
              <div className="text-lg font-medium">{f.name}</div>
              <div className="text-sm text-[var(--muted)]">{f.location || '—'}</div>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  )
}
