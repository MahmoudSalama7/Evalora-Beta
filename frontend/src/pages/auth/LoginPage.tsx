import * as React from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuthStore } from '../../stores/auth-store'
import { useNotificationStore } from '../../stores/notification-store'
import { Button } from '../../components/ui/Button'
import { Input } from '../../components/ui/Input'
import { Select } from '../../components/ui/Select'

export const LoginPage: React.FC = () => {
  const navigate = useNavigate();
  const login = useAuthStore((state) => state.login);
  const addToast = useNotificationStore((state) => state.addToast);
  
  const [email, setEmail] = React.useState('hr@evalora.ai');
  const [role, setRole] = React.useState<'hr' | 'candidate'>('hr');
  const [isLoading, setIsLoading] = React.useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email) {
      addToast('Please enter an email address', 'error');
      return;
    }
    
    setIsLoading(true);
    try {
      const user = await login(email, role);
      addToast(`Welcome back, ${user.name}!`, 'success');
      if (user.role === 'hr') {
        navigate('/hr/dashboard');
      } else {
        navigate('/candidate/dashboard');
      }
    } catch (err: any) {
      addToast(err.message || 'Login failed', 'error');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="w-full flex flex-col gap-6">
      <div className="flex flex-col text-center gap-1.5">
        <h1 className="text-3xl font-extrabold text-white tracking-tight bg-gradient-to-r from-primary-400 to-indigo-400 bg-clip-text text-transparent">
          Welcome back
        </h1>
        <p className="text-slate-400 text-sm">
          Enter your credentials to access your dashboard
        </p>
      </div>

      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <Input
          type="email"
          label="Email Address"
          placeholder="name@company.com"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        
        <Select
          label="Access Role"
          value={role}
          onChange={(e) => setRole(e.target.value as 'hr' | 'candidate')}
          options={[
            { value: 'hr', label: 'HR / Recruiter Portal' },
            { value: 'candidate', label: 'Candidate Dashboard' }
          ]}
        />

        <div className="flex items-center justify-between text-xs mt-1">
          <label className="flex items-center gap-2 cursor-pointer text-slate-400 select-none">
            <input type="checkbox" className="rounded border-slate-800 bg-slate-950 text-primary-600 focus:ring-0" />
            Remember me
          </label>
          <Link to="/forgot-password" className="text-primary-400 hover:text-primary-300 font-medium">
            Forgot password?
          </Link>
        </div>

        <Button type="submit" className="w-full py-3" isLoading={isLoading}>
          Sign In
        </Button>
      </form>

      {/* Social Login Divider */}
      <div className="relative my-2 flex items-center justify-center">
        <div className="absolute inset-0 flex items-center">
          <span className="w-full border-t border-slate-800" />
        </div>
        <span className="relative px-3 bg-[#0f172a] text-xs font-semibold text-slate-500 uppercase tracking-wider">
          Or continue with
        </span>
      </div>

      <div className="grid grid-cols-2 gap-3">
        <Button variant="outline" className="w-full py-2.5 flex items-center justify-center gap-2" onClick={() => addToast('Google login is not wired yet.', 'info')}>
          <svg className="w-4 h-4" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12.24 10.285V14.4h6.887c-.648 2.41-2.519 4.113-5.136 4.113-3.072 0-5.561-2.49-5.561-5.561s2.49-5.561 5.561-5.561c1.378 0 2.63.5 3.606 1.319l3.1-3.1C18.82 2.215 15.75 1.05 12.24 1.05 6.09 1.05 1.05 6.09 1.05 12.24s5.04 11.19 11.19 11.19c5.895 0 10.87-4.14 10.87-11.19 0-.693-.06-1.353-.178-1.955H12.24z"/>
          </svg>
          Google
        </Button>
        <Button variant="outline" className="w-full py-2.5 flex items-center justify-center gap-2" onClick={() => addToast('GitHub login is not wired yet.', 'info')}>
          <svg className="w-4 h-4" viewBox="0 0 24 24" fill="currentColor">
            <path fillRule="evenodd" clipRule="evenodd" d="M12 2C6.477 2 2 6.477 2 12c0 4.42 2.865 8.166 6.839 9.489.5.092.682-.217.682-.482 0-.237-.008-.866-.013-1.7-2.782.603-3.369-1.34-3.369-1.34-.454-1.156-1.11-1.464-1.11-1.464-.908-.62.069-.608.069-.608 1.003.07 1.531 1.03 1.531 1.03.892 1.529 2.341 1.087 2.91.831.092-.646.35-1.086.636-1.336-2.22-.253-4.555-1.11-4.555-4.943 0-1.091.39-1.984 1.029-2.683-.103-.253-.446-1.27.098-2.647 0 0 .84-.269 2.75 1.025A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.294 2.747-1.025 2.747-1.025.546 1.377.203 2.394.1 2.647.64.699 1.028 1.592 1.028 2.683 0 3.842-2.339 4.687-4.566 4.935.359.309.678.919.678 1.852 0 1.336-.012 2.415-.012 2.743 0 .267.18.579.688.481C19.137 20.162 22 16.418 22 12c0-5.523-4.477-10-10-10z"/>
          </svg>
          GitHub
        </Button>
      </div>

      <div className="text-center text-sm text-slate-400 mt-2">
        Don't have an account?{' '}
        <Link to="/signup" className="text-primary-400 hover:text-primary-300 font-semibold">
          Sign up
        </Link>
      </div>
    </div>
  );
};
