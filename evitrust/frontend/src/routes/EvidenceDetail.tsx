import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { getEvidence, verifyEvidence } from '../api/evidence'
import { latestAnalysis, analyze } from '../api/analysis'
import { getDecision, decide } from '../api/decisions'
import { report } from '../api/reports'
import { evidenceAudit } from '../api/audit'
import EvidencePreview from '../components/EvidencePreview'
import RiskBadge from '../components/RiskBadge'
import ExplanationCards from '../components/ExplanationCards'
import ConfidenceBar from '../components/ConfidenceBar'
import DecisionPanel from '../components/DecisionPanel'
import Timeline from '../components/Timeline'

export default function EvidenceDetail() {
  const { id = '' } = useParams()
  const [evidence, setEvidence] = useState<any>()
  const [analysis, setAnalysis] = useState<any>()
  const [verification, setVerification] = useState<any>()
  const [decision, setDecision] = useState<any>()
  const [events, setEvents] = useState<any[]>([])
  const [reportUrl, setReportUrl] = useState('')

  const load = () => {
    getEvidence(id).then(r => setEvidence(r.data))
    latestAnalysis(id).then(r => setAnalysis(r.data)).catch(()=>setAnalysis(null))
    verifyEvidence(id).then(r => setVerification(r.data)).catch(()=>setVerification(null))
    getDecision(id).then(r => setDecision(r.data)).catch(()=>setDecision(null))
    evidenceAudit(id).then(r => setEvents(r.data))
  }
  useEffect(load, [id])

  return <div className='grid'>
    <div className='col-8'>
      <EvidencePreview evidence={evidence} />
      <div className='card'><h3>Risk</h3><div><RiskBadge risk={analysis?.risk_level} /> Score: {analysis?.risk_score ?? 'N/A'}</div><button onClick={async ()=>{await analyze(id); load()}}>Run Analysis</button></div>
      <ConfidenceBar confidence={analysis?.confidence} uncertainty={analysis?.uncertainty} />
      <ExplanationCards explanations={analysis?.explanations} />
      <DecisionPanel onSubmit={async (d,c)=>{await decide(id,{decision:d,comment:c}); load()}} />
      {decision && <div className='card'><h3>Latest Decision</h3><p>{decision.decision}</p><p>{decision.comment}</p></div>}
    </div>
    <div className='col-4'>
      <div className='card'><h3>Verification</h3><p>Code: {verification?.verification_code || 'N/A'}</p><p>Merkle: {verification?.case_merkle_root || 'N/A'}</p><button onClick={async ()=>{const r=await report(id);setReportUrl(r.data.url)}}>Generate Report</button>{reportUrl && <a href={reportUrl} target='_blank'>Open report</a>}</div>
      <Timeline events={events} />
    </div>
  </div>
}
