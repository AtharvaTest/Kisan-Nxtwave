import { api } from './client'

export const login = (payload: { email: string; password: string }) => api.post('/auth/login', payload)
export const me = () => api.get('/auth/me')
