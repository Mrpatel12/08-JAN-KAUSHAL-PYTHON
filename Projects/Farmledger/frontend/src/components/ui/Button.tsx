import React from 'react'

type Props = React.ButtonHTMLAttributes<HTMLButtonElement> & { variant?: 'primary' | 'ghost' }

export default function Button({ variant = 'primary', className = '', ...props }: Props) {
  const base = 'px-4 py-2 rounded shadow-sm '
  const styles = variant === 'primary' ? 'bg-slate-800 text-white' : 'bg-transparent text-slate-800'
  return <button className={base + styles + ' ' + className} {...props} />
}
