import React, { createContext, useContext, useEffect, useState } from 'react'
import * as authService from '@/services/auth'
import api from '@/services/api'
import { useNavigate } from 'react-router-dom'

type User = { id: string; email: string; full_name?: string }

type AuthContextValue = {
  user: User | null
  login: (email: string, password: string) => Promise<void>
  register: (payload: { full_name?: string; email: string; password: string }) => Promise<void>
  logout: () => void
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined)

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null)
  const navigate = useNavigate()

  useEffect(() => {
    (async () => {
      try {
        const res = await authService.me()
        setUser(res.data)
      } catch (e) {
        setUser(null)
      }
    })()
  }, [])

  async function login(email: string, password: string) {
    await authService.login(email, password)
    const res = await authService.me()
    setUser(res.data)
    navigate('/app')
  }

  async function register(payload: { full_name?: string; email: string; password: string }) {
    await authService.register(payload)
    // optionally auto-login
    await login(payload.email, payload.password)
  }

  function logout() {
    authService.logout()
    setUser(null)
    navigate('/login')
  }

  return <AuthContext.Provider value={{ user, login, register, logout }}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}
