import React, { useEffect } from 'react'

type ToastProps = { id?: string; message: string; onClose?: () => void }

export default function Toast({ message, onClose }: ToastProps) {
  useEffect(() => {
    const t = setTimeout(() => onClose && onClose(), 4000)
    return () => clearTimeout(t)
  }, [onClose])

  return (
    <div className="fixed bottom-6 right-6 bg-slate-900 text-white px-4 py-2 rounded shadow">
      {message}
    </div>
  )
}
