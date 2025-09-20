import type { NextApiRequest, NextApiResponse } from 'next'

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  try {
    if (req.method !== 'POST') return res.status(405).json({ success: false, error: 'Method not allowed' })
    const { provider, plan } = req.body as { provider: 'stripe' | 'paystack'; plan: 'free' | 'pro' | 'premium' }
    // Placeholder: call Stripe or Paystack SDKs
    return res.status(200).json({ success: true, data: { checkoutUrl: 'https://example.com/checkout' } })
  } catch (e: any) {
    return res.status(500).json({ success: false, error: e?.message || 'Payment error' })
  }
}


