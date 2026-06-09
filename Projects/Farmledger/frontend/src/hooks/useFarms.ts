import { useQuery } from '@tanstack/react-query'
import api from '@/services/api'

export function useFarms() {
  return useQuery(['farms'], async () => {
    const res = await api.get('/farms/')
    return res.data
  })
}

export function useFarm(id: string) {
  return useQuery(['farm', id], async () => {
    const res = await api.get(`/farms/${id}/`)
    return res.data
  })
}

export function useFarmStats(id: string) {
  return useQuery(['farm', id, 'stats'], async () => {
    const res = await api.get(`/farms/${id}/stats/`)
    return res.data
  })
}
