import { useState } from 'react'
import { useParams } from 'react-router-dom'
import { uploadEvidence } from '../api/evidence'
import { getUser } from '../api/client'
import FileDropzone from '../components/FileDropzone'

export default function EvidenceUpload() {
  const { id = '' } = useParams()
  const user = getUser()
  const [file, setFile] = useState<File | null>(null)
  const [type, setType] = useState('IMAGE')
  const [msg, setMsg] = useState('')

  const submit = async () => {
    if (!file) return
    const form = new FormData()
    form.append('type', type)
    form.append('uploaded_by_name', user?.name || 'Unknown')
    form.append('uploaded_by_email', user?.email || 'unknown@local')
    form.append('file', file)
    const r = await uploadEvidence(id, form)
    setMsg(r.data.duplicate ? `Duplicate evidence: ${r.data.existing_evidence_id}` : `Uploaded: ${r.data._id}`)
  }

  return <div className='card'><h2>Upload Evidence</h2><select value={type} onChange={e=>setType(e.target.value)}><option>IMAGE</option><option>VIDEO</option><option>AUDIO</option></select><FileDropzone onChange={setFile}/><button onClick={submit}>Upload</button><p>{msg}</p></div>
}
