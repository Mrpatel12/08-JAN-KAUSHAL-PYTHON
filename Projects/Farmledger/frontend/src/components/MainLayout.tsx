import React from 'react'
import { Outlet } from 'react-router-dom'
import TopNav from './TopNav'
import Sidebar from './Sidebar'

export default function MainLayout() {
  return (
    <div className="min-h-screen flex bg-slate-50">
      <Sidebar />
      <div className="flex-1">
        <TopNav />
        <main className="p-6">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
