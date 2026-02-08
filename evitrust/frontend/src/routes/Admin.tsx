import { useState } from 'react'
import { search } from '../api/admin'

export default function Admin() {
  const [risk, setRisk] = useState('')
  const [type, setType] = useState('')
  const [status, setStatus] = useState('')
  const [rows, setRows] = useState<any[]>([])
  return <div className='card'><h2>Admin Search</h2><div className='grid'><div className='col-4'><input placeholder='Risk' value={risk} onChange={e=>setRisk(e.target.value)} /></div><div className='col-4'><input placeholder='Type' value={type} onChange={e=>setType(e.target.value)} /></div><div className='col-4'><input placeholder='Status' value={status} onChange={e=>setStatus(e.target.value)} /></div></div><button onClick={async ()=> setRows((await search(risk,type,status)).data)}>Search</button><ul>{rows.map(r => <li key={r._id}>{r.filename_original} - {r.status}</li>)}</ul></div>
}
