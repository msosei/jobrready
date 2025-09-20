import { NextRequest } from 'next/server'

export async function POST(req: NextRequest) {
  try {
    const { gapStart, gapEnd, userId } = await req.json()
    const data = {
      narrative: 'During this period, I focused on upskilling and personal growth...',
      gapStart,
      gapEnd,
      userId,
      generatedAt: new Date().toISOString(),
    }
    return Response.json({ success: true, data })
  } catch (e: any) {
    return Response.json({ success: false, error: e?.message || 'Failed' }, { status: 500 })
  }
}


