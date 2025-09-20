type Props = {
  data: { label: string; value: number }[]
}

export default function AnalyticsChart({ data }: Props) {
  const max = Math.max(1, ...data.map(d => d.value))
  return (
    <div className="grid grid-cols-6 gap-3 items-end h-40">
      {data.map((d) => (
        <div key={d.label} className="text-center">
          <div
            className="bg-brand/70 rounded-t"
            style={{ height: `${(d.value / max) * 100}%` }}
            title={`${d.label}: ${d.value}`}
          />
          <div className="text-xs mt-1">{d.label}</div>
        </div>
      ))}
    </div>
  )
}


