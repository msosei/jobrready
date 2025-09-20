type Props = {
  title: string
  company: string
  description: string
}

export default function JobCard({ title, company, description }: Props) {
  return (
    <div className="border rounded-md p-4 hover:shadow-sm transition">
      <h3 className="font-semibold">{title}</h3>
      <p className="text-sm text-gray-600">{company}</p>
      <p className="text-sm mt-2 line-clamp-3">{description}</p>
      <div className="mt-3 flex gap-2">
        <button className="px-3 py-1 bg-brand text-white rounded">Save</button>
        <button className="px-3 py-1 border rounded">Apply</button>
      </div>
    </div>
  )
}


