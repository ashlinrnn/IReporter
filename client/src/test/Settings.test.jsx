import { render, screen, fireEvent } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import { describe, it, expect, beforeEach } from 'vitest'
import Settings from '../app/pages/Settings'

beforeEach(() => {
  localStorage.setItem('user', JSON.stringify({ username: 'TestUser', email: 'test@test.com' }))
})

const renderSettings = () => render(
  <BrowserRouter><Settings /></BrowserRouter>
)

describe('Settings Page', () => {
  it('renders settings heading', () => {
    renderSettings()
    expect(screen.getByText('SETTINGS')).toBeInTheDocument()
  })

  it('loads user data from localStorage', () => {
    renderSettings()
    expect(screen.getByDisplayValue('TestUser')).toBeInTheDocument()
    expect(screen.getByDisplayValue('test@test.com')).toBeInTheDocument()
  })

  it('updates username input', () => {
    renderSettings()
    const input = screen.getByDisplayValue('TestUser')
    fireEvent.change(input, { target: { value: 'NewUsername' } })
    expect(input.value).toBe('NewUsername')
  })

  it('has save changes button', () => {
    renderSettings()
    expect(screen.getByText('SAVE CHANGES')).toBeInTheDocument()
  })

  it('has theme toggle button', () => {
  renderSettings()
  const toggleBtn = 
    screen.queryByText('Switch to Light Mode') || 
    screen.queryByText('Switch to Dark Mode')
  expect(toggleBtn).toBeInTheDocument()
})
})