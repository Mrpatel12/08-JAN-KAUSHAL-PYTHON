import React, { useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import Input from '@/components/ui/Input'
import Button from '@/components/ui/Button'
import Select from '@/components/ui/Select'
import { useFarms } from '@/hooks/useFarms'
import { useCrops } from '@/hooks/useCrops'
import { useCreateExpense, useExpense, useUpdateExpense } from '@/hooks/useExpenses'

export default function ExpenseForm() {
  const { id } = useParams()
  const navigate = useNavigate()
  const { data: farmsData } = useFarms()
  const farms = farmsData?.results || farmsData || []
  const { data: cropsData } = useCrops()
  const crops = cropsData?.results || cropsData || []

  const { data: existing } = useExpense(id as string)
  const create = useCreateExpense()
  const update = useUpdateExpense(id as string)

  const [form, setForm] = useState({ farm_id: '', crop: '', category: '', amount: '', occurred_at: '', notes: '' })

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    const payload = { ...form }
    try {
      if (id) await update.mutateAsync(payload)
      else await create.mutateAsync(payload)
      navigate('/app/expenses')
    } catch (err) {
      console.error(err)
    }
  }

  return (
    <div className="p-6 max-w-md">
      <h1 className="text-2xl font-semibold">{id ? 'Edit Expense' : 'New Expense'}</h1>
      <form className="mt-4" onSubmit={handleSubmit}>
        <label className="block text-sm">Farm</label>
        <Select value={form.farm_id} onChange={(e) => setForm({ ...form, farm_id: e.target.value })} className="mb-3">
          <option value="">Select farm</option>
          {farms.map((f: any) => <option key={f.id} value={f.id}>{f.name}</option>)}
        </Select>

        <label className="block text-sm">Crop (optional)</label>
        <Select value={form.crop} onChange={(e) => setForm({ ...form, crop: e.target.value })} className="mb-3">
          <option value="">None</option>
          {crops.map((c: any) => <option key={c.id} value={c.id}>{c.name}</option>)}
        </Select>

        <label className="block text-sm">Category</label>
        <Input value={form.category} onChange={(e) => setForm({ ...form, category: e.target.value })} className="mt-1 mb-3" />

        <label className="block text-sm">Amount</label>
        <Input type="number" value={form.amount} onChange={(e) => setForm({ ...form, amount: e.target.value })} className="mt-1 mb-3" />

        <label className="block text-sm">Occurred at</label>
        <Input type="datetime-local" value={form.occurred_at} onChange={(e) => setForm({ ...form, occurred_at: e.target.value })} className="mt-1 mb-3" />

        <label className="block text-sm">Notes</label>
        <Input value={form.notes} onChange={(e) => setForm({ ...form, notes: e.target.value })} className="mt-1 mb-4" />

        <div className="flex gap-2">
          <Button type="submit">Save</Button>
          <Button type="button" variant="ghost" onClick={() => navigate(-1)}>Cancel</Button>
        </div>
      </form>
    </div>
  )
}
