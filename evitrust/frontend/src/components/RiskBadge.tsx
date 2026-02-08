export default function RiskBadge({ risk }: { risk?: string }) {
  if (!risk) return <span className='badge'>N/A</span>
  return <span className={`badge ${risk}`}>{risk}</span>
}
