import React from 'react'
import ThemeToggle from './ui/ThemeToggle'
import Input from './ui/Input'
import { serverLogout } from '@/services/auth'
import { useNavigate } from 'react-router-dom'

export default function TopNav() {
  const navigate = useNavigate()
  return (
    <header className="h-14 border-b bg-white flex items-center px-4">
      <div className="flex-1"> 
        <div style={{ width: 288 }}>
          <Input placeholder="Search farms, crops..." />
        </div>
      </div>
      <div className="ml-4 flex items-center gap-3">
        <ThemeToggle />
        <button className="text-sm text-slate-700" onClick={async () => { await serverLogout(); navigate('/login') }}>Sign out</button>
      </div>
    </header>
  )
}
