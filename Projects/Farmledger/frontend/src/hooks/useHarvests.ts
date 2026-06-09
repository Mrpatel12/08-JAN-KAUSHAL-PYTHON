import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import api from '@/services/api'

export function useHarvests() {
  return useQuery(['harvests'], async () => {
    const res = await api.get('/harvests/')
    return res.data
  })
}

export function useHarvest(id: string) {
  return useQuery(['harvest', id], async () => {
    const res = await api.get(`/harvests/${id}/`)
    return res.data
  })
}

export function useCreateHarvest() {
  const qc = useQueryClient()
  return useMutation(async (payload: any) => {
    const res = await api.post('/harvests/', payload)
    return res.data
  }, { onSuccess: () => qc.invalidateQueries(['harvests']) })
}

export function useUpdateHarvest(id: string) {
  const qc = useQueryClient()
  return useMutation(async (payload: any) => {
    const res = await api.patch(`/harvests/${id}/`, payload)
    return res.data
  }, { onSuccess: () => qc.invalidateQueries(['harvests', ['harvest', id]]) })
}

export function useDeleteHarvest() {
  const qc = useQueryClient()
  return useMutation(async (id: string) => {
    await api.delete(`/harvests/${id}/`)
  }, { onSuccess: () => qc.invalidateQueries(['harvests']) })
}
