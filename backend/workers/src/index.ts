import { Queue, Worker, QueueScheduler, JobsOptions } from 'bullmq'
import IORedis from 'ioredis'
import dotenv from 'dotenv'
import axios from 'axios'

dotenv.config()

const connection = new IORedis(process.env.REDIS_URL || 'redis://localhost:6379')

export const AUTO_APPLY_QUEUE = 'auto-apply'

const queue = new Queue(AUTO_APPLY_QUEUE, { connection })
new QueueScheduler(AUTO_APPLY_QUEUE, { connection })

new Worker(AUTO_APPLY_QUEUE, async (job) => {
  const { jobId, userId } = job.data as { jobId: string; userId: string }
  // Placeholder: call backend or external site automation
  await axios.post(`${process.env.API_URL || 'http://localhost:8000'}/applications/apply`, {
    job_id: jobId,
    user_id: userId,
  })
  return { applied: true }
}, { connection })

export async function enqueueAutoApply(jobId: string, userId: string, opts?: JobsOptions) {
  return queue.add('apply', { jobId, userId }, opts)
}

console.log('Worker started. Listening for jobs...')


