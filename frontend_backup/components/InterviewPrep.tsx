import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { useState } from 'react'
import { AI } from '@/lib/ai'

export default function InterviewPrep() {
  const [session, setSession] = useState<any>(null)
  const [starting, setStarting] = useState(false)

  async function startSession() {
    setStarting(true)
    try {
      const { success, data } = await AI.mockInterview({ jobTitle: 'Software Engineer', difficulty: 'medium', userId: 'user-123' })
      if (success) setSession(data)
    } catch (e) {
      console.error('Failed to start interview session')
    } finally {
      setStarting(false)
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Interview Prep</CardTitle>
        <CardDescription>
          Practice with AI-powered mock interviews and get personalized feedback
        </CardDescription>
      </CardHeader>
      <CardContent>
        {!session ? (
          <Button onClick={startSession} disabled={starting}>
            {starting ? 'Starting...' : 'Start Mock Interview'}
          </Button>
        ) : (
          <div className="space-y-4">
            <p className="text-sm text-gray-600">
              Session ID: {session.sessionId}
            </p>
            <div className="p-4 bg-blue-50 rounded">
              <p className="font-medium">Question 1:</p>
              <p className="text-sm mt-1">{session.currentQuestion}</p>
            </div>
            <Button variant="outline">Answer Question</Button>
          </div>
        )}
      </CardContent>
    </Card>
  )
}
