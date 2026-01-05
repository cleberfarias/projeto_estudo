// frontend/src/stores/auth.ts
import { defineStore } from 'pinia'
import { ref } from 'vue'

type User = { id: string; name: string; email: string; picture?: string; auth_provider?: string }

const STORAGE_KEY = 'app_auth'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(null)
  const user = ref<User | null>(null)

  function persist() {
    localStorage.setItem(STORAGE_KEY, JSON.stringify({ token: token.value, user: user.value }))
  }
  function load() {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (!raw) return
    try {
      const parsed = JSON.parse(raw)
      token.value = parsed.token
      user.value = parsed.user
    } catch { /* ignore */ }
  }
  function clear() {
    token.value = null
    user.value = null
    localStorage.removeItem(STORAGE_KEY)
  }

  async function login(baseUrl: string, email: string, password: string) {
    const res = await fetch(`${baseUrl}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    })
    if (!res.ok) {
      try {
        const err = await res.json()
        throw new Error(err.detail || err.message || 'Credenciais inválidas')
      } catch {
        throw new Error('Credenciais inválidas')
      }
    }
    const data = await res.json()
    token.value = data.access_token
    user.value = { 
      id: data.user.id,
      name: data.user.name, 
      email: data.user.email 
    }
    persist()
  }

  async function register(baseUrl: string, name: string, email: string, password: string) {
    const res = await fetch(`${baseUrl}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, email, password })
    })
    if (!res.ok) {
      try {
        const err = await res.json()
        throw new Error(err.detail || err.message || 'Falha ao registrar')
      } catch {
        throw new Error('Falha ao registrar')
      }
    }
    
    await login(baseUrl, email, password)
  }

  async function googleLogin(baseUrl: string, googleToken: string) {
    const res = await fetch(`${baseUrl}/auth/google`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ token: googleToken })
    })
    if (!res.ok) {
      // tenta extrair detalhe do backend para mensagens mais claras
      try {
        const err = await res.json()
        throw new Error(err.detail || err.message || `Falha na autenticação Google (status ${res.status})`)
      } catch (e: any) {
        throw new Error(e.message || 'Falha na autenticação Google')
      }
    }
    const data = await res.json()
    token.value = data.access_token
    user.value = { 
      id: data.user.id,
      name: data.user.name, 
      email: data.user.email,
      picture: data.user.picture,
      auth_provider: data.user.auth_provider
    }
    persist()
  }

  function logout() {
    clear()
  }

  // Verifica se o token está expirado
  function isTokenExpired(): boolean {
    const t = token.value
    if (!t) return true

    try {
      // Decodifica o payload do JWT (parte do meio)
      const raw = (t ?? '').split('.')[1]
      if (!raw) return true
      const payload = JSON.parse(atob(raw))
      const exp = payload.exp * 1000 // Converte para milliseconds
      const now = Date.now()

      // Token expira em menos de 1 minuto? Considera expirado
      return exp - now < 60000
    } catch {
      return true
    }
  }

  // Verifica se está autenticado com token válido
  function isAuthenticated(): boolean {
    return token.value !== null && !isTokenExpired()
  }

  return { token, user, login, register, googleLogin, logout, load, isTokenExpired, isAuthenticated }
})
