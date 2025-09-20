import { NextRequest } from 'next/server'

export async function POST(req: NextRequest) {
  try {
    const { skills, experience, userId } = await req.json()
    const data = {
      title: 'E-Commerce Dashboard',
      description: 'A full-stack e-commerce dashboard...',
      techStack: ['React', 'Node.js', 'PostgreSQL'],
      githubUrl: `https://github.com/${userId}/ecommerce-dashboard`,
      demoUrl: 'https://ecommerce-dashboard.vercel.app'
    }
    return Response.json({ success: true, data })
  } catch (e: any) {
    return Response.json({ success: false, error: e?.message || 'Failed' }, { status: 500 })
  }
}


