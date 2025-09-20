export async function sendEmail(to: string, subject: string, body: string) {
  // Placeholder email sender; integrate with Postmark/Sendgrid
  console.log('Email ->', { to, subject })
  return { success: true }
}

export async function notifyJobStatus(userId: string, payload: { jobId: string; status: string }) {
  // Lookup user email via Supabase if needed
  return sendEmail('user@example.com', `Job ${payload.status}`, `Your application ${payload.jobId} is ${payload.status}`)
}


