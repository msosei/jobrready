import Navbar from '@/components/Navbar'
import Footer from '@/components/Footer'
import JobCard from '@/components/JobCard'

export default function Discover() {
  const jobs = [
    { title: 'Frontend Engineer', company: 'Acme Corp', description: 'Work on Next.js apps...' },
    { title: 'Backend Engineer', company: 'Globex', description: 'Build FastAPI services...' },
  ]
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <main className="max-w-6xl mx-auto w-full p-4 flex-1">
        <h1 className="text-2xl font-semibold">Discover Jobs</h1>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
          {jobs.map((j) => <JobCard key={j.title} {...j} />)}
        </div>
      </main>
      <Footer />
    </div>
  )
}


