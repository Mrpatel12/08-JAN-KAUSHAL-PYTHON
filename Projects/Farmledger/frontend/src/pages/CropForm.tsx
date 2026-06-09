import React, { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { useFarms } from '@/hooks/useFarms'
import { useCreateCrop, useCrop, useUpdateCrop } from '@/hooks/useCrops'
import Input from '@/components/ui/Input'
import Button from '@/components/ui/Button'
import Select from '@/components/ui/Select'

export default function CropForm() {
  const { id } = useParams()
  const navigate = useNavigate()
  const { data: farmsData } = useFarms()
  const farms = farmsData?.results || farmsData || []

  const { data: existing } = useCrop(id as string)
  const create = useCreateCrop()
  const update = useUpdateCrop(id as string)

  const [form, setForm] = useState({ farm_id: '', name: '', variety: '', planted_at: '', expected_harvest_at: '', area_planted: '' })

  useEffect(() => {
    if (existing) {
      setForm({
        farm_id: existing.farm,
        name: existing.name || '',
        variety: existing.variety || '',
        planted_at: existing.planted_at || '',
        expected_harvest_at: existing.expected_harvest_at || '',
        area_planted: existing.area_planted || '',
      })
    }
  }, [existing])

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    const payload = {
      farm_id: form.farm_id,
      name: form.name,
      variety: form.variety,
      planted_at: form.planted_at || null,
      expected_harvest_at: form.expected_harvest_at || null,
      area_planted: form.area_planted || null,
    }

    try {
      if (id) {
        await update.mutateAsync(payload)
      } else {
        await create.mutateAsync(payload)
      }
      navigate('/app/crops')
    } catch (err) {
      console.error(err)
    }
  }

  return (
    <div className="p-6">
      <h1 className="text-2xl font-semibold">{id ? 'Edit Crop' : 'New Crop'}</h1>
      <form className="mt-4 max-w-md" onSubmit={handleSubmit}>
        <label className="block text-sm">Farm</label>
        <Select value={form.farm_id} onChange={(e) => setForm({ ...form, farm_id: e.target.value })} className="mb-3">
          <option value="">Select farm</option>
          {farms.map((f: any) => (
            <option value={f.id} key={f.id}>{f.name}</option>
          ))}
        </Select>

        <label className="block text-sm">Name</label>
        <Input className="mt-1 mb-3" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} required />

        <label className="block text-sm">Variety</label>
        <Input className="mt-1 mb-3" value={form.variety} onChange={(e) => setForm({ ...form, variety: e.target.value })} />

        <label className="block text-sm">Planted at</label>
        <Input type="date" className="mt-1 mb-3" value={form.planted_at} onChange={(e) => setForm({ ...form, planted_at: e.target.value })} />

        <label className="block text-sm">Expected harvest</label>
        <Input type="date" className="mt-1 mb-3" value={form.expected_harvest_at} onChange={(e) => setForm({ ...form, expected_harvest_at: e.target.value })} />

        <label className="block text-sm">Area planted</label>
        <Input type="number" step="0.01" className="mt-1 mb-4" value={form.area_planted} onChange={(e) => setForm({ ...form, area_planted: e.target.value })} />

        <div className="flex gap-2">
          <Button className="bg-slate-800 text-white">Save</Button>
          <Button type="button" onClick={() => navigate(-1)} variant="ghost">Cancel</Button>
        </div>
      </form>
    </div>
  )
}
