import Navbar from '@/components/Navbar'
import Footer from '@/components/Footer'

export default function Billing() {
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <main className="max-w-6xl mx-auto w-full p-4 flex-1">
        <h1 className="text-2xl font-semibold">Billing</h1>
        <p className="text-gray-600">Manage your subscription</p>
        <div className="mt-4 flex gap-4">
          <button className="px-4 py-2 bg-brand text-white rounded">Subscribe Pro</button>
          <button className="px-4 py-2 border rounded">Manage</button>
        </div>
      </main>
      <Footer />
    </div>
  )
}


