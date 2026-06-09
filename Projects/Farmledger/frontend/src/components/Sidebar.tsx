import React from 'react'
import { NavLink } from 'react-router-dom'

export default function Sidebar() {
  return (
    <aside className="w-64 bg-white border-r min-h-screen">
      <div className="p-4 text-xl font-bold">FarmLedger</div>
      <nav className="p-4">
        <ul className="space-y-2">
          <li>
            <NavLink to="/app" className={({isActive}) => isActive ? 'font-semibold' : ''}>Dashboard</NavLink>
          </li>
          <li>
            <NavLink to="/app/farms" className={({isActive}) => isActive ? 'font-semibold' : ''}>Farms</NavLink>
          </li>
          <li>
            <NavLink to="/app/crops" className={({isActive}) => isActive ? 'font-semibold' : ''}>Crops</NavLink>
          </li>
        </ul>
      </nav>
    </aside>
  )
}
