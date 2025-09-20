import Navbar from '@/components/Navbar'
import Footer from '@/components/Footer'
import ApplicationCard from '@/components/ApplicationCard'

export default function Applications() {
  const items = [
    { jobTitle: 'Frontend Engineer', company: 'Acme Corp', status: 'submitted', date: '2025-06-01' },
    { jobTitle: 'Backend Engineer', company: 'Globex', status: 'interview', date: '2025-06-03' },
  ]
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <main className="max-w-6xl mx-auto w-full p-4 flex-1">
        <h1 className="text-2xl font-semibold">Applications</h1>
        <div className="grid gap-3 mt-4">
          {items.map((i) => <ApplicationCard key={i.jobTitle} {...i} />)}
        </div>
      </main>
      <Footer />
    </div>
  )
}


