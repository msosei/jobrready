type Props = {
  jobTitle: string
  company: string
  status: string
  date: string
}

export default function ApplicationCard({ jobTitle, company, status, date }: Props) {
  return (
    <div className="border rounded-md p-4 flex items-center justify-between">
      <div>
        <h3 className="font-semibold">{jobTitle}</h3>
        <p className="text-sm text-gray-600">{company}</p>
      </div>
      <div className="text-right text-sm">
        <span className="px-2 py-1 rounded bg-gray-100">{status}</span>
        <div className="text-gray-500 mt-1">{date}</div>
      </div>
    </div>
  )
}


