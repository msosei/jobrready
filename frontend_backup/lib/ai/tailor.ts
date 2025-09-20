import { AI } from '@/lib/ai'

export async function tailorToJob(params: { jobId: string; userId: string }) {
  return AI.tailorApplication(params)
}


