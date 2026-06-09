import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import Login from './pages/Login'
import Register from './pages/Register'
import PasswordResetRequest from './pages/PasswordResetRequest'
import PasswordResetConfirm from './pages/PasswordResetConfirm'
import VerifyEmail from './pages/VerifyEmail'
import MainLayout from './components/MainLayout'
import Farms from './pages/Farms'
import FarmDetail from './pages/FarmDetail'
import CropsList from './pages/CropsList'
import CropForm from './pages/CropForm'
import CropDetail from './pages/CropDetail'
import RequireAuth from './components/RequireAuth'
import ExpensesList from './pages/ExpensesList'
import ExpenseForm from './pages/ExpenseForm'
import HarvestsList from './pages/HarvestsList'
import HarvestForm from './pages/HarvestForm'

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/password-reset" element={<PasswordResetRequest />} />
      <Route path="/password-reset/confirm" element={<PasswordResetConfirm />} />
      <Route path="/verify-email" element={<VerifyEmail />} />
      <Route path="/app" element={<RequireAuth><MainLayout /></RequireAuth>}> 
        <Route index element={<Dashboard />} />
        <Route path="farms" element={<Farms />} />
        <Route path="farms/:id" element={<FarmDetail />} />
        <Route path="crops" element={<CropsList />} />
        <Route path="crops/new" element={<CropForm />} />
        <Route path="crops/:id" element={<CropDetail />} />
        <Route path="crops/:id/edit" element={<CropForm />} />
        <Route path="expenses" element={<ExpensesList />} />
        <Route path="expenses/new" element={<ExpenseForm />} />
        <Route path="expenses/:id" element={<ExpenseForm />} />
        <Route path="harvests" element={<HarvestsList />} />
        <Route path="harvests/new" element={<HarvestForm />} />
        <Route path="harvests/:id" element={<HarvestForm />} />
      </Route>
      <Route path="/" element={<Navigate to="/app" replace />} />
    </Routes>
  )
}
