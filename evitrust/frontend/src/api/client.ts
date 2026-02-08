import axios from 'axios'

const token = localStorage.getItem('evitrust_token')

export const api = axios.create({ baseURL: 'http://localhost:8000/api' })
if (token) api.defaults.headers.common.Authorization = `Bearer ${token}`

export const setToken = (t: string) => {
  localStorage.setItem('evitrust_token', t)
  api.defaults.headers.common.Authorization = `Bearer ${t}`
}

export const setUser = (u: any) => localStorage.setItem('evitrust_user', JSON.stringify(u))
export const getUser = () => {
  const raw = localStorage.getItem('evitrust_user')
  return raw ? JSON.parse(raw) : null
}
