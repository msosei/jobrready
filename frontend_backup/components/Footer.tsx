export default function Footer() {
  return (
    <footer className="w-full border-t bg-white mt-12">
      <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between text-sm text-gray-500">
        <span>© {new Date().getFullYear()} MyBrand</span>
        <span>Built with ❤️ for job seekers</span>
      </div>
    </footer>
  )
}


