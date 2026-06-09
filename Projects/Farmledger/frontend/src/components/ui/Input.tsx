import React from 'react'

type Props = React.InputHTMLAttributes<HTMLInputElement>

export default function Input(props: Props) {
  return (
    <input
      {...props}
      className={`w-full rounded border border-slate-200 px-3 py-2 focus:ring-2 focus:ring-[var(--accent)] ${props.className || ''}`}
      style={{ background: 'var(--surface)', color: 'var(--text)' }}
    />
  )
}
