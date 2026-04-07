import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import { describe, it, expect } from 'vitest'
import SignUp from '../app/pages/SignUp'

const renderSignUp = () => render(
  <BrowserRouter><SignUp /></BrowserRouter>
)

describe('SignUp Page', () => {
  it('renders all form fields', () => {
    renderSignUp()
    expect(screen.getByPlaceholderText('Username')).toBeInTheDocument()
    expect(screen.getByPlaceholderText('Email')).toBeInTheDocument()
    expect(screen.getByPlaceholderText('Password')).toBeInTheDocument()
    expect(screen.getByPlaceholderText('Confirm Password')).toBeInTheDocument()
  })

  it('shows error when username is too short', async () => {
    renderSignUp()
    fireEvent.change(screen.getByPlaceholderText('Username'), { target: { value: 'ab' } })
    fireEvent.click(screen.getByText('Create Account'))
    await waitFor(() => {
      expect(screen.getByText('Username must be at least 3 characters')).toBeInTheDocument()
    })
  })

  it('shows error for invalid email', async () => {
    renderSignUp()
    fireEvent.change(screen.getByPlaceholderText('Username'), { target: { value: 'testuser' } })
    fireEvent.change(screen.getByPlaceholderText('Email'), { target: { value: 'bademail' } })
    fireEvent.click(screen.getByText('Create Account'))
    await waitFor(() => {
      expect(screen.getByText('Enter a valid email')).toBeInTheDocument()
    })
  })

  it('shows error when passwords do not match', async () => {
    renderSignUp()
    fireEvent.change(screen.getByPlaceholderText('Username'), { target: { value: 'testuser' } })
    fireEvent.change(screen.getByPlaceholderText('Email'), { target: { value: 'test@test.com' } })
    fireEvent.change(screen.getByPlaceholderText('Password'), { target: { value: 'password123' } })
    fireEvent.change(screen.getByPlaceholderText('Confirm Password'), { target: { value: 'different123' } })
    fireEvent.click(screen.getByText('Create Account'))
    await waitFor(() => {
      expect(screen.getByText('Passwords do not match')).toBeInTheDocument()
    })
  })

  it('has link to login page', () => {
    renderSignUp()
    expect(screen.getByText('Sign In')).toBeInTheDocument()
  })
})