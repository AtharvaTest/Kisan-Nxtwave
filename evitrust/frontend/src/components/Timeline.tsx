export default function Timeline({ events = [] }: { events?: any[] }) {
  return <div className='card'><h3>Audit Timeline</h3><ul>{events.map((e:any)=><li key={e._id}>{e.created_at} — {e.event_type}</li>)}</ul></div>
}
