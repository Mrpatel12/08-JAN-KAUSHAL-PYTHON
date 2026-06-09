import api from './api'

type TokenResponse = { access: string; refresh: string }

export async function login(email: string, password: string) {
  const res = await api.post<TokenResponse>('/auth/login/', { email, password })
  const { access, refresh } = res.data
  localStorage.setItem('accessToken', access)
  localStorage.setItem('refreshToken', refresh)
  return res.data
}

export async function register(payload: { full_name?: string; email: string; password: string }) {
  return api.post('/auth/register/', payload)
}

export function logout() {
  localStorage.removeItem('accessToken')
  localStorage.removeItem('refreshToken')
}

export async function serverLogout() {
  const refresh = localStorage.getItem('refreshToken')
  if (!refresh) return
  try {
    await api.post('/auth/logout/', { refresh })
  } catch (err) {
    // ignore server errors on logout
  }
  logout()
}

export async function me() {
  return api.get('/auth/me/')
}

export async function verifyEmail(uid: string, token: string) {
  return api.get('/auth/verify-email/', { params: { uid, token } })
}

export async function requestPasswordReset(email: string) {
  return api.post('/auth/password-reset/', { email })
}

export async function confirmPasswordReset(uid: string, token: string, new_password: string) {
  return api.post('/auth/password-reset-confirm/', { uid, token, new_password })
}
