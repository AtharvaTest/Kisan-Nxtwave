export default function ExplanationCards({ explanations }: { explanations?: any }) {
  if (!explanations) return null
  return <div className='card'><h3>Explainability</h3><p>{explanations.summary}</p><ul>{(explanations.reasons || []).map((r: any, i: number) => <li key={i}><b>{r.title}</b>: {r.detail}</li>)}</ul></div>
}
