import Navbar from '@/components/Navbar'
import Footer from '@/components/Footer'
import ResumeUploader from '@/components/ResumeUploader'

export default function Profiles() {
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <main className="max-w-6xl mx-auto w-full p-4 flex-1">
        <h1 className="text-2xl font-semibold">Profiles</h1>
        <p className="text-gray-600">Manage resume and profile settings</p>
        <div className="mt-4">
          <ResumeUploader />
        </div>
      </main>
      <Footer />
    </div>
  )
}


