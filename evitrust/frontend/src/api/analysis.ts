import { api } from './client'

export const analyze = (id: string) => api.post(`/evidence/${id}/analyze`)
export const latestAnalysis = (id: string) => api.get(`/evidence/${id}/analysis`)
