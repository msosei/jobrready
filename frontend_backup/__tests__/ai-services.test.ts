import { createMocks } from 'node-mocks-http'
import { POST as tailorApplication } from '../app/api/ai/tailor-application/route'
import { POST as mockInterview } from '../app/api/ai/mock-interview/route'
import { POST as gapNarrative } from '../app/api/ai/gap-narrative/route'
import { POST as portfolioProject } from '../app/api/ai/portfolio-project/route'
import { POST as personalWebsite } from '../app/api/ai/personal-website/route'
import { POST as bulkApply } from '../app/api/ai/bulk-apply/route'

describe('AI Services API Routes', () => {
  describe('/api/ai/tailor-application', () => {
    it('should tailor application successfully', async () => {
      const res = await tailorApplication(new Request('http://test', { method: 'POST', body: JSON.stringify({ jobId: 'test-job-123', userId: 'test-user-123' }) }))
      expect(res.status).toBe(200)
      const json = await res.json()
      expect(json.success).toBe(true)
      expect(json.data).toHaveProperty('tailoredResume')
    })
  })

  describe('/api/ai/mock-interview', () => {
    it('should start mock interview session', async () => {
      const res = await mockInterview(new Request('http://test', { method: 'POST', body: JSON.stringify({ jobTitle: 'Software Engineer', difficulty: 'medium', userId: 'test-user-123' }) }))
      expect(res.status).toBe(200)
      const data = await res.json()
      expect(data.success).toBe(true)
      expect(data.data).toHaveProperty('sessionId')
    })
  })

  describe('/api/ai/gap-narrative', () => {
    it('should generate gap narrative', async () => {
      const res = await gapNarrative(new Request('http://test', { method: 'POST', body: JSON.stringify({ gapStart: '2023-01-01', gapEnd: '2023-06-01', userId: 'test-user-123' }) }))
      const data = await res.json()
      expect(data.success).toBe(true)
      expect(data.data).toHaveProperty('narrative')
    })
  })

  describe('/api/ai/portfolio-project', () => {
    it('should generate portfolio project', async () => {
      const res = await portfolioProject(new Request('http://test', { method: 'POST', body: JSON.stringify({ skills: ['React', 'Node.js'], experience: 'intermediate', userId: 'test-user-123' }) }))
      const data = await res.json()
      expect(data.success).toBe(true)
      expect(data.data).toHaveProperty('title')
    })
  })

  describe('/api/ai/personal-website', () => {
    it('should generate personal website', async () => {
      const res = await personalWebsite(new Request('http://test', { method: 'POST', body: JSON.stringify({ userId: 'test-user-123', template: 'developer', preferences: { colorScheme: 'blue' } }) }))
      const data = await res.json()
      expect(data.success).toBe(true)
      expect(data.data).toHaveProperty('vercelUrl')
    })
  })

  describe('/api/ai/bulk-apply', () => {
    it('should start bulk apply queue', async () => {
      const res = await bulkApply(new Request('http://test', { method: 'POST', body: JSON.stringify({ userId: 'test-user-123', filters: { keywords: ['engineer'] }, settings: { maxDaily: 10 } }) }))
      const data = await res.json()
      expect(data.success).toBe(true)
      expect(data.data).toHaveProperty('queueId')
    })
  })
})
