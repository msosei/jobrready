import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { useState } from 'react'
import { AI } from '@/lib/ai'

export default function BulkApply() {
  const [queue, setQueue] = useState<any>(null)
  const [starting, setStarting] = useState(false)

  async function startBulkApply() {
    setStarting(true)
    try {
      const { success, data } = await AI.bulkApply({
        userId: 'user-123',
        filters: { keywords: ['software engineer', 'developer'], location: 'remote', experience: '2-5 years' },
        settings: { maxDaily: 10, pauseBetween: 30 }
      })
      if (success) setQueue(data)
    } catch (e) {
      console.error('Failed to start bulk apply')
    } finally {
      setStarting(false)
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Bulk Apply Orchestrator</CardTitle>
        <CardDescription>
          Queue-based bulk job applications with ethical guardrails
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="text-sm font-medium">Keywords</label>
              <input 
                type="text" 
                className="w-full p-2 border rounded mt-1"
                placeholder="software engineer, developer"
              />
            </div>
            <div>
              <label className="text-sm font-medium">Location</label>
              <input 
                type="text" 
                className="w-full p-2 border rounded mt-1"
                placeholder="remote, new york"
              />
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="text-sm font-medium">Max Daily</label>
              <input 
                type="number" 
                className="w-full p-2 border rounded mt-1"
                defaultValue={10}
              />
            </div>
            <div>
              <label className="text-sm font-medium">Pause (seconds)</label>
              <input 
                type="number" 
                className="w-full p-2 border rounded mt-1"
                defaultValue={30}
              />
            </div>
          </div>
          <Button onClick={startBulkApply} disabled={starting}>
            {starting ? 'Starting...' : 'Start Bulk Apply'}
          </Button>
          {queue && (
            <div className="p-4 bg-gray-50 rounded">
              <p className="text-sm font-medium">Bulk Apply Started</p>
              <p className="text-sm text-gray-600 mt-1">
                Queue ID: {queue.queueId}
              </p>
              <p className="text-sm text-gray-600">
                Status: {queue.status}
              </p>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  )
}
