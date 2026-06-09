import React from 'react'

type Props = React.SelectHTMLAttributes<HTMLSelectElement>

export default function Select(props: Props) {
  return (
    <select
      {...props}
      className={`w-full rounded border border-slate-200 px-3 py-2 ${props.className || ''}`}
      style={{ background: 'var(--surface)', color: 'var(--text)' }}
    />
  )
}
