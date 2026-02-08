import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { getCase, getMerkle } from '../api/cases'
import { listEvidence } from '../api/evidence'
import { latestAnalysis } from '../api/analysis'
import { timeline } from '../api/audit'
import RiskBadge from '../components/RiskBadge'
import AuditLogTable from '../components/AuditLogTable'

export default function CaseView() {
  const { id = '' } = useParams()
  const [data, setData] = useState<any>()
  const [evidence, setEvidence] = useState<any[]>([])
  const [events, setEvents] = useState<any[]>([])
  const [merkle, setMerkle] = useState<any>()
  const [riskByEvidence, setRiskByEvidence] = useState<Record<string, string>>({})

  useEffect(() => {
    getCase(id).then(r => setData(r.data))
    listEvidence(id).then(async r => {
      setEvidence(r.data)
      const rows = await Promise.all(r.data.map((e: any) => latestAnalysis(e._id).then(x => [e._id, x.data.risk_level]).catch(() => [e._id, 'N/A'])))
      setRiskByEvidence(Object.fromEntries(rows))
    })
    timeline(id).then(r => setEvents(r.data))
    getMerkle(id).then(r => setMerkle(r.data))
  }, [id])

  return <div className='grid'>
    <div className='col-8 card'><h2>{data?.title}</h2><p>{data?.description}</p><p>Case Merkle Root: {merkle?.merkle_root || 'N/A'}</p><Link to={`/case/${id}/upload`}><button>Upload Evidence</button></Link><ul>{evidence.map(e => <li key={e._id}><Link to={`/evidence/${e._id}`}>{e.filename_original}</Link> - {e.type} - <RiskBadge risk={riskByEvidence[e._id]} /></li>)}</ul></div>
    <div className='col-4'><AuditLogTable events={events} /></div>
  </div>
}
