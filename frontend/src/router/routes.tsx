import type { RouteObject } from 'react-router-dom'
import { PublicLayout } from '../layouts/PublicLayout'
import { LoginPage } from '../pages/auth/LoginPage'
import { SignUpPage } from '../pages/auth/SignUpPage'
import { ForgotPasswordPage } from '../pages/auth/ForgotPasswordPage'
import { ResetPasswordPage } from '../pages/auth/ResetPasswordPage'

import { RecruiterLayout } from '../layouts/RecruiterLayout'
import { DashboardPage as HRDashboard } from '../pages/hr/DashboardPage'

import { CandidateLayout } from '../layouts/CandidateLayout'
import { DashboardPage as CandidateDashboard } from '../pages/candidate/DashboardPage'

// Stub pages for additional routes to keep navigation working without breaking

const StubPage = ({ title }: { title: string }) => (
  <div className="p-6 glass-panel rounded-xl">
    <h2 className="text-xl font-bold text-white">{title}</h2>
    <p className="text-slate-400 text-sm mt-2">This module is part of the layout shell and is ready for feature wiring.</p>
  </div>
);

export const routes: RouteObject[] = [
  // Public Routes (Auth)
  {
    path: '/',
    element: <PublicLayout />,
    children: [
      { path: '', element: <LoginPage /> },
      { path: 'login', element: <LoginPage /> },
      { path: 'signup', element: <SignUpPage /> },
      { path: 'forgot-password', element: <ForgotPasswordPage /> },
      { path: 'reset-password', element: <ResetPasswordPage /> }
    ]
  },
  // Recruiter Portal Routes
  {
    path: '/hr',
    element: <RecruiterLayout />,
    children: [
      { path: 'dashboard', element: <HRDashboard /> },
      { path: 'recruitment', element: <StubPage title="Recruitment Overview" /> },
      { path: 'jobs', element: <StubPage title="Job Openings" /> },
      { path: 'candidates', element: <StubPage title="Candidates Management" /> },
      { path: 'interviews', element: <StubPage title="Interview Schedules" /> },
      { path: 'reports', element: <StubPage title="Hiring Reports" /> },
      { path: 'analytics', element: <StubPage title="System Analytics" /> },
      { path: 'settings', element: <StubPage title="Organization Settings" /> }
    ]
  },
  // Candidate Dashboard Routes
  {
    path: '/candidate',
    element: <CandidateLayout />,
    children: [
      { path: 'dashboard', element: <CandidateDashboard /> },
      { path: 'interviews', element: <StubPage title="My Interviews" /> },
      { path: 'results', element: <StubPage title="Assessment Results" /> },
      { path: 'profile', element: <StubPage title="Candidate Profile" /> },
      { path: 'settings', element: <StubPage title="Candidate Settings" /> }
    ]
  }
];
