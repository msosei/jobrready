import { AI } from '@/lib/ai'

export async function generateCoverLetter(params: { userId: string; jobId: string }) {
  // Reuse existing cover-letter API if available; fallback to tailor
  const res = await AI.tailorApplication(params)
  if (res.success) {
    return { success: true as const, data: { coverLetter: res.data?.tailoredCoverLetter } }
  }
  return { success: false as const, error: res.error || 'Failed to generate cover letter' }
}


