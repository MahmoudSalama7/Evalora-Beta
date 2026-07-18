import * as React from 'react'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import { routes } from './router/routes'
import { useAuthStore } from './stores/auth-store'
import { useThemeStore } from './stores/theme-store'

const router = createBrowserRouter(routes);

export default function App() {
  const initializeAuth = useAuthStore((state) => state.initialize);
  const initializeTheme = useThemeStore((state) => state.initializeTheme);

  React.useEffect(() => {
    initializeAuth();
    initializeTheme();
  }, [initializeAuth, initializeTheme]);

  return <RouterProvider router={router} />;
}
