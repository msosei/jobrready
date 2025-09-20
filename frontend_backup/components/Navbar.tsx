import Link from 'next/link'

export default function Navbar() {
  return (
    <nav className="w-full border-b bg-white">
      <div className="max-w-6xl mx-auto px-4 h-14 flex items-center justify-between">
        <Link href="/" className="text-brand font-semibold">MyBrand</Link>
        <div className="flex gap-4 text-sm">
          <Link href="/dashboard">Dashboard</Link>
          <Link href="/discover">Discover</Link>
          <Link href="/profiles">Profiles</Link>
          <Link href="/applications">Applications</Link>
          <Link href="/billing">Billing</Link>
          <Link href="/automate">Automate</Link>
        </div>
      </div>
    </nav>
  )
}


