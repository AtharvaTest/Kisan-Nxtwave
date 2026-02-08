import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { createCase } from '../api/cases'

export default function CaseCreate() {
  const nav = useNavigate()
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  return <div className='card'><h2>Create Case</h2><input placeholder='Title' value={title} onChange={e=>setTitle(e.target.value)} /><textarea placeholder='Description' value={description} onChange={e=>setDescription(e.target.value)} /><button onClick={async ()=>{ const r = await createCase({ title, description }); nav(`/case/${r.data._id}`)}}>Create</button></div>
}
