import React, { useState } from 'react'
import { useAuth } from '@/hooks/useAuth'
import Input from '@/components/ui/Input'
import Button from '@/components/ui/Button'
import { Link } from 'react-router-dom'

export default function Login() {
  const { login } = useAuth()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState<string | null>(null)

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setError(null)
    try {
      await login(email, password)
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Login failed')
    }
  }

  return (
    <div className="h-screen flex items-center justify-center">
      <div className="w-full max-w-md p-6 bg-white rounded shadow">
        <h2 className="text-xl font-semibold mb-4">Sign in to FarmLedger</h2>
        <form onSubmit={handleSubmit}>
          <label className="block text-sm">Email</label>
          <Input value={email} onChange={(e) => setEmail(e.target.value)} className="mt-1 mb-3" />
          <label className="block text-sm">Password</label>
          <Input value={password} onChange={(e) => setPassword(e.target.value)} type="password" className="mt-1 mb-4" />
          {error && <div className="text-red-600 mb-2">{error}</div>}
          <Button type="submit" className="w-full">Sign in</Button>
          <div className="text-sm mt-3 text-center">
            <Link to="/password-reset" className="text-blue-600">Forgot password?</Link>
          </div>
        </form>
      </div>
    </div>
  )
}
