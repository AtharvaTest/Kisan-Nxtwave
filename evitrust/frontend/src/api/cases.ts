import { api } from './client'

export const listCases = () => api.get('/cases')
export const createCase = (payload: { title: string; description?: string }) => api.post('/cases', payload)
export const getCase = (id: string) => api.get(`/cases/${id}`)
export const getMerkle = (id: string) => api.get(`/cases/${id}/merkle`)
