import { NextRequest } from 'next/server'

export async function POST(req: NextRequest) {
  try {
    const { userId, template, preferences } = await req.json()
    const data = {
      id: `website_${Date.now()}`,
      userId,
      template,
      vercelUrl: `https://${userId}-portfolio.vercel.app`,
      status: 'deployed',
      deployedAt: new Date().toISOString()
    }
    return Response.json({ success: true, data })
  } catch (e: any) {
    return Response.json({ success: false, error: e?.message || 'Failed' }, { status: 500 })
  }
}


