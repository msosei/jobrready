import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { useState } from 'react'
import { AI } from '@/lib/ai'

export default function GapNarratives() {
  const [narrative, setNarrative] = useState<string | null>(null)
  const [generating, setGenerating] = useState(false)

  async function generateNarrative() {
    setGenerating(true)
    try {
      const { success, data } = await AI.gapNarrative({ gapStart: '2023-01-01', gapEnd: '2023-06-01', userId: 'user-123' })
      if (success) setNarrative(data?.narrative)
    } catch (e) {
      setNarrative('Error generating narrative')
    } finally {
      setGenerating(false)
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Fix My Job Gaps</CardTitle>
        <CardDescription>
          Generate professional narratives to explain employment gaps
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="text-sm font-medium">Gap Start</label>
              <input 
                type="date" 
                className="w-full p-2 border rounded mt-1"
                defaultValue="2023-01-01"
              />
            </div>
            <div>
              <label className="text-sm font-medium">Gap End</label>
              <input 
                type="date" 
                className="w-full p-2 border rounded mt-1"
                defaultValue="2023-06-01"
              />
            </div>
          </div>
          <Button onClick={generateNarrative} disabled={generating}>
            {generating ? 'Generating...' : 'Generate Narrative'}
          </Button>
          {narrative && (
            <div className="p-4 bg-gray-50 rounded">
              <p className="text-sm">{narrative}</p>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  )
}
