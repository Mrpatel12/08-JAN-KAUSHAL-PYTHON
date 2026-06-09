import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import api from '@/services/api'

export function useCrops() {
  return useQuery(['crops'], async () => {
    const res = await api.get('/crops/')
    return res.data
  })
}

export function useCrop(id: string) {
  return useQuery(['crop', id], async () => {
    const res = await api.get(`/crops/${id}/`)
    return res.data
  })
}

export function useCreateCrop() {
  const qc = useQueryClient()
  return useMutation(
    async (payload: any) => {
      const res = await api.post('/crops/', payload)
      return res.data
    },
    { onSuccess: () => qc.invalidateQueries(['crops']) }
  )
}

export function useUpdateCrop(id: string) {
  const qc = useQueryClient()
  return useMutation(
    async (payload: any) => {
      const res = await api.patch(`/crops/${id}/`, payload)
      return res.data
    },
    { onSuccess: () => qc.invalidateQueries(['crops', ['crop', id]]) }
  )
}

export function useDeleteCrop() {
  const qc = useQueryClient()
  return useMutation(
    async (id: string) => {
      await api.delete(`/crops/${id}/`)
    },
    { onSuccess: () => qc.invalidateQueries(['crops']) }
  )
}
