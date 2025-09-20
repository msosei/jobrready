import { NextRequest } from 'next/server'

export async function POST(req: NextRequest) {
  try {
    const { jobTitle, difficulty, userId } = await req.json()
    const data = {
      sessionId: `session_${Date.now()}`,
      jobTitle,
      difficulty,
      userId,
      currentQuestion: 'Tell me about yourself',
      totalQuestions: 5,
      createdAt: new Date().toISOString()
    }
    return Response.json({ success: true, data })
  } catch (e: any) {
    return Response.json({ success: false, error: e?.message || 'Failed' }, { status: 500 })
  }
}


