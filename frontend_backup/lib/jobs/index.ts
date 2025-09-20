export type JobListing = {
  id: string
  title: string
  company: string
  location?: string
  source: 'indeed' | 'glassdoor' | 'jobberman' | 'internal'
  url?: string
}

export async function searchJobs(query: { q: string; location?: string }) {
  // Placeholder scraper integration; replace with server-side fetchers
  const items: JobListing[] = [
    { id: '1', title: 'Frontend Engineer', company: 'Acme', source: 'indeed', url: '#' },
    { id: '2', title: 'Backend Engineer', company: 'Globex', source: 'glassdoor', url: '#' },
  ]
  return items
}


