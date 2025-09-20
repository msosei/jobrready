import { useRef, useState } from 'react'

export default function ResumeUploader() {
  const inputRef = useRef<HTMLInputElement | null>(null)
  const [uploading, setUploading] = useState(false)
  const [message, setMessage] = useState<string | null>(null)

  async function handleUpload(file: File) {
    setUploading(true)
    setMessage(null)
    try {
      const form = new FormData()
      form.append('file', file)
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000'}/resume/upload`, {
        method: 'POST',
        body: form,
      })
      if (!res.ok) throw new Error('Upload failed')
      setMessage('Resume uploaded and parsed successfully!')
    } catch (e: any) {
      setMessage(e.message || 'Upload failed')
    } finally {
      setUploading(false)
    }
  }

  return (
    <div>
      <input
        type="file"
        accept=".pdf,.doc,.docx"
        ref={inputRef}
        className="hidden"
        onChange={(e) => {
          const f = e.target.files?.[0]
          if (f) handleUpload(f)
        }}
      />
      <button
        onClick={() => inputRef.current?.click()}
        className="px-4 py-2 bg-brand text-white rounded"
        disabled={uploading}
      >
        {uploading ? 'Uploading...' : 'Upload Resume'}
      </button>
      {message && <p className="text-sm mt-2">{message}</p>}
    </div>
  )
}


