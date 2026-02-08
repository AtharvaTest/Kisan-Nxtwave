import { api } from './client'

export const search = (risk = '', type = '', status = '') => api.get(`/admin/search?risk=${risk}&type=${type}&status=${status}`)
