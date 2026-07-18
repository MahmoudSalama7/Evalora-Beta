import { create } from 'zustand'

interface ThemeState {
  theme: 'light' | 'dark';
  toggleTheme: () => void;
  initializeTheme: () => void;
}

export const useThemeStore = create<ThemeState>((set, get) => ({
  theme: 'dark', // default to premium dark mode
  initializeTheme: () => {
    const savedTheme = localStorage.getItem('evalora_theme') as 'light' | 'dark' | null;
    const theme = savedTheme || 'dark';
    
    // Apply theme classes to standard document element
    const root = window.document.documentElement;
    root.classList.remove('light', 'dark');
    root.classList.add(theme);
    
    set({ theme });
  },
  toggleTheme: () => {
    const currentTheme = get().theme;
    const nextTheme = currentTheme === 'light' ? 'dark' : 'light';
    
    const root = window.document.documentElement;
    root.classList.remove('light', 'dark');
    root.classList.add(nextTheme);
    
    localStorage.setItem('evalora_theme', nextTheme);
    set({ theme: nextTheme });
  }
}));
