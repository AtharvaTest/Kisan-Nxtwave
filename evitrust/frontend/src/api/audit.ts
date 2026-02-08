import { api } from './client'

export const timeline = (caseId: string) => api.get(`/cases/${caseId}/timeline`)
export const evidenceAudit = (id: string) => api.get(`/evidence/${id}/audit`)
