type TailorPayload = { jobId: string; userId: string }
type MockInterviewPayload = { jobTitle: string; difficulty: string; userId: string }
type GapNarrativePayload = { gapStart: string; gapEnd: string; userId: string }
type PortfolioProjectPayload = { skills: string[]; experience: string; userId: string }
type PersonalWebsitePayload = { userId: string; template: string; preferences?: Record<string, any> }
type BulkApplyPayload = { userId: string; filters: any; settings: any }

async function postJson<T>(url: string, body: any): Promise<{ success: boolean; data?: T; error?: string }> {
  try {
    const res = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    })
    const json = await res.json()
    if (!res.ok) {
      return { success: false, error: json.error || 'Request failed' }
    }
    return { success: true, data: json }
  } catch (e: any) {
    return { success: false, error: e?.message || 'Network error' }
  }
}

export const AI = {
  tailorApplication: (payload: TailorPayload) => postJson<any>('/api/ai/tailor-application', payload),
  mockInterview: (payload: MockInterviewPayload) => postJson<any>('/api/ai/mock-interview', payload),
  gapNarrative: (payload: GapNarrativePayload) => postJson<any>('/api/ai/gap-narrative', payload),
  portfolioProject: (payload: PortfolioProjectPayload) => postJson<any>('/api/ai/portfolio-project', payload),
  personalWebsite: (payload: PersonalWebsitePayload) => postJson<any>('/api/ai/personal-website', payload),
  bulkApply: (payload: BulkApplyPayload) => postJson<any>('/api/ai/bulk-apply', payload),
}


