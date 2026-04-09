import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import { describe, it, expect, vi } from 'vitest'
import Login from '../app/pages/Login'

const renderLogin = () => render(
  <BrowserRouter><Login /></BrowserRouter>
)

describe('Login Page', () => {
  it('renders login form', () => {
    renderLogin()
    expect(screen.getByPlaceholderText('Email')).toBeInTheDocument()
    expect(screen.getByPlaceholderText('Password')).toBeInTheDocument()
    expect(screen.getByText('Sign In')).toBeInTheDocument()
  })

  it('shows error when email is empty', async () => {
    renderLogin()
    fireEvent.click(screen.getByText('Sign In'))
    await waitFor(() => {
      expect(screen.getByText('Email is required')).toBeInTheDocument()
    })
  })

  it('shows error for invalid email format', async () => {
    renderLogin()
    fireEvent.change(screen.getByPlaceholderText('Email'), { target: { value: 'notanemail' } })
    fireEvent.click(screen.getByText('Sign In'))
    await waitFor(() => {
      expect(screen.getByText('Enter a valid email')).toBeInTheDocument()
    })
  })

  it('shows error when password is empty', async () => {
    renderLogin()
    fireEvent.change(screen.getByPlaceholderText('Email'), { target: { value: 'test@test.com' } })
    fireEvent.click(screen.getByText('Sign In'))
    await waitFor(() => {
      expect(screen.getByText('Password is required')).toBeInTheDocument()
    })
  })

  it('shows error when password is too short', async () => {
    renderLogin()
    fireEvent.change(screen.getByPlaceholderText('Email'), { target: { value: 'test@test.com' } })
    fireEvent.change(screen.getByPlaceholderText('Password'), { target: { value: '123' } })
    fireEvent.click(screen.getByText('Sign In'))
    await waitFor(() => {
      expect(screen.getByText('Password must be at least 6 characters')).toBeInTheDocument()
    })
  })

  it('has link to signup page', () => {
    renderLogin()
    expect(screen.getByText('Create an Account')).toBeInTheDocument()
  })
})