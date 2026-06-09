import React from 'react'
import { useParams, Link, useNavigate } from 'react-router-dom'
import { useCrop, useDeleteCrop } from '@/hooks/useCrops'

export default function CropDetail() {
  const { id } = useParams()
  const navigate = useNavigate()
  const { data: crop, isLoading } = useCrop(id as string)
  const del = useDeleteCrop()

  if (isLoading) return <div className="p-6">Loading...</div>

  async function handleDelete() {
    if (!confirm('Delete this crop?')) return
    await del.mutateAsync(id as string)
    navigate('/app/crops')
  }

  return (
    <div className="p-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold">{crop.name}</h1>
        <div className="flex gap-2">
          <Link to={`/app/crops/${id}/edit`} className="px-3 py-1 border rounded">Edit</Link>
          <button onClick={handleDelete} className="px-3 py-1 bg-red-600 text-white rounded">Delete</button>
        </div>
      </div>

      <div className="mt-4 grid grid-cols-2 gap-4">
        <div className="p-4 bg-white rounded shadow">
          <div className="text-sm text-slate-500">Variety</div>
          <div className="mt-1">{crop.variety || '—'}</div>
        </div>
        <div className="p-4 bg-white rounded shadow">
          <div className="text-sm text-slate-500">Status</div>
          <div className="mt-1">{crop.status}</div>
        </div>
      </div>
    </div>
  )
}
