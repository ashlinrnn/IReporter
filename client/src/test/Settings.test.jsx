import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { vi } from 'vitest';
import Settings from '../pages/Settings';
import { api } from '../utils/api';

// Mock the entire api module
vi.mock('../utils/api', () => ({
  api: {
    me: vi.fn(),
    updateUser: vi.fn(),
    uploadProfilePic: vi.fn(),
  },
}));

// Helper to render Settings with mocked API
const renderSettings = () => {
  render(<Settings />);
};

describe('Settings Page', () => {
  beforeEach(() => {
    // Reset mocks before each test
    vi.clearAllMocks();
    // Clear localStorage
    localStorage.clear();
  });

  it('renders settings heading after loading', async () => {
    // Mock successful API response
    api.me.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        user: {
          id: 1,
          username: 'TestUser',
          email: 'test@test.com',
          phone_number: '+254712345678',
          profile_pic_url: null,
        },
      }),
    });

    renderSettings();

    // Wait for loading to finish and heading to appear
    await waitFor(() => {
      expect(screen.getByText('SETTINGS')).toBeInTheDocument();
    });
  });

  it('loads user data from API', async () => {
    api.me.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        user: {
          id: 1,
          username: 'TestUser',
          email: 'test@test.com',
          phone_number: '+254712345678',
          profile_pic_url: null,
        },
      }),
    });

    renderSettings();

    await waitFor(() => {
      expect(screen.getByDisplayValue('TestUser')).toBeInTheDocument();
      expect(screen.getByDisplayValue('test@test.com')).toBeInTheDocument();
      expect(screen.getByDisplayValue('+254712345678')).toBeInTheDocument();
    });
  });

  it('updates username input', async () => {
    api.me.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        user: {
          id: 1,
          username: 'TestUser',
          email: 'test@test.com',
          phone_number: '+254712345678',
          profile_pic_url: null,
        },
      }),
    });

    renderSettings();

    await waitFor(() => {
      expect(screen.getByDisplayValue('TestUser')).toBeInTheDocument();
    });

    const input = screen.getByDisplayValue('TestUser');
    fireEvent.change(input, { target: { value: 'NewUsername' } });
    expect(input.value).toBe('NewUsername');
  });

  it('has save changes button', async () => {
    api.me.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        user: {
          id: 1,
          username: 'TestUser',
          email: 'test@test.com',
          phone_number: '+254712345678',
          profile_pic_url: null,
        },
      }),
    });

    renderSettings();

    await waitFor(() => {
      expect(screen.getByText('SAVE CHANGES')).toBeInTheDocument();
    });
  });

  it('has theme toggle button', async () => {
    api.me.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        user: {
          id: 1,
          username: 'TestUser',
          email: 'test@test.com',
          phone_number: '+254712345678',
          profile_pic_url: null,
        },
      }),
    });

    renderSettings();

    await waitFor(() => {
      const toggleBtn = screen.getByText(/Switch to (Light|Dark) Mode/i);
      expect(toggleBtn).toBeInTheDocument();
    });
  });
});