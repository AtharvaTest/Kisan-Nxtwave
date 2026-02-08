export default function FileDropzone({ onChange }: { onChange: (f: File | null) => void }) {
  return <input type='file' onChange={e => onChange(e.target.files?.[0] || null)} />
}
