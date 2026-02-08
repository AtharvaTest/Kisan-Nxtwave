export default function AuditLogTable({ events=[] }: {events?: any[]}) {
  return <div className='card'><table style={{width:'100%'}}><thead><tr><th>Time</th><th>Type</th><th>Hash</th></tr></thead><tbody>{events.map((e:any)=><tr key={e._id}><td>{e.created_at}</td><td>{e.event_type}</td><td>{(e.entry_hash||'').slice(0,18)}...</td></tr>)}</tbody></table></div>
}
