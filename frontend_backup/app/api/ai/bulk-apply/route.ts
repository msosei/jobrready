import { NextRequest } from 'next/server'

export async function POST(req: NextRequest) {
  try {
    const { userId, filters, settings } = await req.json()
    const data = {
      queueId: `bulk_${Date.now()}`,
      userId,
      filters,
      settings,
      status: 'pending',
      createdAt: new Date().toISOString()
    }
    return Response.json({ success: true, data })
  } catch (e: any) {
    return Response.json({ success: false, error: e?.message || 'Failed' }, { status: 500 })
  }
}


