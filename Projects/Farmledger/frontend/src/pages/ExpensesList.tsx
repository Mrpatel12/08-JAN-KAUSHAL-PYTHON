import React from 'react'
import { Link } from 'react-router-dom'
import { useExpenses } from '@/hooks/useExpenses'
import Button from '@/components/ui/Button'
import Card from '@/components/ui/Card'

export default function ExpensesList() {
  const { data, isLoading } = useExpenses()
  const items = data?.results || data || []

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-semibold">Expenses</h1>
        <Link to="/app/expenses/new"><Button>New Expense</Button></Link>
      </div>
      <div className="grid gap-3">
        {isLoading && <div>Loading...</div>}
        {items.map((e: any) => (
          <Card key={e.id}>
            <div className="flex justify-between">
              <div>
                <div className="font-medium">{e.category || 'Expense'}</div>
                <div className="text-sm text-slate-600">{e.amount} {e.currency}</div>
              </div>
              <div className="text-sm">{new Date(e.occurred_at).toLocaleString()}</div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  )
}
