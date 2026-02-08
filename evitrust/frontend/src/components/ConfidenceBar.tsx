export default function ConfidenceBar({ confidence = 0, uncertainty = 0 }: { confidence?: number; uncertainty?: number }) {
  return <div className='card'><div>Confidence: {(confidence * 100).toFixed(0)}%</div><div>Uncertainty: {(uncertainty * 100).toFixed(0)}%</div></div>
}
