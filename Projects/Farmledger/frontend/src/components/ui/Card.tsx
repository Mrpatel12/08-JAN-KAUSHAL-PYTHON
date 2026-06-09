import React from 'react'

export default function Card({ children, className = '' }: { children: React.ReactNode; className?: string }) {
  return (
    <div className={`${className} p-4 rounded shadow-sm surface`}>
      {children}
    </div>
  )
}
