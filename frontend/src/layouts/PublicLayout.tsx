import * as React from 'react'
import { Outlet, Navigate } from 'react-router-dom'
import { useAuthStore } from '../stores/auth-store'
import { Card } from '../components/ui/Card'
import { ToastContainer } from '../components/ui/Toast'

export const PublicLayout: React.FC = () => {
  const { isAuthenticated, user } = useAuthStore();

  if (isAuthenticated && user) {
    return <Navigate to={user.role === 'hr' ? '/hr/dashboard' : '/candidate/dashboard'} replace />;
  }

  return (
    <div className="min-h-screen relative flex items-center justify-center bg-[#0b0f19] px-4 py-12 overflow-hidden">
      {/* Dynamic Aesthetic Background Gradients */}
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-primary-600/10 rounded-full filter blur-[100px] animate-pulse-slow pointer-events-none" />
      <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-indigo-600/10 rounded-full filter blur-[100px] animate-pulse-slow pointer-events-none" style={{ animationDelay: '4s' }} />

      {/* Main Container */}
      <div className="w-full max-w-md z-10">
        <div className="flex items-center justify-center gap-2 mb-8">
          <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-primary-500 to-indigo-600 flex items-center justify-center font-black text-white text-lg tracking-wider shadow-lg shadow-primary-950/40">
            E
          </div>
          <span className="text-xl font-bold tracking-tight text-white font-sans">
            Evalora<span className="text-primary-400 font-medium">.ai</span>
          </span>
        </div>

        <Card className="px-8 py-10 bg-slate-900/40 backdrop-blur-xl border-slate-800/80 shadow-2xl relative">
          <Outlet />
        </Card>
      </div>

      <ToastContainer />
    </div>
  );
};
export default PublicLayout;
