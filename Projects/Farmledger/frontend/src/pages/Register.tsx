import React, { useState } from 'react'
import Input from '@/components/ui/Input'
import Button from '@/components/ui/Button'
import { useAuth } from '@/hooks/useAuth'
import { useNavigate } from 'react-router-dom'

export default function Register() {
  const { register } = useAuth()
  const [fullName, setFullName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    await register({ full_name: fullName, email, password })
    // show brief confirmation then redirect to login
    navigate('/verify-email')
  }

  const navigate = useNavigate()

  return (
    <div className="h-screen flex items-center justify-center">
      <div className="w-full max-w-md p-6 bg-white rounded shadow">
        <h2 className="text-xl font-semibold mb-4">Create an account</h2>
        <form onSubmit={handleSubmit}>
          <label className="block text-sm">Full name</label>
          <Input value={fullName} onChange={(e) => setFullName(e.target.value)} className="mt-1 mb-3" />
          <label className="block text-sm">Email</label>
          <Input value={email} onChange={(e) => setEmail(e.target.value)} className="mt-1 mb-3" />
          <label className="block text-sm">Password</label>
          <Input type="password" value={password} onChange={(e) => setPassword(e.target.value)} className="mt-1 mb-4" />
          <Button type="submit" className="w-full">Register</Button>
        </form>
      </div>
    </div>
  )
}
