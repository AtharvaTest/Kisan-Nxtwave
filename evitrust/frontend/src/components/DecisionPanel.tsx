import { useState } from 'react'

export default function DecisionPanel({ onSubmit }: { onSubmit: (decision: string, comment: string) => void }) {
  const [decision, setDecision] = useState('FLAG')
  const [comment, setComment] = useState('')
  return <div className='card'><h3>Decision</h3><select value={decision} onChange={e=>setDecision(e.target.value)}><option>ACCEPT</option><option>FLAG</option><option>REJECT</option></select><textarea placeholder='Mandatory comment' value={comment} onChange={e=>setComment(e.target.value)} /><button onClick={()=>onSubmit(decision, comment)}>Submit Decision</button></div>
}
