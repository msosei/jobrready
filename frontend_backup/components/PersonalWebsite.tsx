import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { useState } from 'react'
import { AI } from '@/lib/ai'

export default function PersonalWebsite() {
  const [website, setWebsite] = useState<any>(null)
  const [generating, setGenerating] = useState(false)

  async function generateWebsite() {
    setGenerating(true)
    try {
      const { success, data } = await AI.personalWebsite({ userId: 'user-123', template: 'developer', preferences: { colorScheme: 'blue', layout: 'modern' } })
      if (success) setWebsite(data)
    } catch (e) {
      console.error('Failed to generate website')
    } finally {
      setGenerating(false)
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Personal Website Generator</CardTitle>
        <CardDescription>
          Auto-generate and deploy your personal portfolio website
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          <Button onClick={generateWebsite} disabled={generating}>
            {generating ? 'Generating...' : 'Generate Website'}
          </Button>
          {website && (
            <div className="p-4 bg-gray-50 rounded">
              <p className="text-sm font-medium">Website Generated!</p>
              <p className="text-sm text-gray-600 mt-1">
                URL: {website.vercelUrl || 'https://your-site.vercel.app'}
              </p>
              <Button variant="outline" size="sm" className="mt-2">
                View Website
              </Button>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  )
}
