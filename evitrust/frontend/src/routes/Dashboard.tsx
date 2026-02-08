import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { listCases } from '../api/cases'

export default function Dashboard() {
  const [cases, setCases] = useState<any[]>([])
  useEffect(() => { listCases().then(r => setCases(r.data)).catch(() => setCases([])) }, [])
  return <div className='card'><h2>Dashboard</h2><p>Total Cases: {cases.length}</p><ul>{cases.map(c => <li key={c._id}><Link to={`/case/${c._id}`}>{c.title}</Link> — {c.status}</li>)}</ul></div>
}
