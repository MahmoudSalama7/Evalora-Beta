import { create } from 'zustand'
import type { User, UserRole } from '../types'

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, role: UserRole) => Promise<User>;
  signup: (name: string, email: string, role: UserRole, company?: string) => Promise<User>;
  logout: () => void;
  initialize: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  token: null,
  isAuthenticated: false,
  isLoading: true,

  initialize: () => {
    const token = localStorage.getItem('evalora_auth_token');
    const userJson = localStorage.getItem('evalora_auth_user');
    
    if (token && userJson) {
      try {
        const user = JSON.parse(userJson);
        set({ user, token, isAuthenticated: true, isLoading: false });
        return;
      } catch {
        // Clear corrupt data
        localStorage.removeItem('evalora_auth_token');
        localStorage.removeItem('evalora_auth_user');
      }
    }
    set({ user: null, token: null, isAuthenticated: false, isLoading: false });
  },

  login: async (email, role) => {
    set({ isLoading: true });
    // Simulate API delay
    await new Promise((resolve) => setTimeout(resolve, 800));

    const name = email.split('@')[0];
    const formattedName = name.charAt(0).toUpperCase() + name.slice(1);
    
    const mockUser: User = {
      id: `user-${Date.now()}`,
      email,
      name: formattedName,
      role,
      company: role === 'hr' ? 'Acme Corp' : undefined,
      avatarUrl: `https://api.dicebear.com/7.x/initials/svg?seed=${formattedName}`
    };

    localStorage.setItem('evalora_auth_token', 'mock-jwt-token-123456');
    localStorage.setItem('evalora_auth_user', JSON.stringify(mockUser));

    set({ user: mockUser, token: 'mock-jwt-token-123456', isAuthenticated: true, isLoading: false });
    return mockUser;
  },

  signup: async (name, email, role, company) => {
    set({ isLoading: true });
    await new Promise((resolve) => setTimeout(resolve, 1000));

    const mockUser: User = {
      id: `user-${Date.now()}`,
      email,
      name,
      role,
      company: role === 'hr' ? (company || 'Acme Corp') : undefined,
      avatarUrl: `https://api.dicebear.com/7.x/initials/svg?seed=${name}`
    };

    localStorage.setItem('evalora_auth_token', 'mock-jwt-token-123456');
    localStorage.setItem('evalora_auth_user', JSON.stringify(mockUser));

    set({ user: mockUser, token: 'mock-jwt-token-123456', isAuthenticated: true, isLoading: false });
    return mockUser;
  },

  logout: () => {
    localStorage.removeItem('evalora_auth_token');
    localStorage.removeItem('evalora_auth_user');
    set({ user: null, token: null, isAuthenticated: false });
  }
}));
