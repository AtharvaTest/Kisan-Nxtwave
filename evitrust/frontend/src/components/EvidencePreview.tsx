export default function EvidencePreview({ evidence }: { evidence?: any }) {
  if (!evidence) return null
  return <div className='card'><h3>Evidence</h3><p>{evidence.filename_original} ({evidence.mime_type})</p><p>SHA256: {evidence.sha256}</p></div>
}
