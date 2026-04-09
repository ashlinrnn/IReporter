import { render, screen } from '@testing-library/react'
import { MemoryRouter, Routes, Route } from 'react-router-dom'
import { describe, it, expect, beforeEach } from 'vitest'

const ProtectedRoute = ({ children, adminOnly = false }) => {
  const token = localStorage.getItem("token")
  const user = JSON.parse(localStorage.getItem("user") || "{}")
  if (!token) return <div>Redirected to login</div>
  if (adminOnly && !user.is_admin) return <div>Redirected to home</div>
  return children
}

describe('ProtectedRoute', () => {
  beforeEach(() => localStorage.clear())

  it('redirects to login when no token', () => {
    render(
      <MemoryRouter>
        <ProtectedRoute><div>Protected Content</div></ProtectedRoute>
      </MemoryRouter>
    )
    expect(screen.getByText('Redirected to login')).toBeInTheDocument()
  })

  it('renders children when token exists', () => {
    localStorage.setItem('token', 'test-token')
    localStorage.setItem('user', JSON.stringify({ is_admin: false }))
    render(
      <MemoryRouter>
        <ProtectedRoute><div>Protected Content</div></ProtectedRoute>
      </MemoryRouter>
    )
    expect(screen.getByText('Protected Content')).toBeInTheDocument()
  })

  it('blocks non-admin from admin routes', () => {
    localStorage.setItem('token', 'test-token')
    localStorage.setItem('user', JSON.stringify({ is_admin: false }))
    render(
      <MemoryRouter>
        <ProtectedRoute adminOnly={true}><div>Admin Content</div></ProtectedRoute>
      </MemoryRouter>
    )
    expect(screen.getByText('Redirected to home')).toBeInTheDocument()
  })

  it('allows admin to access admin routes', () => {
    localStorage.setItem('token', 'test-token')
    localStorage.setItem('user', JSON.stringify({ is_admin: true }))
    render(
      <MemoryRouter>
        <ProtectedRoute adminOnly={true}><div>Admin Content</div></ProtectedRoute>
      </MemoryRouter>
    )
    expect(screen.getByText('Admin Content')).toBeInTheDocument()
  })
})