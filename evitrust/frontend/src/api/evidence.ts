import { api } from './client'

export const listEvidence = (caseId: string) => api.get(`/cases/${caseId}/evidence`)
export const getEvidence = (id: string) => api.get(`/evidence/${id}`)
export const verifyEvidence = (id: string) => api.get(`/evidence/${id}/verify`)
export const uploadEvidence = (caseId: string, form: FormData) => api.post(`/cases/${caseId}/evidence/upload`, form)
export const getDownload = (id: string) => api.get(`/evidence/${id}/download`)
