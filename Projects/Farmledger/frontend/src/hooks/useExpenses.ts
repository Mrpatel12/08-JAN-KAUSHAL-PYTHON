import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import api from '@/services/api'

export function useExpenses() {
  return useQuery(['expenses'], async () => {
    const res = await api.get('/expenses/')
    return res.data
  })
}

export function useExpense(id: string) {
  return useQuery(['expense', id], async () => {
    const res = await api.get(`/expenses/${id}/`)
    return res.data
  })
}

export function useCreateExpense() {
  const qc = useQueryClient()
  return useMutation(async (payload: any) => {
    const res = await api.post('/expenses/', payload)
    return res.data
  }, { onSuccess: () => qc.invalidateQueries(['expenses']) })
}

export function useUpdateExpense(id: string) {
  const qc = useQueryClient()
  return useMutation(async (payload: any) => {
    const res = await api.patch(`/expenses/${id}/`, payload)
    return res.data
  }, { onSuccess: () => qc.invalidateQueries(['expenses', ['expense', id]]) })
}

export function useDeleteExpense() {
  const qc = useQueryClient()
  return useMutation(async (id: string) => {
    await api.delete(`/expenses/${id}/`)
  }, { onSuccess: () => qc.invalidateQueries(['expenses']) })
}
