import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { useState } from 'react'
import { tailorToJob } from '@/lib/ai/tailor'

export default function TailorApplication() {
  const [tailoring, setTailoring] = useState(false)
  const [result, setResult] = useState<string | null>(null)

  async function handleTailor() {
    setTailoring(true)
    try {
      const { success, data, error } = await tailorToJob({ jobId: 'sample-job-123', userId: 'user-123' })
      if (!success) throw new Error(error || 'Tailor failed')
      setResult(data?.tailoredResume ? JSON.stringify(data.tailoredResume, null, 2) : 'Tailoring completed')
    } catch (e) {
      setResult('Error tailoring application')
    } finally {
      setTailoring(false)
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Tailor My Application</CardTitle>
        <CardDescription>
          AI-powered resume and cover letter tailoring for specific job descriptions
        </CardDescription>
      </CardHeader>
      <CardContent>
        <Button onClick={handleTailor} disabled={tailoring}>
          {tailoring ? 'Tailoring...' : 'Tailor Application'}
        </Button>
        {result && (
          <div className="mt-4 p-4 bg-gray-50 rounded">
            <pre className="text-sm">{result}</pre>
          </div>
        )}
      </CardContent>
    </Card>
  )
}
