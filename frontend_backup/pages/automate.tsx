import Navbar from '@/components/Navbar'
import Footer from '@/components/Footer'
import Link from 'next/link'

export default function Automate() {
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <main className="max-w-6xl mx-auto w-full p-4 flex-1">
        <h1 className="text-2xl font-semibold">Automate Applications</h1>
        <p className="text-gray-600">Install our Chrome extension and configure preferences</p>
        <div className="mt-4">
          <Link href="/chrome-extension" className="px-4 py-2 bg-brand text-white rounded">View Instructions</Link>
        </div>
      </main>
      <Footer />
    </div>
  )
}


