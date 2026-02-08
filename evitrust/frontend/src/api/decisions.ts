import { api } from './client'

export const decide = (id: string, payload: { decision: string; comment: string }) => api.post(`/evidence/${id}/decision`, payload)
export const getDecision = (id: string) => api.get(`/evidence/${id}/decision`)
