import Link from 'next/link'

export default function Home() {
  return (
    <main className="min-h-screen grid place-items-center p-8">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-brand">MyBrand</h1>
        <p className="text-gray-600 mt-2">AI-powered job application platform</p>
        <div className="mt-6 flex gap-4 justify-center">
          <Link href="/dashboard" className="px-4 py-2 bg-brand text-white rounded-md">Go to Dashboard</Link>
          <Link href="/discover" className="px-4 py-2 border rounded-md">Discover Jobs</Link>
        </div>
      </div>
    </main>
  )
}


