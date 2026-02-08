import { api } from './client'

export const report = (id: string) => api.get(`/evidence/${id}/report.pdf`)
