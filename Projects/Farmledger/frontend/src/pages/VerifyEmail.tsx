import React, { useEffect, useState } from 'react'
import { useSearchParams, useNavigate } from 'react-router-dom'
import { verifyEmail } from '@/services/auth'

export default function VerifyEmail() {
  const [searchParams] = useSearchParams()
  const navigate = useNavigate()
  const uid = searchParams.get('uid') || ''
  const token = searchParams.get('token') || ''
  const [status, setStatus] = useState<'idle' | 'success' | 'error'>('idle')

  useEffect(() => {
    async function run() {
      try {
        await verifyEmail(uid, token)
        setStatus('success')
        setTimeout(() => navigate('/login'), 1500)
      } catch (err) {
        setStatus('error')
      }
    }
    if (uid && token) run()
  }, [uid, token])

  return (
    <div className="max-w-md mx-auto p-6">
      <h1 className="text-xl font-semibold">Email verification</h1>
      <div className="mt-4">
        {status === 'idle' && 'Verifying...'}
        {status === 'success' && 'Email verified — redirecting to login.'}
        {status === 'error' && 'Verification failed or link expired.'}
      </div>
    </div>
  )
}
