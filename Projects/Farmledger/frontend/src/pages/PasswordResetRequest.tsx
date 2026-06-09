import React, { useState } from 'react'
import Input from '@/components/ui/Input'
import Button from '@/components/ui/Button'
import { requestPasswordReset } from '@/services/auth'

export default function PasswordResetRequest() {
  const [email, setEmail] = useState('')
  const [sent, setSent] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setError(null)
    try {
      await requestPasswordReset(email)
      setSent(true)
    } catch (err: any) {
      setError(err?.message || 'Failed to send reset email')
    }
  }

  return (
    <div className="max-w-md mx-auto p-6">
      <h1 className="text-xl font-semibold">Reset password</h1>
      {!sent ? (
        <form className="mt-4" onSubmit={handleSubmit}>
          <label className="block text-sm">Email</label>
          <Input value={email} onChange={(e) => setEmail(e.target.value)} className="mt-1 mb-4" />
          {error && <div className="text-red-600 mb-2">{error}</div>}
          <Button type="submit">Send reset link</Button>
        </form>
      ) : (
        <div className="mt-4">If the email exists, a reset link has been sent.</div>
      )}
    </div>
  )
}
