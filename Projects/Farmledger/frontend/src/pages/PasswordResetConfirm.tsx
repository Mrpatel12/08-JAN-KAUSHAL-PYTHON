import React, { useState } from 'react'
import { useSearchParams, useNavigate } from 'react-router-dom'
import Input from '@/components/ui/Input'
import Button from '@/components/ui/Button'
import { confirmPasswordReset } from '@/services/auth'

export default function PasswordResetConfirm() {
  const [searchParams] = useSearchParams()
  const navigate = useNavigate()
  const uid = searchParams.get('uid') || ''
  const token = searchParams.get('token') || ''

  const [password, setPassword] = useState('')
  const [error, setError] = useState<string | null>(null)

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setError(null)
    try {
      await confirmPasswordReset(uid, token, password)
      navigate('/login')
    } catch (err: any) {
      setError(err?.message || 'Failed to reset password')
    }
  }

  return (
    <div className="max-w-md mx-auto p-6">
      <h1 className="text-xl font-semibold">Set a new password</h1>
      <form className="mt-4" onSubmit={handleSubmit}>
        <label className="block text-sm">New password</label>
        <Input value={password} onChange={(e) => setPassword(e.target.value)} type="password" className="mt-1 mb-4" />
        {error && <div className="text-red-600 mb-2">{error}</div>}
        <Button type="submit">Reset password</Button>
      </form>
    </div>
  )
}
