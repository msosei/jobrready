import { NextRequest } from 'next/server'

export async function POST(req: NextRequest) {
  try {
    const { jobId, userId } = await req.json()
    // Mock AI tailoring, replace with OpenAI call via server-side libs
    const data = {
      tailoredResume: { summary: 'Tailored summary...', skills: ['TS', 'React'] },
      tailoredCoverLetter: 'Dear Hiring Manager...'
    }
    return Response.json({ success: true, data }, { status: 200 })
  } catch (e: any) {
    return Response.json({ success: false, error: e?.message || 'Failed' }, { status: 500 })
  }
}


