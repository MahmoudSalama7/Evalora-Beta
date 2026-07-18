import * as React from 'react'
import { Outlet, Navigate } from 'react-router-dom'
import { useAuthStore } from '../stores/auth-store'
import { CandidateSidebar } from '../components/navigation/CandidateSidebar'
import { TopNav } from '../components/navigation/TopNav'
import { ToastContainer } from '../components/ui/Toast'

export const CandidateLayout: React.FC = () => {
  const { isAuthenticated, user, isLoading } = useAuthStore();

  if (isLoading) {
    return (
      <div className="min-h-screen bg-[#0b0f19] flex items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-primary-500" />
      </div>
    );
  }

  if (!isAuthenticated || !user) {
    return <Navigate to="/login" replace />;
  }

  if (user.role !== 'candidate') {
    return <Navigate to="/hr/dashboard" replace />;
  }

  return (
    <div className="flex h-screen w-screen bg-[#0b0f19] text-slate-100 overflow-hidden">
      {/* Sidebar Navigation */}
      <CandidateSidebar />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0 h-full overflow-hidden">
        {/* Top Header */}
        <TopNav />

        {/* Content Container */}
        <main className="flex-1 overflow-y-auto p-8 relative">
          <Outlet />
        </main>
      </div>

      {/* Notifications system */}
      <ToastContainer />
    </div>
  );
};
export default CandidateLayout;
