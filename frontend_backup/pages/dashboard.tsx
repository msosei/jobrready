import Navbar from '@/components/Navbar'
import Footer from '@/components/Footer'
import AnalyticsChart from '@/components/AnalyticsChart'
import TailorApplication from '@/components/TailorApplication'
import InterviewPrep from '@/components/InterviewPrep'
import GapNarratives from '@/components/GapNarratives'
import PortfolioProjects from '@/components/PortfolioProjects'
import PersonalWebsite from '@/components/PersonalWebsite'
import BulkApply from '@/components/BulkApply'

export default function Dashboard() {
  const data = [
    { label: 'Mon', value: 2 },
    { label: 'Tue', value: 5 },
    { label: 'Wed', value: 4 },
    { label: 'Thu', value: 7 },
    { label: 'Fri', value: 3 },
    { label: 'Sat', value: 1 },
  ]
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <main className="max-w-6xl mx-auto w-full p-4 flex-1">
        <h1 className="text-2xl font-semibold">Dashboard</h1>
        <p className="text-gray-600">AI-powered job application tools</p>
        
        <div className="mt-6">
          <AnalyticsChart data={data} />
        </div>

        <div className="mt-8 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <TailorApplication />
          <InterviewPrep />
          <GapNarratives />
          <PortfolioProjects />
          <PersonalWebsite />
          <BulkApply />
        </div>
      </main>
      <Footer />
    </div>
  )
}


